import io
from pathlib import Path

import pytest
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas

from markitdown import MarkItDown, StreamInfo


def test_bbox_pdf_scanned_fallback(tmp_path: Path):
    pytesseract = pytest.importorskip("pytesseract")
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        pytest.skip("tesseract not installed")
    img = Image.new("RGB", (200, 60), color="white")
    d = ImageDraw.Draw(img)
    d.text((10, 10), "OCR", fill="black")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    c.drawInlineImage(Image.open(img_bytes), 0, 0)
    c.save()
    pdf_bytes = buf.getvalue()

    md = MarkItDown()
    res = md.convert_stream(
        io.BytesIO(pdf_bytes),
        stream_info=StreamInfo(extension=".pdf"),
        emit_bbox=True,
    )
    assert res.bbox is not None
    assert len(res.bbox.words) >= 1
    for w in res.bbox.words:
        assert all(0 <= v <= 1 for v in w.bbox_norm)
