"""
Test OCR functionality for markitdown converters.

Tests OCR text extraction from images embedded in PDF, DOCX, XLSX, and PPTX files.
Validates context preservation, multi-sheet processing, and accuracy.
"""

import sys
from pathlib import Path
from typing import BinaryIO

import pytest

# Mark all tests in this module as unittests
pytestmark = pytest.mark.unittests

# Add src to path for direct imports during testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown.converters._ocr_service import MultiBackendOCRService, OCRBackend
from markitdown.converters._pdf_converter_with_ocr import PdfConverterWithOCR
from markitdown.converters._docx_converter_with_ocr import DocxConverterWithOCR
from markitdown.converters._xlsx_converter_with_ocr import XlsxConverterWithOCR
from markitdown.converters._pptx_converter_with_ocr import PptxConverterWithOCR
from markitdown._stream_info import StreamInfo


# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "ocr_test_data"


@pytest.fixture(scope="module")
def ocr_service():
    """Create OCR service with Tesseract backend."""
    try:
        import pytesseract
        # Try to configure Tesseract if on Windows
        if sys.platform == 'win32':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        return MultiBackendOCRService(backends=[OCRBackend.TESSERACT])
    except ImportError:
        pytest.skip("pytesseract not installed")


def test_tesseract_available():
    """Test that Tesseract OCR is available."""
    try:
        import pytesseract
        if sys.platform == 'win32':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        version = pytesseract.get_tesseract_version()
        assert version is not None, "Tesseract version should be available"

    except ImportError:
        pytest.skip("pytesseract not installed")
    except Exception as e:
        pytest.skip(f"Tesseract not available: {e}")


def test_pdf_ocr_basic(ocr_service):
    """Test PDF OCR extraction with context preservation."""
    converter = PdfConverterWithOCR()
    pdf_path = TEST_DATA_DIR / "pdf_complex_layout.pdf"

    if not pdf_path.exists():
        pytest.skip(f"Test file not found: {pdf_path}")

    with open(pdf_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".pdf"), ocr_service=ocr_service)
        markdown = result.text_content

    # Validate structure and content
    assert "## Page" in markdown, "Should have page marker"
    assert "[Image:" in markdown, "Should have image marker"
    assert "WARNING" in markdown or "Handle" in markdown, "Should extract OCR text"


def test_pdf_ocr_image_at_end(ocr_service):
    """Test PDF with image at document end."""
    converter = PdfConverterWithOCR()
    pdf_path = TEST_DATA_DIR / "pdf_image_end.pdf"

    if not pdf_path.exists():
        pytest.skip(f"Test file not found: {pdf_path}")

    with open(pdf_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".pdf"), ocr_service=ocr_service)
        markdown = result.text_content

    # Validate image appears after main content
    assert "Main Content" in markdown, "Should have main content"
    assert "Contact" in markdown or "support" in markdown, "Should extract OCR text"

    if "Main Content" in markdown and "[Image:" in markdown:
        main_idx = markdown.index("Main Content")
        img_idx = markdown.index("[Image:")
        assert main_idx < img_idx, "Main content should appear before image"


def test_docx_ocr_basic(ocr_service):
    """Test DOCX OCR extraction without duplicates."""
    converter = DocxConverterWithOCR()
    docx_path = TEST_DATA_DIR / "docx_complex_layout.docx"

    if not docx_path.exists():
        pytest.skip(f"Test file not found: {docx_path}")

    with open(docx_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".docx"), ocr_service=ocr_service)
        markdown = result.text_content

    # Validate structure
    assert "Complex Document" in markdown or "Security" in markdown, "Should have document content"
    assert "[Image OCR:" in markdown or "NOTICE" in markdown or "SSL" in markdown, "Should extract OCR text"

    # Ensure no duplicates (critical fix validation)
    if "NOTICE" in markdown:
        notice_count = markdown.count("NOTICE: SSL Certificate")
        assert notice_count <= 1, f"OCR text should not be duplicated (found {notice_count} times)"


