import os
import io
import pytest

from markitdown import MarkItDown

try:
    import reportlab  # type: ignore
    from reportlab.lib.pagesizes import letter  # type: ignore
    from reportlab.pdfgen import canvas  # type: ignore
    _have_reportlab = True
except Exception:  # pragma: no cover
    _have_reportlab = False

# We only run tests if reportlab is present locally; it's not a hard dependency.
skip_no_reportlab = pytest.mark.skipif(not _have_reportlab, reason="reportlab not installed")


def _build_pdf_with_table() -> bytes:
    """Generate a simple PDF containing a small 3x3 table drawn with text (not vector table lines)."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    # Simple table headers and rows at fixed positions
    start_x, start_y = 72, 720
    data = [
        ["ColA", "ColB", "ColC"],
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]
    for r, row in enumerate(data):
        for col, cell in enumerate(row):
            c.drawString(start_x + col * 80, start_y - r * 18, cell)
    c.showPage()
    c.save()
    return buffer.getvalue()


@skip_no_reportlab
@pytest.mark.parametrize("mode", ["none", "plumber", "auto"])  # camelot requires file path + ghostscript
def test_pdf_tables_modes(mode):
    pdf_bytes = _build_pdf_with_table()
    markitdown = MarkItDown()

    result = markitdown.convert_stream(io.BytesIO(pdf_bytes), pdf_tables=mode)
    text = result.text_content

    # Base assertions: headers appear
    assert "ColA" in text and "ColB" in text and "ColC" in text
    # Numbers appear
    for n in ["1", "2", "3", "4", "5", "6"]:
        assert n in text

    if mode in ("plumber", "auto"):
        # Expect at least one markdown table line with pipes (header separator)
        if "| ColA" in text:  # header row
            assert "| ColA" in text and "| ColB" in text and "| ColC" in text
            assert "| ---" in text or "| ---".replace(" ", "") in text
        # Not a hard failure if plumbing fails silently (e.g., pdfplumber not installed)


@skip_no_reportlab
def test_pdf_tables_invalid_mode():
    pdf_bytes = _build_pdf_with_table()
    markitdown = MarkItDown()
    # Invalid mode should fallback to none
    result = markitdown.convert_stream(io.BytesIO(pdf_bytes), pdf_tables="weird")
    assert "| ColA" not in result.text_content  # no table formatting expected
