"""Tests for XlsxConverter cleanup logic (R14).

Verifies that trailing all-NaN rows, fully-empty columns, and `Unnamed: N`
header noise are stripped before serialization. This protects against
real-world Excel files where users "use" thousands of cells they never
actually populated, causing the converter to emit megabytes of empty
table rows.
"""
from __future__ import annotations

import io

import pytest

from markitdown import MarkItDown, StreamInfo


@pytest.fixture
def md():
    return MarkItDown()


def _make_xlsx_with_padding(real_rows: int, empty_rows: int):
    """Build an .xlsx in memory with N real rows then M trailing empty rows."""
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "data"
    ws.append(["A", "B", "C"])
    for i in range(real_rows):
        ws.append([f"r{i}", i, i * 1.5])
    for _ in range(empty_rows):
        ws.append([None, None, None])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def test_xlsx_strips_trailing_empty_rows(md):
    """970 trailing empty rows must not appear as 970 empty table rows."""
    buf = _make_xlsx_with_padding(real_rows=30, empty_rows=970)
    result = md.convert_stream(buf, stream_info=StreamInfo(extension=".xlsx"))
    # All 30 real rows present
    for i in range(30):
        assert f"r{i}" in result.markdown
    # No "NaN" leakage from padding
    assert "NaN" not in result.markdown
    # Output stays compact (would be ~50 KB without cleanup)
    assert len(result.markdown) < 5000


def test_xlsx_strips_fully_empty_columns(md):
    """Columns containing only NaN must be dropped from the markdown table."""
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["keep1", "drop_me", "keep2"])
    for i in range(5):
        ws.append([f"v{i}", None, f"w{i}"])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    result = md.convert_stream(buf, stream_info=StreamInfo(extension=".xlsx"))
    assert "keep1" in result.markdown
    assert "keep2" in result.markdown
    # The all-NaN column header should not appear
    assert "drop_me" not in result.markdown


def test_xlsx_skips_completely_empty_sheets(md):
    """A workbook with one populated sheet and one fully empty sheet must
    emit only the populated sheet's H2 header."""
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "real"
    ws1.append(["x", "y"])
    ws1.append([1, 2])
    wb.create_sheet(title="ghost")  # entirely empty
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    result = md.convert_stream(buf, stream_info=StreamInfo(extension=".xlsx"))
    assert "## real" in result.markdown
    assert "## ghost" not in result.markdown


def test_xlsx_renames_unnamed_columns(md):
    """Auto-generated `Unnamed: N` column headers must be hidden."""
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    # First row entirely blank → pandas falls back to Unnamed: 0/1/...
    ws.append([None, None, None])
    ws.append(["real_a", "real_b", "real_c"])
    ws.append([1, 2, 3])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    result = md.convert_stream(buf, stream_info=StreamInfo(extension=".xlsx"))
    assert "Unnamed:" not in result.markdown