def test_docx_ocr_image_at_end(ocr_service):
    """Test DOCX with image at document end."""
    converter = DocxConverterWithOCR()
    docx_path = TEST_DATA_DIR / "docx_image_end.docx"

    if not docx_path.exists():
        pytest.skip(f"Test file not found: {docx_path}")

    with open(docx_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".docx"), ocr_service=ocr_service)
        markdown = result.text_content

    assert "Report" in markdown or "findings" in markdown, "Should have document content"
    assert "FOOTER" in markdown or "Document ID" in markdown, "Should extract OCR text at end"


def test_xlsx_ocr_multisheet(ocr_service):
    """Test XLSX OCR with multi-sheet processing and cell references."""
    converter = XlsxConverterWithOCR()
    xlsx_path = TEST_DATA_DIR / "xlsx_complex_layout.xlsx"

    if not xlsx_path.exists():
        pytest.skip(f"Test file not found: {xlsx_path}")

    with open(xlsx_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".xlsx"), ocr_service=ocr_service)
        markdown = result.text_content

    # Validate multi-sheet processing
    sheet_count = markdown.count("##")
    assert sheet_count >= 2, f"Should process multiple sheets (found {sheet_count})"

    # Validate image sections with cell references
    assert "Images in this sheet:" in markdown, "Should have image sections"
    assert "cell" in markdown.lower(), "Should track cell references"

    # Check for OCR text
    has_ocr = any(keyword in markdown for keyword in ["Figure", "Chart", "Monthly", "Trend"])
    assert has_ocr, "Should extract OCR text from images"


def test_xlsx_ocr_cell_references(ocr_service):
    """Test XLSX cell position tracking."""
    converter = XlsxConverterWithOCR()
    xlsx_path = TEST_DATA_DIR / "xlsx_image_start.xlsx"

    if not xlsx_path.exists():
        pytest.skip(f"Test file not found: {xlsx_path}")

    with open(xlsx_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".xlsx"), ocr_service=ocr_service)
        markdown = result.text_content

    # Validate cell references present
    assert "Image near cell" in markdown, "Should have cell reference tracking"

    # Check multiple sheets processed
    assert "Sales Q1" in markdown or "Forecast" in markdown, "Should process named sheets"


def test_pptx_ocr_basic(ocr_service):
    """Test PPTX OCR with alt text integration."""
    converter = PptxConverterWithOCR()
    pptx_path = TEST_DATA_DIR / "pptx_complex_layout.pptx"

    if not pptx_path.exists():
        pytest.skip(f"Test file not found: {pptx_path}")

    with open(pptx_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".pptx"), ocr_service=ocr_service)
        markdown = result.text_content

    # Validate structure
    assert "Slide number:" in markdown, "Should have slide markers"
    assert "Product Comparison" in markdown or "Market Share" in markdown, "Should have slide content"
    assert "![" in markdown, "Should have markdown images with OCR in alt text"


def test_pptx_ocr_multipage(ocr_service):
    """Test PPTX with multiple slides."""
    converter = PptxConverterWithOCR()
    pptx_path = TEST_DATA_DIR / "pptx_image_end.pptx"

    if not pptx_path.exists():
        pytest.skip(f"Test file not found: {pptx_path}")

    with open(pptx_path, 'rb') as f:
        result = converter.convert(f, StreamInfo(extension=".pptx"), ocr_service=ocr_service)
        markdown = result.text_content

    # Validate multiple slides
    slide_count = markdown.count("Slide number:")
    assert slide_count >= 2, f"Should have multiple slides (found {slide_count})"

    # Check OCR text in alt text
    assert "Contact" in markdown or "info" in markdown or "techcorp" in markdown, "Should extract OCR text"


def test_ocr_service_fallback(ocr_service):
    """Test OCR service graceful handling."""
    from PIL import Image
    import io

    # Create a simple test image
    img = Image.new('RGB', (400, 100), color='white')
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.text((10, 30), "Test Text", fill='black')

    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)

    result = ocr_service.extract_text(img_stream)

    # Should either succeed or fail gracefully
    assert result is not None, "Should return result object"
    assert hasattr(result, 'text'), "Result should have text attribute"
    assert hasattr(result, 'backend_used'), "Result should have backend_used attribute"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
