import io
import re
import sys
from typing import BinaryIO, Any, Dict, List, Optional, Tuple

from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import openpyxl
except ImportError:
    _xlsx_dependency_exc_info = sys.exc_info()

_xls_dependency_exc_info = None
try:
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

_CURRENCY_PREFIXES = re.compile(r"^[\$€£¥₩₽₹₨฿₫₪₴₸₺₼₾]")


def _has_currency_format(number_format: Optional[str]) -> Optional[str]:
    """Check if number format indicates currency and return the currency symbol if so."""
    if not number_format or number_format == "General":
        return None
    match = _CURRENCY_PREFIXES.match(number_format)
    if match:
        return match.group(0)
    return None


def _build_currency_map(ws: Any) -> Dict[Tuple[int, int], str]:
    """Build {(row_idx, col_idx): symbol} for currency-formatted cells."""
    currency_map: Dict[Tuple[int, int], str] = {}
    for row in ws.iter_rows():
        for cell in row:
            symbol = _has_currency_format(cell.number_format)
            if symbol:
                currency_map[(cell.row - 1, cell.column - 1)] = symbol
    return currency_map


def _markdown_table_from_worksheet(ws: Any, currency_map: Dict[Tuple[int, int], str]) -> str:
    """Convert an openpyxl worksheet to a Markdown table with currency symbols."""
    rows: List[List[str]] = []
    for row_idx, row in enumerate(ws.iter_rows()):
        cells: List[str] = []
        for col_idx, cell in enumerate(row):
            if cell.value is None:
                cells.append("")
            elif (row_idx, col_idx) in currency_map:
                symbol = currency_map[(row_idx, col_idx)]
                v = cell.value
                if isinstance(v, float) and v == int(v):
                    v = int(v)
                cells.append(f"{symbol}{v}")
            else:
                cells.append(str(cell.value))
        rows.append(cells)
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join(["---"] * len(rows[0])) + " |"
    body_lines = ["| " + " | ".join(r) + " |" for r in rows[1:]]
    body = "\n".join(body_lines)
    return header + "\n" + sep + ("\n" + body if body else "")


class XlsxConverter(DocumentConverter):
    """
    Converts XLSX files to Markdown, with each sheet presented as a separate Markdown table.
    """

    def __init__(self):
        super().__init__()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _xlsx_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xlsx",
                    feature="xlsx",
                )
            ) from _xlsx_dependency_exc_info[
                1
            ].with_traceback(
                _xlsx_dependency_exc_info[2]
            )

        file_stream.seek(0)
        wb = openpyxl.load_workbook(file_stream, data_only=True)
        md_content = ""
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            currency_map = _build_currency_map(ws)
            md_content += f"## {sheet_name}\n"
            md_content += _markdown_table_from_worksheet(ws, currency_map) + "\n\n"
        wb.close()
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
        **kwargs: Any,
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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _xls_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xls",
                    feature="xls",
                )
            ) from _xls_dependency_exc_info[
                1
            ].with_traceback(
                _xls_dependency_exc_info[2]
            )

        import pandas as pd
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
