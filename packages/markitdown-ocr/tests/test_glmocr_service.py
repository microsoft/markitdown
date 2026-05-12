"""Tests for GlmOcrService."""

import io
from unittest.mock import MagicMock, patch

import pytest

from markitdown_ocr._ocr_service import GlmOcrService, OCRResult


class TestGlmOcrServiceInit:
    """Tests for GlmOcrService initialization."""

    def test_init_requires_api_key(self):
        """GlmOcrService should raise ValueError for empty api_key."""
        with patch.dict("sys.modules", {"zai": MagicMock()}):
            with pytest.raises(ValueError, match="GLMOCR_API_KEY"):
                GlmOcrService(api_key="")

    def test_init_with_valid_key(self):
        """GlmOcrService should initialize with a valid API key."""
        with patch.dict("sys.modules", {"zai": MagicMock()}):
            service = GlmOcrService(api_key="test-key")
            assert service.model == "glm-ocr"
            assert service.timeout == 120


class TestGlmOcrServiceExtractText:
    """Tests for GlmOcrService.extract_text."""

    def _make_service(self) -> GlmOcrService:
        """Create a GlmOcrService with mocked client."""
        service = GlmOcrService.__new__(GlmOcrService)
        service.model = "glm-ocr"
        service.timeout = 120
        service.client = MagicMock()
        return service

    def test_extract_text_returns_ocr_result(self):
        """extract_text should always return OCRResult."""
        service = self._make_service()
        service.client.layout_parsing.create.side_effect = Exception("API error")

        image_stream = io.BytesIO(b"fake image data")
        result = service.extract_text(image_stream)

        assert isinstance(result, OCRResult)
        assert result.backend_used == "glm_ocr"
        assert result.error is not None

    def test_extract_text_md_results_used_directly(self):
        """md_results is already Markdown — should be used as-is, no HTML conversion."""
        service = self._make_service()

        # Simulate real API response: md_results contains Markdown table
        mock_response = MagicMock()
        mock_response.md_results = "| Name | Value |\n| --- | --- |\n| Hello | World |"
        mock_response.layout_details = None
        service.client.layout_parsing.create.return_value = mock_response

        image_stream = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = service.extract_text(image_stream)

        assert isinstance(result, OCRResult)
        assert result.backend_used == "glm_ocr"
        assert result.error is None
        # Markdown table should be preserved as-is
        assert "| Name | Value |" in result.text
        assert "| --- | --- |" in result.text
        assert "| Hello | World |" in result.text

    def test_extract_text_md_results_with_heading(self):
        """md_results with Markdown heading should be preserved."""
        service = self._make_service()

        mock_response = MagicMock()
        mock_response.md_results = "# Report Title\n\nSome paragraph text."
        mock_response.layout_details = None
        service.client.layout_parsing.create.return_value = mock_response

        image_stream = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = service.extract_text(image_stream)

        assert result.error is None
        assert "# Report Title" in result.text
        assert "Some paragraph text." in result.text

    def test_extract_text_success_with_layout_details(self):
        """extract_text should fallback to layout_details when md_results is empty."""
        service = self._make_service()

        mock_detail1 = MagicMock()
        mock_detail1.content = "First block text"
        mock_detail2 = MagicMock()
        mock_detail2.content = "Second block text"

        mock_response = MagicMock()
        mock_response.md_results = ""
        mock_response.layout_details = [[mock_detail1, mock_detail2]]
        service.client.layout_parsing.create.return_value = mock_response

        image_stream = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = service.extract_text(image_stream)

        assert isinstance(result, OCRResult)
        assert result.backend_used == "glm_ocr"
        assert result.error is None
        assert "First block text" in result.text
        assert "Second block text" in result.text

    def test_extract_text_layout_details_joined_with_double_newline(self):
        """layout_details content blocks should be joined with double newline."""
        service = self._make_service()

        mock_detail1 = MagicMock()
        mock_detail1.content = "Block A"
        mock_detail2 = MagicMock()
        mock_detail2.content = "Block B"

        mock_response = MagicMock()
        mock_response.md_results = ""
        mock_response.layout_details = [[mock_detail1], [mock_detail2]]
        service.client.layout_parsing.create.return_value = mock_response

        image_stream = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = service.extract_text(image_stream)

        assert "Block A\n\nBlock B" in result.text

    def test_extract_text_empty_response(self):
        """extract_text should handle empty response gracefully."""
        service = self._make_service()

        mock_response = MagicMock()
        mock_response.md_results = ""
        mock_response.layout_details = []
        service.client.layout_parsing.create.return_value = mock_response

        image_stream = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = service.extract_text(image_stream)

        assert isinstance(result, OCRResult)
        assert result.text == ""
        assert result.error is None

    def test_extract_text_jpeg_detection(self):
        """extract_text should detect JPEG from magic bytes."""
        service = self._make_service()

        mock_response = MagicMock()
        mock_response.md_results = "Some text"
        mock_response.layout_details = None
        service.client.layout_parsing.create.return_value = mock_response

        # JPEG magic bytes
        image_stream = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
        result = service.extract_text(image_stream)

        assert isinstance(result, OCRResult)
        assert result.error is None

    def test_extract_text_resets_stream_position(self):
        """extract_text should reset stream position after processing."""
        service = self._make_service()

        mock_response = MagicMock()
        mock_response.md_results = "Text"
        mock_response.layout_details = None
        service.client.layout_parsing.create.return_value = mock_response

        image_stream = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        image_stream.seek(5)  # Set non-zero position
        service.extract_text(image_stream)
        assert image_stream.tell() == 0

    def test_extract_text_md_results_stripped(self):
        """md_results should be stripped of leading/trailing whitespace."""
        service = self._make_service()

        mock_response = MagicMock()
        mock_response.md_results = "  \n  Hello World  \n  "
        mock_response.layout_details = None
        service.client.layout_parsing.create.return_value = mock_response

        image_stream = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = service.extract_text(image_stream)

        assert result.text == "Hello World"

    def test_no_html_to_markdown_method(self):
        """GlmOcrService should NOT have _html_to_markdown or _convert_html_table."""
        service = self._make_service()
        assert not hasattr(service, "_html_to_markdown")
        assert not hasattr(service, "_convert_html_table")
