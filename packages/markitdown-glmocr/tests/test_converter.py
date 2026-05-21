"""Tests for markitdown-glmocr converter."""

import io
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from markitdown_glmocr._converter import GlmOcrConverter
from markitdown_glmocr._config import ScanDetectionMode


class TestGlmOcrConverter:
    """Converter tests."""

    @patch("markitdown_glmocr._converter.glmocr")
    def test_accepts_pdf_extension(self, mock_glmocr):
        """Accept .pdf extension."""
        converter = GlmOcrConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=".pdf", mimetype=None)

        assert converter.accepts(stream, stream_info) is True

    @patch("markitdown_glmocr._converter.glmocr")
    def test_accepts_pdf_mimetype(self, mock_glmocr):
        """Accept PDF MIME type."""
        converter = GlmOcrConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=None, mimetype="application/pdf")

        assert converter.accepts(stream, stream_info) is True

    @patch("markitdown_glmocr._converter.glmocr")
    def test_rejects_non_pdf(self, mock_glmocr):
        """Reject non-PDF files."""
        converter = GlmOcrConverter()
        stream = io.BytesIO(b"not a pdf")
        stream_info = MagicMock(extension=".txt", mimetype="text/plain")

        assert converter.accepts(stream, stream_info) is False

    @patch("markitdown_glmocr._converter.glmocr")
    def test_table_to_markdown(self, mock_glmocr):
        """Table to Markdown conversion."""
        converter = GlmOcrConverter()
        table = [
            ["Name", "Age", "City"],
            ["Alice", "25", "Beijing"],
            ["Bob", "30", "Shanghai"],
        ]

        result = converter._table_to_markdown(table)

        assert "|" in result
        assert "Name" in result
        assert "Alice" in result
        assert "---" in result  # Separator

    @patch("markitdown_glmocr._converter.glmocr")
    def test_plain_text_page_without_ai(self, mock_glmocr):
        """Plain text page without AI."""
        converter = GlmOcrConverter(
            scan_detection_mode=ScanDetectionMode.PAGE_BY_PAGE,
        )

        # Mock page
        page = MagicMock()
        page.images = []
        page.find_tables.return_value = []
        page.curves = []
        page.extract_text.return_value = "Hello World"
        page.extract_tables.return_value = []
        page.close = MagicMock()

        # Mock PDF
        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_glmocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        assert "Hello World" in result.markdown

    @patch("markitdown_glmocr._converter.glmocr")
    def test_force_ai_mode(self, mock_glmocr):
        """Force AI mode."""
        # Mock glmocr instance
        mock_result = MagicMock()
        mock_result.markdown_result = "AI result"
        mock_result.to_dict.return_value = {}

        mock_glmocr_instance = MagicMock()
        mock_glmocr_instance.parse.return_value = mock_result
        mock_glmocr.GlmOcr.return_value = mock_glmocr_instance

        converter = GlmOcrConverter(force_ai=True)
        # Force initialization of the mocked glmocr
        converter._get_glmocr = lambda: mock_glmocr_instance

        # Even plain text page
        page = MagicMock()
        page.images = []
        page.find_tables.return_value = []
        page.curves = []
        page.extract_text.return_value = "Plain text"
        page.extract_tables.return_value = []
        page.close = MagicMock()

        # Mock to_image
        mock_img = MagicMock()
        page.to_image.return_value = mock_img

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_glmocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        # Should call AI (because force_ai=True)
        mock_glmocr_instance.parse.assert_called_once()
