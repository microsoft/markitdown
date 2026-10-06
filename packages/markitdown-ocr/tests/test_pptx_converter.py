"""
Unit tests for PptxConverterWithOCR.

For each PPTX test file: convert with a mock OCR service then compare the
full output string against the expected snapshot.

OCR blocks use shared HTML escaping and Markdown hard breaks:
    *[Image OCR]
    MOCK\\_OCR\\_TEXT\\_12345
    [End OCR]*

Slide text, notes, and layout come from the core PPTX converter.
"""

import io
import sys
from pathlib import Path
from typing import Any

import pytest
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_ocr._ocr_service import OCRResult  # noqa: E402
from markitdown_ocr._pptx_converter_with_ocr import (  # noqa: E402
    PptxConverterWithOCR,
)
from markitdown import StreamInfo  # noqa: E402

TEST_DATA_DIR = Path(__file__).parent / "ocr_test_data"

_MOCK_TEXT = "MOCK_OCR_TEXT_12345"
_OCR_BLOCK = "*[Image OCR]\\\nMOCK\\_OCR\\_TEXT\\_12345\\\n[End OCR]*"


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
    expected = "<!-- Slide number: 1 -->\n# Welcome\n\n\n" + _OCR_BLOCK
    assert _convert("pptx_image_start.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_image_middle.pptx
# ---------------------------------------------------------------------------


def test_pptx_image_middle(svc: MockOCRService) -> None:
    # Slide 1: Introduction | Slide 2: Architecture + image | Slide 3: Conclusion  # noqa: E501
    expected = (
        "<!-- Slide number: 1 -->\n# Introduction"
        "\n\n<!-- Slide number: 2 -->\n# Architecture\n\n\n"
        + _OCR_BLOCK
        + "\n\n<!-- Slide number: 3 -->\n# Conclusion"
    )
    assert _convert("pptx_image_middle.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_image_end.pptx
# ---------------------------------------------------------------------------


def test_pptx_image_end(svc: MockOCRService) -> None:
    # Slide 1: Presentation | Slide 2: Thank You + image
    expected = (
        "<!-- Slide number: 1 -->\n# Presentation"
        "\n\n<!-- Slide number: 2 -->\n# Thank You\n\n\n" + _OCR_BLOCK
    )
    assert _convert("pptx_image_end.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_multiple_images.pptx
# ---------------------------------------------------------------------------


def test_pptx_multiple_images(svc: MockOCRService) -> None:
    # Slide 1: two images, no title text
    expected = "<!-- Slide number: 1 -->\n\n" + _OCR_BLOCK + "\n\n" + _OCR_BLOCK
    assert _convert("pptx_multiple_images.pptx", svc) == expected


# ---------------------------------------------------------------------------
# pptx_complex_layout.pptx
# ---------------------------------------------------------------------------


def test_pptx_complex_layout(svc: MockOCRService) -> None:
    expected = (
        "<!-- Slide number: 1 -->\n# Product Comparison"
        "\n\nOur products lead the market\n\n" + _OCR_BLOCK
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


def _chart_presentation(title: str | None) -> io.BytesIO:
    # Modify an in-memory copy of an existing deck; keep its fixture intact.
    presentation = Presentation(TEST_DATA_DIR / "pptx_image_middle.pptx")
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    data = CategoryChartData()
    data.categories = ["Cat 1"]
    data.add_series("Series 1", [10.0])
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(1),
        Inches(1),
        Inches(5),
        Inches(3),
        data,
    ).chart
    chart.has_title = True
    if title is not None:
        chart.chart_title.text_frame.text = title
    assert chart.chart_title.has_text_frame is (title is not None)
    stream = io.BytesIO()
    presentation.save(stream)
    stream.seek(0)
    return stream


@pytest.mark.parametrize("title", [None, "Revenue"])
def test_pptx_ocr_chart_title_text_frame(title: str | None) -> None:
    stream = _chart_presentation(title)
    # Reload the serialized package so the real parser reads title XML.
    chart = Presentation(stream).slides[-1].shapes[-1].chart
    converter = PptxConverterWithOCR()
    result = converter._convert_chart_to_markdown(chart)
    heading = "### Chart" if title is None else "### Chart: Revenue"
    assert result.strip().splitlines()[0] == heading
    assert "Cat 1" in result
    assert "Series 1" in result
    assert "10.0" in result
    # Accessing a title without a text frame must not create one.
    assert chart.chart_title.has_text_frame is (title is not None)
    stream.seek(0)
    markdown = converter.convert(stream, StreamInfo(extension=".pptx")).markdown
    assert result.strip() in markdown
