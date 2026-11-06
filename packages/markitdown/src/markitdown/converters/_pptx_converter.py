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
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.presentationml",
]

ACCEPTED_FILE_EXTENSIONS = [".pptx"]

# Minimum vertical overlap, as a fraction of the shorter shape's height, for two
# shapes to count as the same row.
_SAME_ROW_OVERLAP_RATIO = 0.5

# A shape at least this tall relative to its band is a full-height "spanner".
_SPANNING_BAND_FRACTION = 0.75

# A shape at least this wide relative to its band is a full-width "header".
_BAND_HEADER_WIDTH_FRACTION = 0.8

# A header may start this far below the band top (fraction of band height) and
# still lead, absorbing real decks' vertical jitter.
_BAND_TOP_TOLERANCE_FRACTION = 0.05


def _sort_shapes_reading_order(shapes: Any) -> list[Any]:
    """Order shapes in reading order: top-to-bottom, left-to-right within a row.

    A strict ``sorted(key=(top, left))`` reads same-row shapes top-first, so a
    two-column body comes out right-then-left when its columns start at slightly
    different heights. Shapes that overlap vertically are grouped into row bands,
    read top-to-bottom and left-to-right within a band; no shape is added or
    dropped. A full-height spanner (a sidebar) sharing a band with a grid is lifted
    out onto its horizontal side so the grid stays row-major, and a full-width
    header (a title or caption sharing a chart's or table's frame) is read on the
    correct side of it.
    """

    def top_of(s: Any) -> float:
        return s.top if s.top is not None else float("-inf")

    def left_of(s: Any) -> float:
        return s.left if s.left is not None else float("-inf")

    def bottom_of(s: Any) -> float:
        if s.top is None:
            return float("-inf")
        return s.top + (s.height or 0)

    def right_of(s: Any) -> float:
        if s.left is None:
            return float("-inf")
        return s.left + (s.width or 0)

    def group_into_bands(shape_list: Any) -> list[dict[str, Any]]:
        bands: list[dict[str, Any]] = []  # {"top", "bottom", "anchor_*", "shapes"}
        for shape in sorted(shape_list, key=lambda s: (top_of(s), left_of(s))):
            top, bottom = top_of(shape), bottom_of(shape)
            best_band = None
            best_overlap = 0.0
            if shape.top is not None and bottom > top:
                for band in bands:
                    # Compare against the band's tallest member, not the growing
                    # union, so overlaps cannot chain down a staircase.
                    a_top, a_bottom = band["anchor_top"], band["anchor_bottom"]
                    overlap = min(bottom, a_bottom) - max(top, a_top)
                    shorter = min(bottom - top, a_bottom - a_top)
                    if (
                        shorter > 0
                        and overlap >= shorter * _SAME_ROW_OVERLAP_RATIO
                        and overlap > best_overlap
                    ):
                        best_band = band
                        best_overlap = overlap
            if best_band is not None:
                best_band["shapes"].append(shape)
                best_band["top"] = min(best_band["top"], top)
                best_band["bottom"] = max(best_band["bottom"], bottom)
                if bottom - top > best_band["anchor_bottom"] - best_band["anchor_top"]:
                    best_band["anchor_top"] = top
                    best_band["anchor_bottom"] = bottom
            else:
                bands.append(
                    {
                        "top": top,
                        "bottom": bottom,
                        "anchor_top": top,
                        "anchor_bottom": bottom,
                        "shapes": [shape],
                    }
                )
        return bands

    ordered_bands: list[dict[str, Any]] = []
    for band in sorted(group_into_bands(shapes), key=lambda b: b["top"]):
        band_height = band["bottom"] - band["top"]
        spanners = [
            s
            for s in band["shapes"]
            if band_height > 0
            and (bottom_of(s) - top_of(s)) >= _SPANNING_BAND_FRACTION * band_height
        ]
        rest = [s for s in band["shapes"] if s not in spanners]
        sub_bands = group_into_bands(rest) if rest else []
        positioned = all(
            s.left is not None and s.width is not None for s in spanners + rest
        )
        if spanners and sub_bands and positioned:
            spanner_band: dict[str, Any] = {
                "top": min(top_of(s) for s in spanners),
                "bottom": max(bottom_of(s) for s in spanners),
                "shapes": spanners,
            }
            should_split = len(sub_bands) >= 2
            single_contained_row = False
            if not should_split:
                # Split a single full-width row out of a frame it starts inside.
                row = sub_bands[0]
                band_left = min(left_of(s) for s in band["shapes"])
                band_right = max(right_of(s) for s in band["shapes"])
                band_width = band_right - band_left
                row_width = max(right_of(s) for s in row["shapes"]) - min(
                    left_of(s) for s in row["shapes"]
                )
                starts_within = (
                    spanner_band["top"] <= row["top"] <= spanner_band["bottom"]
                )
                if (
                    starts_within
                    and band_width > 0
                    and row_width >= _BAND_HEADER_WIDTH_FRACTION * band_width
                ):
                    should_split = True
                    single_contained_row = True
            if should_split:
                sub_bands = sorted(sub_bands, key=lambda b: b["top"])
                if single_contained_row:
                    # A row riding at the frame's top (a title) reads first; a row
                    # that starts lower (a caption or footer) reads after the frame.
                    # The tolerance keeps a title starting a few EMU down leading.
                    height = spanner_band["bottom"] - spanner_band["top"]
                    cutoff = spanner_band["top"] + _BAND_TOP_TOLERANCE_FRACTION * height
                    if sub_bands[0]["top"] <= cutoff:
                        ordered_bands.extend(sub_bands)
                        ordered_bands.append(spanner_band)
                    else:
                        ordered_bands.append(spanner_band)
                        ordered_bands.extend(sub_bands)
                else:
                    content_left = min(left_of(s) for s in rest)
                    content_right = max(right_of(s) for s in rest)
                    tallest = max(spanners, key=lambda s: bottom_of(s) - top_of(s))
                    if right_of(tallest) <= content_left:  # spanner left of content
                        ordered_bands.append(spanner_band)
                        ordered_bands.extend(sub_bands)
                    elif left_of(tallest) >= content_right:  # spanner right of content
                        ordered_bands.extend(sub_bands)
                        ordered_bands.append(spanner_band)
                    else:  # overlaps horizontally: fall back to top order
                        ordered_bands.extend(
                            sorted(sub_bands + [spanner_band], key=lambda b: b["top"])
                        )
                continue
        ordered_bands.append(band)

    def order_within_band(band_shapes: list[Any]) -> list[Any]:
        # Left-to-right, but a full-width shape starting at the band top leads.
        if len(band_shapes) <= 1:
            return list(band_shapes)
        band_left = min(left_of(s) for s in band_shapes)
        band_right = max(right_of(s) for s in band_shapes)
        band_width = band_right - band_left
        band_top = min(top_of(s) for s in band_shapes)
        band_bottom = max(bottom_of(s) for s in band_shapes)
        top_cutoff = band_top + _BAND_TOP_TOLERANCE_FRACTION * (band_bottom - band_top)
        headers = [
            s
            for s in band_shapes
            if top_of(s) <= top_cutoff
            and band_width > 0
            and (right_of(s) - left_of(s)) >= _BAND_HEADER_WIDTH_FRACTION * band_width
        ]
        rest = [s for s in band_shapes if s not in headers]
        if not headers or not rest:
            return sorted(band_shapes, key=lambda s: (left_of(s), top_of(s)))
        return sorted(headers, key=lambda s: (top_of(s), left_of(s))) + sorted(
            rest, key=lambda s: (left_of(s), top_of(s))
        )

    ordered: list[Any] = []
    for band in ordered_bands:
        ordered.extend(order_within_band(band["shapes"]))
    return ordered


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
                    text = shape.text or ""
                    if shape == title:
                        if text.strip():
                            md_content += "# " + text.lstrip() + "\n"
                    else:
                        md_content += text + "\n"

                # Group Shapes
                if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
                    for subshape in _sort_shapes_reading_order(shape.shapes):
                        get_shape_content(subshape, **kwargs)

            for shape in _sort_shapes_reading_order(slide.shapes):
                get_shape_content(shape, **kwargs)

            md_content = md_content.strip()

            if slide.has_notes_slide:
                # PowerPoint attaches a notes slide to a slide whose notes pane
                # has merely been opened, so having one says nothing about there
                # being notes to read. Only head a section that has content.
                notes_frame = slide.notes_slide.notes_text_frame
                notes_text = (notes_frame.text or "") if notes_frame is not None else ""
                if notes_text.strip():
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
