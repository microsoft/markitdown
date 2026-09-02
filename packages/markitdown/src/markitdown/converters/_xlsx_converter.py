import sys
import re
from numbers import Real
from typing import BinaryIO, Any
from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import pandas as pd
    from openpyxl import load_workbook
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

_CURRENCY_FORMAT_PATTERN = re.compile(r"\[\$([^\]-]+)(?:-[0-9A-Fa-f]+)?\]")
_CURRENCY_SYMBOLS = (
    "$",
    "€",
    "£",
    "¥",
    "₹",
    "₩",
    "₽",
    "₺",
    "₪",
    "₫",
    "฿",
    "₦",
    "₱",
)


def _get_currency_symbol(number_format: str) -> str | None:
    match = _CURRENCY_FORMAT_PATTERN.search(number_format)
    if match is not None:
        symbol = match.group(1).replace("\\", "").strip()
        if symbol:
            return symbol

    for symbol in _CURRENCY_SYMBOLS:
        if symbol in number_format:
            return symbol

    return None


def _get_decimal_places(number_format: str) -> int:
    positive_format = number_format.split(";")[0]
    if "." not in positive_format:
        return 0

    decimal_part = positive_format.split(".", 1)[1]
    return len([character for character in decimal_part if character in ("0", "#")])


def _currency_is_suffix(number_format: str, currency_symbol: str) -> bool:
    positive_format = _CURRENCY_FORMAT_PATTERN.sub(
        currency_symbol, number_format.split(";")[0]
    )
    symbol_index = positive_format.find(currency_symbol)
    placeholder_indexes = [
        positive_format.find(character)
        for character in ("0", "#")
        if positive_format.find(character) >= 0
    ]

    if symbol_index < 0 or not placeholder_indexes:
        return False

    return symbol_index > min(placeholder_indexes)


def _format_currency_value(value: Any, number_format: str) -> str | None:
    currency_symbol = _get_currency_symbol(number_format)
    if (
        currency_symbol is None
        or not isinstance(value, Real)
        or isinstance(value, bool)
    ):
        return None

    decimal_places = _get_decimal_places(number_format)
    use_grouping = "," in number_format
    absolute_value = abs(value)
    number = (
        f"{absolute_value:,.{decimal_places}f}"
        if use_grouping
        else f"{absolute_value:.{decimal_places}f}"
    )
    sign = "-" if value < 0 else ""

    if _currency_is_suffix(number_format, currency_symbol):
        return f"{sign}{number} {currency_symbol}"

    return f"{sign}{currency_symbol}{number}"


def _apply_xlsx_number_formats(df: "pd.DataFrame", worksheet: Any) -> "pd.DataFrame":
    formatted_df = df.astype(object).copy()

    for row_index in range(len(formatted_df.index)):
        for column_index in range(len(formatted_df.columns)):
            cell = worksheet.cell(row=row_index + 2, column=column_index + 1)
            formatted_value = _format_currency_value(cell.value, cell.number_format)
            if formatted_value is not None:
                formatted_df.iat[row_index, column_index] = formatted_value

    return formatted_df


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
        file_stream.seek(0)
        workbook = load_workbook(file_stream, data_only=True, read_only=True)

        md_content = ""
        for s in sheets:
            md_content += f"## {s}\n"
            sheet = workbook[s]
            formatted_sheet = _apply_xlsx_number_formats(sheets[s], sheet)
            html_content = formatted_sheet.to_html(index=False)
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
