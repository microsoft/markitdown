"""
Test OCR functionality for markitdown converters.

Tests OCR text extraction from images embedded in PDF, DOCX, XLSX, and PPTX files.
Validates context preservation, multi-sheet processing, positioning accuracy, and text matching.
"""

import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Any

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


# ==============================================================================
# EXPECTED OCR RESULTS - Ground Truth for Validation
# ==============================================================================


@dataclass
class ImagePosition:
    """Track expected position of an image in document."""

    position: str  # "start", "middle", "end"
    page_or_sheet: int  # Page number (PDF/DOCX) or sheet index (XLSX)
    expected_text: str  # Expected OCR text (partial match)
    before_marker: str | None = None  # Text that should appear before image
    after_marker: str | None = None  # Text that should appear after image


# Expected OCR results for test files
EXPECTED_OCR_RESULTS: dict[str, list[ImagePosition]] = {
    # PDF Tests
    "pdf_complex_layout.pdf": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="WARNING",
            before_marker="ItemQuantity",
            after_marker="Widget A",
        )
    ],
    "pdf_image_end.pdf": [
        ImagePosition(
            position="end",
            page_or_sheet=1,
            expected_text="Contact",
            before_marker="Keep reading",
            after_marker=None,
        )
    ],
    "pdf_image_start.pdf": [
        ImagePosition(
            position="start",
            page_or_sheet=1,
            expected_text="START",
            before_marker=None,
            after_marker="This is text",
        )
    ],
    "pdf_image_middle.pdf": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="MIDDLE",
            before_marker="introductory text",
            after_marker="Section 2",
        )
    ],
    "pdf_multiple_images.pdf": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="Image 1",
            before_marker="Multiple Images",
            after_marker="Text between",
        ),
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="Image 2",
            before_marker="Text between",
            after_marker="Final text",
        ),
    ],
    "pdf_multipage.pdf": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="PAGE 1 IMAGE",
            before_marker="BEFORE the image",
            after_marker="AFTER the image",
        ),
        ImagePosition(
            position="end",
            page_or_sheet=2,
            expected_text="PAGE 2 IMAGE",
            before_marker="Final paragraph",
            after_marker=None,
        ),
        ImagePosition(
            position="start",
            page_or_sheet=3,
            expected_text="PAGE 3 IMAGE",
            before_marker=None,
            after_marker="Content that follows",
        ),
    ],
    # DOCX Tests
    "docx_complex_layout.docx": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="NOTICE",
            before_marker="Security notice",
            after_marker=None,
        )
    ],
    "docx_image_end.docx": [
        ImagePosition(
            position="end",
            page_or_sheet=1,
            expected_text="FOOTER",
            before_marker="Recommendations",
            after_marker=None,
        )
    ],
    "docx_image_start.docx": [
        ImagePosition(
            position="start",
            page_or_sheet=1,
            expected_text="HEADER",
            before_marker=None,
            after_marker="main content",
        )
    ],
    "docx_image_middle.docx": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="FIGURE 1",
            before_marker="see an image below",
            after_marker="Analysis",
        )
    ],
    "docx_multiple_images.docx": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="Chart 1",
            before_marker="First section",
            after_marker="Second section",
        ),
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="Chart 2",
            before_marker="Second section",
            after_marker="Conclusion",
        ),
    ],
    "docx_multipage.docx": [
        ImagePosition(
            position="middle",
            page_or_sheet=1,
            expected_text="DOCX PAGE 1",
            before_marker="BEFORE IMAGE",
            after_marker="AFTER IMAGE",
        ),
        ImagePosition(
            position="end",
            page_or_sheet=2,
            expected_text="DOCX PAGE 2",
            before_marker="Final paragraph",
            after_marker=None,
        ),
        ImagePosition(
            position="start",
            page_or_sheet=3,
            expected_text="DOCX PAGE 3",
            before_marker=None,
            after_marker="Content that follows",
        ),
    ],
}


