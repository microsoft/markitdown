import io
import json
from pathlib import Path
import io
import json
import pytest

import jsonschema
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas

from markitdown import MarkItDown, StreamInfo


def _make_pdf() -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(100, 700, "One")
    c.showPage()
    c.save()
    return buf.getvalue()


def _make_png() -> bytes:
    img = Image.new("RGB", (100, 40), color="white")
    d = ImageDraw.Draw(img)
    d.text((5, 5), "img", fill="black")
    b = io.BytesIO()
    img.save(b, format="PNG")
    return b.getvalue()


def _validate(bbox_dict, schema):
    jsonschema.validate(instance=bbox_dict, schema=schema)


def test_bbox_schema_validation(tmp_path: Path):
    pytesseract = pytest.importorskip("pytesseract")
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        pytest.skip("tesseract not installed")
    schema = json.load(open(Path(__file__).parent / "schema.json"))
    md = MarkItDown()

    pdf_res = md.convert_stream(
        io.BytesIO(_make_pdf()),
        stream_info=StreamInfo(extension=".pdf"),
        emit_bbox=True,
    )
    assert pdf_res.bbox is not None
    _validate(pdf_res.bbox.to_dict(), schema)

    png_res = md.convert_stream(
        io.BytesIO(_make_png()),
        stream_info=StreamInfo(extension=".png"),
        emit_bbox=True,
    )
    assert png_res.bbox is not None
    _validate(png_res.bbox.to_dict(), schema)
