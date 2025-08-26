import io
from markitdown.converters._doc_intel_converter import (
    DocumentIntelligenceConverter,
    DocumentIntelligenceFileType,
)
from markitdown._stream_info import StreamInfo


def _make_converter(file_types):
    conv = DocumentIntelligenceConverter.__new__(DocumentIntelligenceConverter)
    conv._file_types = file_types
    return conv


def test_docintel_accepts_html_extension():
    conv = _make_converter([DocumentIntelligenceFileType.HTML])
    stream_info = StreamInfo(mimetype=None, extension=".html")
    assert conv.accepts(io.BytesIO(b""), stream_info)


def test_docintel_accepts_html_mimetype():
    conv = _make_converter([DocumentIntelligenceFileType.HTML])
    stream_info = StreamInfo(mimetype="text/html", extension=None)
    assert conv.accepts(io.BytesIO(b""), stream_info)
    stream_info = StreamInfo(mimetype="application/xhtml+xml", extension=None)
    assert conv.accepts(io.BytesIO(b""), stream_info)
