import io
import os

import pytest

from markitdown import MarkItDown

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


def _convert_html(html: str) -> str:
    return (
        MarkItDown()
        .convert_stream(io.BytesIO(html.encode("utf-8")), file_extension=".html")
        .markdown
    )


def _table_lines(markdown: str) -> list[str]:
    return [
        line.strip() for line in markdown.splitlines() if line.strip().startswith("|")
    ]


@pytest.mark.parametrize(
    "html",
    [
        # What mammoth hands over for a Word table: no <thead>, no <th>.
        "<table><tr><td>Product</td><td>Spec</td></tr><tr><td>Cable</td><td>USB-C</td></tr></table>",
        # The same table wrapped in a <tbody>, which is what a browser's DOM has.
        "<table><tbody><tr><td>Product</td><td>Spec</td></tr><tr><td>Cable</td><td>USB-C</td></tr></tbody></table>",
    ],
)
def test_a_table_without_th_uses_its_first_row_as_the_header(html: str) -> None:
    assert _table_lines(_convert_html(html)) == [
        "| Product | Spec |",
        "| --- | --- |",
        "| Cable | USB-C |",
    ]


@pytest.mark.parametrize(
    "html",
    [
        "<table><tr><th>Product</th><th>Spec</th></tr><tr><td>Cable</td><td>USB-C</td></tr></table>",
        "<table><thead><tr><th>Product</th><th>Spec</th></tr></thead>"
        "<tbody><tr><td>Cable</td><td>USB-C</td></tr></tbody></table>",
    ],
)
def test_a_table_that_marks_its_header_is_unchanged(html: str) -> None:
    assert _table_lines(_convert_html(html)) == [
        "| Product | Spec |",
        "| --- | --- |",
        "| Cable | USB-C |",
    ]


def test_a_docx_table_keeps_its_first_row_as_the_header() -> None:
    """End to end, on the repository's own `test.docx`.

    Its table starts `1 2 3 4 5 6`, which is the row that was being pushed below
    a blank header.
    """
    pytest.importorskip("mammoth")

    with open(os.path.join(TEST_FILES_DIR, "test.docx"), "rb") as stream:
        markdown = MarkItDown().convert_stream(stream, file_extension=".docx").markdown

    lines = _table_lines(markdown)

    assert lines[0] == "| 1 | 2 | 3 | 4 | 5 | 6 |"
    assert lines[1] == "| --- | --- | --- | --- | --- | --- |"
