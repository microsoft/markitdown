"""Currency-formatted Excel cells keep their label (microsoft/markitdown#53)."""

import io
import re
import zipfile

import openpyxl
import pytest

from markitdown import StreamInfo
from markitdown.converters import XlsxConverter

_INFO = StreamInfo(extension=".xlsx")

_DIMENSION_REF_RE = re.compile(rb'(<dimension ref=")[^"]+(")')


def _workbook() -> bytes:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    sheet.append(["Item", "Count", "Cost", "Weight", "Total"])
    sheet.append(["Breakfast", 20, 5, None, 100])
    sheet.append(["Laptops", 5, 1199, None, 5995])
    sheet.append(["Car tires", 8, 199, "150 kg", 1592])
    for row in sheet.iter_rows(min_row=2, min_col=3, max_col=3):
        for cell in row:
            cell.number_format = '"$"#,##0.00'
    for row in sheet.iter_rows(min_row=2, min_col=5, max_col=5):
        for cell in row:
            cell.number_format = '"$"#,##0.00'
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def _convert(data: bytes) -> str:
    return XlsxConverter().convert(io.BytesIO(data), _INFO).markdown


def test_currency_cells_keep_their_label() -> None:
    markdown = _convert(_workbook())
    assert "$5" in markdown
    assert "$1199" in markdown
    assert "$100" in markdown
    assert "Breakfast" in markdown
    assert "150 kg" in markdown


def test_plain_cells_are_untouched() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Item", "Count"])
    sheet.append(["Breakfast", 20])
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    markdown = _convert(stream.getvalue())
    assert "| Breakfast | 20 |" in markdown
    assert "$" not in markdown


def test_euro_suffix_format() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Price"])
    sheet.append([42])
    sheet["A2"].number_format = "#,##0.00 [$€-x-euro2]"
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    assert "42€" in _convert(stream.getvalue())


def test_section_specific_currency_uses_cell_value() -> None:
    from markitdown.converters._xlsx_converter import (
        _currency_symbol,
        _is_currency_position_prefix,
        _select_format_section,
    )

    fmt = '"$"#,##0;"€"#,##0'
    assert _select_format_section(fmt, 5) == '"$"#,##0'
    assert _select_format_section(fmt, -5) == '"€"#,##0'
    assert _currency_symbol(fmt, 5) == "$"
    assert _currency_symbol(fmt, -5) == "€"
    assert _is_currency_position_prefix(fmt, 5)
    assert _is_currency_position_prefix(fmt, -5)

    # 3 sections: positive / negative / zero
    fmt3 = '"$"#,##0;"€"#,##0;"¥"#,##0'
    assert _currency_symbol(fmt3, 5) == "$"
    assert _currency_symbol(fmt3, -5) == "€"
    assert _currency_symbol(fmt3, 0) == "¥"

    # end-to-end: negative keeps its own section currency
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Balance"])
    sheet.append([10])
    sheet.append([-5])
    sheet["A2"].number_format = fmt
    sheet["A3"].number_format = fmt
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    markdown = _convert(stream.getvalue())
    assert "$10" in markdown
    assert "€" in markdown
    assert "$-5" not in markdown


def test_thai_baht_format() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Price"])
    sheet.append([42])
    sheet["A2"].number_format = '"฿"#,##0'
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    assert "฿42" in _convert(stream.getvalue())


def test_quoted_semicolon_is_not_a_section_separator() -> None:
    from markitdown.converters._xlsx_converter import _select_format_section

    assert _select_format_section('"$;gross"#,##0', -5) == '"$;gross"#,##0'


def test_locale_only_block_produces_no_label() -> None:
    from markitdown.converters._xlsx_converter import _currency_symbol

    assert _currency_symbol("[$-409]#,##0.00", 42) is None
    assert _currency_symbol("[$-409]0%", 0.42) is None

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Price", "Rate"])
    sheet.append([42, 0.42])
    sheet["A2"].number_format = "[$-409]#,##0.00"
    sheet["B2"].number_format = "[$-409]0%"
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    markdown = _convert(stream.getvalue())
    assert "$" not in markdown


