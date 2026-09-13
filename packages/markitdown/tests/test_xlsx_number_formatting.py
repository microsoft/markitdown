from io import BytesIO

import openpyxl

from markitdown import MarkItDown, StreamInfo


def _convert_workbook(workbook: openpyxl.Workbook) -> str:
    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)
    return MarkItDown().convert(
        stream, stream_info=StreamInfo(extension=".xlsx")
    ).markdown


def test_integer_column_with_blank_cell_renders_without_trailing_point_zero() -> None:
    # A blank cell makes pandas read the column as float64, which used to
    # render every whole number in it as "1.0" even though Excel shows "1".
    workbook = openpyxl.Workbook()
    sheet = workbook.active
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


def test_integer_column_with_numeric_header_and_blank_cell() -> None:
    # A numeric header row (e.g. years) keeps the column numeric even before
    # the header is split off, so the whole column is read as float64 and
    # its data cells used to render as "1.0" beside clean "5" cells.
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet"
    sheet.append([2023, 2024])
    sheet.append([1, 5])
    sheet.append([None, 6])
    sheet.append([3, 7])

    markdown = _convert_workbook(workbook)

    assert "| 1 | 5 |" in markdown
    assert "| 3 | 7 |" in markdown
    assert "1.0" not in markdown
    assert "3.0" not in markdown


def test_fractional_numbers_keep_their_decimals() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet"
    sheet.append(["Price"])
    sheet.append([2.5])
    sheet.append([None])

    markdown = _convert_workbook(workbook)

    assert "2.5" in markdown


def test_fully_populated_integer_column_is_unchanged() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet"
    sheet.append(["Qty"])
    sheet.append([2])
    sheet.append([4])

    markdown = _convert_workbook(workbook)

    assert "| 2 |" in markdown
    assert "| 4 |" in markdown
