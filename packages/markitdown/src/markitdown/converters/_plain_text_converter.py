import sys

from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/",
    "application/json",
]

# Mimetypes to ignore (commonly confused extensions)
IGNORE_MIME_TYPE_PREFIXES = [
    "text/vnd.in3d.spot",  # .spo wich is confused with xls, doc, etc.
    "text/vnd.graphviz",  # .dot which is confused with xls, doc, etc.
]


class PlainTextConverter(DocumentConverter):
    """Anything with content type text/plain"""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        for prefix in IGNORE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return False

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
        if stream_info.charset:
            text_content = file_stream.read().decode(stream_info.charset)
        else:
            text_content = str(from_bytes(file_stream.read()).best())

        return DocumentConverterResult(markdown=text_content)
