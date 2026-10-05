import sys
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import unword
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """
    Converts legacy Microsoft Word .doc files (Word 97-2003, OLE/CFB binary
    format) to Markdown using the unword package.
    """

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
        # Check the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        parsed = unword.parse_doc(file_stream.read())

        md_content = parsed.body_text or ""

        # Optionally append any extracted textbox contents
        keep_textboxes = kwargs.get("keep_textboxes", True)
        if keep_textboxes and parsed.textboxes:
            textboxes = "\n\n".join(
                tb.strip() for tb in parsed.textboxes if tb and tb.strip()
            )
            if textboxes:
                md_content = md_content.rstrip() + "\n\n# Text Boxes\n\n" + textboxes

        return DocumentConverterResult(markdown=md_content.strip())
