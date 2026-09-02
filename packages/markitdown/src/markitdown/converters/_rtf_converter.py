import sys

from typing import BinaryIO, Any

from charset_normalizer import from_bytes

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    from striprtf.striprtf import rtf_to_text
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/rtf",
    "application/x-rtf",
    "text/rtf",
    "text/richtext",
]

ACCEPTED_FILE_EXTENSIONS = [".rtf"]


class RtfConverter(DocumentConverter):
    """
    Converts RTF (Rich Text Format) files to Markdown. RTF formatting control
    words are stripped and the underlying text content is preserved.
    """

    def __init__(self):
        super().__init__()

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
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".rtf",
                    feature="rtf",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        # RTF is an ASCII-based format, but may declare a code page for any
        # non-ASCII bytes. Decode defensively so we always hand a str to
        # striprtf, which performs the actual control-word stripping.
        if stream_info.charset:
            rtf_content = file_stream.read().decode(stream_info.charset)
        else:
            rtf_content = str(from_bytes(file_stream.read()).best())

        text = rtf_to_text(rtf_content)

        return DocumentConverterResult(markdown=text.strip())
