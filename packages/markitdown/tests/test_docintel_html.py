import io
import markitdown.converters._doc_intel_converter as docintel
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


def test_docintel_uses_sdk_default_api_version(monkeypatch):
    captured_args = {}

    class FakeDocumentIntelligenceClient:
        def __init__(self, **kwargs):
            captured_args.update(kwargs)

    monkeypatch.setattr(docintel, "_dependency_exc_info", None)
    monkeypatch.setattr(
        docintel, "DocumentIntelligenceClient", FakeDocumentIntelligenceClient
    )

    credential = object()
    conv = DocumentIntelligenceConverter(
        endpoint="https://example.cognitiveservices.azure.com/",
        credential=credential,
    )

    assert conv.api_version is None
    assert "api_version" not in captured_args
    assert captured_args["endpoint"] == "https://example.cognitiveservices.azure.com/"
    assert captured_args["credential"] is credential


def test_docintel_passes_explicit_api_version(monkeypatch):
    captured_args = {}

    class FakeDocumentIntelligenceClient:
        def __init__(self, **kwargs):
            captured_args.update(kwargs)

    monkeypatch.setattr(docintel, "_dependency_exc_info", None)
    monkeypatch.setattr(
        docintel, "DocumentIntelligenceClient", FakeDocumentIntelligenceClient
    )

    DocumentIntelligenceConverter(
        endpoint="https://example.cognitiveservices.azure.com/",
        credential=object(),
        api_version="2024-07-31-preview",
    )

    assert captured_args["api_version"] == "2024-07-31-preview"