def validate_image_position(
    markdown: str, image_pos: ImagePosition, verbose: bool = False
) -> tuple[bool, str]:
    """
    Validate that an image appears at the expected position with expected text.

    Returns:
        Tuple of (success: bool, message: str)
    """
    # Check expected text is present
    if image_pos.expected_text not in markdown:
        return (
            False,
            f"Expected OCR text '{image_pos.expected_text}' not found in output",
        )

    # Get position of expected text
    text_idx = markdown.index(image_pos.expected_text)

    # Validate position relative to markers
    if image_pos.before_marker:
        if image_pos.before_marker not in markdown:
            return False, f"Before marker '{image_pos.before_marker}' not found"
        before_idx = markdown.index(image_pos.before_marker)
        if before_idx >= text_idx:
            return (
                False,
                f"Image text (pos {text_idx}) should appear AFTER before marker (pos {before_idx})",
            )

    if image_pos.after_marker:
        if image_pos.after_marker not in markdown:
            return False, f"After marker '{image_pos.after_marker}' not found"
        after_idx = markdown.index(image_pos.after_marker)
        if text_idx >= after_idx:
            return (
                False,
                f"Image text (pos {text_idx}) should appear BEFORE after marker (pos {after_idx})",
            )

    # Build success message
    msg_parts = [f"Image at {image_pos.position} position validated"]
    if image_pos.before_marker:
        before_idx = markdown.index(image_pos.before_marker)
        msg_parts.append(f"before_marker(pos:{before_idx})")
    msg_parts.append(f"image(pos:{text_idx})")
    if image_pos.after_marker:
        after_idx = markdown.index(image_pos.after_marker)
        msg_parts.append(f"after_marker(pos:{after_idx})")

    return True, " -> ".join(msg_parts)


def validate_no_base64_images(markdown: str) -> tuple[bool, str]:
    """Validate that no base64 encoded images are present in output."""
    if "data:image" in markdown or "base64" in markdown:
        return False, "Base64 images found in output (should be replaced with OCR text)"
    return True, "No base64 images found"


@pytest.fixture(scope="module")
def ocr_service() -> Any:
    """Create OCR service with Tesseract backend."""
    try:
        import pytesseract

        # Try to configure Tesseract if on Windows
        if sys.platform == "win32":
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )

        return MultiBackendOCRService(backends=[OCRBackend.TESSERACT])
    except ImportError:
        pytest.skip("pytesseract not installed")


def test_tesseract_available() -> None:
    """Test that Tesseract OCR is available."""
    try:
        import pytesseract

        if sys.platform == "win32":
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )

        version = pytesseract.get_tesseract_version()
        assert version is not None, "Tesseract version should be available"

    except ImportError:
        pytest.skip("pytesseract not installed")
    except Exception as e:
        pytest.skip(f"Tesseract not available: {e}")


