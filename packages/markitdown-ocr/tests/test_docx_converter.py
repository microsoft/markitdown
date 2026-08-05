"""
Unit tests for DocxConverterWithOCR.

For each DOCX test file: convert with a mock OCR service then compare the
full output string against the expected snapshot.

OCR block format used by the converter:
    *[Image OCR]
    MOCK_OCR_TEXT_12345
    [End OCR]*
"""

import io
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_ocr._ocr_service import OCRResult  # noqa: E402
from markitdown_ocr._docx_converter_with_ocr import (  # noqa: E402
    DocxConverterWithOCR,
)
from markitdown import StreamInfo  # noqa: E402

TEST_DATA_DIR = Path(__file__).parent / "ocr_test_data"

_MOCK_TEXT = "MOCK_OCR_TEXT_12345"


class MockOCRService:
    def extract_text(  # noqa: ANN101
        self, image_stream: Any, **kwargs: Any
    ) -> OCRResult:
        return OCRResult(text=_MOCK_TEXT, backend_used="mock")


@pytest.fixture(scope="module")
def svc() -> MockOCRService:
    return MockOCRService()


def _convert(filename: str, ocr_service: MockOCRService) -> str:
    path = TEST_DATA_DIR / filename
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")
    converter = DocxConverterWithOCR()
    with open(path, "rb") as f:
        return converter.convert(
            f, StreamInfo(extension=".docx"), ocr_service=ocr_service
        ).text_content


# ---------------------------------------------------------------------------
# docx_image_start.docx
# ---------------------------------------------------------------------------


def test_docx_image_start(svc: MockOCRService) -> None:
    expected = (
        "Document with Image at Start\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n"
        "This is the main content after the header image.\n\n"
        "More text content here."
    )
    assert _convert("docx_image_start.docx", svc) == expected


# ---------------------------------------------------------------------------
# docx_image_middle.docx
# ---------------------------------------------------------------------------


def test_docx_image_middle(svc: MockOCRService) -> None:
    expected = (
        "# Introduction\n\n"
        "This is the introduction section.\n\n"
        "We will see an image below.\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n"
        "# Analysis\n\n"
        "This section comes after the image."
    )
    assert _convert("docx_image_middle.docx", svc) == expected


# ---------------------------------------------------------------------------
# docx_image_end.docx
# ---------------------------------------------------------------------------


def test_docx_image_end(svc: MockOCRService) -> None:
    expected = (
        "Report\n\n"
        "Main findings of the report.\n\n"
        "Details and analysis.\n\n"
        "Recommendations.\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    )
    assert _convert("docx_image_end.docx", svc) == expected


# ---------------------------------------------------------------------------
# docx_multiple_images.docx
# ---------------------------------------------------------------------------


def test_docx_multiple_images(svc: MockOCRService) -> None:
    expected = (
        "Multi-Image Document\n\n"
        "First section\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n"
        "Second section with another image\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n"
        "Conclusion"
    )
    assert _convert("docx_multiple_images.docx", svc) == expected


# ---------------------------------------------------------------------------
# docx_multipage.docx
# ---------------------------------------------------------------------------


def test_docx_multipage(svc: MockOCRService) -> None:
    expected = (
        "# Page 1 - Mixed Content\n\n"
        "This is the first paragraph on page 1.\n\n"
        "BEFORE IMAGE: Important content appears here.\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n"
        "AFTER IMAGE: This content follows the image.\n\n"
        "More text on page 1.\n\n"
        "# Page 2 - Image at End\n\n"
        "Content on page 2.\n\n"
        "Multiple paragraphs of text.\n\n"
        "Building up to the image...\n\n"
        "Final paragraph before image.\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n"
        "# Page 3 - Image at Start\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*\n\n"
        "Content that follows the header image.\n\n"
        "AFTER IMAGE: This text is after the image."
    )
    assert _convert("docx_multipage.docx", svc) == expected


# ---------------------------------------------------------------------------
# docx_complex_layout.docx
# ---------------------------------------------------------------------------


def test_docx_complex_layout(svc: MockOCRService) -> None:
    expected = (
        "Complex Document\n\n"
        "|  |  |\n"
        "| --- | --- |\n"
        "| Feature | Status |\n"
        "| Authentication | Active |\n"
        "| Encryption | Enabled |\n\n"
        "Security notice:\n\n"
        "*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    )
    assert _convert("docx_complex_layout.docx", svc) == expected


class SequencedOCRService:
    def extract_text(self, image_stream: Any, **kwargs: Any) -> OCRResult:
        image_name = image_stream.read().decode()
        if image_name == "empty":
            return OCRResult(text="", backend_used="mock")
        if image_name == "error":
            raise RuntimeError("OCR unavailable")
        return OCRResult(text=f"OCR {image_name}", backend_used="mock")


class FakeMammothImage:
    content_type = "image/png"
    alt_text = None

    def __init__(self, name: str):
        self._name = name

    def open(self) -> io.BytesIO:
        return io.BytesIO(self._name.encode())


def test_docx_ocr_failures_do_not_shift_later_occurrences() -> None:
    def convert_to_html(
        _stream: Any, *, convert_image: Any, **kwargs: Any
    ) -> SimpleNamespace:
        image_html = []
        for image_name in ("empty", "error", "later"):
            element = convert_image(FakeMammothImage(image_name))[0]
            placeholder = element.attributes["src"]
            image_html.append(
                f'<p><img alt="{placeholder}" src="{placeholder}" /></p>'
            )
        return SimpleNamespace(
            value=f"<p>Before</p>{image_html[0]}<p>Middle</p>"
            f"{image_html[1]}<p>After</p>{image_html[2]}<p>End</p>"
        )

    converter = DocxConverterWithOCR()
    with (
        patch(
            "markitdown_ocr._docx_converter_with_ocr.pre_process_docx",
            return_value=io.BytesIO(b"docx"),
        ),
        patch(
            "markitdown_ocr._docx_converter_with_ocr.mammoth.convert_to_html",
            side_effect=convert_to_html,
        ),
    ):
        markdown = converter.convert(
            io.BytesIO(b"docx"),
            StreamInfo(extension=".docx"),
            ocr_service=SequencedOCRService(),
        ).text_content

    assert "MARKITDOWNOCRBLOCK" not in markdown
    assert "OCR later" in markdown
    assert "OCR empty" not in markdown
    assert markdown.index("Middle") < markdown.index("After") < markdown.index(
        "*[Image OCR]\nOCR later\n[End OCR]*"
    )


# ---------------------------------------------------------------------------
# No OCR service — no OCR tags emitted
# ---------------------------------------------------------------------------


def test_docx_no_ocr_service_no_tags() -> None:
    path = TEST_DATA_DIR / "docx_image_middle.docx"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")
    converter = DocxConverterWithOCR()
    with open(path, "rb") as f:
        md = converter.convert(f, StreamInfo(extension=".docx")).text_content
    assert "*[Image OCR]" not in md
    assert "[End OCR]*" not in md
