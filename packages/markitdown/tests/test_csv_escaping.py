#!/usr/bin/env python3 -m pytest
"""Tests for CSV values that would otherwise break the Markdown table.

The CSV converter builds its table by joining cells with `" | "`. Two
characters that are perfectly legal inside a CSV field corrupt that structure
if they are passed through untouched:

* a pipe is read as a column separator, so the row gains columns the header
  never declared — a renderer discards the surplus and the data is lost;
* a newline inside a quoted field ends the row early, leaving the remainder as
  stray text after the table.

Neither case raises, so both fail silently.
"""

import io
import re

from markitdown import MarkItDown


def _convert(csv_bytes: bytes) -> str:
    return (
        MarkItDown()
        .convert_stream(io.BytesIO(csv_bytes), file_extension=".csv")
        .markdown
    )


def test_pipe_in_cell_is_escaped() -> None:
    markdown = _convert(b'name,description\nWidget,"cheap | fast"\n')

    # The pipe must be escaped rather than emitted raw, or it splits the row.
    assert "| Widget | cheap \\| fast |" in markdown

    # Every row must declare exactly as many columns as the header. Split on
    # pipes that are not backslash-escaped.
    for line in markdown.splitlines():
        assert len(re.split(r"(?<!\\)\|", line)) - 2 == 2


def test_newline_in_quoted_cell_does_not_split_the_row() -> None:
    markdown = _convert(b'name,notes\nWidget,"line one\nline two"\n')

    # The table must stay on one line per record.
    assert len(markdown.splitlines()) == 3
    assert "| Widget | line one<br>line two |" in markdown


def test_pipe_in_header_is_escaped() -> None:
    markdown = _convert(b'"a | b",c\n1,2\n')

    assert "| a \\| b | c |" in markdown


def test_plain_values_are_unchanged() -> None:
    # Guards against over-escaping ordinary content.
    markdown = _convert(b"name,description\nWidget,cheap and fast\n")

    assert "| Widget | cheap and fast |" in markdown
    assert "\\" not in markdown


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
