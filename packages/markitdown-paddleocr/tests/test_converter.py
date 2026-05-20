"""Tests for PaddleOcrConverter."""

import io
import pytest
from unittest.mock import MagicMock, patch

from markitdown_paddleocr._converter import PaddleOcrConverter


class TestPaddleOcrConverterAccepts:
    """Accepts method tests."""

    def test_accepts_pdf_extension(self):
        """Accept .pdf extension."""
        converter = PaddleOcrConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=".pdf", mimetype=None)
        assert converter.accepts(stream, stream_info) is True

    def test_accepts_pdf_mimetype(self):
        """Accept PDF MIME type."""
        converter = PaddleOcrConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=None, mimetype="application/pdf")
        assert converter.accepts(stream, stream_info) is True

    def test_accepts_image_extensions(self):
        """Accept image extensions."""
        converter = PaddleOcrConverter()
        for ext in [".jpg", ".jpeg", ".png"]:
            stream = io.BytesIO(b"fake")
            stream_info = MagicMock(extension=ext, mimetype=None)
            assert converter.accepts(stream, stream_info) is True

    def test_rejects_non_supported(self):
        """Reject non-supported files."""
        converter = PaddleOcrConverter()
        stream = io.BytesIO(b"not a pdf")
        stream_info = MagicMock(extension=".txt", mimetype="text/plain")
        assert converter.accepts(stream, stream_info) is False


class TestPaddleOcrConverterTable:
    """Table to Markdown conversion tests."""

    def test_table_to_markdown(self):
        """Table to Markdown conversion."""
        converter = PaddleOcrConverter()
        table = [
            ["Name", "Age", "City"],
            ["Alice", "25", "Beijing"],
            ["Bob", "30", "Shanghai"],
        ]
        result = converter._table_to_markdown(table)
        assert "|" in result
        assert "Name" in result
        assert "Alice" in result
        assert "---" in result

    def test_empty_table(self):
        """Empty table returns empty string."""
        converter = PaddleOcrConverter()
        assert converter._table_to_markdown([]) == ""

    def test_table_with_none_values(self):
        """Table with None values."""
        converter = PaddleOcrConverter()
        table = [
            ["A", None, "C"],
            ["1", "2", None],
        ]
        result = converter._table_to_markdown(table)
        assert "|" in result
        assert "A" in result


class TestPaddleOcrConverterImage:
    """Image conversion tests."""

    def test_convert_image_success(self):
        """Convert image with PaddleOCR success."""
        converter = PaddleOcrConverter(token="test-token")

        mock_client = MagicMock()
        mock_client.ocr.return_value = "# Image Title\n\nContent"
        converter._client = mock_client

        stream = io.BytesIO(b"fake-image")
        stream_info = MagicMock(extension=".png", mimetype="image/png")
        result = converter.convert(stream, stream_info)

        assert "# Image Title" in result.markdown
        mock_client.ocr.assert_called_once()

    def test_convert_image_error(self):
        """Convert image with PaddleOCR error returns comment."""
        converter = PaddleOcrConverter(token="test-token")

        mock_client = MagicMock()
        mock_client.ocr.side_effect = Exception("API Error")
        converter._client = mock_client

        stream = io.BytesIO(b"fake-image")
        stream_info = MagicMock(extension=".png", mimetype="image/png")
        result = converter.convert(stream, stream_info)

        assert "Error converting image" in result.markdown


class TestPaddleOcrConverterPdf:
    """PDF conversion tests."""

    def test_plain_text_page(self):
        """Plain text page uses pdfplumber."""
        converter = PaddleOcrConverter()

        page = MagicMock()
        page.images = []
        page.find_tables.return_value = []
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Hello World"
        page.close = MagicMock()

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_paddleocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf
            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock(extension=".pdf", mimetype=None))

        assert "Hello World" in result.markdown

    def test_complex_page_uses_paddleocr(self):
        """Complex page uses PaddleOCR."""
        converter = PaddleOcrConverter(token="test-token")

        mock_client = MagicMock()
        mock_client.ocr.return_value = "OCR result for complex page"
        converter._client = mock_client

        page = MagicMock()
        page.images = [MagicMock()]
        page.find_tables.return_value = []
        page.to_image.return_value.save = MagicMock(
            side_effect=lambda buf, format: buf.write(b"fake-png")
        )
        page.close = MagicMock()

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_paddleocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf
            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock(extension=".pdf", mimetype=None))

        mock_client.ocr.assert_called_once()
        assert "OCR result" in result.markdown

    def test_force_ai_mode(self):
        """Force AI mode uses PaddleOCR for all pages."""
        converter = PaddleOcrConverter(token="test-token", force_ai=True)

        mock_client = MagicMock()
        mock_client.ocr.return_value = "AI result"
        converter._client = mock_client

        page = MagicMock()
        page.images = []
        page.find_tables.return_value = []
        page.to_image.return_value.save = MagicMock(
            side_effect=lambda buf, format: buf.write(b"fake-png")
        )
        page.close = MagicMock()

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("markitdown_paddleocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf
            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock(extension=".pdf", mimetype=None))

        mock_client.ocr.assert_called_once()


class TestPaddleOcrConverterConfig:
    """Config initialization tests."""

    def test_default_config(self):
        """Default configuration values."""
        converter = PaddleOcrConverter()
        assert converter.model == "PaddleOCR-VL-1.5"
        assert converter.poll_interval == 2.0
        assert converter.poll_timeout == 300.0
        assert converter.force_ai is False

    def test_custom_config(self):
        """Custom configuration values."""
        converter = PaddleOcrConverter(
            token="my-token",
            model="custom-model",
            poll_interval=5.0,
            poll_timeout=600.0,
            force_ai=True,
            use_chart_recognition=True,
        )
        assert converter.token == "my-token"
        assert converter.model == "custom-model"
        assert converter.poll_interval == 5.0
        assert converter.poll_timeout == 600.0
        assert converter.force_ai is True
        assert converter.use_chart_recognition is True
