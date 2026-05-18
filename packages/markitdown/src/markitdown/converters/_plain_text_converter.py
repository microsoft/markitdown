import sys
import logging

from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import FileConversionException

logger = logging.getLogger(__name__)

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth  # noqa: F401
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/",
    "application/json",
    "application/markdown",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".txt",
    ".text",
    ".md",
    ".markdown",
    ".json",
    ".jsonl",
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

        # If we have a charset, we can safely assume it's text
        # With Magika in the earlier stages, this handles most cases
        if stream_info.charset is not None:
            return True

        # Otherwise, check the mimetype and extension
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
        raw_bytes = file_stream.read()
        if not raw_bytes:
            return DocumentConverterResult(markdown="")

        try:
            if stream_info.charset:
                text_content = raw_bytes.decode(stream_info.charset)
            else:
                text_content = str(from_bytes(raw_bytes).best())
        except (UnicodeDecodeError, LookupError) as e:
            logger.warning("PlainText encoding detection failed: %s", e)
            raise FileConversionException(
                f"PlainTextConverter: unable to decode content with charset={stream_info.charset}: {e}"
            ) from e

        return DocumentConverterResult(markdown=text_content)
