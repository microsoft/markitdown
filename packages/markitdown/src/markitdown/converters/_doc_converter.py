import sys
from typing import Any, BinaryIO

from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE, FileConversionException

#using unword dependency
_dependency_exc_info = None
unword = None
try:
    import unword as _unword
    unword = _unword
except ImportError:
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword", "application/x-msword"
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """
    Converts DOC (Word 97-2003) files to Markdown. Uses unword package 
    as parser backend to extract body text with heading levels,
    page breaks, and textbox contents.
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
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )
        
        try:
            doc = unword.parse_doc(file_stream.read())
        except Exception as e:
            raise FileConversionException(f"Failed to parse .doc file: {e}") from e

        title = getattr(doc, "title", None) or getattr(doc, "metadata", {}).get("title")
        return DocumentConverterResult(markdown=doc.body_text.strip(), title=title)
