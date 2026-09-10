"""Regression tests for CR-only CSV record separators (issue #2411)."""

import io

import pytest

from markitdown import MarkItDown, StreamInfo


@pytest.fixture(scope="module")
def converter() -> MarkItDown:
    return MarkItDown(enable_plugins=False)


@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"], ids=["LF", "CRLF", "CR"])
@pytest.mark.parametrize("final_newline", [False, True])
def test_csv_record_separators_produce_a_table(
    converter: MarkItDown, newline: str, final_newline: bool
) -> None:
    content = newline.join(["name,age", "Alice,30"])
    if final_newline:
        content += newline

    result = converter.convert_stream(
        io.BytesIO(content.encode("utf-8")),
        stream_info=StreamInfo(extension=".csv", charset="utf-8"),
    )

    assert result.markdown == "| name | age |\n| --- | --- |\n| Alice | 30 |"


@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"], ids=["LF", "CRLF", "CR"])
@pytest.mark.parametrize(
    "cell_newline", ["\n", "\r\n", "\r"], ids=["cell-LF", "cell-CRLF", "cell-CR"]
)
def test_csv_quoted_line_break_stays_inside_its_cell(
    converter: MarkItDown, newline: str, cell_newline: str
) -> None:
    content = newline.join(
        ["name,notes", f'Alice,"first{cell_newline}second"', "Bob,plain"]
    )

    result = converter.convert_stream(
        io.BytesIO(content.encode("utf-8")),
        stream_info=StreamInfo(extension=".csv", charset="utf-8"),
    )

    assert result.markdown == (
        "| name | notes |\n"
        "| --- | --- |\n"
        "| Alice | first second |\n"
        "| Bob | plain |"
    )
