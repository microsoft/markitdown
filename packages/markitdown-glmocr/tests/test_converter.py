"""Tests for markitdown-glmocr converter."""

import io
import pytest
from unittest.mock import MagicMock, patch

from markitdown_glmocr._converter import GlmOcrPdfConverter
from markitdown_glmocr._ai_service import AIService, AIResult
from markitdown_glmocr._page_analyzer import PageType


class TestGlmOcrPdfConverter:
    """Converter tests."""

    def test_accepts_pdf_extension(self):
        """Accept .pdf extension."""
        converter = GlmOcrPdfConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=".pdf", mimetype=None)

        assert converter.accepts(stream, stream_info) is True

    def test_accepts_pdf_mimetype(self):
        """Accept PDF MIME type."""
        converter = GlmOcrPdfConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=None, mimetype="application/pdf")

        assert converter.accepts(stream, stream_info) is True

    def test_rejects_non_pdf(self):
        """Reject non-PDF files."""
        converter = GlmOcrPdfConverter()
        stream = io.BytesIO(b"not a pdf")
        stream_info = MagicMock(extension=".txt", mimetype="text/plain")

        assert converter.accepts(stream, stream_info) is False

    def test_table_to_markdown(self):
        """Table to Markdown conversion."""
        converter = GlmOcrPdfConverter()
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

    def test_plain_text_page_without_ai(self):
        """Plain text page without AI."""
        converter = GlmOcrPdfConverter()

        # Mock page
        page = MagicMock()
        page.images = []
        page.objects = {}
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Hello World"
        page.close = MagicMock()

        # Mock PDF
        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_glmocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        assert "Hello World" in result.markdown

    def test_complex_page_with_ai(self):
        """Complex page with AI."""
        # Mock AI service
        ai_service = MagicMock(spec=AIService)
        ai_service.image_to_markdown.return_value = AIResult(
            success=True,
            text="# AI Generated\n\nThis is from AI."
        )

        converter = GlmOcrPdfConverter(ai_service=ai_service)

        # Mock page
        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Plain text"
        page.to_image.return_value.original = MagicMock()
        page.close = MagicMock()

        # Mock image save
        img_stream = io.BytesIO()
        page.to_image.return_value.original.save = lambda s, format: s.write(b"fake")

        # Mock PDF
        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_glmocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        # Should call AI
        ai_service.image_to_markdown.assert_called_once()
        assert "AI Generated" in result.markdown

    def test_force_ai_mode(self):
        """Force AI mode."""
        ai_service = MagicMock(spec=AIService)
        ai_service.image_to_markdown.return_value = AIResult(
            success=True,
            text="AI result"
        )

        converter = GlmOcrPdfConverter(ai_service=ai_service, force_ai=True)

        # Even plain text page
        page = MagicMock()
        page.images = []
        page.objects = {}
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Plain text"
        page.to_image.return_value.original = MagicMock()
        page.close = MagicMock()

        img_stream = io.BytesIO()
        page.to_image.return_value.original.save = lambda s, format: s.write(b"fake")

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_glmocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        # Should call AI (because force_ai=True)
        ai_service.image_to_markdown.assert_called_once()

    def test_fallback_on_ai_failure(self):
        """Fallback on AI failure."""
        ai_service = MagicMock(spec=AIService)
        ai_service.image_to_markdown.return_value = AIResult(
            success=False,
            text="",
            error="API error"
        )

        converter = GlmOcrPdfConverter(ai_service=ai_service)

        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Fallback text"
        page.to_image.return_value.original = MagicMock()
        page.close = MagicMock()

        img_stream = io.BytesIO()
        page.to_image.return_value.original.save = lambda s, format: s.write(b"fake")

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_glmocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        # Should fallback to default text
        assert "Fallback text" in result.markdown