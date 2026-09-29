"""
Unit tests for PdfConverterWithOCR.

For each PDF test file: convert with a mock OCR service then compare the
full output string against the expected snapshot.

OCR block format used by the converter:
    *[Image OCR]
    MOCK_OCR_TEXT_12345
    [End OCR]*
"""

import io
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_ocr._ocr_service import OCRResult  # noqa: E402
from markitdown_ocr._pdf_converter_with_ocr import (  # noqa: E402
    PdfConverterWithOCR,
)
from markitdown import StreamInfo  # noqa: E402

TEST_DATA_DIR = Path(__file__).parent / "ocr_test_data"

_MOCK_TEXT = "MOCK_OCR_TEXT_12345"
_OCR_BLOCK = f"*[Image OCR]\n{_MOCK_TEXT}\n[End OCR]*"
_PAGE_1_SCANNED = f"## Page 1\n\n\n\n\n{_OCR_BLOCK}"


class MockOCRService:
    def extract_text(
        self,  # noqa: ANN101
        image_stream: Any,
        **kwargs: Any,
    ) -> OCRResult:
        return OCRResult(text=_MOCK_TEXT, backend_used="mock")


@pytest.fixture(scope="module")
def svc() -> MockOCRService:
    return MockOCRService()


def _convert(filename: str, ocr_service: MockOCRService) -> str:
    path = TEST_DATA_DIR / filename
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")
    converter = PdfConverterWithOCR()
    with open(path, "rb") as f:
        return converter.convert(
            f, StreamInfo(extension=".pdf"), ocr_service=ocr_service
        ).text_content


# ---------------------------------------------------------------------------
# pdf_image_start.pdf
# ---------------------------------------------------------------------------


def test_pdf_image_start(svc: MockOCRService) -> None:
    expected = (
        "## Page 1\n\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "This is text BEFORE the image.\n\n"
        "The image should appear above this text.\n\n"
        "This is more content after the image."
    )
    assert _convert("pdf_image_start.pdf", svc) == expected


# ---------------------------------------------------------------------------
# pdf_image_middle.pdf
# ---------------------------------------------------------------------------


def test_pdf_image_middle(svc: MockOCRService) -> None:
    expected = (
        "## Page 1\n\n\n"
        "Section 1: Introduction\n\n"
        "This document contains an image in the middle.\n\n"
        "Here is some introductory text.\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "Section 2: Details\n\n"
        "This text appears AFTER the image."
    )
    assert _convert("pdf_image_middle.pdf", svc) == expected


# ---------------------------------------------------------------------------
# pdf_image_end.pdf
# ---------------------------------------------------------------------------


