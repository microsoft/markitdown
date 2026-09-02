import io
from markitdown.converters._doc_intel_converter import (
    DEFAULT_DOCUMENT_INTELLIGENCE_API_VERSION,
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


def test_docintel_default_api_version(monkeypatch):
    captured = {}

    class FakeClient:
        def __init__(self, *, endpoint, api_version, credential):
            captured["endpoint"] = endpoint
            captured["api_version"] = api_version
            captured["credential"] = credential

    monkeypatch.setattr(
        "markitdown.converters._doc_intel_converter._dependency_exc_info", None
    )
    monkeypatch.setattr(
        "markitdown.converters._doc_intel_converter.DocumentIntelligenceClient",
        FakeClient,
    )

    credential = object()
    converter = DocumentIntelligenceConverter(
        endpoint="https://example.cognitiveservices.azure.com/",
        credential=credential,
    )

    assert converter.api_version == DEFAULT_DOCUMENT_INTELLIGENCE_API_VERSION
    assert captured["api_version"] == DEFAULT_DOCUMENT_INTELLIGENCE_API_VERSION
    assert captured["credential"] is credential


def test_docintel_explicit_api_version(monkeypatch):
    captured = {}

    class FakeClient:
        def __init__(self, *, endpoint, api_version, credential):
            captured["api_version"] = api_version

    monkeypatch.setattr(
        "markitdown.converters._doc_intel_converter._dependency_exc_info", None
    )
    monkeypatch.setattr(
        "markitdown.converters._doc_intel_converter.DocumentIntelligenceClient",
        FakeClient,
    )

    converter = DocumentIntelligenceConverter(
        endpoint="https://example.cognitiveservices.azure.com/",
        credential=object(),
        api_version="2024-07-31-preview",
    )

    assert converter.api_version == "2024-07-31-preview"
    assert captured["api_version"] == "2024-07-31-preview"
