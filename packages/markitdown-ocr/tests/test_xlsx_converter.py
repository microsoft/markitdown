"""
Unit tests for XlsxConverterWithOCR.

For each XLSX test file: convert with a mock OCR service then compare the
full output string against the expected snapshot.

OCR block format used by the converter:
    *[Image OCR]
    MOCK\\_OCR\\_TEXT\\_12345
    [End OCR]*

Images are grouped at the end of each sheet under:
    ### Images in this sheet:
"""

import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_ocr._ocr_service import OCRResult  # noqa: E402
from markitdown_ocr._xlsx_converter_with_ocr import (  # noqa: E402
    XlsxConverterWithOCR,
)
from markitdown import StreamInfo  # noqa: E402

TEST_DATA_DIR = Path(__file__).parent / "ocr_test_data"

_MOCK_TEXT = "MOCK_OCR_TEXT_12345"


_OCR_BLOCK = "*[Image OCR]  \nMOCK\\_OCR\\_TEXT\\_12345  \n[End OCR]*"


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
    converter = XlsxConverterWithOCR()
    with open(path, "rb") as f:
        return converter.convert(
            f, StreamInfo(extension=".xlsx"), ocr_service=ocr_service
        ).text_content


# ---------------------------------------------------------------------------
# xlsx_image_start.xlsx
# ---------------------------------------------------------------------------


def test_xlsx_image_start(svc: MockOCRService) -> None:
    expected = (
        "## Sales Q1\n"
        "| Product | Sales |\n"
        "| --- | --- |\n"
        "| Widget A | 100 |\n"
        "| Widget B | 150 |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}\n\n"
        "## Forecast Q2\n"
        "| Projected Sales | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "| Widget A | 120 |\n"
        "| Widget B | 180 |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}"
    )
    assert _convert("xlsx_image_start.xlsx", svc) == expected


# ---------------------------------------------------------------------------
# xlsx_image_middle.xlsx
# ---------------------------------------------------------------------------


def test_xlsx_image_middle(svc: MockOCRService) -> None:
    expected = (
        "## Revenue\n"
        "| Q1 Report | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "|  |  |\n"
        "| Revenue | $50,000 |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "| Profit Margin | 40% |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}\n\n"
        "## Expenses\n"
        "| Expense Breakdown | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "|  |  |\n"
        "| Expenses | $30,000 |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "| Savings | $5,000 |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}"
    )
    assert _convert("xlsx_image_middle.xlsx", svc) == expected


# ---------------------------------------------------------------------------
# xlsx_image_end.xlsx
# ---------------------------------------------------------------------------


def test_xlsx_image_end(svc: MockOCRService) -> None:
    expected = (
        "## Sheet\n"
        "| Financial Summary | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "| Total Revenue | $500,000 |\n"
        "| Total Expenses | $300,000 |\n"
        "| Net Profit | $200,000 |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "| Signature: |  |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}\n\n"
        "## Budget\n"
        "| Budget Allocation | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "| Marketing | $100,000 |\n"
        "| R&D | $150,000 |\n"
        "| Operations | $50,000 |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "|  |  |\n"
        "| Approved: |  |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}"
    )
    assert _convert("xlsx_image_end.xlsx", svc) == expected


# ---------------------------------------------------------------------------
# xlsx_multiple_images.xlsx
# ---------------------------------------------------------------------------


def test_xlsx_multiple_images(svc: MockOCRService) -> None:
    expected = (
        "## Overview\n"
        "| Dashboard |\n"
        "| --- |\n"
        "| Status: Active |\n"
        "|  |\n"
        "|  |\n"
        "|  |\n"
        "|  |\n"
        "| Performance Summary |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}\n\n"
        f"{_OCR_BLOCK}\n\n"
        "## Details\n"
        "| Detailed Metrics |\n"
        "| --- |\n"
        "| System Health |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}\n\n"
        "## Summary\n"
        "| Quarter Summary |\n"
        "| --- |\n"
        "| Overall Performance |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}"
    )
    assert _convert("xlsx_multiple_images.xlsx", svc) == expected


# ---------------------------------------------------------------------------
# xlsx_complex_layout.xlsx
# ---------------------------------------------------------------------------


def test_xlsx_complex_layout(svc: MockOCRService) -> None:
    expected = (
        "## Complex Report\n"
        "| Annual Report 2024 | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "|  |  |\n"
        "| Month | Sales |\n"
        "| Jan | 1000 |\n"
        "| Feb | 1200 |\n"
        "|  |  |\n"
        "| Total | 2200 |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}\n\n"
        f"{_OCR_BLOCK}\n\n"
        "## Customers\n"
        "| Customer Metrics | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "|  |  |\n"
        "| New Customers | 250 |\n"
        "| Retention Rate | 92% |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}\n\n"
        "## Regions\n"
        "| Regional Breakdown | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "|  |  |\n"
        "| Region | Revenue |\n"
        "| North | $800K |\n"
        "| South | $600K |\n\n"
        "### Images in this sheet:\n\n"
        f"{_OCR_BLOCK}"
    )
    assert _convert("xlsx_complex_layout.xlsx", svc) == expected


# ---------------------------------------------------------------------------
# No OCR service — no OCR tags emitted
# ---------------------------------------------------------------------------


def test_xlsx_no_ocr_service_no_tags() -> None:
    path = TEST_DATA_DIR / "xlsx_image_middle.xlsx"
    if not path.exists():
        pytest.skip(f"Test file not found: {path}")
    converter = XlsxConverterWithOCR()
    with open(path, "rb") as f:
        md = converter.convert(f, StreamInfo(extension=".xlsx")).text_content
    assert "*[Image OCR]" not in md
    assert "[End OCR]*" not in md
