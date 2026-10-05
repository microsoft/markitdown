"""Keep the XLSX table shortcut aligned with the public conversion output."""

import inspect
import io
from unittest.mock import Mock

import openpyxl
import pandas as pd
import pytest
from markitdown import MarkItDown, StreamInfo
from markitdown.converters import XlsxConverter, _xlsx_converter
from markitdown.converters._html_converter import HtmlConverter
from markitdown.converters._markdownify import _CustomMarkdownify


def _workbook(*sheets: tuple[str, list[list[object]]]) -> bytes:
    workbook = openpyxl.Workbook()
    workbook.remove(workbook.active)
    for name, rows in sheets:
        sheet = workbook.create_sheet(name)
        for row in rows:
            sheet.append(row)
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def _legacy_output(data: bytes, **kwargs: object) -> str:
    sheets = pd.read_excel(io.BytesIO(data), sheet_name=None, engine="openpyxl")
    converter = HtmlConverter()
    return "\n\n".join(
        f"## {name}\n"
        + converter.convert_string(
            sheet.to_html(index=False), **kwargs
        ).markdown.strip()
        for name, sheet in sheets.items()
    )


def test_public_xlsx_conversion_keeps_table_output_without_html_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = _workbook(
        ("People", [["Name", "Count"], ["Ada", 2], ["Björk & Co", 3]]),
        ("Notes", [["Text"], ["<tag> *bold* | pipe"]]),
    )
    expected = _legacy_output(data)
    assert "## People\n| Name | Count |\n| --- | --- |\n| Ada | 2 |" in expected
    assert "Björk & Co" in expected
    assert "\\*bold\\*" in expected

    def unexpected_fallback(*args: object, **kwargs: object) -> None:
        raise AssertionError("ordinary pandas tables should use the table shortcut")

    monkeypatch.setattr(HtmlConverter, "convert_string", unexpected_fallback)
    actual = (
        MarkItDown().convert_stream(io.BytesIO(data), file_extension=".xlsx").markdown
    )
    assert actual == expected


def test_unicode_whitespace_uses_legacy_html_conversion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = _workbook(("Unicode", [["Text"], ["one\u00a0two"]]))
    expected = _legacy_output(data)
    converter = XlsxConverter()
    original = converter._html_converter.convert_string
    fallback = Mock(wraps=original)
    monkeypatch.setattr(converter._html_converter, "convert_string", fallback)

    actual = converter.convert(io.BytesIO(data), StreamInfo(extension=".xlsx")).markdown

    assert actual == expected
    assert "one" in actual and "two" in actual
    fallback.assert_called_once()


def test_formatting_options_still_reach_legacy_html_converter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = _workbook(("Options", [["first_name"], ["a_b"]]))
    options = {"escape_underscores": False}
    expected = _legacy_output(data, **options)
    converter = XlsxConverter()
    original = converter._html_converter.convert_string
    fallback = Mock(wraps=original)
    monkeypatch.setattr(converter._html_converter, "convert_string", fallback)

    actual = converter.convert(
        io.BytesIO(data), StreamInfo(extension=".xlsx"), **options
    ).markdown

    assert actual == expected
    assert "a_b" in actual
    fallback.assert_called_once()
    assert fallback.call_args.kwargs == options


def test_empty_and_header_only_sheets_keep_native_output() -> None:
    data = _workbook(
        ("Empty", []),
        ("Headers", [["First", "Second"]]),
    )
    actual = (
        MarkItDown().convert_stream(io.BytesIO(data), file_extension=".xlsx").markdown
    )
    assert actual == _legacy_output(data)
    assert actual.startswith("## Empty\n")
    assert "## Headers\n| First | Second |" in actual


@pytest.mark.parametrize("value", ["a_b *c*", "one\u00a0two"])
def test_older_markdownify_escape_signature_keeps_public_xlsx_output(
    monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    data = _workbook(("Legacy", [["Text"], [value]]))
    expected = _legacy_output(data)
    original_escape = _CustomMarkdownify.escape
    has_parent_tags = "parent_tags" in inspect.signature(original_escape).parameters

    class LegacyEscapeFormatter(_CustomMarkdownify):
        def escape(self, text: str) -> str:
            if has_parent_tags:
                return original_escape(self, text, [])
            return original_escape(self, text)

    monkeypatch.setattr(_xlsx_converter, "_CustomMarkdownify", LegacyEscapeFormatter)
    actual = (
        MarkItDown().convert_stream(io.BytesIO(data), file_extension=".xlsx").markdown
    )
    assert actual == expected