def test_pdf_ocr_basic(ocr_service: Any) -> None:
    """Test PDF OCR extraction with context preservation and position validation."""
    converter = PdfConverterWithOCR()
    pdf_path = TEST_DATA_DIR / "pdf_complex_layout.pdf"

    if not pdf_path.exists():
        pytest.skip(f"Test file not found: {pdf_path}")

    with open(pdf_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".pdf"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate structure and content
    assert "## Page" in markdown, "Should have page marker"
    assert "[Image:" in markdown, "Should have image marker"

    # Validate expected OCR results with position tracking
    filename = pdf_path.name
    if filename in EXPECTED_OCR_RESULTS:
        for img_pos in EXPECTED_OCR_RESULTS[filename]:
            success, message = validate_image_position(markdown, img_pos, verbose=True)
            assert success, f"Position validation failed: {message}"
            print(f"  [PASS] {message}")  # Verbose output for pytest -s


def test_pdf_ocr_image_at_end(ocr_service: Any) -> None:
    """Test PDF with image at document end with position validation."""
    converter = PdfConverterWithOCR()
    pdf_path = TEST_DATA_DIR / "pdf_image_end.pdf"

    if not pdf_path.exists():
        pytest.skip(f"Test file not found: {pdf_path}")

    with open(pdf_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".pdf"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate with expected results
    filename = pdf_path.name
    if filename in EXPECTED_OCR_RESULTS:
        for img_pos in EXPECTED_OCR_RESULTS[filename]:
            success, message = validate_image_position(markdown, img_pos, verbose=True)
            assert success, f"Position validation failed: {message}"
            print(f"  [PASS] {message}")


def test_docx_ocr_basic(ocr_service: Any) -> None:
    """Test DOCX OCR extraction with position validation and no base64 check."""
    converter = DocxConverterWithOCR()
    docx_path = TEST_DATA_DIR / "docx_complex_layout.docx"

    if not docx_path.exists():
        pytest.skip(f"Test file not found: {docx_path}")

    with open(docx_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".docx"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate no base64 images
    success, message = validate_no_base64_images(markdown)
    assert success, message
    print(f"  ✓ {message}")

    # Validate structure
    assert "[Image OCR:" in markdown, "Should have OCR markers"

    # Ensure no duplicates (critical fix validation)
    if "NOTICE" in markdown:
        notice_count = markdown.count("NOTICE: SSL Certificate")
        assert (
            notice_count <= 1
        ), f"OCR text should not be duplicated (found {notice_count} times)"

    # Validate expected OCR results with position tracking
    filename = docx_path.name
    if filename in EXPECTED_OCR_RESULTS:
        for img_pos in EXPECTED_OCR_RESULTS[filename]:
            success, message = validate_image_position(markdown, img_pos, verbose=True)
            assert success, f"Position validation failed: {message}"
            print(f"  [PASS] {message}")


def test_docx_ocr_image_at_end(ocr_service: Any) -> None:
    """Test DOCX with image at document end with position validation."""
    converter = DocxConverterWithOCR()
    docx_path = TEST_DATA_DIR / "docx_image_end.docx"

    if not docx_path.exists():
        pytest.skip(f"Test file not found: {docx_path}")

    with open(docx_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".docx"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate no base64 images
    success, message = validate_no_base64_images(markdown)
    assert success, message

    # Validate with expected results
    filename = docx_path.name
    if filename in EXPECTED_OCR_RESULTS:
        for img_pos in EXPECTED_OCR_RESULTS[filename]:
            success, message = validate_image_position(markdown, img_pos, verbose=True)
            assert success, f"Position validation failed: {message}"
            print(f"  [PASS] {message}")


def test_xlsx_ocr_multisheet(ocr_service: Any) -> None:
    """Test XLSX OCR with multi-sheet processing and cell references."""
    converter = XlsxConverterWithOCR()
    xlsx_path = TEST_DATA_DIR / "xlsx_complex_layout.xlsx"

    if not xlsx_path.exists():
        pytest.skip(f"Test file not found: {xlsx_path}")

    with open(xlsx_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".xlsx"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate multi-sheet processing
    sheet_count = markdown.count("##")
    assert sheet_count >= 2, f"Should process multiple sheets (found {sheet_count})"

    # Validate image sections with cell references
    assert "Images in this sheet:" in markdown, "Should have image sections"
    assert "cell" in markdown.lower(), "Should track cell references"

    # Check for OCR text
    has_ocr = any(
        keyword in markdown for keyword in ["Figure", "Chart", "Monthly", "Trend"]
    )
    assert has_ocr, "Should extract OCR text from images"


def test_xlsx_ocr_cell_references(ocr_service: Any) -> None:
    """Test XLSX cell position tracking."""
    converter = XlsxConverterWithOCR()
    xlsx_path = TEST_DATA_DIR / "xlsx_image_start.xlsx"

    if not xlsx_path.exists():
        pytest.skip(f"Test file not found: {xlsx_path}")

    with open(xlsx_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".xlsx"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate cell references present
    assert "Image near cell" in markdown, "Should have cell reference tracking"

    # Check multiple sheets processed
    assert (
        "Sales Q1" in markdown or "Forecast" in markdown
    ), "Should process named sheets"


def test_pptx_ocr_basic(ocr_service: Any) -> None:
    """Test PPTX OCR with alt text integration."""
    converter = PptxConverterWithOCR()
    pptx_path = TEST_DATA_DIR / "pptx_complex_layout.pptx"

    if not pptx_path.exists():
        pytest.skip(f"Test file not found: {pptx_path}")

    with open(pptx_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".pptx"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate structure
    assert "Slide number:" in markdown, "Should have slide markers"
    assert (
        "Product Comparison" in markdown or "Market Share" in markdown
    ), "Should have slide content"
    assert "![" in markdown, "Should have markdown images with OCR in alt text"


def test_pptx_ocr_multipage(ocr_service: Any) -> None:
    """Test PPTX with multiple slides."""
    converter = PptxConverterWithOCR()
    pptx_path = TEST_DATA_DIR / "pptx_image_end.pptx"

    if not pptx_path.exists():
        pytest.skip(f"Test file not found: {pptx_path}")

    with open(pptx_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=".pptx"), ocr_service=ocr_service
        )
        markdown = result.text_content

    # Validate multiple slides
    slide_count = markdown.count("Slide number:")
    assert slide_count >= 2, f"Should have multiple slides (found {slide_count})"

    # Check OCR text in alt text
    assert (
        "Contact" in markdown or "info" in markdown or "techcorp" in markdown
    ), "Should extract OCR text"


def test_ocr_service_fallback(ocr_service: Any) -> None:
    """Test OCR service graceful handling."""
    from PIL import Image
    import io

    # Create a simple test image
    img = Image.new("RGB", (400, 100), color="white")
    from PIL import ImageDraw

    draw = ImageDraw.Draw(img)
    draw.text((10, 30), "Test Text", fill="black")

    img_stream = io.BytesIO()
    img.save(img_stream, format="PNG")
    img_stream.seek(0)

    result = ocr_service.extract_text(img_stream)

    # Should either succeed or fail gracefully
    assert result is not None, "Should return result object"
    assert hasattr(result, "text"), "Result should have text attribute"
    assert hasattr(result, "backend_used"), "Result should have backend_used attribute"


@pytest.mark.parametrize(
    "filename",
    [
        "pdf_complex_layout.pdf",
        "pdf_image_end.pdf",
        "pdf_image_start.pdf",
        "pdf_image_middle.pdf",
        "pdf_multiple_images.pdf",
        "pdf_multipage.pdf",
        "docx_complex_layout.docx",
        "docx_image_end.docx",
        "docx_image_start.docx",
        "docx_image_middle.docx",
        "docx_multiple_images.docx",
        "docx_multipage.docx",
    ],
)
def test_comprehensive_ocr_positioning(ocr_service: Any, filename: str) -> None:
    """
    Comprehensive test validating OCR text extraction and positioning for all test files.

    This test:
    1. Validates expected OCR text is extracted
    2. Validates image positioning relative to surrounding text
    3. For DOCX: validates no base64 images in output
    4. Compares extracted text against expected ground truth
    """
    file_path = TEST_DATA_DIR / filename

    if not file_path.exists():
        pytest.skip(f"Test file not found: {file_path}")

    if filename not in EXPECTED_OCR_RESULTS:
        pytest.skip(f"No expected results defined for {filename}")

    # Determine converter based on extension
    converter: Any
    if filename.endswith(".pdf"):
        converter = PdfConverterWithOCR()
        extension = ".pdf"
    elif filename.endswith(".docx"):
        converter = DocxConverterWithOCR()
        extension = ".docx"
    else:
        pytest.skip(f"Unsupported file type for {filename}")

    # Convert document
    print(f"\n{'='*60}")
    print(f"Testing: {filename}")
    print(f"{'='*60}")

    with open(file_path, "rb") as f:
        result = converter.convert(
            f, StreamInfo(extension=extension), ocr_service=ocr_service
        )
        markdown = result.text_content

    # For DOCX files, validate no base64 images
    if filename.endswith(".docx"):
        success, message = validate_no_base64_images(markdown)
        assert success, f"Base64 validation failed for {filename}: {message}"
        print(f"  [PASS] Base64 check: {message}")

    # Validate all expected image positions
    expected_images = EXPECTED_OCR_RESULTS[filename]
    print(f"  Validating {len(expected_images)} image(s)...")

    for idx, img_pos in enumerate(expected_images, 1):
        success, message = validate_image_position(markdown, img_pos, verbose=True)
        assert success, f"Image {idx} validation failed for {filename}: {message}"
        print(f"  [PASS] Image {idx}: {message}")

    print(
        f"  [SUCCESS] All {len(expected_images)} images validated successfully for {filename}"
    )


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
