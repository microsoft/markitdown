import io
import sys
import time

from markitdown import MarkItDown, StreamInfo


def test_no_overhead_when_disabled():
    md = MarkItDown()
    sys.modules.pop("pytesseract", None)
    sys.modules.pop("pdfplumber", None)
    stream = io.BytesIO(b"hello world")
    start = time.time()
    md.convert_stream(stream, stream_info=StreamInfo(extension=".txt"), emit_bbox=False)
    t_disabled = time.time() - start
    assert "pytesseract" not in sys.modules
    assert "pdfplumber" not in sys.modules
    assert t_disabled < 0.5

    stream = io.BytesIO(b"hello world")
    start = time.time()
    md.convert_stream(stream, stream_info=StreamInfo(extension=".txt"), emit_bbox=True)
    t_enabled = time.time() - start
    assert t_enabled < 0.5
    assert "pytesseract" not in sys.modules
    assert "pdfplumber" not in sys.modules
