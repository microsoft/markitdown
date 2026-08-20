import io
import sys
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Load dependencies
_dependency_exc_info = None
try:
    import pandas as pd
except ImportError:
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/csv",
    "application/csv",
]
ACCEPTED_FILE_EXTENSIONS = [".csv"]


class CsvConverter(DocumentConverter):
    """
    Converts CSV files to Markdown tables.
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
        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True
        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True
        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".csv",
                    feature="csv",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]
        # Read the file content
        if stream_info.charset:
            content = file_stream.read().decode(stream_info.charset)
        else:
            content = str(from_bytes(file_stream.read()).best())

        # Parse CSV content using pandas
        df = pd.read_csv(io.StringIO(content))

        if df.empty:
            return DocumentConverterResult(markdown="")

        html_content = df.to_html(index=False)
        md_content = self._html_converter.convert_string(
            html_content, **kwargs
        ).markdown.strip()

        return DocumentConverterResult(markdown=md_content.strip())
