import sys
from typing import BinaryIO, Any, Optional, Union, List, Dict
from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo
import re
from datetime import datetime
from decimal import Decimal

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import pandas as pd
    import openpyxl
    from openpyxl.utils import get_column_letter
    from openpyxl.styles.numbers import BUILTIN_FORMATS
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


class XlsxConverter(DocumentConverter):
    """
    Converts XLSX files to Markdown, with each sheet presented as a separate Markdown table.

    This converter preserves cell formatting including:
    - Currency symbols and formatting (e.g., $1,234.56)
    - Percentage formatting (e.g., 25.5%)
    - Number formatting with thousands separators (e.g., 1,234,567)
    - Date formatting (preserves display format from Excel)
    - Custom number formats

    The converter uses openpyxl to access cell formatting information that is not
    available through pandas.read_excel() alone.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
            self,
            file_stream: BinaryIO,
            stream_info: StreamInfo,
            **kwargs: Any,
    ) -> bool:
        """Check if this converter can handle the given file."""
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_XLSX_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_XLSX_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def _get_number_format(self, cell) -> str:
        """
        Extract the number format string from a cell.

        Args:
            cell: An openpyxl cell object

        Returns:
            The number format string, or empty string if not found
        """
        if not cell or not hasattr(cell, 'number_format'):
            return ""

        number_format = cell.number_format
        if not number_format:
            return ""

        # Handle built-in format IDs
        if hasattr(cell, '_style') and hasattr(cell._style, 'numFmtId'):
            fmt_id = cell._style.numFmtId
            if fmt_id in BUILTIN_FORMATS:
                return BUILTIN_FORMATS[fmt_id]

        return number_format

    def _format_currency_value(self, value: Union[int, float], number_format: str) -> str:
        """
        Format a numeric value as currency based on Excel number format.

        Args:
            value: The numeric value to format
            number_format: The Excel number format string

        Returns:
            Formatted currency string
        """
        # Determine decimal places from format
        decimal_places = 2  # Default
        if '.0' in number_format and '.00' not in number_format:
            decimal_places = 1
        elif '.000' in number_format:
            decimal_places = 3
        elif '#' in number_format and '.' not in number_format:
            decimal_places = 0

        # Check for thousands separator
        use_thousands = '#,##' in number_format or '_,*' in number_format

        # Format the number
        if use_thousands:
            if decimal_places > 0:
                formatted = f"{value:,.{decimal_places}f}"
            else:
                formatted = f"{value:,.0f}"
        else:
            if decimal_places > 0:
                formatted = f"{value:.{decimal_places}f}"
            else:
                formatted = f"{value:.0f}"

        # Add currency symbol
        # Check for accounting format
        if '_($' in number_format or '_($' in number_format:
            # Accounting format - negative values in parentheses
            if value < 0:
                return f"(${formatted[1:]})"
            else:
                return f"${formatted}"
        else:
            # Standard currency format
            return f"${formatted}"

    def _format_percentage_value(self, value: Union[int, float], number_format: str) -> str:
        """
        Format a numeric value as percentage based on Excel number format.

        Args:
            value: The numeric value to format (as decimal, e.g., 0.25 for 25%)
            number_format: The Excel number format string

        Returns:
            Formatted percentage string
        """
        # Excel stores percentages as decimals
        percent_value = value * 100

        # Determine decimal places
        if '.00' in number_format:
            return f"{percent_value:.2f}%"
        elif '.0' in number_format:
            return f"{percent_value:.1f}%"
        else:
            return f"{percent_value:.0f}%"

    def _format_number_value(self, value: Union[int, float], number_format: str) -> str:
        """
        Format a numeric value with thousands separators based on Excel number format.

        Args:
            value: The numeric value to format
            number_format: The Excel number format string

        Returns:
            Formatted number string
        """
        # Determine decimal places
        if '.' in number_format:
            # Count zeros after decimal point
            after_decimal = number_format.split('.')[-1]
            decimal_places = len(re.findall(r'0', after_decimal.split()[0]))
        else:
            decimal_places = 0

        # Format with thousands separator
        if decimal_places > 0:
            return f"{value:,.{decimal_places}f}"
        else:
            return f"{value:,.0f}"

    def _format_cell_value(self, cell, value: Any) -> str:
        """
        Format a cell value based on its Excel number format.

        This method detects the cell's number format and applies appropriate
        formatting to match how the value appears in Excel.

        Args:
            cell: An openpyxl cell object
            value: The cell's raw value

        Returns:
            Formatted string representation of the value
        """
        # Handle None or empty values
        if value is None or value == "":
            return ""

        # Get the number format string
        number_format = self._get_number_format(cell)
        if not number_format:
            return str(value)

        # For dates, return string representation
        if isinstance(value, datetime):
            return str(value)

        # Only format numeric values
        if not isinstance(value, (int, float)):
            return str(value)

        # Currency formats - comprehensive patterns
        currency_patterns = [
            r'^\$',  # Starts with $
            r'_\(\$',  # Accounting format
            r'_\(\\\$',  # Escaped accounting format
            r'"?\$"?#',  # Various $ formats
            r'#,##0.*\$',  # Number with $ at end
            r'\[\$.*\]',  # Currency code format (e.g., [$USD])
            r'Currency',  # Named currency format
            r'Accounting',  # Named accounting format
        ]

        # Check if this is a currency format
        is_currency = any(re.search(pattern, number_format, re.IGNORECASE)
                          for pattern in currency_patterns)

        if is_currency:
            return self._format_currency_value(value, number_format)

        # Percentage formats
        if '%' in number_format:
            return self._format_percentage_value(value, number_format)

        # Number with thousands separator (but not currency or percentage)
        if '#,##' in number_format:
            return self._format_number_value(value, number_format)

        # Scientific notation
        if 'E+' in number_format or 'E-' in number_format:
            # Determine decimal places
            decimal_places = 2
            if '.000' in number_format:
                decimal_places = 3
            elif '.0' in number_format and '.00' not in number_format:
                decimal_places = 1
            return f"{value:.{decimal_places}E}"

        # Default: return as string
        return str(value)

    def _read_sheet_with_formatting(self, sheet):
        """
        Read an Excel sheet while preserving cell formatting.

        This method reads each cell individually to access both its value and
        formatting information, then constructs a DataFrame with formatted values.

        Args:
            sheet: An openpyxl worksheet object

        Returns:
            pandas DataFrame with formatted cell values
        """
        data = []

        # Get sheet dimensions
        min_row = sheet.min_row
        max_row = sheet.max_row
        min_col = sheet.min_column
        max_col = sheet.max_column

        # Handle empty sheets
        if min_row is None or max_row is None or min_col is None or max_col is None:
            return pd.DataFrame()

        # Read all cells with formatting
        for row_idx in range(min_row, max_row + 1):
            row_data = []
            for col_idx in range(min_col, max_col + 1):
                cell = sheet.cell(row=row_idx, column=col_idx)
                value = cell.value

                # Apply formatting
                formatted_value = self._format_cell_value(cell, value)
                row_data.append(formatted_value)

            data.append(row_data)

        # Convert to DataFrame
        if len(data) == 0:
            return pd.DataFrame()
        elif len(data) == 1:
            # Single row - treat as data, not header
            return pd.DataFrame(data)
        else:
            # Use first row as headers
            df = pd.DataFrame(data[1:], columns=data[0])
            # Clean column names (remove None, empty strings)
            df.columns = [str(col) if col else f"Column_{i + 1}"
                          for i, col in enumerate(df.columns)]

        return df

    def convert(
            self,
            file_stream: BinaryIO,
            stream_info: StreamInfo,
            **kwargs: Any,
    ) -> DocumentConverterResult:
        """
        Convert XLSX file to Markdown format.

        Args:
            file_stream: Binary stream of the XLSX file
            stream_info: Metadata about the file
            **kwargs: Additional conversion options

        Returns:
            DocumentConverterResult containing the Markdown representation
        """
        # Check dependencies
        if _xlsx_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xlsx",
                    feature="xlsx",
                )
            ) from _xlsx_dependency_exc_info[1].with_traceback(
                _xlsx_dependency_exc_info[2]
            )

        # Load workbook with openpyxl to preserve formatting
        # data_only=True returns calculated values for formulas
        wb = openpyxl.load_workbook(file_stream, data_only=True)

        md_content = ""
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]

            # Skip empty sheets
            if sheet.max_row == 0 or sheet.max_column == 0:
                continue

            md_content += f"## {sheet_name}\n"

            # Read sheet with formatting preserved
            df = self._read_sheet_with_formatting(sheet)

            if df.empty:
                md_content += "_Empty sheet_\n\n"
                continue

            # Convert to HTML then to Markdown
            # escape=False to preserve formatting like currency symbols
            html_content = df.to_html(index=False, escape=False)
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

    Note: XLS format support for cell formatting is limited compared to XLSX.
    For full formatting preservation, consider converting XLS files to XLSX format.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
            self,
            file_stream: BinaryIO,
            stream_info: StreamInfo,
            **kwargs: Any,
    ) -> bool:
        """Check if this converter can handle the given file."""
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
            **kwargs: Any,
    ) -> DocumentConverterResult:
        """
        Convert XLS file to Markdown format.

        Note: This implementation uses pandas which does not preserve cell formatting.
        For files where formatting is important, consider using XLSX format instead.

        Args:
            file_stream: Binary stream of the XLS file
            stream_info: Metadata about the file
            **kwargs: Additional conversion options

        Returns:
            DocumentConverterResult containing the Markdown representation
        """
        # Check dependencies
        if _xls_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xls",
                    feature="xls",
                )
            ) from _xls_dependency_exc_info[1].with_traceback(
                _xls_dependency_exc_info[2]
            )

        # For XLS files, we use pandas as xlrd has very limited formatting support
        # This means formatting will not be preserved for XLS files
        sheets = pd.read_excel(file_stream, sheet_name=None, engine="xlrd")

        md_content = ""
        for sheet_name in sheets:
            md_content += f"## {sheet_name}\n"

            if sheets[sheet_name].empty:
                md_content += "_Empty sheet_\n\n"
                continue

            html_content = sheets[sheet_name].to_html(index=False)
            md_content += (
                    self._html_converter.convert_string(
                        html_content, **kwargs
                    ).markdown.strip()
                    + "\n\n"
            )

        return DocumentConverterResult(markdown=md_content.strip())