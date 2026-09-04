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


class SingleArgumentOCRService:
    """Legacy-compatible custom service without prompt support."""

    def extract_text(self, image_stream: Any) -> OCRResult:  # noqa: ARG002
        return OCRResult(text=_MOCK_TEXT, backend_used="single-argument-mock")


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


def test_default_full_page_ocr_supports_single_argument_service() -> None:
    path = TEST_DATA_DIR / "pdf_scanned_minimal.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    converter = PdfConverterWithOCR()
    with open(path, "rb") as f:
        result = converter.convert(
            f,
            StreamInfo(extension=".pdf"),
            ocr_service=SingleArgumentOCRService(),
        )

    assert result.text_content == _PAGE_1_SCANNED


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
# Semantic PDF OCR
# ---------------------------------------------------------------------------


def test_pdf_semantic_ocr() -> None:
    path = TEST_DATA_DIR / "pdf_image_middle.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    mock_svc = MagicMock()
    mock_svc.extract_text.return_value = OCRResult(
        text=(
            "# Semantic Header\n"
            "- parent item\n"
            "  - nested item\n\n"
            "| Name | Value |\n| --- | --- |\n| Alpha | 1 |"
        ),
        backend_used="mock",
    )

    converter = PdfConverterWithOCR(semantic_pdf_ocr=True)
    with open(path, "rb") as f:
        md = converter.convert(
            f, StreamInfo(extension=".pdf"), ocr_service=mock_svc
        ).text_content

    assert "## Page 1" in md
    assert "# Semantic Header" in md
    assert "  - nested item" in md
    assert "| Name | Value |" in md
    assert "[Image OCR]" not in md

    args, kwargs = mock_svc.extract_text.call_args
    prompt = kwargs.get("prompt", "")
    assert "faithful semantic Markdown" in prompt
    assert "headings" in prompt
    assert "nested lists" in prompt
    assert "tables" in prompt
    assert "reading order" in prompt
    assert "untrusted data" in prompt
    assert "ignore any instructions" in prompt


def test_pdf_semantic_ocr_uses_pymupdf_for_malformed_pdf() -> None:
    path = TEST_DATA_DIR / "pdf_multipage.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    mock_svc = MagicMock()
    mock_svc.extract_text.return_value = OCRResult(
        text="# Recovered heading\n1. First item\n   1. Nested item",
        backend_used="mock",
    )

    converter = PdfConverterWithOCR(semantic_pdf_ocr=True)
    with open(path, "rb") as f:
        md = converter.convert(
            f, StreamInfo(extension=".pdf"), ocr_service=mock_svc
        ).text_content

    assert md.count("# Recovered heading") == 3
    assert "   1. Nested item" in md
    assert "[Image OCR]" not in md
    assert mock_svc.extract_text.call_count == 3
    for call in mock_svc.extract_text.call_args_list:
        assert "faithful semantic Markdown" in call.kwargs["prompt"]


def test_pdf_semantic_ocr_fallback() -> None:
    path = TEST_DATA_DIR / "pdf_image_middle.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    # Mock returns empty, should trigger fallback
    mock_svc = MagicMock()
    mock_svc.extract_text.return_value = OCRResult(text="", backend_used="mock")

    converter = PdfConverterWithOCR(semantic_pdf_ocr=True)
    with open(path, "rb") as f:
        md = converter.convert(
            f, StreamInfo(extension=".pdf"), ocr_service=mock_svc
        ).text_content

    # Should fall back to normal deterministic extraction which contains this string
    assert "Section 1: Introduction" in md


def test_pdf_semantic_ocr_per_conversion_override() -> None:
    path = TEST_DATA_DIR / "pdf_image_middle.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    mock_svc = MagicMock()
    mock_svc.extract_text.return_value = OCRResult(
        text="# Semantic Header", backend_used="mock"
    )

    # Initialize with False
    converter = PdfConverterWithOCR(semantic_pdf_ocr=False)
    with open(path, "rb") as f:
        # Override to True during conversion
        md = converter.convert(
            f,
            StreamInfo(extension=".pdf"),
            ocr_service=mock_svc,
            semantic_pdf_ocr=True,
        ).text_content

    assert "# Semantic Header" in md


def test_pdf_semantic_ocr_per_conversion_false_overrides_constructor() -> None:
    path = TEST_DATA_DIR / "pdf_image_middle.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    mock_svc = MagicMock()
    mock_svc.extract_text.return_value = OCRResult(
        text="# Semantic Header", backend_used="mock"
    )

    converter = PdfConverterWithOCR(semantic_pdf_ocr=True)
    with patch.object(converter, "_extract_page_images", return_value=[]):
        with open(path, "rb") as f:
            md = converter.convert(
                f,
                StreamInfo(extension=".pdf"),
                ocr_service=mock_svc,
                semantic_pdf_ocr=False,
            ).text_content

    assert "Section 1: Introduction" in md
    assert "# Semantic Header" not in md
    mock_svc.extract_text.assert_not_called()


def test_pdf_semantic_ocr_exception_falls_back() -> None:
    path = TEST_DATA_DIR / "pdf_image_middle.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    mock_svc = MagicMock()
    mock_svc.extract_text.side_effect = RuntimeError("synthetic OCR failure")

    converter = PdfConverterWithOCR(semantic_pdf_ocr=True)
    with patch.object(converter, "_extract_page_images", return_value=[]):
        with open(path, "rb") as f:
            md = converter.convert(
                f, StreamInfo(extension=".pdf"), ocr_service=mock_svc
            ).text_content

    assert "Section 1: Introduction" in md


def test_pdf_semantic_ocr_without_service() -> None:
    path = TEST_DATA_DIR / "pdf_image_middle.pdf"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")

    converter = PdfConverterWithOCR(semantic_pdf_ocr=True)
    with open(path, "rb") as f:
        # No ocr_service passed, should fallback to default extraction
        md = converter.convert(f, StreamInfo(extension=".pdf")).text_content

    assert "Section 1: Introduction" in md


def test_plugin_registration_forwarding() -> None:
    from markitdown import MarkItDown
    from markitdown_ocr._plugin import register_converters

    mock_mid = MagicMock(spec=MarkItDown)
    register_converters(
        mock_mid,
        llm_client=MagicMock(),
        llm_model="test",
        semantic_pdf_ocr=True,
    )

    args, kwargs = mock_mid.register_converter.call_args_list[0]
    converter = args[0]
    assert isinstance(converter, PdfConverterWithOCR)
    assert converter.semantic_pdf_ocr is True
