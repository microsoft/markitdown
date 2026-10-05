"""CSV conversion, escaping, blank rows, and line endings."""

import io

import pytest

from markitdown import MarkItDown, StreamInfo


# Record separators


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


# Long blank runs


@pytest.mark.parametrize("position", ["leading", "after_header", "trailing", "all"])
def test_csv_long_blank_runs(position: str) -> None:
    blank = b"\n" * 100_000
    header = b"name,value\n"
    # An internal blank row and a wider data row must survive trimming.
    data = b"Alice,1\n\nBob,2,extra\n"
    content = {
        "leading": blank + header + data,
        "after_header": header + blank + data,
        "trailing": header + data + blank,
        "all": blank,
    }[position]

    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(content),
        stream_info=StreamInfo(extension=".csv", charset="utf-8"),
    )

    expected = (
        "| name | value |  |\n"
        "| --- | --- | --- |\n"
        "| Alice | 1 |  |\n"
        "|  |  |  |\n"
        "| Bob | 2 | extra |"
    )
    assert result.markdown == ("" if position == "all" else expected)


# Conversion regressions

###############################################################################
# CSV converter.
###############################################################################


def _convert_csv(data: bytes, charset: str | None = None) -> str:
    stream_info = StreamInfo(extension=".csv", charset=charset)
    return (
        MarkItDown()
        .convert_stream(io.BytesIO(data), stream_info=stream_info)
        .text_content
    )


def test_csv_utf8_bom_is_stripped_from_the_header() -> None:
    result = _convert_csv(b"\xef\xbb\xbfname,age\nAlice,30\n")

    assert "\ufeff" not in result
    assert result.startswith("| name | age |")
    assert "| Alice | 30 |" in result


def test_csv_utf8_bom_is_stripped_when_charset_is_known() -> None:
    result = _convert_csv(b"\xef\xbb\xbfname,age\nAlice,30\n", charset="utf-8")

    assert "\ufeff" not in result
    assert result.startswith("| name | age |")


def test_csv_leading_blank_line_does_not_destroy_the_table() -> None:
    result = _convert_csv(b"\nname,age\nAlice,30\n")

    assert result == "| name | age |\n| --- | --- |\n| Alice | 30 |"


def test_csv_trailing_blank_lines_are_skipped() -> None:
    result = _convert_csv(b"name,age\nAlice,30\n\n\n")

    assert result == "| name | age |\n| --- | --- |\n| Alice | 30 |"


def test_csv_blank_lines_between_rows_are_kept() -> None:
    result = _convert_csv(b"name,age\n\nAlice,30\n\nBob,40\n")

    assert (
        result == "| name | age |\n| --- | --- |\n| Alice | 30 |\n|  |  |\n| Bob | 40 |"
    )


def test_csv_all_blank_input_returns_empty_markdown() -> None:
    result = _convert_csv(b"\n\n\n")

    assert result == ""


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            b"banner\nname,age,city\nAlice,30,Seattle\n",
            "| banner |  |  |\n| --- | --- | --- |\n"
            "| name | age | city |\n| Alice | 30 | Seattle |",
        ),
        (
            b"name,age\nAlice\n\nBob,40,Seattle\nCarol,25\n",
            "| name | age |  |\n| --- | --- | --- |\n"
            "| Alice |  |  |\n|  |  |  |\n"
            "| Bob | 40 | Seattle |\n| Carol | 25 |  |",
        ),
        (
            b"name\nAlice,,\n",
            "| name |  |  |\n| --- | --- | --- |\n| Alice |  |  |",
        ),
        (
            b"name,age,city\nAlice,30\nBob\n",
            "| name | age | city |\n| --- | --- | --- |\n"
            "| Alice | 30 |  |\n| Bob |  |  |",
        ),
    ],
    ids=["preamble", "widest-row-late", "trailing-empty-fields", "widest-header"],
)
def test_csv_table_matches_widest_row(data: bytes, expected: str) -> None:
    assert _convert_csv(data) == expected


def test_csv_pipe_in_cell_is_escaped() -> None:
    result = _convert_csv(b'name,description\nWidget,"cheap | fast"\n')

    # The pipe must be escaped rather than emitted raw, or it splits the row.
    assert "| Widget | cheap \\| fast |" in result


def test_csv_pipe_preceded_by_backslash_is_still_escaped() -> None:
    # `left\|right` must not become `left\\|right`: the doubled backslash is a
    # literal backslash, which would leave the pipe acting as a delimiter and
    # let a renderer drop `right`. The run of backslashes is doubled instead,
    # so the escaping `\|` survives.
    result = _convert_csv(b'name,description\nWidget,"left\\|right"\n')

    assert r"| Widget | left\\\|right |" in result


def test_csv_pipe_preceded_by_two_backslashes_is_still_escaped() -> None:
    # An even-length run is just as dangerous once the naive `\|` is appended,
    # so check a longer run as well.
    result = _convert_csv(b'name,description\nWidget,"left\\\\|right"\n')

    assert r"| Widget | left\\\\\|right |" in result


def test_csv_newline_in_quoted_cell_does_not_split_the_row() -> None:
    result = _convert_csv(b'name,notes\nWidget,"line one\nline two"\n')

    # The table must stay on one line per record; the embedded break collapses
    # to a space.
    assert len(result.splitlines()) == 3
    assert "| Widget | line one line two |" in result


def test_csv_carriage_returns_in_quoted_cell_collapse_to_spaces() -> None:
    result = _convert_csv(b'name,notes\nWidget,"line one\r\nline two\rline three"\n')

    assert len(result.splitlines()) == 3
    assert "| Widget | line one line two line three |" in result


def test_csv_pipe_in_header_is_escaped() -> None:
    result = _convert_csv(b'"a | b",c\n1,2\n')

    assert "| a \\| b | c |" in result


def test_csv_plain_values_are_unchanged() -> None:
    # Guards against over-escaping ordinary content.
    result = _convert_csv(b"name,description\nWidget,cheap and fast\n")

    assert "| Widget | cheap and fast |" in result
    assert "\\" not in result


def test_csv_backslash_without_a_pipe_is_left_alone() -> None:
    # Only backslashes that guard a pipe are doubled; a Windows path stays
    # readable.
    result = _convert_csv(b"name,path\nWidget,C:\\temp\\file.txt\n")

    assert r"| Widget | C:\temp\file.txt |" in result


@pytest.mark.parametrize(
    "suffix,escaped_suffix",
    [("", ""), ("|", r"\|"), ("x|", r"x\|")],
)
def test_csv_long_backslash_runs(suffix: str, escaped_suffix: str) -> None:
    backslashes = "\\" * 65_536
    value = backslashes + suffix
    expected = backslashes * (2 if suffix == "|" else 1) + escaped_suffix

    result = _convert_csv(f"{value}\n{value}\n".encode("utf-8"), charset="utf-8")

    assert result == f"| {expected} |\n| --- |\n| {expected} |"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
