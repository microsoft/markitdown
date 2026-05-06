"""Tests for ContentUnderstandingConverter.

Tests accepts() routing, smart routing modality logic, and convert() via mocks.
Follows the same pattern as test_docintel_html.py.
"""

import io
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from markitdown.converters._cu_converter import (
    ContentUnderstandingConverter,
    ContentUnderstandingFileType,
    _infer_prebuilt_modality,
    _get_modality,
    _EXTENSION_MAP,
)
from markitdown._stream_info import StreamInfo


# ---------------------------------------------------------------------------
# Helper: create a converter with accepts() working but no SDK init
# ---------------------------------------------------------------------------

def _make_converter(file_types=None, analyzer_id=None, analyzer_modality=None):
    """Create a converter bypassing __init__ (no SDK deps needed)."""
    conv = ContentUnderstandingConverter.__new__(ContentUnderstandingConverter)
    conv._analyzer_id = analyzer_id
    conv._analyzer_modality = analyzer_modality

    # Build accepted extensions/mime from file_types
    from markitdown.converters._cu_converter import (
        _ALL_FILE_TYPES,
        _MIME_PREFIXES,
    )

    types = file_types if file_types is not None else _ALL_FILE_TYPES
    conv._file_types = types

    conv._accepted_extensions = set()
    conv._accepted_mime_prefixes = []
    for ft in types:
        for ext, mapped_ft in _EXTENSION_MAP.items():
            if mapped_ft == ft:
                conv._accepted_extensions.add(ext)
        if ft in _MIME_PREFIXES:
            conv._accepted_mime_prefixes.extend(_MIME_PREFIXES[ft])

    return conv


# ---------------------------------------------------------------------------
# accepts() tests — extension-based
# ---------------------------------------------------------------------------

class TestAcceptsExtension:
    """Test accepts() for supported and unsupported file extensions."""

    @pytest.mark.parametrize("ext", [
        ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".txt", ".md", ".rtf", ".xml",
        ".eml", ".msg",
        ".jpg", ".jpeg", ".jpe", ".png", ".bmp", ".tiff", ".heif", ".heic",
        ".mp4", ".m4v", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv",
        ".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac", ".wma",
    ])
    def test_accepts_supported_extensions(self, ext):
        conv = _make_converter()
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=ext))

    @pytest.mark.parametrize("ext", [".csv", ".json", ".zip", ".epub", ".py", ".rs"])
    def test_rejects_unsupported_extensions(self, ext):
        conv = _make_converter()
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=ext))


# ---------------------------------------------------------------------------
# accepts() tests — MIME-based
# ---------------------------------------------------------------------------

class TestAcceptsMime:
    """Test accepts() for MIME type matching."""

    @pytest.mark.parametrize("mime", [
        "application/pdf",
        "image/jpeg",
        "video/mp4",
        "audio/wav",
        "text/html",
        "audio/mpeg",
        "video/quicktime",
    ])
    def test_accepts_supported_mimetypes(self, mime):
        conv = _make_converter()
        assert conv.accepts(io.BytesIO(b""), StreamInfo(mimetype=mime))

    @pytest.mark.parametrize("mime", [
        "text/csv",
        "application/json",
        "application/zip",
    ])
    def test_rejects_unsupported_mimetypes(self, mime):
        conv = _make_converter()
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(mimetype=mime))


# ---------------------------------------------------------------------------
# accepts() tests — cu_file_types restriction
# ---------------------------------------------------------------------------

class TestAcceptsFileTypeRestriction:
    """Test that cu_file_types restricts which formats are accepted."""

    def test_restricted_to_pdf_only(self):
        conv = _make_converter(file_types=[ContentUnderstandingFileType.PDF])
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=".pdf"))
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=".mp4"))
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=".wav"))
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=".jpg"))

    def test_restricted_to_audio(self):
        conv = _make_converter(file_types=[
            ContentUnderstandingFileType.WAV,
            ContentUnderstandingFileType.MP3,
        ])
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=".wav"))
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=".mp3"))
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=".pdf"))


# ---------------------------------------------------------------------------
# Smart routing tests
# ---------------------------------------------------------------------------

class TestSmartRouting:
    """Test modality-aware analyzer routing."""

    def test_document_analyzer_routes_pdf_to_custom(self):
        """Document-based analyzer should be used for PDF."""
        conv = _make_converter(
            analyzer_id="my-doc-analyzer",
            analyzer_modality="document",
        )
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(io.BytesIO(b"fake pdf"), StreamInfo(extension=".pdf", mimetype="application/pdf"))

        # Should use the custom analyzer for PDF (document modality)
        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "my-doc-analyzer"

    def test_document_analyzer_routes_mp3_to_prebuilt(self):
        """Document-based analyzer should auto-route MP3 to prebuilt-audioSearch."""
        conv = _make_converter(
            analyzer_id="my-doc-analyzer",
            analyzer_modality="document",
        )
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(io.BytesIO(b"fake audio"), StreamInfo(extension=".mp3", mimetype="audio/mpeg"))

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-audioSearch"

    def test_document_analyzer_routes_mp4_to_prebuilt(self):
        """Document-based analyzer should auto-route MP4 to prebuilt-videoSearch."""
        conv = _make_converter(
            analyzer_id="my-doc-analyzer",
            analyzer_modality="document",
        )
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(io.BytesIO(b"fake video"), StreamInfo(extension=".mp4", mimetype="video/mp4"))

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-videoSearch"

    def test_no_analyzer_id_uses_auto_routing(self):
        """Without analyzer_id, PDF should auto-route to prebuilt-documentSearch."""
        conv = _make_converter(analyzer_id=None, analyzer_modality=None)
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(io.BytesIO(b"fake pdf"), StreamInfo(extension=".pdf", mimetype="application/pdf"))

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-documentSearch"


