import sys
from typing import BinaryIO, Any
from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import pandas as pd
except ImportError:
    _dependency_exc_info = sys.exc_info()


ACCEPTED_CSV_MIME_TYPE_PREFIXES = [
    "text/csv",
    "application/csv"
]
ACCEPTED_CSV_FILE_EXTENSIONS = [".csv"]

class CsvConverter(DocumentConverter):
    """
    Converts CSV files to Markdown.
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

        if extension in ACCEPTED_CSV_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_CSV_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ):
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".csv",
                    feature="csv",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        content = pd.read_csv(file_stream, encoding=encoding)
        md_content = self._html_converter.convert_string(
            content.to_html(index=False), **kwargs
        ).markdown.strip()
        return DocumentConverterResult(markdown=md_content)
