"""Tests for AI service with zai-sdk."""

import io
import pytest
from unittest.mock import MagicMock, patch

from markitdown_glmocr._ai_service import AIService, AIResult
from markitdown_glmocr._config import GlmOcrConfig


class TestAIService:
    """AI Service tests with zai-sdk."""

    def test_missing_zai_sdk_raises_error(self):
        """Missing zai-sdk raises error."""
        with patch("markitdown_glmocr._ai_service.ZhipuAiClient", None):
            with pytest.raises(ImportError, match="zai-sdk is required"):
                AIService(api_key="test")

    def test_missing_api_key_raises_error(self):
        """Missing API key raises error."""
        with patch("markitdown_glmocr._ai_service.ZhipuAiClient", MagicMock()):
            with pytest.raises(ValueError, match="API key is required"):
                AIService(api_key="")

    def test_successful_conversion(self):
        """Successful conversion."""
        # Mock ZhipuAiClient
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.md_results = "<table><tr><td>Test</td></tr></table>"
        mock_response.layout_details = []
        mock_client.layout_parsing.create.return_value = mock_response

        with patch("markitdown_glmocr._ai_service.ZhipuAiClient", return_value=mock_client):
            service = AIService(api_key="test-api-key")
            result = service.image_to_markdown(io.BytesIO(b"fake-image"))

        assert result.success is True
        assert "Test" in result.text

    def test_html_table_conversion(self):
        """HTML table to Markdown conversion."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.md_results = '<table><tr><td>A</td><td>B</td></tr><tr><td>1</td><td>2</td></tr></table>'
        mock_response.layout_details = []
        mock_client.layout_parsing.create.return_value = mock_response

        with patch("markitdown_glmocr._ai_service.ZhipuAiClient", return_value=mock_client):
            service = AIService(api_key="test-api-key")
            result = service.image_to_markdown(io.BytesIO(b"fake-image"))

        assert result.success is True
        assert "| A | B |" in result.text
        assert "|---|---|" in result.text
        assert "| 1 | 2 |" in result.text

    def test_empty_result(self):
        """Empty result handling."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.md_results = ""
        mock_response.layout_details = []
        mock_client.layout_parsing.create.return_value = mock_response

        with patch("markitdown_glmocr._ai_service.ZhipuAiClient", return_value=mock_client):
            service = AIService(api_key="test-api-key")
            result = service.image_to_markdown(io.BytesIO(b"fake-image"))

        assert result.success is True
        assert result.text == ""

    def test_error_handling(self):
        """Error handling."""
        mock_client = MagicMock()
        mock_client.layout_parsing.create.side_effect = Exception("API Error")

        with patch("markitdown_glmocr._ai_service.ZhipuAiClient", return_value=mock_client):
            service = AIService(api_key="test-api-key")
            result = service.image_to_markdown(io.BytesIO(b"fake-image"))

        assert result.success is False
        assert "API Error" in result.error

    def test_base64_encoding(self):
        """Test base64 encoding of image."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.md_results = "test"
        mock_response.layout_details = []
        mock_client.layout_parsing.create.return_value = mock_response

        with patch("markitdown_glmocr._ai_service.ZhipuAiClient", return_value=mock_client):
            service = AIService(api_key="test-api-key")
            result = service.image_to_markdown(io.BytesIO(b"fake-image"), "test.png")

        assert result.success is True
        
        # Verify data URI was used
        call_args = mock_client.layout_parsing.create.call_args
        file_arg = call_args.kwargs['file']
        assert file_arg.startswith("data:image/png;base64,")