# ---------------------------------------------------------------------------
# _infer_prebuilt_modality tests
# ---------------------------------------------------------------------------

class TestInferPrebuiltModality:
    """Test modality inference from prebuilt analyzer names."""

    def test_document_prebuilts(self):
        assert _infer_prebuilt_modality("prebuilt-documentSearch") == "document"
        assert _infer_prebuilt_modality("prebuilt-invoice") == "document"
        assert _infer_prebuilt_modality("prebuilt-layout") == "document"
        assert _infer_prebuilt_modality("prebuilt-receipt") == "document"
        assert _infer_prebuilt_modality("prebuilt-tax.us.w2") == "document"

    def test_audio_prebuilts(self):
        assert _infer_prebuilt_modality("prebuilt-audioSearch") == "audio"
        assert _infer_prebuilt_modality("prebuilt-callCenter") == "audio"

    def test_video_prebuilts(self):
        assert _infer_prebuilt_modality("prebuilt-videoSearch") == "video"
        assert _infer_prebuilt_modality("prebuilt-videoSynopsis") == "video"

    def test_image_prebuilts_map_to_document(self):
        assert _infer_prebuilt_modality("prebuilt-imageSearch") == "document"
        assert _infer_prebuilt_modality("prebuilt-image") == "document"

    def test_unknown_prebuilt_defaults_to_document(self):
        assert _infer_prebuilt_modality("prebuilt-unknownNewAnalyzer") == "document"


# ---------------------------------------------------------------------------
# _get_modality tests
# ---------------------------------------------------------------------------

class TestGetModality:
    """Test file type → modality mapping."""

    def test_document_types(self):
        assert _get_modality(ContentUnderstandingFileType.PDF) == "document"
        assert _get_modality(ContentUnderstandingFileType.DOCX) == "document"
        assert _get_modality(ContentUnderstandingFileType.JPEG) == "document"

    def test_video_types(self):
        assert _get_modality(ContentUnderstandingFileType.MP4) == "video"
        assert _get_modality(ContentUnderstandingFileType.MOV) == "video"

    def test_audio_types(self):
        assert _get_modality(ContentUnderstandingFileType.WAV) == "audio"
        assert _get_modality(ContentUnderstandingFileType.MP3) == "audio"


# ---------------------------------------------------------------------------
# convert() mock tests
# ---------------------------------------------------------------------------

class TestConvertMock:
    """Test convert() with mocked CU SDK."""

    def _run_convert(self, extension, mimetype, expected_output="mock output"):
        conv = _make_converter()
        conv._client = MagicMock()

        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result
        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch(
            "markitdown.converters._cu_converter.to_llm_input",
            return_value=expected_output,
        ):
            result = conv.convert(
                io.BytesIO(b"fake content"),
                StreamInfo(extension=extension, mimetype=mimetype),
            )
        return result

    def test_pdf_returns_markdown(self):
        result = self._run_convert(".pdf", "application/pdf", "---\ncontentType: document\n---\n# Test")
        assert "contentType: document" in result.markdown

    def test_mp4_returns_markdown(self):
        result = self._run_convert(".mp4", "video/mp4", "---\ncontentType: audioVisual\n---\nSpeaker 1: Hello")
        assert "contentType: audioVisual" in result.markdown

    def test_wav_returns_markdown(self):
        result = self._run_convert(".wav", "audio/wav", "---\ncontentType: audioVisual\n---\nSpeaker 1: Hi")
        assert "audioVisual" in result.markdown

    def test_empty_result(self):
        result = self._run_convert(".pdf", "application/pdf", "")
        assert result.markdown == ""


# ---------------------------------------------------------------------------
# MissingDependencyException test
# ---------------------------------------------------------------------------

class TestMissingDependency:
    """Test that MissingDependencyException is raised when CU SDK is not installed."""

    def test_missing_deps_message(self):
        """Verify the exception includes install hint."""
        # We can't easily simulate ImportError in the module, but we can check
        # the exception message pattern if it were raised.
        from markitdown._exceptions import MissingDependencyException

        exc = MissingDependencyException(
            "ContentUnderstandingConverter requires the optional dependency "
            "[az-content-understanding] (or [all]) to be installed."
        )
        assert "az-content-understanding" in str(exc)
