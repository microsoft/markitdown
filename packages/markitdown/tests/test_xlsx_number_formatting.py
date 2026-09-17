"""Whole numbers must not render as ``1.0`` when a blank promotes the column to float."""

from io import BytesIO

import openpyxl
import pandas as pd

from markitdown import MarkItDown, StreamInfo
from markitdown.converters._xlsx_converter import _format_integral_columns


def _convert_workbook(workbook: openpyxl.Workbook) -> str:
    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)
    return (
        MarkItDown(enable_plugins=False)
        .convert_stream(stream, stream_info=StreamInfo(extension=".xlsx"))
        .markdown
    )


def test_integer_column_with_blank_cell_renders_without_trailing_point_zero() -> None:
    # A blank cell makes pandas read the column as float64, which used to
    # render every whole number in it as "1.0" even though Excel shows "1".
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "Sheet"
    sheet.append(["count"])
    sheet.append([1])
    sheet.append([None])
    sheet.append([2])

    markdown = _convert_workbook(workbook)

    assert "| 1 |" in markdown
    assert "| 2 |" in markdown
    assert "1.0" not in markdown
    assert "2.0" not in markdown


def test_integer_column_with_blank_beside_clean_integer_column() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "Sheet"
    sheet.append(["Qty", "Note"])
    sheet.append([1, "first"])
    sheet.append([None, "gap"])
    sheet.append([3, "last"])

    markdown = _convert_workbook(workbook)

    assert "| 1 | first |" in markdown
    assert "| 3 | last |" in markdown
    assert "1.0" not in markdown
    assert "3.0" not in markdown


def test_fractional_numbers_keep_their_decimals() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "Sheet"
    sheet.append(["Price"])
    sheet.append([2.5])
    sheet.append([None])

    markdown = _convert_workbook(workbook)

    assert "2.5" in markdown


def test_fully_populated_integer_column_is_unchanged() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "Sheet"
    sheet.append(["Qty"])
    sheet.append([2])
    sheet.append([4])

    markdown = _convert_workbook(workbook)

    assert "| 2 |" in markdown
    assert "| 4 |" in markdown


def test_format_integral_columns_helper_preserves_fractions_and_empties() -> None:
    # Shared by both the .xlsx and .xls converters before to_html.
    sheet = pd.DataFrame({"a": [1.0, None, 2.0], "b": [1.5, None, 2.0]})
    formatted = _format_integral_columns(sheet.copy())

    assert formatted["a"].tolist()[0] == 1
    assert formatted["a"].tolist()[2] == 2
    assert pd.isna(formatted["a"].tolist()[1])
    assert formatted["b"].tolist()[0] == 1.5
    assert isinstance(formatted["a"].tolist()[0], int)
