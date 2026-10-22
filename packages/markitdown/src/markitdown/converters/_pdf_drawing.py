"""Opt-in PDF drawing views and located labels, without semantic inference."""
import base64
import io
from html import escape
from typing import BinaryIO

from .._base_converter import DocumentConverterResult


def _located_words(page):
    from pdfplumber.utils import extract_words

    groups = {"upright": [], "rotated 90": [], "rotated 180": [], "rotated 270": []}
    for char in page.chars:
        a, b = char.get("matrix", (1, 0))[:2]
        if abs(a) >= abs(b):
            direction = "upright" if a >= 0 else "rotated 180"
        else:
            direction = "rotated 90" if b > 0 else "rotated 270"
        groups[direction].append(char)
    words = []
    for direction, chars in groups.items():
        extracted = extract_words(
            chars,
            char_dir="rtl" if direction == "rotated 180" else "ltr",
            char_dir_rotated="btt" if direction == "rotated 90" else "ttb",
        )
        for word in extracted:
            word["drawing_orientation"] = direction
        words.extend(extracted)
    return sorted(words, key=lambda word: (word["top"], word["x0"]))


def convert_drawing(
    stream: BinaryIO, *, inline_images: bool
) -> DocumentConverterResult:
    import pdfplumber

    chunks = [
        "> Warning: Drawing conversion is not lossless. Page views are rasterized; "
        "located labels do not establish measurements or dimension-to-feature relationships. "
        "Review the source drawing before using dimensions.\n\n"
    ]
    assets: dict[str, bytes] = {}
    report = [
        "# Drawing conversion report\n\n",
        "**Lossless: no.** This report is not exhaustive and does not certify completeness.\n\n",
        "## Unresolved information\n\n",
        "- Drawing semantics, dimension-to-feature relationships, constraints, scale, "
        "units, and tolerances are not inferred.\n",
        "- Vector paths, line styles, symbols, and visible layer content appear only "
        "in raster views, not as editable drawing entities.\n",
        "- Raster-only and outlined text is not transcribed by OCR. Angled lettering is grouped by its dominant writing direction; label grouping may be imperfect.\n",
        "- Hidden layers, interactive content, attachments, and non-text annotations "
        "are not reconstructed.\n",
        "- Page views cover the visible CropBox at up to 200 DPI, capped at 8192 pixels "
        "on the longest edge. Rasterization can lose fine details.\n",
        "- Images must be provided to a visual consumer separately from plain-text "
        "Markdown. Inline base64 is not equivalent to visual input; viewer support varies.\n\n",
        "## Page results\n\n",
    ]
    with pdfplumber.open(stream) as pdf:
        for page in pdf.pages:
            try:
                words = _located_words(page)
                annotations = [a for a in page.annots if a.get("contents")]
                dpi = min(200.0, 8192 * 72 / max(page.width, page.height))
                image = page.to_image(resolution=dpi, antialias=True).original
                try:
                    png = io.BytesIO()
                    image.save(png, format="PNG")
                    size = image.size
                finally:
                    image.close()
                name = f"page-{page.page_number}.png"
                if inline_images:
                    image_url = "data:image/png;base64," + base64.b64encode(
                        png.getvalue()
                    ).decode("ascii")
                else:
                    assets[name] = png.getvalue()
                    image_url = name
                chunks.append(
                    f"## Page {page.page_number}\n\n![Drawing page {page.page_number}]({image_url})\n\n"
                )
                chunks.append(
                    "### Located labels\n\nBounding boxes use PDF points in the rotated "
                    "page coordinate system, not engineering dimensions. MediaBox bounds are "
                    "listed in the report. The page view "
                    "uses the CropBox; labels outside it can still be listed.\n\n"
                )
                rows = [("Text", w["text"], w["drawing_orientation"], w) for w in words]
                rows += [
                    ("Annotation", a["contents"], "unspecified", a) for a in annotations
                ]
                if rows:
                    chunks.append(
                        "| Source | Label | Orientation | x0 | top | x1 | bottom |\n| --- | --- | --- | --- | --- | --- | --- |\n"
                    )
                    for source, label, orientation, item in rows:
                        # Untrusted label contents must not become Markdown/HTML syntax.
                        label = (
                            escape(label)
                            .replace("|", "&#124;")
                            .replace("\\", "&#92;")
                            .replace("[", "&#91;")
                            .replace("]", "&#93;")
                            .replace("`", "&#96;")
                            .replace("*", "&#42;")
                            .replace("_", "&#95;")
                            .replace("\r\n", "\n")
                            .replace("\r", "\n")
                            .replace("\n", "<br>")
                        )
                        coords = " | ".join(
                            f"{item[key]:.2f}" for key in ("x0", "top", "x1", "bottom")
                        )
                        chunks.append(
                            f"| {source} | {label} | {orientation} | {coords} |\n"
                        )
                    chunks.append("\n")
                else:
                    chunks.append(
                        "No embedded labels or textual annotations were extracted.\n\n"
                    )
                report.append(
                    f"### Page {page.page_number}\n\n"
                    f"- MediaBox bounds (x0, top, x1, bottom): {page.mediabox}.\n"
                    f"- CropBox bounds: {page.cropbox}.\n"
                    f"- Extracted embedded words: {len(words)}.\n"
                    f"- Extracted textual annotations (including SHX): {len(annotations)}.\n"
                    f"- Page view: {size[0]} x {size[1]} pixels at {dpi:.2f} DPI.\n"
                    f"- PNG bytes: {len(png.getvalue())}.\n"
                    f'- Image storage: {"inline data URI" if inline_images else "external asset"}.\n'
                    "- Drawing semantics: unresolved.\n\n"
                )
                if not rows:
                    report.append(
                        "No searchable labels were extracted; this page is available only as a raster view.\n\n"
                    )
            finally:
                page.close()
    return DocumentConverterResult(
        markdown="".join(chunks).strip(),
        assets=assets,
        conversion_report="".join(report).strip(),
    )
