"""Build minimal PDFs containing vector graphics, using only the standard library.

Run from packages/markitdown with:
    python tests/test_files/generate_vector_graphics_fixtures.py
Only vector_graphics_*.pdf is written. Output is deterministic.

Each page carries a short text line (Helvetica) plus drawing operators:
- vector_graphics_curve.pdf: one page with a Bezier pie slice.
- vector_graphics_mixed.pdf: page 1 curve, page 2 text only, page 3 polyline chart.
- vector_graphics_rule_only.pdf: a horizontal rule and a rectangle box (no curves).
- vector_graphics_form_xobject.pdf: a Bezier drawn inside a form XObject.
"""

from pathlib import Path
from typing import List, Optional

FIXTURES = Path(__file__).resolve().parent

PIE_SLICE = "300 400 m 400 400 l 400 455 355 500 300 500 c h f"
POLYLINE = "100 100 m 150 200 l 200 150 l 250 300 l 300 250 l S"
RULE_AND_BOX = "72 650 m 540 650 l S 100 300 200 100 re S"


def _text(line: str) -> str:
    return f"BT /F1 12 Tf 72 720 Td ({line}) Tj ET"


def _build_pdf(pages: List[str], form_xobject: Optional[str] = None) -> bytes:
    """Return PDF bytes with one content stream per page."""
    objects: List[bytes] = []

    def add(body: str) -> int:
        objects.append(body.encode("latin-1"))
        return len(objects)

    def add_stream(content: str, extra: str = "") -> int:
        data = content.encode("latin-1")
        return add(f"<</Length {len(data)}{extra}>>stream\n{content}\nendstream")

    catalog = add("")  # placeholder, filled in below
    pages_obj = add("")  # placeholder, filled in below
    font = add("<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>")
    xobject_res = ""
    if form_xobject is not None:
        fx = add_stream(form_xobject, "/Type/XObject/Subtype/Form/BBox[0 0 612 792]")
        xobject_res = f"/XObject<</Fx {fx} 0 R>>"

    kids = []
    for content in pages:
        contents = add_stream(content)
        page = add(
            f"<</Type/Page/Parent {pages_obj} 0 R/MediaBox[0 0 612 792]"
            f"/Resources<</Font<</F1 {font} 0 R>>{xobject_res}>>"
            f"/Contents {contents} 0 R>>"
        )
        kids.append(f"{page} 0 R")

    objects[catalog - 1] = f"<</Type/Catalog/Pages {pages_obj} 0 R>>".encode()
    objects[pages_obj - 1] = (
        f"<</Type/Pages/Kids[{' '.join(kids)}]/Count {len(kids)}>>".encode()
    )

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (
        f"trailer<</Size {len(objects) + 1}/Root {catalog} 0 R>>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode()
    return bytes(out)


def main() -> None:
    fixtures = {
        "vector_graphics_curve.pdf": _build_pdf(
            [_text("Quarterly revenue chart") + "\n" + PIE_SLICE]
        ),
        "vector_graphics_mixed.pdf": _build_pdf(
            [
                _text("Page one has a pie chart") + "\n" + PIE_SLICE,
                _text("Page two is text only"),
                _text("Page three has a line chart") + "\n" + POLYLINE,
            ]
        ),
        "vector_graphics_rule_only.pdf": _build_pdf(
            [_text("Ruled page with a box") + "\n" + RULE_AND_BOX]
        ),
        "vector_graphics_form_xobject.pdf": _build_pdf(
            [_text("Figure drawn in a form XObject") + "\n/Fx Do"],
            form_xobject=PIE_SLICE,
        ),
    }
    for name, data in fixtures.items():
        (FIXTURES / name).write_bytes(data)


if __name__ == "__main__":
    main()
