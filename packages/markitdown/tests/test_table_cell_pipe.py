import io
import re

import pytest

from markitdown import MarkItDown

_UNESCAPED_PIPE = re.compile(r"(?<!\\)((?:\\\\)*)\|")
# CommonMark: a backslash escapes ASCII punctuation, and nothing else.
_ESCAPE = re.compile(r"\\([!-/:-@\[-`{-~])")


def _convert(data: bytes, extension: str) -> str:
    return (
        MarkItDown().convert_stream(io.BytesIO(data), file_extension=extension).markdown
    )


def _rows(markdown: str) -> list[list[str]]:
    """Read the markdown table back the way a reader does.

    A row is split on every pipe that is not escaped, and each cell then has its
    backslash escapes resolved -- so a cell comes back as the text it held.
    """
    rows = []
    for line in markdown.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = _UNESCAPED_PIPE.split(line.strip("|"))[::2]
        rows.append([_ESCAPE.sub(r"\1", cell).strip() for cell in cells])
    return rows


@pytest.mark.parametrize(
    ("cell", "expected"),
    [
        # A part number, a shell command and a regex alternation all carry one.
        ("USB-A|USB-C", "USB-A|USB-C"),
        ("grep -E 'a|b'", "grep -E 'a|b'"),
        ("a||b", "a||b"),
        # A backslash already in the cell must not consume the escape.
        (r"a\|b", r"a\|b"),
        (r"C:\path", r"C:\path"),
        ("plain", "plain"),
    ],
)
def test_a_pipe_in_a_cell_stays_inside_the_cell(cell: str, expected: str) -> None:
    html = f"<table><tr><th>Product</th><th>Spec</th></tr><tr><td>Cable</td><td>{cell}</td></tr></table>"

    rows = _rows(_convert(html.encode("utf-8"), ".html"))

    assert rows[0] == ["Product", "Spec"]
    assert rows[-1] == ["Cable", expected]


def test_a_pipe_in_a_header_cell_stays_inside_the_cell() -> None:
    html = "<table><tr><th>Cable a|b</th><th>Spec</th></tr><tr><td>1</td><td>2</td></tr></table>"

    rows = _rows(_convert(html.encode("utf-8"), ".html"))

    assert rows[0] == ["Cable a|b", "Spec"]
    assert rows[-1] == ["1", "2"]


def test_a_pipe_outside_a_table_is_left_alone() -> None:
    assert _convert(b"<p>stdin | stdout</p>", ".html").strip() == "stdin | stdout"


def test_a_spreadsheet_cell_holding_a_pipe_keeps_its_column() -> None:
    openpyxl = pytest.importorskip("openpyxl")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Product", "Spec"])
    sheet.append(["Cable", "USB-A|USB-C"])
    sheet.append(["Hub", "4 ports"])
    buffer = io.BytesIO()
    workbook.save(buffer)

    rows = _rows(_convert(buffer.getvalue(), ".xlsx"))

    assert rows[0] == ["Product", "Spec"]
    assert rows[-2] == ["Cable", "USB-A|USB-C"]
    assert rows[-1] == ["Hub", "4 ports"]
