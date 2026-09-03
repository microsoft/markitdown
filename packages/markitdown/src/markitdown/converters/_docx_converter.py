import sys
import io
from warnings import warn

from typing import BinaryIO, Any, Optional

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth

except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

ACCEPTED_FILE_EXTENSIONS = [".docx"]

_UNDERLINE_STYLE_MAP = "u => u"


def _read_embedded_style_map(file_stream: BinaryIO) -> Optional[str]:
    """Read the style map embedded in a .docx, if it has one."""
    position = file_stream.tell()
    try:
        return mammoth.read_embedded_style_map(file_stream)
    finally:
        file_stream.seek(position)


def convert_docx_to_html(file_stream: BinaryIO, style_map: Optional[str] = None) -> str:
    """Convert a .docx stream to HTML, preserving underlined runs.

    Mammoth resolves style mappings in order and the first match wins, so the
    ``u => u`` default -- which exists because mammoth otherwise drops
    underlines -- is composed last, after the caller's mappings and after any
    style map embedded in the document. The embedded map is read and ordered
    here rather than left to mammoth, since mammoth would place it *after* the
    mappings passed in and our default would silently override it.

    Shared so that converters replacing this one (e.g., plugins) get the same
    behavior without duplicating it.
    """
    pre_process_stream = pre_process_docx(file_stream)
    style_map = "\n".join(
        part
        for part in (
            style_map,
            _read_embedded_style_map(pre_process_stream),
            _UNDERLINE_STYLE_MAP,
        )
        if part
    )
    return mammoth.convert_to_html(
        pre_process_stream,
        style_map=style_map,
        include_embedded_style_map=False,
    ).value


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g., headings) and tables are preserved where possible.
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
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".docx",
                    feature="docx",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        return self._html_converter.convert_string(
            convert_docx_to_html(file_stream, kwargs.get("style_map", None)),
            **kwargs,
        )
