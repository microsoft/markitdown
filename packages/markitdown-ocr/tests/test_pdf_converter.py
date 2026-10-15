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


def test_scanned_page_uses_full_page_ocr(svc: MockOCRService) -> None:
    """An empty-text page is rendered instead of OCRing embedded decorations."""
    converter = PdfConverterWithOCR()
    page = MagicMock()
    page.extract_text.return_value = ""
    page.to_image.return_value.original = MagicMock()

    pdf = MagicMock()
    pdf.pages = [page]
    pdf.__enter__.return_value = pdf

    with (
        patch("pdfplumber.open", return_value=pdf) as open_pdf,
        patch.object(converter, "_extract_page_images") as extract_images,
    ):
        result = converter.convert(
            io.BytesIO(b"pdf"),
            StreamInfo(extension=".pdf"),
            ocr_service=svc,
        )

    assert _OCR_BLOCK in result.text_content
    page.to_image.assert_called_once_with(resolution=300)
    extract_images.assert_not_called()
    open_pdf.assert_called_once()


def test_scanned_page_falls_back_to_embedded_image_ocr_when_rendering_fails(
    svc: MockOCRService,
) -> None:
    """A render failure must not discard a decodable embedded scan."""
    converter = PdfConverterWithOCR()
    page = MagicMock()
    page.extract_text.return_value = ""
    page.to_image.side_effect = RuntimeError("render failed")

    pdf = MagicMock()
    pdf.pages = [page]
    pdf.__enter__.return_value = pdf
    image_stream = io.BytesIO(b"embedded scan")

    with (
        patch("pdfplumber.open", return_value=pdf),
        patch.object(
            converter,
            "_extract_page_images",
            return_value=[{"stream": image_stream, "y_pos": 0, "name": "scan"}],
        ) as extract_images,
    ):
        result = converter.convert(
            io.BytesIO(b"pdf"),
            StreamInfo(extension=".pdf"),
            ocr_service=svc,
        )

    assert _OCR_BLOCK in result.text_content
    extract_images.assert_called_once_with(page)


def test_convert_reuses_open_page_for_image_extraction(svc: MockOCRService) -> None:
    """Embedded-image extraction must not reopen and reparse the PDF."""
    converter = PdfConverterWithOCR()
    page = MagicMock()
    page.extract_text.return_value = "body"
    page.chars = []

    pdf = MagicMock()
    pdf.pages = [page]
    pdf.__enter__.return_value = pdf

    with (
        patch("pdfplumber.open", return_value=pdf) as open_pdf,
        patch.object(
            converter, "_extract_page_images", return_value=[]
        ) as extract_images,
    ):
        converter.convert(
            io.BytesIO(b"pdf"),
            StreamInfo(extension=".pdf"),
            ocr_service=svc,
        )

    extract_images.assert_called_once_with(page)
    open_pdf.assert_called_once()


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


@pytest.mark.parametrize("outcome", ["text", "empty", "ocr_error", "encode_error"])
def test_ocr_page_closes_rendered_images(monkeypatch, outcome: str) -> None:
    import pdfplumber

    converter = PdfConverterWithOCR()
    rendered = []

    class OCR:
        def extract_text(self, stream):
            assert stream.read(8) == b"\x89PNG\r\n\x1a\n"
            if outcome == "ocr_error":
                raise RuntimeError("OCR failed")
            return OCRResult(
                text=_MOCK_TEXT if outcome == "text" else "", backend_used="mock"
            )

    with pdfplumber.open(TEST_DATA_DIR / "pdf_scanned_minimal.pdf") as pdf:
        page = pdf.pages[0]
        to_image = page.to_image

        def capture_render(**kwargs):
            image = to_image(**kwargs)
            rendered.append(image)
            if outcome == "encode_error":

                def fail_save(*args, **kwargs):
                    raise RuntimeError("encoding failed")

                monkeypatch.setattr(image.original, "save", fail_save)
            return image

        monkeypatch.setattr(page, "to_image", capture_render)
        if outcome.endswith("error"):
            message = "OCR failed" if outcome == "ocr_error" else "encoding failed"
            with pytest.raises(RuntimeError, match=message):
                converter._ocr_page(page, OCR())
        else:
            result = converter._ocr_page(page, OCR())
            assert result == (
                _OCR_BLOCK
                if outcome == "text"
                else "*[No text could be extracted from this page]*"
            )

        assert len(rendered) == 1
        assert rendered[0].original is not rendered[0].annotated
        for image in (rendered[0].original, rendered[0].annotated):
            with pytest.raises(ValueError, match="closed image"):
                image.getpixel((0, 0))
