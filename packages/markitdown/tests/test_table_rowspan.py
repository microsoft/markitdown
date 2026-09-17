import io
import re
import time

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


def test_a_rowspan_of_zero_fills_the_rest_of_its_row_group() -> None:
    """`rowspan="0"` reaches to the last row of the group, so all of the rows
    below the cell need the placeholder, not just one.
    """
    html = (
        "<table><tr><th>Region</th><th>Product</th><th>Units</th></tr>"
        "<tr><td rowspan='0'>EU</td><td>Cable</td><td>12</td></tr>"
        "<tr><td>Hub</td><td>7</td></tr>"
        "<tr><td>Dock</td><td>4</td></tr></table>"
    )

    assert _rows(_convert(html.encode("utf-8"), ".html")) == [
        ["Region", "Product", "Units"],
        ["---", "---", "---"],
        ["EU", "Cable", "12"],
        ["", "Hub", "7"],
        ["", "Dock", "4"],
    ]


@pytest.mark.parametrize("rowspan", ["0", "5"])
def test_a_rowspan_stops_at_the_end_of_its_row_group(rowspan: str) -> None:
    """A span reaches no further than the group it starts in, so the `tfoot`
    row keeps its own columns whether the span is open ended or just too long.
    """
    html = (
        "<table>"
        f"<tbody><tr><td rowspan='{rowspan}'>EU</td><td>Cable</td><td>12</td></tr>"
        "<tr><td>Hub</td><td>7</td></tr></tbody>"
        "<tfoot><tr><td>Total</td><td>19</td></tr></tfoot></table>"
    )

    rows = _rows(_convert(html.encode("utf-8"), ".html"))

    assert rows[2:4] == [["EU", "Cable", "12"], ["", "Hub", "7"]]
    assert rows[-1] == ["Total", "19"]


def test_a_colspan_of_zero_is_one_column() -> None:
    """HTML5 dropped `colspan="0"`, and a browser reads it as a single column."""
    html = (
        "<table><tr><th>A</th><th>B</th></tr>"
        "<tr><td colspan='0'>x</td><td>1</td></tr></table>"
    )

    assert _rows(_convert(html.encode("utf-8"), ".html"))[2:] == [["x", "1"]]


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


def test_a_span_attribute_does_not_blow_up_the_output() -> None:
    """One cell spanning 1000 rows and 1000 columns asked for a million
    placeholders: 19 KB of HTML became 3 MB of Markdown in 20 s. Past a few
    placeholders per real cell the table is converted as markdownify converts
    it, without the padding."""
    html = (
        "<table><tr><td rowspan='1000' colspan='1000'>x</td></tr>"
        + "<tr><td>a</td></tr>" * 999
        + "</table><p>after</p>"
    )

    started = time.perf_counter()
    markdown = _convert(html.encode("utf-8"), ".html")
    elapsed = time.perf_counter() - started

    assert elapsed < 5
    assert len(markdown) < 10 * len(html)
    assert markdown.rstrip().endswith("after")


def test_a_rowspan_of_zero_goes_through_the_same_budget() -> None:
    """`rowspan="0"` asks for the rest of the row group without naming a number,
    so it has to be counted like any other span: 200 of them over 2000 rows ask
    for 399,800 placeholders and the table is left as markdownify writes it."""
    html = (
        "<table><tbody><tr>"
        + "<td rowspan='0'>x</td>" * 200
        + "</tr>"
        + "<tr><td>a</td></tr>" * 1999
        + "</tbody></table><p>after</p>"
    )

    started = time.perf_counter()
    markdown = _convert(html.encode("utf-8"), ".html")
    elapsed = time.perf_counter() - started

    assert elapsed < 5
    assert len(markdown) < 10 * len(html)
    assert markdown.rstrip().endswith("after")


def test_many_rowspans_are_filled_in_linear_time() -> None:
    """Inserting each placeholder with insert_before scanned its siblings, so
    30,000 of them in front of one cell took about 12 s."""
    spans = 30_000
    html = (
        "<table><tr>"
        + "<td rowspan='2'>h</td>" * spans
        + "</tr><tr><td>last</td></tr></table>"
    )

    started = time.perf_counter()
    rows = _rows(_convert(html.encode("utf-8"), ".html"))
    elapsed = time.perf_counter() - started

    assert elapsed < 5
    assert rows[-1] == [""] * spans + ["last"]
