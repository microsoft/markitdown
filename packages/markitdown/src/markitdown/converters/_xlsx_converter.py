"""XLSX/XLS converter — converts Excel spreadsheets to Markdown tables via HTML intermediary."""

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


def _clean_sheet(df):
    """Strip fully-empty rows/columns and auto-generated `Unnamed: N` headers.

    Real-world spreadsheets routinely contain:
    - Trailing all-NaN rows (Excel "uses" cells the user never touched).
    - Sparse 'note' columns that are 99% empty.
    - Header rows that pandas read as `Unnamed: 0/1/...` because the real
      header lives a few rows down.

    Serializing all of this verbatim produces megabytes of noise (e.g. the
    real-world fixture 威廉希尔赔率体系.xlsx produced 1.38M chars and 103 MiB
    peak before this cleanup). After cleanup it drops to a few KB.
    """
    if df is None or df.empty:
        return df
    # Drop completely empty rows and columns
    df = df.dropna(how="all").dropna(axis=1, how="all")
    # Rename Unnamed columns to empty string so they don't pollute headers
    rename_map = {c: "" for c in df.columns if str(c).startswith("Unnamed:")}
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


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
        return self._accepted_by_mime_or_ext(
            stream_info, ACCEPTED_XLSX_MIME_TYPE_PREFIXES, ACCEPTED_XLSX_FILE_EXTENSIONS
        )

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
        md_content = ""
        for s in sheets:
            cleaned = _clean_sheet(sheets[s])
            if cleaned is None or cleaned.empty:
                continue
            md_content += f"## {s}\n"
            html_content = cleaned.to_html(index=False)
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
        return self._accepted_by_mime_or_ext(
            stream_info, ACCEPTED_XLS_MIME_TYPE_PREFIXES, ACCEPTED_XLS_FILE_EXTENSIONS
        )

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
            cleaned = _clean_sheet(sheets[s])
            if cleaned is None or cleaned.empty:
                continue
            md_content += f"## {s}\n"
            html_content = cleaned.to_html(index=False)
            md_content += (
                self._html_converter.convert_string(
                    html_content, **kwargs
                ).markdown.strip()
                + "\n\n"
            )

        return DocumentConverterResult(markdown=md_content.strip())
