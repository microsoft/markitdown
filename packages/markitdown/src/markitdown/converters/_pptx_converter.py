import sys
import base64
import mimetypes
import os
import io
import re
import html
import posixpath
import warnings

from typing import BinaryIO, Any, Dict, Optional, Set, Tuple
from operator import attrgetter

from ._html_converter import HtmlConverter
from ._llm_caption import llm_caption
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import pptx
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.presentationml",
]

ACCEPTED_FILE_EXTENSIONS = [".pptx"]


class PptxConverter(DocumentConverter):
    """
    Converts PPTX files to Markdown. Supports heading, tables and images with alt text.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pptx",
                    feature="pptx",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        # Resolve the optional image extraction directory.
        # When ``extract_images_to`` is provided (and ``keep_data_uris`` is not
        # set), embedded images are written to this directory and referenced
        # by relative filename in the markdown output. When neither option is
        # set the legacy placeholder behaviour is preserved for backwards
        # compatibility.
        extract_images_to: Optional[str] = kwargs.get("extract_images_to")
        keep_data_uris: bool = bool(kwargs.get("keep_data_uris", False))

        # ``extract_dir_resolved`` is the absolute path used for actual file
        # I/O (so we can ``os.makedirs`` and ``open`` reliably regardless of
        # the caller's CWD). ``extract_dir_for_link`` preserves the user's
        # original input verbatim and is used to build the markdown image
        # references, so consumers can locate the rendered files relative to
        # whatever path they passed in (e.g. ``imgs/`` stays relative).
        extract_dir_resolved: Optional[str] = None
        extract_dir_for_link: Optional[str] = None
        if extract_images_to and not keep_data_uris:
            extract_dir_resolved = os.path.abspath(extract_images_to)
            extract_dir_for_link = extract_images_to
            try:
                os.makedirs(extract_dir_resolved, exist_ok=True)
            except OSError as exc:
                warnings.warn(
                    f"Could not create image extraction directory "
                    f"{extract_dir_resolved!r}: {exc}; falling back to placeholder "
                    f"filenames.",
                    stacklevel=2,
                )
                extract_dir_resolved = None
                extract_dir_for_link = None

        # Track filename uniqueness across the deck and reuse identical images
        # by content hash so duplicate blobs are written to disk only once.
        used_names: Set[str] = set()
        hash_to_name: Dict[str, str] = {}

        # Perform the conversion
        presentation = pptx.Presentation(file_stream)
        md_content = ""
        slide_num = 0
        for slide in presentation.slides:
            slide_num += 1

            md_content += f"\n\n<!-- Slide number: {slide_num} -->\n"

            title = slide.shapes.title

            # Per-slide counter incremented for every visited shape (including
            # nested group children) so each image gets a stable, monotonic
            # index for filename construction.
            shape_counter = [0]

            def get_shape_content(shape, **kwargs):
                nonlocal md_content
                shape_counter[0] += 1
                current_shape_idx = shape_counter[0]
                # Pictures
                if self._is_picture(shape):
                    # https://github.com/scanny/python-pptx/pull/512#issuecomment-1713100069

                    llm_description = ""
                    alt_text = ""

                    # Potentially generate a description using an LLM
                    llm_client = kwargs.get("llm_client")
                    llm_model = kwargs.get("llm_model")
                    if llm_client is not None and llm_model is not None:
                        # Prepare a file_stream and stream_info for the image data
                        image_filename = shape.image.filename
                        image_extension = None
                        if image_filename:
                            image_extension = os.path.splitext(image_filename)[1]
                        image_stream_info = StreamInfo(
                            mimetype=shape.image.content_type,
                            extension=image_extension,
                            filename=image_filename,
                        )

                        image_stream = io.BytesIO(shape.image.blob)

                        # Caption the image
                        try:
                            llm_description = llm_caption(
                                image_stream,
                                image_stream_info,
                                client=llm_client,
                                model=llm_model,
                                prompt=kwargs.get("llm_prompt"),
                            )
                        except Exception:
                            # Unable to generate a description
                            pass

                    # Also grab any description embedded in the deck
                    try:
                        alt_text = shape._element._nvXxPr.cNvPr.attrib.get("descr", "")
                    except Exception:
                        # Unable to get alt text
                        pass

                    # Prepare the alt, escaping any special characters
                    alt_text = "\n".join([llm_description, alt_text]) or shape.name
                    alt_text = re.sub(r"[\r\n\[\]]", " ", alt_text)
                    alt_text = re.sub(r"\s+", " ", alt_text).strip()

                    # If keep_data_uris is True, use base64 encoding for images.
                    # keep_data_uris takes precedence over extract_images_to.
                    if keep_data_uris:
                        blob = shape.image.blob
                        content_type = shape.image.content_type or "image/png"
                        b64_string = base64.b64encode(blob).decode("utf-8")
                        md_content += f"\n![{alt_text}](data:{content_type};base64,{b64_string})\n"
                    elif extract_dir_resolved is not None:
                        # Try to write the image to disk; fall back to the
                        # legacy placeholder if anything goes wrong.
                        try:
                            target_path, ref_name = self._resolve_image_target(
                                extract_dir_resolved,
                                slide_num,
                                current_shape_idx,
                                shape,
                                used_names,
                                hash_to_name,
                            )
                            if target_path is not None:
                                # Write first; only commit dedup/uniqueness
                                # state to the shared dicts after a
                                # successful write so a write failure does
                                # not strand future references on a
                                # non-existent file.
                                with open(target_path, "wb") as fh:
                                    fh.write(shape.image.blob)
                                used_names.add(ref_name)
                                sha1 = getattr(shape.image, "sha1", None)
                                if sha1:
                                    hash_to_name[sha1] = ref_name
                            link = self._build_markdown_link(
                                extract_dir_for_link, ref_name
                            )
                            md_content += f"\n![{alt_text}]({link})\n"
                        except Exception as exc:
                            warnings.warn(
                                f"Failed to extract embedded PPTX image "
                                f"(slide {slide_num}, shape {shape.name!r}): "
                                f"{exc}; falling back to placeholder filename.",
                                stacklevel=2,
                            )
                            filename = re.sub(r"\W", "", shape.name) + ".jpg"
                            md_content += "\n![" + alt_text + "](" + filename + ")\n"
                    else:
                        # A placeholder name (legacy behaviour).
                        filename = re.sub(r"\W", "", shape.name) + ".jpg"
                        md_content += "\n![" + alt_text + "](" + filename + ")\n"

                # Tables
                if self._is_table(shape):
                    md_content += self._convert_table_to_markdown(shape.table, **kwargs)

                # Charts
                if shape.has_chart:
                    md_content += self._convert_chart_to_markdown(shape.chart)

                # Text areas
                elif shape.has_text_frame:
                    if shape == title:
                        md_content += "# " + shape.text.lstrip() + "\n"
                    else:
                        md_content += shape.text + "\n"

                # Group Shapes
                if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
                    sorted_shapes = sorted(
                        shape.shapes,
                        key=lambda x: (
                            float("-inf") if not x.top else x.top,
                            float("-inf") if not x.left else x.left,
                        ),
                    )
                    for subshape in sorted_shapes:
                        get_shape_content(subshape, **kwargs)

            sorted_shapes = sorted(
                slide.shapes,
                key=lambda x: (
                    float("-inf") if not x.top else x.top,
                    float("-inf") if not x.left else x.left,
                ),
            )
            for shape in sorted_shapes:
                get_shape_content(shape, **kwargs)

            md_content = md_content.strip()

            if slide.has_notes_slide:
                md_content += "\n\n### Notes:\n"
                notes_frame = slide.notes_slide.notes_text_frame
                if notes_frame is not None:
                    md_content += notes_frame.text
                md_content = md_content.strip()

        return DocumentConverterResult(markdown=md_content.strip())

    def _is_picture(self, shape):
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            return True
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PLACEHOLDER:
            if hasattr(shape, "image"):
                return True
        return False

    def _is_table(self, shape):
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.TABLE:
            return True
        return False

    def _sanitize_image_basename(self, name: str, fallback: str) -> str:
        """Return a filesystem-safe basename for an embedded image.

        Keeps Unicode word characters (including CJK) and ``-``; replaces any
        other character with ``_``. Path separators and ``..`` are scrubbed
        defensively. When the resulting string is empty, ``fallback`` is used.
        """
        cleaned = (name or "").strip()
        # Defensively strip path separators / parent-directory traversals
        # before regex sanitisation.
        cleaned = cleaned.replace("/", "_").replace("\\", "_").replace("..", "_")
        cleaned = re.sub(r"[^\w\-]", "_", cleaned, flags=re.UNICODE)
        cleaned = cleaned.strip("._")
        if not cleaned:
            cleaned = fallback
        return cleaned

    def _resolve_image_target(
        self,
        extract_dir: str,
        slide_num: int,
        shape_idx: int,
        shape: Any,
        used_names: Set[str],
        hash_to_name: Dict[str, str],
    ) -> Tuple[Optional[str], str]:
        """Return ``(absolute_path_to_write_or_None, markdown_reference)``.

        If the image's content hash has been seen before, returns
        ``(None, existing_reference)`` so the caller skips writing and reuses
        the previous filename. Otherwise computes a unique filename in
        ``extract_dir`` and returns the absolute path to write to plus the
        relative filename to embed in the markdown.

        This method does **not** mutate ``used_names`` or ``hash_to_name``.
        The caller is expected to commit the returned ``ref_name`` to those
        dicts only after the file has been successfully written, so a write
        failure does not poison the dedup state for subsequent shapes.
        """
        image = shape.image

        # Deduplicate by content hash when available.
        sha1 = getattr(image, "sha1", None)
        if sha1 and sha1 in hash_to_name:
            return None, hash_to_name[sha1]

        # Pick an extension. python-pptx normally returns a lowercase
        # dot-less extension via ``image.ext`` (e.g. ``"png"`` / ``"jpeg"``)
        # but for image types it does not recognise (SVG, EMF, ICO, ...) it
        # raises ``ValueError`` instead of returning ``None``. Wrap each
        # source in its own ``try`` so we can fall through cleanly.
        ext = ""
        try:
            raw_ext = getattr(image, "ext", None)
        except Exception:
            raw_ext = None
        if raw_ext:
            ext = str(raw_ext).lstrip(".").lower()

        if not ext:
            try:
                content_type = getattr(image, "content_type", None) or ""
            except Exception:
                content_type = ""
            if content_type:
                guessed = mimetypes.guess_extension(content_type)
                if guessed:
                    ext = guessed.lstrip(".").lower()

        if not ext:
            try:
                image_filename = getattr(image, "filename", None) or ""
            except Exception:
                image_filename = ""
            if image_filename:
                _, fname_ext = os.path.splitext(image_filename)
                ext = fname_ext.lstrip(".").lower()

        if not ext:
            ext = "bin"

        sanitized = self._sanitize_image_basename(
            getattr(shape, "name", "") or "",
            fallback=f"image{shape_idx}",
        )

        base_name = f"slide{slide_num:02d}_{shape_idx}_{sanitized}"
        candidate = f"{base_name}.{ext}"
        suffix = 2
        # Avoid collisions with names this conversion has already allocated
        # *and* with files that already exist on disk from a previous run or
        # another caller. ``used_names`` covers in-process allocations (which
        # also live on disk after we write them); ``os.path.exists`` covers
        # files we did not put there ourselves so we never silently overwrite
        # them.
        while candidate in used_names or os.path.exists(
            os.path.join(extract_dir, candidate)
        ):
            candidate = f"{base_name}_{suffix}.{ext}"
            suffix += 1

        target_path = os.path.join(extract_dir, candidate)
        return target_path, candidate

    @staticmethod
    def _build_markdown_link(extract_dir_for_link: Optional[str], filename: str) -> str:
        """Compose the markdown image reference.

        Joins the user-supplied ``extract_images_to`` value (``imgs/`` or
        ``/abs/path``) with ``filename`` using forward slashes so the
        resulting markdown is portable and never contains backslashes on
        Windows. Falls back to the bare filename when no directory is
        configured (this branch is mainly defensive — callers only invoke
        this when extraction is enabled).
        """
        if not extract_dir_for_link:
            return filename
        # Normalise any backslashes the caller may have used (Windows-style
        # input) and strip trailing separators before joining.
        prefix = extract_dir_for_link.replace("\\", "/").rstrip("/")
        if not prefix:
            return filename
        return posixpath.join(prefix, filename)

    def _convert_table_to_markdown(self, table, **kwargs):
        # Write the table as HTML, then convert it to Markdown
        html_table = "<html><body><table>"
        first_row = True
        for row in table.rows:
            html_table += "<tr>"
            for cell in row.cells:
                if first_row:
                    html_table += "<th>" + html.escape(cell.text) + "</th>"
                else:
                    html_table += "<td>" + html.escape(cell.text) + "</td>"
            html_table += "</tr>"
            first_row = False
        html_table += "</table></body></html>"

        return (
            self._html_converter.convert_string(html_table, **kwargs).markdown.strip()
            + "\n"
        )

    def _convert_chart_to_markdown(self, chart):
        try:
            md = "\n\n### Chart"
            if chart.has_title:
                md += f": {chart.chart_title.text_frame.text}"
            md += "\n\n"
            data = []
            category_names = [c.label for c in chart.plots[0].categories]
            series_list = list(chart.series)
            series_names = [s.name for s in series_list]
            data.append(["Category"] + series_names)

            # Materialize each series' values once. Accessing series.values[idx]
            # inside the nested loop is O(n^2) in python-pptx (each lookup does an
            # XPath scan of all points), which is extremely slow on large charts.
            series_values = [list(s.values) for s in series_list]

            for idx, category in enumerate(category_names):
                row = [category]
                for sv in series_values:
                    row.append(sv[idx] if idx < len(sv) else None)
                data.append(row)

            markdown_table = []
            for row in data:
                markdown_table.append("| " + " | ".join(map(str, row)) + " |")
            header = markdown_table[0]
            separator = "|" + "|".join(["---"] * len(data[0])) + "|"
            return md + "\n".join([header, separator] + markdown_table[1:])
        except ValueError as e:
            # Handle the specific error for unsupported chart types
            if "unsupported plot type" in str(e):
                return "\n\n[unsupported chart]\n\n"
        except Exception:
            # Catch any other exceptions that might occur
            return "\n\n[unsupported chart]\n\n"
