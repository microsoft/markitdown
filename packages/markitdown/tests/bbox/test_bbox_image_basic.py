import io
from pathlib import Path
import io

import pytest
from PIL import Image, ImageDraw

from markitdown import MarkItDown, StreamInfo


def test_bbox_image_basic(tmp_path: Path):
    pytesseract = pytest.importorskip("pytesseract")
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        pytest.skip("tesseract not installed")
    img = Image.new("RGB", (200, 60), color="white")
    d = ImageDraw.Draw(img)
    d.text((10, 10), "Hello 123", fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    md = MarkItDown()
    res = md.convert_stream(
        buf,
        stream_info=StreamInfo(extension=".png"),
        emit_bbox=True,
    )
    assert res.bbox is not None
    bbox = res.bbox
    assert bbox.words
    for w in bbox.words:
        assert all(0 <= v <= 1 for v in w.bbox_norm)
