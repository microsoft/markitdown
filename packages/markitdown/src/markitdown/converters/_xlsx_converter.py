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

        excel_file = pd.ExcelFile(file_stream, engine="openpyxl")
        sheet_names = excel_file.sheet_names

        # Handle --list-sheets
        if kwargs.get("list_sheets"):
            print("Available sheets:")
            for i, sheet in enumerate(sheet_names):
                print(f"  {i+1}. {sheet}")
            return DocumentConverterResult(markdown="")
            
        # Handle --interactive
        sheet_selection = kwargs.get("sheet_selection") or []
        if kwargs.get("interactive"):
            print("Available sheets:")
            for i, sheet in enumerate(sheet_names):
                print(f"  {i+1}. {sheet}")
            
            selection = input("Enter the numbers or names of the sheets to convert (comma-separated), or press Enter for all: ")
            if selection.strip():
                sheet_selection = []
                for s in selection.split(","):
                    s = s.strip()
                    if s.isdigit():
                        idx = int(s) - 1
                        if 0 <= idx < len(sheet_names):
                            sheet_selection.append(sheet_names[idx])
                        else:
                            raise ValueError(f"Invalid sheet number: {s}")
                    else:
                        if s in sheet_names:
                            sheet_selection.append(s)
                        else:
                            raise ValueError(f"Invalid sheet name: {s}")

        # Ensure sheet_selection contains valid sheets
        sheets_to_read = sheet_selection if sheet_selection else sheet_names
        for s in sheets_to_read:
            if s not in sheet_names:
                raise ValueError(f"Sheet not found: {s}")

        sheets = pd.read_excel(excel_file, sheet_name=sheets_to_read)
        if not isinstance(sheets, dict):
            # Fallback if pandas returns a single DataFrame
            sheets = {sheets_to_read[0]: sheets}

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

        excel_file = pd.ExcelFile(file_stream, engine="xlrd")
        sheet_names = excel_file.sheet_names

        # Handle --list-sheets
        if kwargs.get("list_sheets"):
            print("Available sheets:")
            for i, sheet in enumerate(sheet_names):
                print(f"  {i+1}. {sheet}")
            return DocumentConverterResult(markdown="")
            
        # Handle --interactive
        sheet_selection = kwargs.get("sheet_selection") or []
        if kwargs.get("interactive"):
            print("Available sheets:")
            for i, sheet in enumerate(sheet_names):
                print(f"  {i+1}. {sheet}")
            
            selection = input("Enter the numbers or names of the sheets to convert (comma-separated), or press Enter for all: ")
            if selection.strip():
                sheet_selection = []
                for s in selection.split(","):
                    s = s.strip()
                    if s.isdigit():
                        idx = int(s) - 1
                        if 0 <= idx < len(sheet_names):
                            sheet_selection.append(sheet_names[idx])
                        else:
                            raise ValueError(f"Invalid sheet number: {s}")
                    else:
                        if s in sheet_names:
                            sheet_selection.append(s)
                        else:
                            raise ValueError(f"Invalid sheet name: {s}")

        # Ensure sheet_selection contains valid sheets
        sheets_to_read = sheet_selection if sheet_selection else sheet_names
        for s in sheets_to_read:
            if s not in sheet_names:
                raise ValueError(f"Sheet not found: {s}")

        sheets = pd.read_excel(excel_file, sheet_name=sheets_to_read)
        if not isinstance(sheets, dict):
            # Fallback if pandas returns a single DataFrame
            sheets = {sheets_to_read[0]: sheets}

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
