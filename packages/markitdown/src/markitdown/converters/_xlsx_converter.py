import re
import sys
from typing import BinaryIO, Any
from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

# Common currency symbols found in Excel number formats
_CURRENCY_SYMBOLS = ["$", "€", "£", "¥", "₹", "₩", "₽", "₺", "₫", "₱", "฿", "₡", "₦", "₴"]

# Regex to detect accounting-style currency formats like '_($* #,##0.00_)'
_ACCOUNTING_FORMAT_RE = re.compile(r"_\(\s*\*?\s*(.)")

# Regex to extract the decimal precision from a number format string
# Matches patterns like #,##0.00 -> 2 decimal places, #,##0 -> 0 decimals
_DECIMAL_PRECISION_RE = re.compile(r"\.(\#*0+)")


def _get_decimal_precision(number_format: str) -> int:
    """Return the number of decimal places implied by an Excel number format.

    ``$#,##0.00`` → 2,  ``€#,##0`` → 0,  ``#,##0.000`` → 3
    """
    m = _DECIMAL_PRECISION_RE.search(number_format)
    if m:
        return len(m.group(1))  # count the '0' and '#' chars after '.'
    return 0

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import pandas as pd
    import openpyxl  # noqa: F401
except ImportError:
    _xlsx_dependency_exc_info = sys.exc_info()

_xls_dependency_exc_info = None
try:
    import pandas as pd  # noqa: F811
    import xlrd  # noqa: F401
except ImportError:
    _xls_dependency_exc_info = sys.exc_info()

ACCEPTED_XLSX_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
]
ACCEPTED_XLSX_FILE_EXTENSIONS = [".xlsx"]

ACCEPTED_XLS_MIME_TYPE_PREFIXES = [
    "application/vnd.ms-excel",
    "application/excel",
]
ACCEPTED_XLS_FILE_EXTENSIONS = [".xls"]


def _extract_currency_symbol(number_format: str) -> str | None:
    """Extract a currency symbol from an Excel number format string.

    Handles standard formats like ``$#,##0.00`` and accounting formats
    like ``_($* #,##0.00_)``.  Returns the symbol character when found,
    otherwise ``None``.
    """
    if not number_format:
        return None

    # Check for a literal currency symbol anywhere in the format
    for sym in _CURRENCY_SYMBOLS:
        if sym in number_format:
            return sym

    # Check accounting-style: first char after '_(' or '_(* '
    m = _ACCOUNTING_FORMAT_RE.search(number_format)
    if m:
        candidate = m.group(1)
        if candidate in _CURRENCY_SYMBOLS:
            return candidate

    return None


def _format_currency_value(value: int | float, symbol: str, precision: int) -> str:
    """Format a numeric value as a currency string.

    Handles negative values with ``-$`` prefix.  Uses thousands separators
    and the specified number of decimal places.
    """
    if value < 0:
        return f"-${abs(value):,.{precision}f}"
    return f"{symbol}{value:,.{precision}f}"


def _apply_currency_formats(file_stream: BinaryIO, sheets: dict) -> dict:
    """Return *sheets* with currency-formatted cells replaced by display strings.

    Uses openpyxl to inspect each cell's ``number_format``.  When a numeric
    cell carries a currency format, its value in the DataFrame is replaced
    with a formatted string (e.g. ``$1,199.00``) so that the currency symbol
    is preserved in the Markdown output (fixes microsoft/markitdown#53).
    """
    import openpyxl

    # Reset stream so openpyxl can read from the beginning
    file_stream.seek(0)
    wb = openpyxl.load_workbook(file_stream, data_only=True, read_only=True)

    for sheet_name, df in sheets.items():
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        # Convert all columns to object so we can store formatted strings
        for col_name in df.columns:
            df[col_name] = df[col_name].astype(object)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row,
                                max_col=ws.max_column):
            for cell in row:
                cell_fmt = getattr(cell, "number_format", None) or ""
                currency = _extract_currency_symbol(cell_fmt)
                if currency is None:
                    continue
                value = cell.value
                if value is None or not isinstance(value, (int, float)):
                    continue
                # Convert 1-based openpyxl coords to 0-based pandas iloc positions
                cell_row = cell.row
                cell_col = cell.column
                if cell_row is None or cell_col is None:
                    continue
                df_row = cell_row - 1 - (1 if df.columns.name is None else 0)
                df_col = cell_col - 1
                if 0 <= df_row < len(df) and 0 <= df_col < len(df.columns):
                    precision = _get_decimal_precision(cell_fmt)
                    df.iat[df_row, df_col] = _format_currency_value(
                        value, currency, precision
                    )

    wb.close()
    return sheets


class XlsxConverter(DocumentConverter):
    """
    Converts XLSX files to Markdown, with each sheet presented as a separate Markdown table.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_XLSX_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_XLSX_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check the dependencies
        if _xlsx_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xlsx",
                    feature="xlsx",
                )
            ) from _xlsx_dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _xlsx_dependency_exc_info[2]
            )

        sheets = pd.read_excel(file_stream, sheet_name=None, engine="openpyxl")
        # Preserve currency/percentage formats that pandas strips (fixes #53)
        file_stream.seek(0)
        sheets = _apply_currency_formats(file_stream, sheets)

        md_content = ""
        for s in sheets:
            md_content += f"## {s}\n"
            html_content = sheets[s].to_html(index=False)
            md_content += (
                self._html_converter.convert_string(
                    html_content, **kwargs
                ).markdown.strip()
                + "\n\n"
            )

        return DocumentConverterResult(markdown=md_content.strip())


class XlsConverter(DocumentConverter):
    """
    Converts XLS files to Markdown, with each sheet presented as a separate Markdown table.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_XLS_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_XLS_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Load the dependencies
        if _xls_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xls",
                    feature="xls",
                )
            ) from _xls_dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _xls_dependency_exc_info[2]
            )

        sheets = pd.read_excel(file_stream, sheet_name=None, engine="xlrd")
        md_content = ""
        for s in sheets:
            md_content += f"## {s}\n"
            html_content = sheets[s].to_html(index=False)
            md_content += (
                self._html_converter.convert_string(
                    html_content, **kwargs
                ).markdown.strip()
                + "\n\n"
            )

        return DocumentConverterResult(markdown=md_content.strip())
