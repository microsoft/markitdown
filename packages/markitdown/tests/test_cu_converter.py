"""Tests for ContentUnderstandingConverter.

Tests accepts() routing, smart routing modality logic, and convert() via mocks.
Follows the same pattern as test_docintel_html.py.
"""

import io
import sys
from unittest.mock import MagicMock, patch

import pytest

from markitdown.converters._cu_converter import (
    ContentUnderstandingConverter,
    ContentUnderstandingFileType,
    _resolve_analyzer_modality,
    _get_modality,
    _detect_file_type,
    _canonical_mime_type,
    _content_type_for,
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

    # Set accepted file types without running SDK-dependent initialization.
    from markitdown.converters._cu_converter import (
        _ALL_FILE_TYPES,
    )

    types = file_types if file_types is not None else _ALL_FILE_TYPES
    conv._file_types = types

    return conv


# ---------------------------------------------------------------------------
# accepts() tests — extension-based
# ---------------------------------------------------------------------------


class TestAcceptsExtension:
    """Test accepts() for supported and unsupported file extensions."""

    @pytest.mark.parametrize(
        "ext",
        [
            ".pdf",
            ".docx",
            ".pptx",
            ".xlsx",
            ".html",
            ".txt",
            ".md",
            ".rtf",
            ".xml",
            ".eml",
            ".msg",
            ".jpg",
            ".jpeg",
            ".jpe",
            ".png",
            ".bmp",
            ".tiff",
            ".heif",
            ".heic",
            ".mp4",
            ".m4v",
            ".mov",
            ".avi",
            ".mkv",
            ".webm",
            ".flv",
            ".wmv",
            ".wav",
            ".mp3",
            ".m4a",
            ".flac",
            ".ogg",
            ".aac",
            ".wma",
        ],
    )
    def test_accepts_supported_extensions(self, ext):
        conv = _make_converter()
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=ext))

    @pytest.mark.parametrize(
        "ext",
        [
            ".csv",
            ".json",
            ".zip",
            ".epub",
            ".py",
            ".rs",
        ],
    )
    def test_rejects_unsupported_extensions(self, ext):
        conv = _make_converter()
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=ext))


# ---------------------------------------------------------------------------
# accepts() tests — MIME-based
# ---------------------------------------------------------------------------


class TestAcceptsMime:
    """Test accepts() for MIME type matching."""

    @pytest.mark.parametrize(
        "mime",
        [
            "application/pdf",
            "image/jpeg",
            "video/mp4",
            "audio/wav",
            "audio/x-wav",
            "text/html",
            "audio/mpeg",
            "audio/x-m4a",
            "audio/x-flac",
            "video/quicktime",
            "video/webm",
            "video/x-m4v",
            "video/x-flv",
            "video/x-ms-wmv",
            "audio/aac",
            "audio/x-ms-wma",
        ],
    )
    def test_accepts_supported_mimetypes(self, mime):
        conv = _make_converter()
        assert conv.accepts(io.BytesIO(b""), StreamInfo(mimetype=mime))

    @pytest.mark.parametrize(
        "mime",
        [
            "text/csv",
            "application/json",
            "application/zip",
        ],
    )
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
        conv = _make_converter(
            file_types=[
                ContentUnderstandingFileType.WAV,
                ContentUnderstandingFileType.MP3,
            ]
        )
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=".wav"))
        assert conv.accepts(io.BytesIO(b""), StreamInfo(extension=".mp3"))
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=".pdf"))

    def test_webm_value_matches_cli_input(self):
        assert ContentUnderstandingFileType("webm") == ContentUnderstandingFileType.WEBM

    def test_m4v_value_matches_cli_input(self):
        assert ContentUnderstandingFileType("m4v") == ContentUnderstandingFileType.M4V


# ---------------------------------------------------------------------------
# file type detection tests
# ---------------------------------------------------------------------------


