"""A .csv file is not always comma separated.

Excel writes the list separator of the machine's locale -- a semicolon across
most of Europe -- and a tab separated export is routinely saved as .csv.
Parsing either one with a comma does not fail: it yields a single column holding
the whole row, separators and all.
"""

import io

import pytest

from markitdown import MarkItDown, StreamInfo


def _convert(content: bytes) -> str:
    return (
        MarkItDown(enable_plugins=False)
        .convert_stream(
            io.BytesIO(content),
            stream_info=StreamInfo(extension=".csv", charset="utf-8"),
        )
        .markdown
    )


_EXPECTED = (
    "| Name | Region | Units |\n"
    "| --- | --- | --- |\n"
    "| Widget | EU | 12 |\n"
    "| Gadget | US | 7 |"
)


@pytest.mark.parametrize("separator", [",", ";", "\t"])
def test_the_separator_the_file_was_written_with_is_used(separator: str) -> None:
    rows = ["Name;Region;Units", "Widget;EU;12", "Gadget;US;7"]
    content = "\n".join(row.replace(";", separator) for row in rows) + "\n"

    assert _convert(content.encode("utf-8")) == _EXPECTED


def test_a_sep_directive_sets_the_separator_and_is_not_a_row() -> None:
    """Excel honours a leading `sep=` line and does not show it."""
    content = b"sep=|\nName|Region|Units\nWidget|EU|12\nGadget|US|7\n"

    assert _convert(content) == _EXPECTED


def test_a_sep_directive_survives_a_bom() -> None:
    content = "﻿sep=;\nName;Region;Units\nWidget;EU;12\nGadget;US;7\n"

    assert _convert(content.encode("utf-8")) == _EXPECTED


def test_a_separator_inside_a_quoted_field_is_not_a_separator() -> None:
    content = b'Name,Note\nWidget,"a; b; c"\nGadget,"d; e; f"\n'

    assert _convert(content) == (
        "| Name | Note |\n"
        "| --- | --- |\n"
        "| Widget | a; b; c |\n"
        "| Gadget | d; e; f |"
    )


def test_a_single_column_file_stays_a_single_column() -> None:
    """Guard: a separator that does not line up across the rows is not one."""
    content = b"Note\na; b\nc; d\n"

    assert _convert(content) == "| Note |\n| --- |\n| a; b |\n| c; d |"


def test_a_ragged_comma_file_is_unchanged() -> None:
    """Guard: the existing padding behaviour for uneven rows still applies."""
    content = b"name,value\nAlice,1\n\nBob,2,extra\n"

    assert _convert(content) == (
        "| name | value |  |\n"
        "| --- | --- | --- |\n"
        "| Alice | 1 |  |\n"
        "|  |  |  |\n"
        "| Bob | 2 | extra |"
    )


def test_an_empty_file_is_unchanged() -> None:
    assert _convert(b"") == ""