def test_pdf_image_end(svc: MockOCRService) -> None:
    expected = (
        "## Page 1\n\n\n"
        "Main Content\n\n"
        "This is the main text content.\n\n"
        "The image will appear at the end.\n\n"
        "Keep reading...\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    )
    assert _convert("pdf_image_end.pdf", svc) == expected


# ---------------------------------------------------------------------------
# pdf_multiple_images.pdf
# ---------------------------------------------------------------------------


def test_pdf_multiple_images(svc: MockOCRService) -> None:
    expected = (
        "## Page 1\n\n\n"
        "Document with Multiple Images\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "Text between first and second image.\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "Final text after all images."
    )
    assert _convert("pdf_multiple_images.pdf", svc) == expected


# ---------------------------------------------------------------------------
# pdf_complex_layout.pdf
# ---------------------------------------------------------------------------


def test_pdf_complex_layout(svc: MockOCRService) -> None:
    expected = (
        "## Page 1\n\n\n"
        "Complex Layout Document\n\n"
        "Table:\n\n"
        "Item Quantity\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "Widget A 5"
    )
    assert _convert("pdf_complex_layout.pdf", svc) == expected


# ---------------------------------------------------------------------------
# pdf_multipage.pdf
# ---------------------------------------------------------------------------


def test_pdf_multipage(svc: MockOCRService) -> None:
    expected = (
        "## Page 1\n\n\n"
        "Page 1 - Content before image\n\n"
        "This is important text that appears BEFORE the image.\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "This text appears AFTER the image on page 1.\n\n"
        "More content follows here.\n\n\n"
        "## Page 2\n\n\n"
        "Page 2 - Content with image at end\n\n"
        "Main content of page 2 starts here.\n\n"
        "This is paragraph 1.\n\n"
        "This is paragraph 2.\n\n"
        "Final paragraph before image.\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n\n"
        "## Page 3\n\n\n"
        "Page 3 - Image at top\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "Content that follows the image.\n\n"
        "This text is AFTER the image."
    )
    assert _convert("pdf_multipage.pdf", svc) == expected


# ---------------------------------------------------------------------------
# pdf_scanned_*.pdf — raster-only pages → full-page OCR
# ---------------------------------------------------------------------------


def test_pdf_scanned_invoice(svc: MockOCRService) -> None:
    assert _convert("pdf_scanned_invoice.pdf", svc) == _PAGE_1_SCANNED


def test_pdf_scanned_meeting_minutes(svc: MockOCRService) -> None:
    assert _convert("pdf_scanned_meeting_minutes.pdf", svc) == _PAGE_1_SCANNED


def test_pdf_scanned_minimal(svc: MockOCRService) -> None:
    assert _convert("pdf_scanned_minimal.pdf", svc) == _PAGE_1_SCANNED


def test_pdf_scanned_sales_report(svc: MockOCRService) -> None:
    assert _convert("pdf_scanned_sales_report.pdf", svc) == _PAGE_1_SCANNED


def test_pdf_scanned_report(svc: MockOCRService) -> None:
    expected = (
        f"{_PAGE_1_SCANNED}\n\n\n\n"
        f"## Page 2\n\n\n\n\n{_OCR_BLOCK}\n\n\n\n"
        f"## Page 3\n\n\n\n\n{_OCR_BLOCK}"
    )
    assert _convert("pdf_scanned_report.pdf", svc) == expected


# ---------------------------------------------------------------------------
# Scanned PDF fallback path (pdfplumber finds no text → full-page OCR)
# ---------------------------------------------------------------------------


def test_pdf_scanned_fallback_format(svc: MockOCRService) -> None:
    """_ocr_full_pages emits *[Image OCR]...[End OCR]* for each page."""
    path = TEST_DATA_DIR / "pdf_image_start.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    converter = PdfConverterWithOCR()
    with patch("pdfplumber.open") as mock_plumber:
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.page_number = 1
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_plumber.return_value = mock_pdf

        with open(path, "rb") as f:
            md = converter._ocr_full_pages(io.BytesIO(f.read()), svc)

    expected = "## Page 1\n\n\n" "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    assert (
        md == expected
    ), f"_ocr_full_pages must produce:\n{expected!r}\nActual:\n{md!r}"


# ---------------------------------------------------------------------------
# No OCR service — no OCR tags emitted
# ---------------------------------------------------------------------------


def test_pdf_no_ocr_service_no_tags() -> None:
    path = TEST_DATA_DIR / "pdf_image_middle.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")
    converter = PdfConverterWithOCR()
    with open(path, "rb") as f:
        md = converter.convert(f, StreamInfo(extension=".pdf")).text_content
    assert "*[Image OCR]" not in md
    assert "[End OCR]*" not in md


# ---------------------------------------------------------------------------
# Native text on a page that also has an embedded image
# ---------------------------------------------------------------------------


def _two_column_page_with_image() -> bytes:
    """One native-text page: two columns sharing a baseline, plus a small image."""
    import fitz  # PyMuPDF is a dependency of this package

    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((50, 100), "Customer Name", fontsize=11)
    page.insert_text((350, 100), "Vendor Name Ltd", fontsize=11)
    page.insert_text((50, 130), "Unit price", fontsize=11)
    page.insert_text((350, 130), "Total price", fontsize=11)
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 60, 40), False)
    pix.set_rect(pix.irect, (200, 30, 30))
    page.insert_image(fitz.Rect(50, 30, 110, 70), stream=pix.tobytes("png"))
    return doc.tobytes()


def test_pdf_page_with_image_keeps_spaces_between_columns(svc: MockOCRService) -> None:
    """Regression: on a page with an embedded image (e.g. a logo) the text used to be
    rebuilt from raw chars joined with "", gluing adjacent columns together
    ("Customer NameVendor Name Ltd")."""
    converter = PdfConverterWithOCR()
    md = converter.convert(
        io.BytesIO(_two_column_page_with_image()),
        StreamInfo(extension=".pdf"),
        ocr_service=svc,
    ).text_content

    assert "Customer Name Vendor Name Ltd" in md
    assert "Unit price Total price" in md
    # the image is still OCR'd and interleaved
    assert _OCR_BLOCK in md