class TestDetectFileType:
    """Test extension and MIME based file type detection."""

    def test_detects_video_from_mime_without_extension(self):
        assert (
            _detect_file_type(StreamInfo(mimetype="video/mp4"))
            == ContentUnderstandingFileType.MP4
        )

    def test_detects_audio_from_mime_without_extension(self):
        assert (
            _detect_file_type(StreamInfo(mimetype="audio/mpeg"))
            == ContentUnderstandingFileType.MP3
        )

    def test_detects_audio_alias_from_mime_without_extension(self):
        assert (
            _detect_file_type(StreamInfo(mimetype="audio/x-wav"))
            == ContentUnderstandingFileType.WAV
        )

    def test_detects_video_alias_from_mime_without_extension(self):
        assert (
            _detect_file_type(StreamInfo(mimetype="video/x-m4v"))
            == ContentUnderstandingFileType.M4V
        )

    @pytest.mark.parametrize(
        ("mimetype", "expected"),
        [
            ("audio/x-wav", "audio/wav"),
            ("audio/x-flac", "audio/flac"),
            ("audio/x-m4a", "audio/mp4"),
            ("video/x-m4v", "video/mp4"),
            ("video/mp4", "video/mp4"),
            (None, "application/octet-stream"),
        ],
    )
    def test_canonical_mime_type(self, mimetype, expected):
        assert _canonical_mime_type(mimetype) == expected

    @pytest.mark.parametrize(
        ("file_type", "mimetype", "expected"),
        [
            (ContentUnderstandingFileType.PDF, None, "application/pdf"),
            (ContentUnderstandingFileType.M4V, None, "video/mp4"),
            (ContentUnderstandingFileType.FLAC, "audio/x-flac", "audio/flac"),
        ],
    )
    def test_content_type_for(self, file_type, mimetype, expected):
        assert _content_type_for(file_type, mimetype) == expected

    @pytest.mark.parametrize(
        ("file_type", "mimetype", "expected"),
        [
            # Extension/file_type wins when mimetype disagrees — the
            # resolved file_type is the single source of truth so that
            # analyzer routing and payload metadata stay consistent.
            (ContentUnderstandingFileType.PDF, "audio/mpeg", "application/pdf"),
            (ContentUnderstandingFileType.MP3, "application/pdf", "audio/mpeg"),
            (ContentUnderstandingFileType.MP4, "image/jpeg", "video/mp4"),
            (ContentUnderstandingFileType.JPEG, "video/mp4", "image/jpeg"),
            # Subtype distinctions are preserved when consistent
            # (e.g., HEIC vs HEIF both map to file_type HEIF; if the
            # caller passed image/heic explicitly, keep it).
            (ContentUnderstandingFileType.HEIF, "image/heic", "image/heic"),
            (ContentUnderstandingFileType.HEIF, "image/heif", "image/heif"),
        ],
    )
    def test_content_type_for_resolves_conflicts_to_file_type(
        self, file_type, mimetype, expected
    ):
        """When extension and mimetype disagree, file_type wins."""
        assert _content_type_for(file_type, mimetype) == expected

    def test_conflicting_extension_and_mimetype_in_convert(self):
        """End-to-end: conflicting StreamInfo routes by extension and
        sends a content_type consistent with the resolved file_type."""
        conv = _make_converter()
        conv._client = MagicMock()
        mock_poller = MagicMock()
        mock_poller.result.return_value = MagicMock(contents=[])
        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch(
            "markitdown.converters._cu_converter.to_llm_input",
            return_value="ok",
        ):
            conv.convert(
                io.BytesIO(b"fake"),
                # .pdf extension but bogus audio mimetype
                StreamInfo(extension=".pdf", mimetype="audio/mpeg"),
            )

        call_kwargs = conv._client.begin_analyze_binary.call_args.kwargs
        # Routed by extension: document modality → prebuilt-documentSearch
        assert call_kwargs["analyzer_id"] == "prebuilt-documentSearch"
        # content_type derived from file_type (PDF), not the conflicting mime
        assert call_kwargs["content_type"] == "application/pdf"

    def test_file_type_restriction_applies_to_mime(self):
        assert (
            _detect_file_type(
                StreamInfo(mimetype="video/mp4"),
                [ContentUnderstandingFileType.PDF],
            )
            is None
        )


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
            conv.convert(
                io.BytesIO(b"fake pdf"),
                StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

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
            conv.convert(
                io.BytesIO(b"fake audio"),
                StreamInfo(extension=".mp3", mimetype="audio/mpeg"),
            )

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
            conv.convert(
                io.BytesIO(b"fake video"),
                StreamInfo(extension=".mp4", mimetype="video/mp4"),
            )

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
            conv.convert(
                io.BytesIO(b"fake pdf"),
                StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-documentSearch"

    def test_no_analyzer_id_routes_image_to_document_search(self):
        """Default image routing should still use prebuilt-documentSearch."""
        conv = _make_converter(analyzer_id=None, analyzer_modality=None)
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(
                io.BytesIO(b"fake image"),
                StreamInfo(extension=".jpg", mimetype="image/jpeg"),
            )

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-documentSearch"

    def test_document_analyzer_routes_image_to_custom(self):
        """Document-based analyzers should still handle image documents."""
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
            conv.convert(
                io.BytesIO(b"fake image"),
                StreamInfo(extension=".jpg", mimetype="image/jpeg"),
            )

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "my-doc-analyzer"

    def test_image_analyzer_routes_jpeg_to_custom(self):
        """Image-based analyzers should be used for image files."""
        conv = _make_converter(
            analyzer_id="my-image-analyzer",
            analyzer_modality="image",
        )
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(
                io.BytesIO(b"fake image"),
                StreamInfo(extension=".jpg", mimetype="image/jpeg"),
            )

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "my-image-analyzer"

    def test_image_analyzer_routes_pdf_to_document_prebuilt(self):
        """Image-based analyzers should not claim non-image document files."""
        conv = _make_converter(
            analyzer_id="my-image-analyzer",
            analyzer_modality="image",
        )
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(
                io.BytesIO(b"fake pdf"),
                StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-documentSearch"

    @pytest.mark.parametrize(
        ("mimetype", "expected_analyzer"),
        [
            ("video/mp4", "prebuilt-videoSearch"),
            ("video/x-m4v", "prebuilt-videoSearch"),
            ("audio/mpeg", "prebuilt-audioSearch"),
            ("audio/x-wav", "prebuilt-audioSearch"),
        ],
    )
    def test_mime_only_input_uses_auto_routing(self, mimetype, expected_analyzer):
        """MIME-only streams should route to the matching modality analyzer."""
        conv = _make_converter(analyzer_id=None, analyzer_modality=None)
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(io.BytesIO(b"fake content"), StreamInfo(mimetype=mimetype))

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == expected_analyzer

    def test_mime_alias_input_uses_canonical_content_type(self):
        """Alias MIME types should be sent to CU as canonical content types."""
        conv = _make_converter(analyzer_id=None, analyzer_modality=None)
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(io.BytesIO(b"fake video"), StreamInfo(mimetype="video/x-m4v"))

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-videoSearch"
        assert call_args.kwargs["content_type"] == "video/mp4"

    def test_extension_only_input_uses_file_type_content_type(self):
        """Extension-only inputs should send CU a matching content type."""
        conv = _make_converter(analyzer_id=None, analyzer_modality=None)
        conv._client = MagicMock()
        mock_result = MagicMock()
        mock_result.contents = []
        mock_poller = MagicMock()
        mock_poller.result.return_value = mock_result

        conv._client.begin_analyze_binary.return_value = mock_poller

        with patch("markitdown.converters._cu_converter.to_llm_input", return_value=""):
            conv.convert(io.BytesIO(b"fake pdf"), StreamInfo(extension=".pdf"))

        call_args = conv._client.begin_analyze_binary.call_args
        assert call_args.kwargs["analyzer_id"] == "prebuilt-documentSearch"
        assert call_args.kwargs["content_type"] == "application/pdf"


# ---------------------------------------------------------------------------
# _infer_prebuilt_modality tests
# ---------------------------------------------------------------------------


class TestResolveAnalyzerModality:
    """Test modality resolution from analyzer IDs."""

    def test_known_document_prebuilts(self):
        client = MagicMock()
        assert (
            _resolve_analyzer_modality(client, "prebuilt-documentSearch") == "document"
        )
        assert _resolve_analyzer_modality(client, "prebuilt-invoice") == "document"
        assert _resolve_analyzer_modality(client, "prebuilt-layout") == "document"
        assert _resolve_analyzer_modality(client, "prebuilt-receipt") == "document"
        assert _resolve_analyzer_modality(client, "prebuilt-tax.us.w2") == "document"
        # Known prebuilts should never call get_analyzer()
        client.get_analyzer.assert_not_called()

    def test_known_audio_prebuilts(self):
        client = MagicMock()
        assert _resolve_analyzer_modality(client, "prebuilt-audioSearch") == "audio"
        assert _resolve_analyzer_modality(client, "prebuilt-callCenter") == "audio"
        client.get_analyzer.assert_not_called()

    def test_known_video_prebuilts(self):
        client = MagicMock()
        assert _resolve_analyzer_modality(client, "prebuilt-videoSearch") == "video"
        assert _resolve_analyzer_modality(client, "prebuilt-videoSynopsis") == "video"
        client.get_analyzer.assert_not_called()

    def test_known_image_prebuilts(self):
        client = MagicMock()
        assert _resolve_analyzer_modality(client, "prebuilt-imageSearch") == "image"
        assert _resolve_analyzer_modality(client, "prebuilt-image") == "image"
        client.get_analyzer.assert_not_called()

    def test_unknown_prebuilt_falls_back_to_get_analyzer(self):
        """Unknown prebuilt-* names should call get_analyzer() for resolution."""
        client = MagicMock()
        mock_analyzer = MagicMock()
        mock_analyzer.base_analyzer_id = "prebuilt-audio"
        client.get_analyzer.return_value = mock_analyzer

        result = _resolve_analyzer_modality(client, "prebuilt-newAnalyzer")
        assert result == "audio"
        client.get_analyzer.assert_called_once_with("prebuilt-newAnalyzer")

    def test_custom_analyzer_calls_get_analyzer(self):
        """Custom analyzers should call get_analyzer() to resolve modality."""
        client = MagicMock()
        mock_analyzer = MagicMock()
        mock_analyzer.base_analyzer_id = "prebuilt-document"
        client.get_analyzer.return_value = mock_analyzer

        result = _resolve_analyzer_modality(client, "my-custom-doc-analyzer")
        assert result == "document"
        client.get_analyzer.assert_called_once_with("my-custom-doc-analyzer")

    def test_custom_analyzer_no_base_defaults_to_document(self):
        """Analyzer with no base_analyzer_id defaults to document."""
        client = MagicMock()
        mock_analyzer = MagicMock()
        mock_analyzer.base_analyzer_id = None
        client.get_analyzer.return_value = mock_analyzer

        result = _resolve_analyzer_modality(client, "my-custom-analyzer")
        assert result == "document"

    def test_get_analyzer_failure_raises_value_error(self):
        """Failed get_analyzer() should raise ValueError."""
        client = MagicMock()
        client.get_analyzer.side_effect = Exception("not found")

        with pytest.raises(ValueError, match="Failed to resolve analyzer 'bad-id'"):
            _resolve_analyzer_modality(client, "bad-id")


# ---------------------------------------------------------------------------
# _get_modality tests
# ---------------------------------------------------------------------------


class TestGetModality:
    """Test file type → modality mapping."""

    def test_document_types(self):
        assert _get_modality(ContentUnderstandingFileType.PDF) == "document"
        assert _get_modality(ContentUnderstandingFileType.DOCX) == "document"

    def test_image_types(self):
        assert _get_modality(ContentUnderstandingFileType.JPEG) == "image"
        assert _get_modality(ContentUnderstandingFileType.PNG) == "image"

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
        result = self._run_convert(
            ".pdf", "application/pdf", "---\ncontentType: document\n---\n# Test"
        )
        assert "contentType: document" in result.markdown

    def test_mp4_returns_markdown(self):
        result = self._run_convert(
            ".mp4", "video/mp4", "---\ncontentType: audioVisual\n---\nSpeaker 1: Hello"
        )
        assert "contentType: audioVisual" in result.markdown

    def test_wav_returns_markdown(self):
        result = self._run_convert(
            ".wav", "audio/wav", "---\ncontentType: audioVisual\n---\nSpeaker 1: Hi"
        )
        assert "audioVisual" in result.markdown

    def test_empty_result(self):
        result = self._run_convert(".pdf", "application/pdf", "")
        assert result.markdown == ""

    def test_jpeg_returns_markdown(self):
        result = self._run_convert(
            ".jpg", "image/jpeg", "---\ncontentType: document\n---\n# Photo"
        )
        assert "contentType: document" in result.markdown


# ---------------------------------------------------------------------------
# Init-time get_analyzer() error wrapping
# ---------------------------------------------------------------------------


class TestGetAnalyzerError:
    """Test that get_analyzer() failures at init produce a clear error."""

    def test_nonexistent_analyzer_raises_value_error(self):
        """A failed get_analyzer() should raise ValueError with analyzer name."""
        with patch(
            "markitdown.converters._cu_converter._dependency_exc_info", None
        ), patch(
            "markitdown.converters._cu_converter.ContentUnderstandingClient"
        ) as MockClient, patch(
            "markitdown.converters._cu_converter.DefaultAzureCredential"
        ):
            mock_client = MagicMock()
            mock_client.get_analyzer.side_effect = Exception("not found")
            MockClient.return_value = mock_client

            with pytest.raises(ValueError, match="Failed to resolve analyzer 'bad-id'"):
                ContentUnderstandingConverter(
                    endpoint="https://fake", analyzer_id="bad-id"
                )


# ---------------------------------------------------------------------------
# Registration priority test
# ---------------------------------------------------------------------------


class TestRegistrationPriority:
    """Test that CU converter is registered with higher priority than Doc Intel."""

    def test_cu_registered_before_docintel(self):
        """When both endpoints are provided, CU should appear before Doc Intel."""
        with patch(
            "markitdown.converters._cu_converter._dependency_exc_info", None
        ), patch(
            "markitdown.converters._cu_converter.ContentUnderstandingClient"
        ), patch(
            "markitdown.converters._cu_converter.DefaultAzureCredential"
        ), patch(
            "markitdown.converters._doc_intel_converter._dependency_exc_info", None
        ), patch(
            "markitdown.converters._doc_intel_converter.DocumentIntelligenceClient"
        ), patch(
            "markitdown.converters._doc_intel_converter.DefaultAzureCredential"
        ):
            from markitdown import MarkItDown
            from markitdown.converters import (
                ContentUnderstandingConverter,
                DocumentIntelligenceConverter,
            )

            md = MarkItDown(
                cu_endpoint="https://fake-cu",
                docintel_endpoint="https://fake-di",
            )

            converter_types = [type(reg.converter) for reg in md._converters]
            cu_idx = converter_types.index(ContentUnderstandingConverter)
            di_idx = converter_types.index(DocumentIntelligenceConverter)
            assert (
                cu_idx < di_idx
            ), "CU should have higher priority (lower index) than Doc Intel"


# ---------------------------------------------------------------------------
# CLI argument tests
# ---------------------------------------------------------------------------


class TestCLIArgs:
    """Test CLI argument parsing for CU flags."""

    def test_use_cu_without_endpoint_exits(self):
        """--use-cu without --cu-endpoint should exit with error."""
        import subprocess

        result = subprocess.run(
            [sys.executable, "-m", "markitdown", "--use-cu", "fake.pdf"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert (
            "cu-endpoint" in result.stderr.lower()
            or "cu-endpoint" in (result.stdout or "").lower()
        )

    def test_use_cu_and_use_docintel_mutually_exclusive(self):
        """--use-cu and --use-docintel cannot be used together."""
        import subprocess

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake",
                "--use-docintel",
                "-e",
                "https://fake-di",
                "fake.pdf",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_cu_file_types_parsing(self):
        """--cu-file-types should parse comma-separated values into enum list."""
        from markitdown.converters import ContentUnderstandingFileType

        raw = "pdf,jpeg,mp4"
        type_names = [t.strip().lower() for t in raw.split(",") if t.strip()]
        cu_types = [ContentUnderstandingFileType(name) for name in type_names]

        assert cu_types == [
            ContentUnderstandingFileType.PDF,
            ContentUnderstandingFileType.JPEG,
            ContentUnderstandingFileType.MP4,
        ]

    def test_cu_file_types_invalid_value(self):
        """Unknown file type name should raise ValueError."""
        from markitdown.converters import ContentUnderstandingFileType

        with pytest.raises(ValueError):
            ContentUnderstandingFileType("nonsense")

    def test_cu_file_types_single_value(self):
        """Single file type (no comma) should parse correctly."""
        from markitdown.converters import ContentUnderstandingFileType

        cu_types = [
            ContentUnderstandingFileType(t.strip().lower())
            for t in "wav".split(",")
            if t.strip()
        ]
        assert cu_types == [ContentUnderstandingFileType.WAV]

    def test_use_cu_wires_kwargs_to_markitdown(self, capsys):
        """--use-cu should pass CU options through to MarkItDown."""
        import markitdown.__main__ as markitdown_cli

        markitdown_instance = MagicMock()
        markitdown_instance.convert.return_value.markdown = "converted"
        markitdown_cls = MagicMock(return_value=markitdown_instance)

        with patch.object(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake-cu",
                "--cu-analyzer",
                "custom-analyzer",
                "--cu-file-types",
                "pdf,jpeg,mp4",
                "fake.pdf",
            ],
        ), patch.object(markitdown_cli, "MarkItDown", markitdown_cls):
            markitdown_cli.main()

        markitdown_cls.assert_called_once_with(
            enable_plugins=False,
            cu_endpoint="https://fake-cu",
            cu_analyzer_id="custom-analyzer",
            cu_file_types=[
                ContentUnderstandingFileType.PDF,
                ContentUnderstandingFileType.JPEG,
                ContentUnderstandingFileType.MP4,
            ],
        )
        markitdown_instance.convert.assert_called_once_with(
            "fake.pdf", stream_info=None, keep_data_uris=False
        )
        assert capsys.readouterr().out == "converted\n"


# ---------------------------------------------------------------------------
# MissingDependencyException test
# ---------------------------------------------------------------------------


class TestMissingDependency:
    """Test that MissingDependencyException is raised when CU SDK is not installed."""

    def test_missing_deps_message(self):
        """Converter construction should surface the optional install hint."""
        import markitdown.converters._cu_converter as cu_converter_module
        from markitdown._exceptions import MissingDependencyException

        import_error = ImportError("No module named 'azure.ai.contentunderstanding'")
        dependency_exc_info = (ImportError, import_error, None)

        with patch.object(
            cu_converter_module, "_dependency_exc_info", dependency_exc_info
        ), pytest.raises(MissingDependencyException) as exc_info:
            ContentUnderstandingConverter(endpoint="https://fake-cu")

        assert "az-content-understanding" in str(exc_info.value)
        assert exc_info.value.__cause__ is import_error
