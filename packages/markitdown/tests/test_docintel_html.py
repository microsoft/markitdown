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


def test_docintel_api_version_default_none():
    from unittest.mock import patch

    with patch(
        "markitdown.converters._doc_intel_converter.DocumentIntelligenceClient"
    ) as mock_client:
        conv = DocumentIntelligenceConverter(
            endpoint="https://example.cognitiveservices.azure.com/",
        )
        assert conv.api_version is None
        mock_client.assert_called_once()
        _, kwargs = mock_client.call_args
        assert "api_version" not in kwargs


def test_docintel_api_version_custom():
    from unittest.mock import patch

    with patch(
        "markitdown.converters._doc_intel_converter.DocumentIntelligenceClient"
    ) as mock_client:
        conv = DocumentIntelligenceConverter(
            endpoint="https://example.cognitiveservices.azure.com/",
            api_version="2024-07-31-preview",
        )
        assert conv.api_version == "2024-07-31-preview"
        mock_client.assert_called_once()
        _, kwargs = mock_client.call_args
        assert kwargs.get("api_version") == "2024-07-31-preview"
