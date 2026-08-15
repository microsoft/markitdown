"""Tests for the CSV converter's handling of BOM and blank rows."""

import io

from markitdown import MarkItDown
from markitdown._stream_info import StreamInfo


def _convert(data: bytes, charset: str | None = None) -> str:
    stream_info = StreamInfo(extension=".csv", charset=charset)
    return (
        MarkItDown()
        .convert_stream(io.BytesIO(data), stream_info=stream_info)
        .text_content
    )


def test_utf8_bom_is_stripped_from_the_header() -> None:
    result = _convert(b"\xef\xbb\xbfname,age\nAlice,30\n")

    assert "\ufeff" not in result
    assert result.startswith("| name | age |")
    assert "| Alice | 30 |" in result


def test_utf8_bom_is_stripped_when_charset_is_known() -> None:
    result = _convert(b"\xef\xbb\xbfname,age\nAlice,30\n", charset="utf-8")

    assert "\ufeff" not in result
    assert result.startswith("| name | age |")


def test_leading_blank_line_does_not_destroy_the_table() -> None:
    result = _convert(b"\nname,age\nAlice,30\n")

    assert result == "| name | age |\n| --- | --- |\n| Alice | 30 |"


def test_trailing_blank_lines_are_skipped() -> None:
    result = _convert(b"name,age\nAlice,30\n\n\n")

    assert result == "| name | age |\n| --- | --- |\n| Alice | 30 |"


def test_blank_lines_between_rows_are_skipped() -> None:
    result = _convert(b"name,age\n\nAlice,30\n\nBob,40\n")

    assert result == "| name | age |\n| --- | --- |\n| Alice | 30 |\n| Bob | 40 |"


def test_all_blank_input_returns_empty_markdown() -> None:
    result = _convert(b"\n\n\n")

    assert result == ""
