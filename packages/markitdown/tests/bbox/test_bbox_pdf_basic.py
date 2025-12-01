import io
from pathlib import Path

import json
import jsonschema
from reportlab.pdfgen import canvas

from markitdown import MarkItDown, StreamInfo


def _make_pdf() -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(100, 700, "Hello")
    c.showPage()
    c.drawString(100, 700, "World")
    c.save()
    return buf.getvalue()


def test_bbox_pdf_basic(tmp_path: Path):
    pdf_bytes = _make_pdf()
    md = MarkItDown()
    res = md.convert_stream(
        io.BytesIO(pdf_bytes),
        stream_info=StreamInfo(extension=".pdf"),
        emit_bbox=True,
    )
    assert res.bbox is not None
    bbox = res.bbox
    assert len(bbox.pages) == 2
    for p in bbox.pages:
        assert p.width > 0 and p.height > 0
    assert bbox.words
    for w in bbox.words:
        assert all(0 <= v <= 1 for v in w.bbox_norm)
        assert 0 <= w.line_id < len(bbox.lines)
    for idx, line in enumerate(bbox.lines):
        lw = [w.text for w in bbox.words if w.line_id == idx]
        assert " ".join(lw).strip() == line.text.strip()
    schema = json.load(open(Path(__file__).parent / "schema.json"))
    jsonschema.validate(instance=bbox.to_dict(), schema=schema)
