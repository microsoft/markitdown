"""Regression tests for #2484 and #2498: Excel conversion must reproduce the
values that are actually stored in the sheet.

``pd.read_excel`` applies pandas' default missing-value handling, which rewrites
the data in two ways:

* literal strings such as ``NA``, ``NULL`` or ``None`` are read as missing
  values, and
* a column that contains a missing value is promoted to ``float64``, so whole
  numbers render as ``2.0`` and blank cells render as the text ``NaN``.

A file converter must not rewrite the user's data that way, so both the .xlsx
and the .xls readers pass ``keep_default_na=False``.
"""

import datetime
import io
import os

import openpyxl
import pytest

from markitdown import MarkItDown, StreamInfo

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
XLS_FIXTURE = os.path.join(TEST_FILES_DIR, "test_na_values.xls")


def _convert_xlsx(rows: list) -> str:
    """Convert an in-memory .xlsx workbook built from ``rows`` into Markdown."""
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row in rows:
        sheet.append(row)
    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return (
        MarkItDown(enable_plugins=False)
        .convert_stream(buffer, stream_info=StreamInfo(extension=".xlsx"))
        .markdown
    )


def test_blank_cell_does_not_promote_whole_numbers_to_float() -> None:
    """#2484: a blank cell must not turn the other integers into ``2.0``."""
    markdown = _convert_xlsx([["count"], [1], [None], [2]])

    assert markdown == "## Sheet\n| count |\n| --- |\n| 1 |\n|  |\n| 2 |"


@pytest.mark.parametrize("literal", ["NA", "NULL", "None", "n/a", "null", "nan"])
def test_literal_missing_value_strings_are_preserved(literal: str) -> None:
    """#2498: strings that look like missing values must survive verbatim."""
    markdown = _convert_xlsx([["value"], [literal]])

    assert markdown == f"## Sheet\n| value |\n| --- |\n| {literal} |"


def test_blank_cell_renders_empty_instead_of_nan() -> None:
    """#2498: a genuinely blank cell must not become the text ``NaN``."""
    markdown = _convert_xlsx([["value"], [None], ["x"]])

    assert markdown == "## Sheet\n| value |\n| --- |\n|  |\n| x |"


def test_xls_conversion_preserves_blanks_and_literals() -> None:
    """#2484 and #2498 also apply to the .xls (xlrd) reader."""
    markdown = MarkItDown(enable_plugins=False).convert(XLS_FIXTURE).markdown

    assert markdown == (
        "## Sheet1\n"
        "| count | value |\n"
        "| --- | --- |\n"
        "| 1 | NA |\n"
        "|  | NULL |\n"
        "| 2 | None |\n"
        "| 3 | n/a |"
    )


def test_dates_and_floats_are_unaffected() -> None:
    """Reading raw cells must not change how other value types are rendered.

    Guards against "fixing" this by reading every column as ``object``, which
    would append a time component to dates and destroy small floats.
    """
    markdown = _convert_xlsx(
        [
            ["when", "approximation"],
            [datetime.datetime(2024, 1, 5), 1.23456789012345e-7],
        ]
    )

    assert markdown == (
        "## Sheet\n"
        "| when | approximation |\n"
        "| --- | --- |\n"
        "| 2024-01-05 | 1.234568e-07 |"
    )
