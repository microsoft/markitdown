import sys
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

# Source anchor emitted ahead of each sheet when source_anchors=True. Paired
# with the injected `xlsx-row` column, this gives every cell a stable
# (file, sheet, spreadsheet row) coordinate for downstream citation.
SHEET_ANCHOR_TEMPLATE = "<!-- Sheet name: {sheet} -->"

# Name of the injected 1-based spreadsheet row column.
ROW_ANCHOR_COLUMN = "xlsx-row"

# pandas.read_excel consumes row 1 as the header, so the first data row is 2.
_FIRST_DATA_ROW = 2


def _sheet_anchor(sheet_name: str) -> str:
    """Return the source anchor for a sheet."""
    return SHEET_ANCHOR_TEMPLATE.format(sheet=sheet_name)


def _with_row_anchors(frame: Any) -> Any:
    """Return a copy of `frame` with a leading 1-based spreadsheet row column."""
    frame = frame.copy()
    frame.insert(
        0, ROW_ANCHOR_COLUMN, range(_FIRST_DATA_ROW, len(frame) + _FIRST_DATA_ROW)
    )
    return frame


def _sheets_to_markdown(sheets: Any, html_converter: Any, kwargs: Any) -> str:
    """Render every sheet as a Markdown table, optionally with source anchors."""
    source_anchors = bool(kwargs.get("source_anchors", False))
    md_content = ""
    for s in sheets:
        if source_anchors:
            md_content += f"{_sheet_anchor(s)}\n"
        md_content += f"## {s}\n"
        frame = _with_row_anchors(sheets[s]) if source_anchors else sheets[s]
        html_content = frame.to_html(index=False)
        md_content += (
            html_converter.convert_string(html_content, **kwargs).markdown.strip()
            + "\n\n"
        )
    return md_content.strip()


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
        return DocumentConverterResult(
            markdown=_sheets_to_markdown(sheets, self._html_converter, kwargs)
        )


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
        return DocumentConverterResult(
            markdown=_sheets_to_markdown(sheets, self._html_converter, kwargs)
        )
