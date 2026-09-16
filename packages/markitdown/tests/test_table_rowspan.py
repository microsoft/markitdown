import io
import re

import pytest

from markitdown import MarkItDown

_UNESCAPED_PIPE = re.compile(r"(?<!\\)((?:\\\\)*)\|")


def _convert(data: bytes, extension: str) -> str:
    return (
        MarkItDown().convert_stream(io.BytesIO(data), file_extension=extension).markdown
    )


def _rows(markdown: str) -> list[list[str]]:
    """Read the markdown table back the way a reader does."""
    rows = []
    for line in markdown.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = _UNESCAPED_PIPE.split(line.strip("|"))[::2]
        rows.append([cell.strip() for cell in cells])
    return rows


def test_a_rowspan_keeps_the_rows_below_it_in_their_columns() -> None:
    """A Markdown table cannot merge cells down, so the span needs empty cells.

    Without them `Hub` reads under `Region` and `7` under `Product`.
    """
    html = (
        "<table><tr><th>Region</th><th>Product</th><th>Units</th></tr>"
        "<tr><td rowspan='2'>EU</td><td>Cable</td><td>12</td></tr>"
        "<tr><td>Hub</td><td>7</td></tr>"
        "<tr><td>US</td><td>Cable</td><td>3</td></tr></table>"
    )

    assert _rows(_convert(html.encode("utf-8"), ".html")) == [
        ["Region", "Product", "Units"],
        ["---", "---", "---"],
        ["EU", "Cable", "12"],
        ["", "Hub", "7"],
        ["US", "Cable", "3"],
    ]


def test_a_rowspan_of_three_fills_both_rows_below() -> None:
    html = (
        "<table><tr><th>A</th><th>B</th></tr>"
        "<tr><td rowspan='3'>x</td><td>1</td></tr>"
        "<tr><td>2</td></tr><tr><td>3</td></tr></table>"
    )

    assert _rows(_convert(html.encode("utf-8"), ".html"))[2:] == [
        ["x", "1"],
        ["", "2"],
        ["", "3"],
    ]


def test_a_rowspan_in_the_last_column_is_filled_at_the_end() -> None:
    html = (
        "<table><tr><th>A</th><th>B</th></tr>"
        "<tr><td>1</td><td rowspan='2'>y</td></tr><tr><td>2</td></tr></table>"
    )

    assert _rows(_convert(html.encode("utf-8"), ".html"))[2:] == [["1", "y"], ["2", ""]]


def test_a_cell_that_spans_in_both_directions_fills_both_columns() -> None:
    html = (
        "<table><tr><th>A</th><th>B</th><th>C</th></tr>"
        "<tr><td rowspan='2' colspan='2'>x</td><td>1</td></tr><tr><td>2</td></tr></table>"
    )

    assert _rows(_convert(html.encode("utf-8"), ".html"))[3] == ["", "", "2"]


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        # The controls: neither carries a rowspan.
        (
            "<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table>",
            [["A", "B"], ["---", "---"], ["1", "2"]],
        ),
        (
            "<table><tr><th>A</th><th>B</th></tr><tr><td colspan='2'>wide</td></tr></table>",
            [["A", "B"], ["---", "---"], ["wide", ""]],
        ),
    ],
)
def test_a_table_without_a_rowspan_is_unchanged(
    html: str, expected: list[list[str]]
) -> None:
    assert _rows(_convert(html.encode("utf-8"), ".html")) == expected


def test_a_merged_word_cell_keeps_the_table_lined_up() -> None:
    """End to end: Word writes a vertically merged cell, mammoth emits rowspan."""
    docx = pytest.importorskip("docx")

    document = docx.Document()
    table = document.add_table(rows=4, cols=3)
    for index, heading in enumerate(["Region", "Product", "Units"]):
        table.cell(0, index).text = heading
    table.cell(1, 1).text = "Cable"
    table.cell(1, 2).text = "12"
    table.cell(2, 1).text = "Hub"
    table.cell(2, 2).text = "7"
    table.cell(3, 0).text = "US"
    table.cell(3, 1).text = "Cable"
    table.cell(3, 2).text = "3"
    table.cell(1, 0).merge(table.cell(2, 0)).text = "EU"

    buffer = io.BytesIO()
    document.save(buffer)

    rows = _rows(_convert(buffer.getvalue(), ".docx"))

    assert rows[-3:] == [["EU", "Cable", "12"], ["", "Hub", "7"], ["US", "Cable", "3"]]
