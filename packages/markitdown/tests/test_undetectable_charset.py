#!/usr/bin/env python3 -m pytest
"""Tests for bytes no charset decodes.

``charset_normalizer.from_bytes(data).best()`` returns ``None`` when nothing
decodes the bytes, and ``str(None)`` is the four-character string ``"None"``,
so a binary file handed over with a text extension became a document whose
entire content was the word "None" -- four characters that were never in the
file.
"""

import io

from charset_normalizer import from_bytes

from markitdown import MarkItDown, StreamInfo

# Random bytes: no charset claims them, which is what makes `best()` answer None.
# Fixed rather than generated, so the test does not depend on chance.
UNDECODABLE = bytes((7 * i * i + 251 * i + 193) % 256 for i in range(4096))


def test_the_fixture_really_is_undecodable() -> None:
    """Guards the guard: if some charset claimed these bytes the rest would pass
    for the wrong reason."""
    assert from_bytes(UNDECODABLE).best() is None


def test_binary_with_a_text_extension_is_not_the_word_none() -> None:
    markitdown = MarkItDown()
    for extension in (".txt", ".md"):
        result = markitdown.convert_stream(
            io.BytesIO(UNDECODABLE), file_extension=extension
        )
        assert result.markdown != "None"


def test_binary_with_a_csv_extension_is_not_a_table_of_none() -> None:
    markitdown = MarkItDown()
    result = markitdown.convert_stream(io.BytesIO(UNDECODABLE), file_extension=".csv")
    assert result.markdown != "| None |\n| --- |"


def test_ordinary_text_is_unchanged() -> None:
    """The fallback only runs when detection fails; everything else is as it was."""
    markitdown = MarkItDown()

    text = markitdown.convert_stream(
        io.BytesIO(b"hello, world\n"), file_extension=".txt"
    )
    assert text.markdown == "hello, world\n"

    table = markitdown.convert_stream(io.BytesIO(b"a,b\n1,2\n"), file_extension=".csv")
    assert table.markdown == "| a | b |\n| --- | --- |\n| 1 | 2 |"


def test_text_containing_the_word_none_survives() -> None:
    """The bug was a whole document reading "None", not the word appearing in
    one."""
    markitdown = MarkItDown()
    result = markitdown.convert_stream(
        io.BytesIO(b"value,note\nNone,missing\n"), file_extension=".csv"
    )
    assert result.markdown == "| value | note |\n| --- | --- |\n| None | missing |"


def test_a_declared_charset_still_wins() -> None:
    """`stream_info.charset` short-circuits detection and is untouched."""
    markitdown = MarkItDown()
    body = "名称,代码\n浦发银行,600000\n".encode("gb18030")
    result = markitdown.convert_stream(
        io.BytesIO(body),
        stream_info=StreamInfo(extension=".csv", charset="gb18030"),
    )
    assert "浦发银行" in result.markdown