def test_full_currency_labels_are_preserved() -> None:
    from markitdown.converters._xlsx_converter import _currency_symbol

    assert _currency_symbol('"R$" #,##0.00', 42) == "R$"
    assert _currency_symbol("[$A$-en-AU]#,##0.00", 42) == "A$"
    assert _currency_symbol("[$USD-409]#,##0.00", 42) == "USD"
    assert _currency_symbol('#,##0.00 "CHF"', 42) == "CHF"
    assert _currency_symbol('$0" net"', 5) == "$"

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["BR", "CH"])
    sheet.append([42, 42])
    sheet["A2"].number_format = '"R$" #,##0.00'
    sheet["B2"].number_format = '#,##0.00 "CHF"'
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    markdown = _convert(stream.getvalue())
    assert "R$42" in markdown
    assert "42CHF" in markdown


def test_conditional_sections_select_by_condition() -> None:
    from markitdown.converters._xlsx_converter import (
        _currency_symbol,
        _select_format_section,
    )

    fmt = '[>=100]"$"0;"€"0'
    assert _select_format_section(fmt, 50) == '"€"0'
    assert _select_format_section(fmt, 150) == '[>=100]"$"0'
    assert _currency_symbol(fmt, 50) == "€"
    assert _currency_symbol(fmt, 150) == "$"
    assert _currency_symbol('[>=100]"$"0;0', 50) is None

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Amount"])
    sheet.append([50])
    sheet.append([150])
    sheet["A2"].number_format = fmt
    sheet["A3"].number_format = fmt
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    markdown = _convert(stream.getvalue())
    assert "€50" in markdown
    assert "$150" in markdown


def test_placement_ignores_bracketed_metadata() -> None:
    from markitdown.converters._xlsx_converter import (
        _is_currency_position_prefix,
    )

    assert _is_currency_position_prefix('[Color10]"$"#,##0', 150) is True
    assert _is_currency_position_prefix('[$-409]#,##0.00"€"', 42) is False
    assert _is_currency_position_prefix('$0" net"', 5) is True
    assert _is_currency_position_prefix("#,##0.00 [$€-x-euro2]", 42) is False


def test_quoted_literal_digit_is_not_placeholder() -> None:
    from markitdown.converters._xlsx_converter import (
        _currency_symbol,
        _is_currency_position_prefix,
    )

    fmt = '"0 $"0'
    assert _currency_symbol(fmt, 5) == "0 $"
    assert _is_currency_position_prefix(fmt, 5) is True

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Price"])
    sheet.append([5])
    sheet["A2"].number_format = fmt
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    markdown = _convert(stream.getvalue())
    assert "0 $5" in markdown
    assert "50 $" not in markdown


def test_escaped_literal_digit_is_not_placeholder() -> None:
    from markitdown.converters._xlsx_converter import (
        _is_currency_position_prefix,
    )

    fmt = r'\0"$"0'
    assert _is_currency_position_prefix(fmt, 5) is True

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Price"])
    sheet.append([5])
    sheet["A2"].number_format = fmt
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    markdown = _convert(stream.getvalue())
    assert "$5" in markdown
    assert "5$" not in markdown


def test_stale_dimension_still_labels_trailing_rows() -> None:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Price"])
    sheet.append([10])
    sheet.append([20])
    sheet["A2"].number_format = '"$"#,##0'
    sheet["A3"].number_format = '"$"#,##0'
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()

    # Simulate a producer with a stale declared dimension covering only the
    # first data row while actual data runs through row 3.
    source = zipfile.ZipFile(io.BytesIO(stream.getvalue()))
    patched = io.BytesIO()
    with zipfile.ZipFile(patched, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == "xl/worksheets/sheet1.xml":
                data = _DIMENSION_REF_RE.sub(rb"\1A1:A2\2", data)
            target.writestr(item, data)
    source.close()

    markdown = _convert(patched.getvalue())
    assert "$10" in markdown
    assert "$20" in markdown
