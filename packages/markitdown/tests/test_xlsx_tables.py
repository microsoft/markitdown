#!/usr/bin/env python3 -m pytest
"""A pipe in an Excel cell must not break the Markdown table.

A cell value like ``x|y`` is data, not a column separator. Without escaping,
the converted row gains a phantom column (``| x|y | 2 |`` in a 2-column
table). See also #2019 / #2266, which fixed the same class of bug for CSV.
"""

import io

import pandas as pd
import pytest

from markitdown import MarkItDown, StreamInfo


def _xlsx_bytes(frame: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        frame.to_excel(writer, sheet_name="Sheet1", index=False)
    return buffer.getvalue()


def _xls_bytes(rows: list) -> bytes:
    xlwt = pytest.importorskip("xlwt")

    book = xlwt.Workbook()
    sheet = book.add_sheet("Sheet1")
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            sheet.write(r, c, value)
    buffer = io.BytesIO()
    book.save(buffer)
    return buffer.getvalue()


def _convert(data: bytes, extension: str) -> str:
    return (
        MarkItDown(enable_plugins=False)
        .convert_stream(
            io.BytesIO(data),
            stream_info=StreamInfo(extension=extension),
        )
        .markdown
    )


def test_xlsx_pipe_in_cell_is_escaped() -> None:
    markdown = _convert(_xlsx_bytes(pd.DataFrame({"a": ["x|y"], "b": ["2"]})), ".xlsx")
    assert "| x\\|y | 2 |" in markdown


def test_xlsx_pipe_in_header_is_escaped() -> None:
    markdown = _convert(_xlsx_bytes(pd.DataFrame({"a|b": ["1"], "c": ["2"]})), ".xlsx")
    assert "| a\\|b | c |" in markdown


def test_xlsx_backslash_before_pipe_stays_literal() -> None:
    # A literal backslash before a pipe must survive: ``a\\|b`` renders as a\|b.
    markdown = _convert(
        _xlsx_bytes(pd.DataFrame({"a": ["a\\|b"], "b": ["2"]})), ".xlsx"
    )
    assert "| a\\\\\\|b | 2 |" in markdown


def test_xls_pipe_in_cell_is_escaped() -> None:
    markdown = _convert(_xls_bytes([["a", "b"], ["x|y", "2"]]), ".xls")
    assert "| x\\|y | 2 |" in markdown
