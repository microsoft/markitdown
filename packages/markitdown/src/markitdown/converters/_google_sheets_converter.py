import io
import re
import sys
from typing import Any, BinaryIO, Optional

import requests

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo
from ._xlsx_converter import XlsxConverter

_dependency_exc_info = None
try:
    import pandas as pd  # noqa: F401
    import openpyxl  # noqa: F401
except ImportError:
    _dependency_exc_info = sys.exc_info()


# Matches https://docs.google.com/spreadsheets/d/<ID>/... and captures the ID.
_SPREADSHEET_URL_RE = re.compile(
    r"^https?://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)"
)


class GoogleSheetsConverter(DocumentConverter):
    """
    Converts a public ("Anyone with the link") Google Sheets URL to Markdown
    by fetching the workbook via the XLSX export endpoint and rendering every
    tab as a separate ## SheetName section, matching XlsxConverter's output.
    """

    def __init__(self) -> None:
        super().__init__()
        self._xlsx_converter = XlsxConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        url = stream_info.url or ""
        return bool(_SPREADSHEET_URL_RE.match(url))

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xlsx",
                    feature="xlsx",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        spreadsheet_id = self._extract_spreadsheet_id(stream_info.url or "")
        export_url = (
            f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"
        )

        response = requests.get(export_url, allow_redirects=True, timeout=30)
        response.raise_for_status()

        xlsx_stream = io.BytesIO(response.content)
        xlsx_info = StreamInfo(
            mimetype=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            extension=".xlsx",
            url=stream_info.url,
        )
        # Strip kwargs we don't want to forward to the inner xlsx converter.
        inner_kwargs = {k: v for k, v in kwargs.items() if k != "_parent_converters"}
        return self._xlsx_converter.convert(xlsx_stream, xlsx_info, **inner_kwargs)

    @staticmethod
    def _extract_spreadsheet_id(url: str) -> Optional[str]:
        m = _SPREADSHEET_URL_RE.match(url)
        return m.group(1) if m else None
