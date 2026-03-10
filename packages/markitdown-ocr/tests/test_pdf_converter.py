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
        "ItemQuantity\n\n\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n\n"
        "Widget A5"
    )
    assert _convert("pdf_complex_layout.pdf", svc) == expected


# ---------------------------------------------------------------------------
# pdf_multipage.pdf — pdfplumber/pdfminer fail (EOF); PyMuPDF fallback used
# ---------------------------------------------------------------------------


def test_pdf_multipage(svc: MockOCRService) -> None:
    # pdfplumber cannot open this file (Unexpected EOF), so _ocr_full_pages
    # falls back to PyMuPDF for page rendering.  Each page becomes one OCR block.
    expected = (
        f"## Page 1\n\n\n{_OCR_BLOCK}\n\n\n"
        f"## Page 2\n\n\n{_OCR_BLOCK}\n\n\n"
        f"## Page 3\n\n\n{_OCR_BLOCK}"
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
