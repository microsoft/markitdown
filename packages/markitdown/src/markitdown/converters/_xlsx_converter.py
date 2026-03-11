import re
import sys
from io import BytesIO
from typing import Any, BinaryIO

from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import pandas as pd
    import openpyxl
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

# Pattern to match currency formats (e.g., "$"#,##0.00, €#,##0.00, £$#,##0.00)
CURRENCY_FORMAT_PATTERN = re.compile(r'["\']([$€£¥₹])["\']|([$€£¥₹])\d|#|0')


def _format_cell_value(cell: "openpyxl.cell.Cell") -> str:
    """
    Format a cell value, preserving currency and other number formats.
    """
    if cell.value is None:
        return ""

    # Check if it's a number type
    if isinstance(cell.value, (int, float)):
        number_format = cell.number_format

        # Check if the number format contains currency symbols
        # Common currency formats: "$"#,##0.00, €#,##0.00, $#,##0.00
        if "$" in number_format or "€" in number_format or "£" in number_format or "¥" in number_format or "₹" in number_format:
            # Try to use openpyxl's built-in formatting
            try:
                formatted = openpyxl.styles.numbers.format(cell.value, number_format)
                # Clean up the formatted value (remove extra spaces, fix formatting)
                formatted = formatted.strip()
                if formatted and formatted != str(cell.value):
                    return formatted
            except Exception:
                pass

            # Fallback: extract currency symbol from format string
            currency_match = re.search(r'["\']([$€£¥₹])["\']|([$€£¥₹])(?=\d|#)', number_format)
            if currency_match:
                currency_symbol = currency_match.group(1) or currency_match.group(2)
                # Format with currency symbol
                if isinstance(cell.value, float):
                    return f"{currency_symbol}{cell.value:,.2f}"
                else:
                    return f"{currency_symbol}{cell.value:,}"

        # Handle percentage format
        if "%" in number_format and isinstance(cell.value, (int, float)):
            return f"{cell.value * 100:.2f}%"

        # Handle decimal places from format
        if "#" in number_format or "0" in number_format:
            # Try to preserve decimal places
            decimal_match = re.search(r'\.(0+|#+)', number_format)
            if decimal_match:
                decimal_places = len(decimal_match.group(1))
                if isinstance(cell.value, float):
                    return f"{cell.value:,.{decimal_places}f}"

        # Default number formatting with thousand separators
        if isinstance(cell.value, float):
            return f"{cell.value:,.2f}"
        elif isinstance(cell.value, int):
            return f"{cell.value:,}"

    return str(cell.value)


def _convert_sheet_to_markdown(ws: "openpyxl.worksheet.worksheet.Worksheet") -> str:
    """
    Convert an openpyxl worksheet to a Markdown table, preserving number formats.
    """
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return ""

    # Get the max column count
    max_cols = max(len(row) for row in rows)

    # Build markdown table
    lines = []

    # Header row
    header = [str(cell) if cell is not None else "" for cell in rows[0]]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")

    # Data rows - need to use openpyxl cells to get formatting
    for row_idx in range(1, len(rows)):
        row = rows[row_idx]
        # Pad row if needed
        row = list(row) + [""] * (max_cols - len(row))

        # Get cell objects for formatting
        cells = list(ws[row_idx + 1])[:max_cols]  # +1 because openpyxl is 1-indexed

        formatted_cells = []
        for i, cell in enumerate(cells):
            if cell.value is not None:
                # Check if we need to use cell object for formatting
                if isinstance(cell.value, (int, float)):
                    formatted_cells.append(_format_cell_value(cell))
                else:
                    formatted_cells.append(str(cell.value))
            else:
                formatted_cells.append("")

        lines.append("| " + " | ".join(formatted_cells) + " |")

    return "\n".join(lines)


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

        # Read the Excel file using openpyxl to preserve number formats
        file_stream.seek(0)
        wb = openpyxl.load_workbook(file_stream, data_only=True)

        md_content = ""
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            md_content += f"## {sheet_name}\n"
            md_content += _convert_sheet_to_markdown(ws) + "\n\n"

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
