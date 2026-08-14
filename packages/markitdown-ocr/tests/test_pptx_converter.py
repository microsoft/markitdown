"""
Unit tests for PptxConverterWithOCR.

For each PPTX test file: convert with a mock OCR service then compare the
full output string against the expected snapshot.

OCR block format used by the converter:
    *[Image OCR]
    MOCK_OCR_TEXT_12345
    [End OCR]*

Note: PPTX slide text uses literal backslash-n (\\n) sequences from the
underlying PPTX converter template; OCR blocks use real newlines.
"""

import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_ocr._ocr_service import OCRResult  # noqa: E402
from markitdown_ocr._pptx_converter_with_ocr import (  # noqa: E402
    PptxConverterWithOCR,
)
from markitdown import StreamInfo  # noqa: E402

TEST_DATA_DIR = Path(__file__).parent / "ocr_test_data"

_MOCK_TEXT = "MOCK_OCR_TEXT_12345"
_OCR_BLOCK = f"*[Image OCR]\n{_MOCK_TEXT}\n[End OCR]*"


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
    converter = PptxConverterWithOCR()
    with open(path, "rb") as f:
        return converter.convert(
            f, StreamInfo(extension=".pptx"), ocr_service=ocr_service
        ).text_content


# ---------------------------------------------------------------------------
# pptx_image_start.pptx
# ---------------------------------------------------------------------------


def test_pptx_image_start(svc: MockOCRService) -> None:
    # Slide 1: title "Welcome" followed by an image
    expected = (
        "\\n\\n<!-- Slide number: 1 -->\\n# Welcome\\n\\n"
        "\n*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    )
    assert _convert("pptx_image_start.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_image_middle.pptx
# ---------------------------------------------------------------------------


def test_pptx_image_middle(svc: MockOCRService) -> None:
    # Slide 1: Introduction | Slide 2: Architecture + image | Slide 3: Conclusion  # noqa: E501
    expected = (
        "\\n\\n<!-- Slide number: 1 -->\\n# Introduction"
        "\\n\\n\\n\\n<!-- Slide number: 2 -->\\n# Architecture\\n\\n"
        "\n*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
        "\\n\\n<!-- Slide number: 3 -->\\n# Conclusion\\n\\n"
    )
    assert _convert("pptx_image_middle.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_image_end.pptx
# ---------------------------------------------------------------------------


def test_pptx_image_end(svc: MockOCRService) -> None:
    # Slide 1: Presentation | Slide 2: Thank You + image
    expected = (
        "\\n\\n<!-- Slide number: 1 -->\\n# Presentation"
        "\\n\\n\\n\\n<!-- Slide number: 2 -->\\n# Thank You\\n\\n"
        "\n*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    )
    assert _convert("pptx_image_end.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_multiple_images.pptx
# ---------------------------------------------------------------------------


def test_pptx_multiple_images(svc: MockOCRService) -> None:
    # Slide 1: two images, no title text
    expected = (
        "\\n\\n<!-- Slide number: 1 -->\\n# \\n"
        "\n*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
        "\n\n*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    )
    assert _convert("pptx_multiple_images.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_complex_layout.pptx
# ---------------------------------------------------------------------------


def test_pptx_complex_layout(svc: MockOCRService) -> None:
    expected = (
        "\\n\\n<!-- Slide number: 1 -->\\n# Product Comparison"
        "\\n\\nOur products lead the market\\n"
        "\n*[Image OCR]\nMOCK_OCR_TEXT_12345\n[End OCR]*"
    )
    assert _convert("pptx_complex_layout.pptx", svc) == expected


# ---------------------------------------------------------------------------
# No OCR service — no OCR tags emitted
# ---------------------------------------------------------------------------


def test_pptx_no_ocr_service_no_tags() -> None:
    path = TEST_DATA_DIR / "pptx_image_middle.pptx"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")
    converter = PptxConverterWithOCR()
    with open(path, "rb") as f:
        md = converter.convert(f, StreamInfo(extension=".pptx")).text_content
    assert "*[Image OCR]" not in md
    assert "[End OCR]*" not in md
