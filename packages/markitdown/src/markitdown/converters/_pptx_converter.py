import sys
import base64
import os
import io
import re
import html

from typing import BinaryIO, Any, Optional

from ._html_converter import HtmlConverter
from ._llm_caption import llm_caption
from ..converter_utils._image import _parse_image_html
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import pptx
    from pptx.text.text import _Run
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.presentationml",
]

ACCEPTED_FILE_EXTENSIONS = [".pptx"]

_BULLET_PLACEHOLDER_TYPES = {
    2,  # PP_PLACEHOLDER.BODY
    7,  # PP_PLACEHOLDER.OBJECT
    6,  # PP_PLACEHOLDER.VERTICAL_BODY
    17,  # PP_PLACEHOLDER.VERTICAL_OBJECT
}


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

        # Perform the conversion
        presentation = pptx.Presentation(file_stream)
        md_content = ""
        slide_num = 0
        for slide in presentation.slides:
            slide_num += 1

            md_content += f"\n\n<!-- Slide number: {slide_num} -->\n"

            title = slide.shapes.title

            def get_shape_content(shape, **kwargs):
                nonlocal md_content
                # Pictures
                if self._is_picture(shape):
                    md_content += self._convert_picture_to_markdown(shape, **kwargs)

                # Tables
                if self._is_table(shape):
                    md_content += self._convert_table_to_markdown(shape.table, **kwargs)

                # Charts
                if shape.has_chart:
                    md_content += self._convert_chart_to_markdown(shape.chart)

                # Text areas
                elif shape.has_text_frame:
                    if shape == title:
                        title_lines = []
                        for p in shape.text_frame.paragraphs:
                            p_text = self._format_paragraph_content(p).strip()
                            if p_text:
                                title_lines.append("# " + p_text)
                        if title_lines:
                            md_content += "\n".join(title_lines) + "\n"
                    else:
                        shape_lines = []
                        ordered_counters: dict[int, int] = {}
                        for p in shape.text_frame.paragraphs:
                            p_text = self._format_paragraph_content(p)
                            if not p_text.strip():
                                shape_lines.append("")
                                ordered_counters.clear()
                                continue

                            is_list, list_type = self._get_paragraph_list_info(p, shape)
                            if is_list:
                                lvl = max(0, getattr(p, "level", 0))
                                indent = "  " * lvl
                                if list_type == "ordered":
                                    count = ordered_counters.get(lvl, 0) + 1
                                    ordered_counters[lvl] = count
                                    for k in list(ordered_counters.keys()):
                                        if k > lvl:
                                            del ordered_counters[k]
                                    prefix = f"{indent}{count}. "
                                else:
                                    ordered_counters.clear()
                                    prefix = f"{indent}* "

                                sublines = p_text.splitlines()
                                shape_lines.append(prefix + sublines[0].lstrip())
                                for subline in sublines[1:]:
                                    shape_lines.append(f"{indent}  " + subline.lstrip())
                            else:
                                ordered_counters.clear()
                                shape_lines.append(p_text)

                        if shape_lines and any(line.strip() for line in shape_lines):
                            md_content += "\n".join(shape_lines) + "\n"

                # Group Shapes
                if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
                    sorted_shapes = sorted(
                        shape.shapes,
                        key=lambda x: (
                            float("-inf") if x.top is None else x.top,
                            float("-inf") if x.left is None else x.left,
                        ),
                    )
                    for subshape in sorted_shapes:
                        get_shape_content(subshape, **kwargs)

            sorted_shapes = sorted(
                slide.shapes,
                key=lambda x: (
                    float("-inf") if x.top is None else x.top,
                    float("-inf") if x.left is None else x.left,
                ),
            )
            for shape in sorted_shapes:
                get_shape_content(shape, **kwargs)

            md_content = md_content.strip()

            if slide.has_notes_slide:
                # PowerPoint attaches a notes slide to a slide whose notes pane
                # has merely been opened, so having one says nothing about there
                # being notes to read. Only head a section that has content.
                notes_frame = slide.notes_slide.notes_text_frame
                if notes_frame is not None and (notes_frame.text or "").strip():
                    notes_lines = [
                        self._format_paragraph_content(p)
                        for p in notes_frame.paragraphs
                    ]
                    notes_text = "\n".join(notes_lines).strip()
                    if notes_text:
                        md_content += "\n\n### Notes:\n" + notes_text
                        md_content = md_content.strip()

        return DocumentConverterResult(markdown=md_content.strip())

    def _image_to_html(
        self,
        image_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Optional[str]:
        """Override to render an embedded image as an HTML fragment.

        The stream is borrowed, seekable, and positioned at zero; do not close
        or retain it. StreamInfo describes the image, not the presentation.
        Existing conversion options are forwarded through kwargs.

        Native LLM captions take precedence. Otherwise, return None or blank
        text to retain the native image representation, or HTML with literal
        text escaped. The fragment passes through HtmlConverter before being
        placed at the picture's position in slide/group order. Hook failures
        propagate through the normal conversion failure path.
        """
        return None

    def _convert_picture_to_markdown(self, shape, **kwargs):
        llm_description = ""
        alt_text = ""
        image_blob, image_content_type, image_filename = self._get_image_info(shape)
        image_stream_info = StreamInfo(
            mimetype=image_content_type,
            extension=os.path.splitext(image_filename)[1] if image_filename else None,
            filename=image_filename,
        )

        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model")
        if llm_client is not None and llm_model is not None and image_blob is not None:
            with io.BytesIO(image_blob) as image_stream:
                try:
                    llm_description = llm_caption(
                        image_stream,
                        image_stream_info,
                        client=llm_client,
                        model=llm_model,
                        prompt=kwargs.get("llm_prompt"),
                    )
                except Exception:
                    # Preserve native caption failure fallback.
                    pass

        if (
            (not llm_description or not llm_description.strip())
            and image_blob is not None
            and type(self)._image_to_html is not PptxConverter._image_to_html
        ):
            with io.BytesIO(image_blob) as image_stream:
                fragment = self._image_to_html(
                    image_stream, image_stream_info, **kwargs
                )
            soup = _parse_image_html(fragment)
            if soup is not None:
                return (
                    "\n"
                    + self._html_converter.convert_string(str(soup), **kwargs).markdown
                    + "\n"
                )

        # Keep native caption/alt Markdown separate from custom image HTML.
        try:
            alt_text = shape._element._nvXxPr.cNvPr.attrib.get("descr", "")
        except Exception:
            pass
        alt_text = (
            "\n".join(
                text for text in [llm_description, alt_text] if text and text.strip()
            )
            or shape.name
        )
        alt_text = re.sub(r"[\r\n\[\]]", " ", alt_text)
        alt_text = re.sub(r"\s+", " ", alt_text).strip()

        if kwargs.get("keep_data_uris", False) and image_blob is not None:
            content_type = image_content_type or "image/png"
            b64_string = base64.b64encode(image_blob).decode("utf-8")
            return f"\n![{alt_text}](data:{content_type};base64,{b64_string})\n"
        filename = re.sub(r"\W", "", shape.name) + ".jpg"
        return "\n![" + alt_text + "](" + filename + ")\n"

    def _find_svg_blip_part(self, shape):
        """Return the image part referenced by an ``<asvg:svgBlip>``, if any.

        PowerPoint stores SVG pictures as a blip whose main ``r:embed`` points
        to a rasterized PNG fallback, plus an ``<asvg:svgBlip>`` extension
        pointing to the SVG. When there is no raster fallback the ``<a:blip>``
        has no ``r:embed`` at all, so python-pptx's ``shape.image`` fails. This
        resolves the SVG part directly from the ``svgBlip`` extension.
        """
        try:
            nsmap = {
                "asvg": "http://schemas.microsoft.com/office/drawing/2016/SVG/main",
            }
            r_embed = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
            for svg_blip in shape._element.findall(".//asvg:svgBlip", nsmap):
                embed_rid = svg_blip.get(r_embed)
                if not embed_rid:
                    continue
                return shape.part.related_part(embed_rid)
        except Exception:
            pass
        return None

    def _get_image_info(self, shape):
        """Return (blob, content_type, filename) for a picture shape.

        Handles SVG images that lack a rasterized fallback. In that case
        ``shape.image`` raises ``ValueError("no embedded image")`` because the
        ``<a:blip>`` has no ``r:embed`` attribute (only an ``<asvg:svgBlip>``
        extension). We fall back to resolving the SVG blip directly.
        """
        try:
            image = shape.image
            return image.blob, image.content_type, image.filename
        except Exception:
            pass

        # Fall back to an embedded SVG blip (image without a raster fallback)
        part = self._find_svg_blip_part(shape)
        if part is not None:
            try:
                filename = os.path.basename(getattr(part, "partname", "") or "") or None
                return part.blob, "image/svg+xml", filename
            except Exception:
                pass

        return None, None, None

    def _is_picture(self, shape):
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            return True
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PLACEHOLDER:
            # ``shape.image`` can raise (e.g. ValueError "no embedded image")
            # for SVG placeholders without a raster fallback, so guard against
            # any exception rather than relying on hasattr (which only swallows
            # AttributeError).
            try:
                if shape.image is not None:
                    return True
            except Exception:
                # Still a picture if it carries an embedded SVG blip.
                if self._find_svg_blip_part(shape) is not None:
                    return True
        return False

    def _is_table(self, shape):
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.TABLE:
            return True
        return False

    def _format_table_cell(self, cell) -> str:
        ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        parts = []
        for p_idx, p in enumerate(cell.text_frame.paragraphs):
            if p_idx > 0:
                parts.append("<br/>")
            p_parts = []
            if hasattr(p, "_p") and p._p is not None:
                for child in p._p:
                    if child.tag == f"{ns}r":
                        try:
                            run = _Run(child, p)
                            t = html.escape(run.text or "")
                            addr = None
                            if run.hyperlink and run.hyperlink.address:
                                addr = run.hyperlink.address.strip()
                            if addr:
                                p_parts.append(f'<a href="{html.escape(addr)}">{t}</a>')
                            else:
                                p_parts.append(t)
                        except Exception:
                            pass
                    elif child.tag == f"{ns}br":
                        p_parts.append("<br/>")
            if not p_parts and p.text:
                p_parts.append(html.escape(p.text))
            parts.extend(p_parts)
        return "".join(parts) if parts else html.escape(cell.text or "")

    def _convert_table_to_markdown(self, table, **kwargs):
        # Write the table as HTML, then convert it to Markdown
        html_table = "<html><body><table>"
        first_row = True
        for row in table.rows:
            html_table += "<tr>"
            for cell in row.cells:
                cell_content = self._format_table_cell(cell)
                if first_row:
                    html_table += "<th>" + cell_content + "</th>"
                else:
                    html_table += "<td>" + cell_content + "</td>"
            html_table += "</tr>"
            first_row = False
        html_table += "</table></body></html>"

        return (
            self._html_converter.convert_string(html_table, **kwargs).markdown.strip()
            + "\n"
        )

    def _format_run_text(self, text: str, address: Optional[str]) -> str:
        if not address or not text.strip():
            return text
        l_ws = len(text) - len(text.lstrip())
        r_ws = len(text) - len(text.rstrip())
        prefix = text[:l_ws]
        suffix = text[len(text) - r_ws :] if r_ws > 0 else ""
        core = text[l_ws : len(text) - r_ws if r_ws > 0 else len(text)]
        if core:
            return f"{prefix}[{core}]({address}){suffix}"
        return text

    def _format_paragraph_content(self, paragraph) -> str:
        ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        elements: list[tuple[str, Optional[str]]] = []

        if hasattr(paragraph, "_p") and paragraph._p is not None:
            for child in paragraph._p:
                if child.tag == f"{ns}r":
                    try:
                        run = _Run(child, paragraph)
                        text = run.text or ""
                        addr = None
                        if run.hyperlink and run.hyperlink.address:
                            addr = run.hyperlink.address.strip()
                        elements.append((text, addr))
                    except Exception:
                        pass
                elif child.tag == f"{ns}br":
                    elements.append(("\n", None))
                elif child.tag == f"{ns}fld":
                    t = child.find(f"{ns}t")
                    if t is not None and t.text:
                        elements.append((t.text, None))

        if not elements:
            if getattr(paragraph, "runs", None):
                for run in paragraph.runs:
                    text = run.text or ""
                    addr = None
                    try:
                        if run.hyperlink and run.hyperlink.address:
                            addr = run.hyperlink.address.strip()
                    except Exception:
                        pass
                    elements.append((text, addr))
            else:
                return paragraph.text or ""

        # Merge adjacent elements with the same hyperlink address
        merged: list[tuple[str, Optional[str]]] = []
        for text, addr in elements:
            if not text:
                continue
            if (
                merged
                and merged[-1][1] == addr
                and "\n" not in text
                and "\n" not in merged[-1][0]
            ):
                prev_text, prev_addr = merged[-1]
                merged[-1] = (prev_text + text, prev_addr)
            else:
                merged.append((text, addr))

        parts = [self._format_run_text(text, addr) for text, addr in merged]
        return "".join(parts)

    def _get_paragraph_list_info(self, paragraph, shape) -> tuple[bool, Optional[str]]:
        ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        pPr = (
            paragraph._p.pPr
            if hasattr(paragraph, "_p") and paragraph._p is not None
            else None
        )

        if pPr is not None:
            if pPr.find(f"{ns}buNone") is not None:
                return False, None
            if pPr.find(f"{ns}buAutoNum") is not None:
                return True, "ordered"
            if (
                pPr.find(f"{ns}buChar") is not None
                or pPr.find(f"{ns}buBlip") is not None
            ):
                return True, "unordered"

        try:
            lvl_tag = f"{ns}lvl{paragraph.level + 1}pPr"
            lst_style = shape._element.find(f".//{ns}lstStyle")
            if lst_style is not None:
                lvl_pr = lst_style.find(lvl_tag)
                if lvl_pr is not None:
                    if lvl_pr.find(f"{ns}buNone") is not None:
                        return False, None
                    if lvl_pr.find(f"{ns}buAutoNum") is not None:
                        return True, "ordered"
                    if (
                        lvl_pr.find(f"{ns}buChar") is not None
                        or lvl_pr.find(f"{ns}buBlip") is not None
                    ):
                        return True, "unordered"
        except Exception:
            pass

        try:
            if (
                getattr(shape, "is_placeholder", False)
                and shape.placeholder_format.type in _BULLET_PLACEHOLDER_TYPES
            ):
                return True, "unordered"
        except Exception:
            pass

        if getattr(paragraph, "level", 0) > 0:
            return True, "unordered"

        return False, None

    def _convert_chart_to_markdown(self, chart):
        try:
            md = "\n\n### Chart"
            # ChartTitle.text_frame is documented as destructive -- it creates
            # a text frame if one isn't already present, so it never returns
            # None. has_text_frame is the property that actually reflects
            # whether a text frame exists.
            if chart.has_title and chart.chart_title.has_text_frame:
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
