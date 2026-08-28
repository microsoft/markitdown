import inspect
import io
from markitdown.converters._doc_intel_converter import (
    DocumentIntelligenceConverter,
    DocumentIntelligenceFileType,
)
from markitdown._stream_info import StreamInfo


def _default_file_types():
    params = inspect.signature(DocumentIntelligenceConverter.__init__).parameters
    return params["file_types"].default


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


def test_docintel_default_file_types_cover_every_supported_type():
    # The file_types docstring promises "Defaults to all supported file types",
    # so the default must stay in sync with the enum.
    assert set(_default_file_types()) == set(DocumentIntelligenceFileType)


def test_docintel_default_accepts_html():
    conv = _make_converter(_default_file_types())
    for stream_info in (
        StreamInfo(mimetype=None, extension=".html"),
        StreamInfo(mimetype="text/html", extension=None),
        StreamInfo(mimetype="application/xhtml+xml", extension=None),
    ):
        assert conv.accepts(io.BytesIO(b""), stream_info)
