import locale
from typing import BinaryIO, Any
from striprtf.striprtf import rtf_to_text

from markitdown import (
    MarkItDown,
    DocumentConverter,
    DocumentConverterResult,
    StreamInfo,
)


__plugin_interface_version__ = (
    1  # The version of the plugin interface that this plugin uses
)

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/rtf",
    "application/rtf",
]

ACCEPTED_FILE_EXTENSIONS = [".rtf"]


def register_converters(markitdown: MarkItDown, **kwargs):
    """
    Called during construction of MarkItDown instances to register converters provided by plugins.
    """

    # Simply create and attach an RtfConverter instance
    markitdown.register_converter(RtfConverter())


class RtfConverter(DocumentConverter):
    """
    Converts an RTF file to in the simplest possible way.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Read the file stream into an str using hte provided charset encoding, or using the system default
        encoding = stream_info.charset or locale.getpreferredencoding()
        stream_data = file_stream.read().decode(encoding)

        # Return the result
        return DocumentConverterResult(
            title=None,
            markdown=rtf_to_text(stream_data),
        )
