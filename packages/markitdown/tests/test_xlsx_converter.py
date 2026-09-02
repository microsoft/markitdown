from io import BytesIO

import openpyxl

from markitdown import MarkItDown, StreamInfo


def _convert_workbook(workbook: openpyxl.Workbook) -> str:
    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)
    return (
        MarkItDown().convert(stream, stream_info=StreamInfo(extension=".xlsx")).markdown
    )


def test_xlsx_drops_empty_rows_and_columns_without_losing_title_row() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet"
    sheet["A1"] = "PROGRESS"
    sheet["A3"] = "Task"
    sheet["C3"] = "Owner"
    sheet["D3"] = "Status"
    sheet["A4"] = "Design"
    sheet["C4"] = "Ana"
    sheet["D4"] = "Done"

    markdown = _convert_workbook(workbook)

    assert (
        markdown
        == """## Sheet
|  |  |  |
| --- | --- | --- |
| PROGRESS |  |  |
| Task | Owner | Status |
| Design | Ana | Done |"""
    )
    assert "Unnamed:" not in markdown
    assert "NaN" not in markdown


def test_xlsx_preserves_complete_first_row_as_header() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Data"
    sheet.append(["Alpha", "Beta"])
    sheet.append([1, 2])

    markdown = _convert_workbook(workbook)

    assert (
        markdown
        == """## Data
| Alpha | Beta |
| --- | --- |
| 1 | 2 |"""
    )
