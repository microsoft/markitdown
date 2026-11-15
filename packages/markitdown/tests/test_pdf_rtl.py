"""PDFs whose right-to-left text (Arabic, Hebrew) is drawn in visual order."""

import io
import unicodedata

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters._pdf_converter import _visual_line_to_logical


def _build_pdf(glyph_lines: list[list[str]], draw_in_visual_order: bool) -> bytes:
    """
    Build a one-page PDF whose glyphs carry the given texts.

    Each line lists glyph texts from left to right as they appear on the page.
    A combining mark is placed on the glyph that follows it in the list. The
    glyphs are drawn either left to right (visual order) or right to left,
    which is the reading order for right-to-left lines.
    """
    codes: dict[str, int] = {}
    for line in glyph_lines:
        for text in line:
            codes.setdefault(text, 0x21 + len(codes))

    def is_mark(text: str) -> bool:
        return unicodedata.category(text[0]) == "Mn"

    operations = []
    for line_no, line in enumerate(glyph_lines):
        y = 700 - 20 * line_no
        placed = []
        x = 72.0
        for text in line:
            placed.append((text, x))
            if not is_mark(text):
                x += 6
        if not draw_in_visual_order:
            placed.reverse()
        for text, x in placed:
            operations.append(f"1 0 0 1 {x:.1f} {y} Tm <{codes[text]:02X}> Tj")
    content = ("BT /F1 10 Tf\n" + "\n".join(operations) + "\nET").encode()

    def utf16_hex(text: str) -> str:
        return text.encode("utf-16-be").hex().upper()

    bfchars = "\n".join(
        f"<{code:02X}> <{utf16_hex(text)}>" for text, code in codes.items()
    )
    cmap = (
        "/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n"
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
        "/CMapName /Adobe-Identity-UCS def\n/CMapType 2 def\n"
        "1 begincodespacerange\n<00> <FF>\nendcodespacerange\n"
        f"{len(codes)} beginbfchar\n{bfchars}\nendbfchar\n"
        "endcmap\nCMapName currentdict /CMap defineresource pop\nend\nend"
    ).encode()
    widths = " ".join("0" if is_mark(text) else "600" for text in codes)

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /TrueType /BaseFont /TestFont "
        + f"/FirstChar 33 /LastChar {0x20 + len(codes)} /Widths [{widths}] ".encode()
        + b"/ToUnicode 6 0 R >>",
        b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
        b"<< /Length %d >>\nstream\n" % len(cmap) + cmap + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(pdf)
    pdf += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for offset in offsets:
        pdf += b"%010d 00000 n \n" % offset
    pdf += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1,
        xref,
    )
    return bytes(pdf)


def _convert(pdf: bytes) -> str:
    result = MarkItDown().convert_stream(
        io.BytesIO(pdf), stream_info=StreamInfo(extension=".pdf")
    )
    return result.text_content.strip()


# Left-to-right glyph texts of right-to-left lines, as a PDF shows them. "لا" is
# one ligature glyph, and the shadda in "لتكوّن" is drawn before the waw it sits on.
VISUAL_LINES = {
    "مرحبا بالعالم": list("ملاعلاب ابحرم"),
    "كتاب (Lorem Ipsum) سنة 2026": list("2026 ةنس )Lorem Ipsum( باتك"),
    "السعر 3.5 دينار أو 50%": list("50% وأ رانيد 3.5 رعسلا"),
    "ولايزال": ["ل", "ا", "ز", "ي", "لا", "و"],
    "لتكوّن": ["ن", "\u0651", "و", "ك", "ت", "ل"],
}


@pytest.mark.parametrize("logical", list(VISUAL_LINES))
def test_visual_order_rtl_line_is_put_in_reading_order(logical):
    assert _visual_line_to_logical(VISUAL_LINES[logical]) == logical


@pytest.mark.parametrize(
    "before,rtl_words,after",
    [
        ("Price in ", "مصر", " is 5"),
        ("Welcome to ", "الشرق الأوسط", " region"),
        ("Only Latin text, 2026", "", ""),
    ],
)
def test_ltr_line_reverses_only_rtl_runs(before, rtl_words, after):
    visual = list(before + rtl_words[::-1] + after)
    assert _visual_line_to_logical(visual) == before + rtl_words + after


def test_pdf_drawn_in_visual_order_is_extracted_in_reading_order():
    pdf = _build_pdf(list(VISUAL_LINES.values()), draw_in_visual_order=True)
    assert _convert(pdf).splitlines() == list(VISUAL_LINES)


def test_pdf_drawn_in_reading_order_is_unchanged():
    lines = ["مرحبا بالعالم", "كتاب جديد"]
    glyph_lines = [list(reversed(line)) for line in lines]
    pdf = _build_pdf(glyph_lines, draw_in_visual_order=False)
    text = _convert(pdf)
    for line in lines:
        assert line in text
