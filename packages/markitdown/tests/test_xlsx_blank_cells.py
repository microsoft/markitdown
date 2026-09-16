"""A blank cell must not rewrite the rest of its column.

`DataFrame.to_html` writes the string ``NaN`` into an empty cell by default, and
pandas upcasts a column that holds one, so a single empty cell turned `12` into
`12.0` and `True` into `1.0` for every other row of that column.
"""

import datetime
import io

import pytest

from markitdown import MarkItDown, StreamInfo

openpyxl = pytest.importorskip("openpyxl")
pytest.importorskip("pandas")


def _xlsx(rows: list[list[object]]) -> io.BytesIO:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    for row in rows:
        sheet.append(row)
    stream = io.BytesIO()
    workbook.save(stream)
    stream.seek(0)
    return stream


def _convert(rows: list[list[object]]) -> str:
    return (
        MarkItDown(enable_plugins=False)
        .convert_stream(
            _xlsx(rows),
            stream_info=StreamInfo(extension=".xlsx"),
        )
        .markdown
    )


def test_blank_cell_stays_blank() -> None:
    markdown = _convert(
        [
            ["Product", "Notes"],
            ["Widget", None],
            ["Gadget", "backordered"],
        ]
    )

    assert markdown == (
        "## Sheet1\n"
        "| Product | Notes |\n"
        "| --- | --- |\n"
        "| Widget |  |\n"
        "| Gadget | backordered |"
    )
    assert "NaN" not in markdown


def test_a_blank_cell_does_not_turn_the_column_into_floats() -> None:
    markdown = _convert(
        [
            ["Units", "Year"],
            [12, 2026],
            [None, 2025],
        ]
    )

    assert markdown == (
        "## Sheet1\n"
        "| Units | Year |\n"
        "| --- | --- |\n"
        "| 12 | 2026 |\n"
        "|  | 2025 |"
    )


def test_a_blank_cell_does_not_turn_booleans_into_numbers() -> None:
    markdown = _convert(
        [
            ["Shipped", "Id"],
            [True, 1],
            [None, 2],
            [False, 3],
        ]
    )

    assert markdown == (
        "## Sheet1\n"
        "| Shipped | Id |\n"
        "| --- | --- |\n"
        "| True | 1 |\n"
        "|  | 2 |\n"
        "| False | 3 |"
    )


def test_a_date_cell_carries_no_time_and_a_blank_one_is_empty() -> None:
    """A date cell has no time to show; a datetime cell keeps the one it has."""
    markdown = _convert(
        [
            ["Due", "Id"],
            [datetime.date(2026, 1, 5), 1],
            [None, 2],
            [datetime.datetime(2026, 2, 9, 14, 30), 3],
        ]
    )

    assert markdown == (
        "## Sheet1\n"
        "| Due | Id |\n"
        "| --- | --- |\n"
        "| 2026-01-05 | 1 |\n"
        "|  | 2 |\n"
        "| 2026-02-09 14:30:00 | 3 |"
    )


def test_a_sheet_without_blanks_is_unchanged() -> None:
    """Guard: the common case must render exactly as it did before."""
    markdown = _convert(
        [
            ["Alpha", "Beta"],
            [89, 82],
            [76, 89],
        ]
    )

    assert markdown == (
        "## Sheet1\n"
        "| Alpha | Beta |\n"
        "| --- | --- |\n"
        "| 89 | 82 |\n"
        "| 76 | 89 |"
    )


def test_a_cell_holding_markup_is_unchanged() -> None:
    """Guard: the HTML round trip through the table renderer is untouched."""
    markdown = _convert(
        [
            ["Note"],
            ["<b>bold</b> & <i>italic</i>"],
        ]
    )

    assert markdown == ("## Sheet1\n| Note |\n| --- |\n| <b>bold</b> & <i>italic</i> |")
