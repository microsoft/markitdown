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
    import openpyxl
except ImportError:
    _xlsx_dependency_exc_info = sys.exc_info()

_xls_dependency_exc_info = None
try:
    import pandas as pd
    import xlrd
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


class ExcelConverterBase(DocumentConverter):
    """Base class for Excel-like converters"""

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def _clean_colname(self, colname: Any) -> Any:
        # Remove Pandas header placeholders
        if isinstance(colname, str) and colname.startswith("Unnamed:"):
            return None
        return colname

    def _convert_excel(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        engine: str,
        na_rep: Any = "",
        remove_header_placeholders: bool = True,
        drop_empty_cols: bool = False,
        drop_empty_rows: bool = False,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        sheets = pd.read_excel(file_stream, sheet_name=None, engine=engine)
        md_content = ""
        for name, sheet in sheets.items():
            md_content += f"## {name}\n"

            if remove_header_placeholders:
                sheet = sheet.rename(columns=lambda col: self._clean_colname(col))

            if drop_empty_cols:
                # Also consider headers to be part of the column
                sheet = sheet.loc[:, sheet.notna().any() | sheet.columns.notna()]

            if drop_empty_rows:
                sheet = sheet.dropna(axis=0, how="all")

            # Coerce any cell that evaluates to `pd.isna(c) == True` to `na_rep`
            # More reliable than using `.to_html(na_rep=...)`: https://github.com/pandas-dev/pandas/issues/11953
            # Because the latter does not replace NaT's
            with pd.option_context("future.no_silent_downcasting", True):
                sheet = sheet.fillna(na_rep, axis=1).infer_objects(copy=False)
                sheet.columns = sheet.columns.fillna(na_rep).infer_objects(copy=False)

            html_content = sheet.to_html(index=False)
            md_content += (
                self._html_converter.convert_string(
                    html_content, **kwargs
                ).markdown.strip()
                + "\n\n"
            )

        return DocumentConverterResult(markdown=md_content.strip())


class XlsxConverter(ExcelConverterBase):
    """
    Converts XLSX files to Markdown, with each sheet presented as a separate Markdown table.
    """

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
            ) from _xlsx_dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _xlsx_dependency_exc_info[2]
            )

        return self._convert_excel(
            file_stream=file_stream,
            stream_info=stream_info,
            engine="openpyxl",
            **kwargs,
        )


class XlsConverter(ExcelConverterBase):
    """
    Converts XLS files to Markdown, with each sheet presented as a separate Markdown table.
    """

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
            ) from _xls_dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _xls_dependency_exc_info[2]
            )

        return self._convert_excel(
            file_stream=file_stream,
            stream_info=stream_info,
            engine="xlrd",
            **kwargs,
        )
