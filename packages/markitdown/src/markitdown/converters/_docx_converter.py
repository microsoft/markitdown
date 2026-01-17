import sys
import io
import logging
from typing import BinaryIO, Any

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

logger = logging.getLogger(__name__)

_dependency_exc_info = None
try:
    import mammoth
except ImportError:
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

ACCEPTED_FILE_EXTENSIONS = [".docx"]


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown.
    Gracefully handles malformed DOCX files with missing style information.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        return (
            extension in ACCEPTED_FILE_EXTENSIONS
            or any(mimetype.startswith(p) for p in ACCEPTED_MIME_TYPE_PREFIXES)
        )

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
                    extension=".docx",
                    feature="docx",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore
                _dependency_exc_info[2]
            )

        style_map = kwargs.get("style_map")

        # Preprocess and fully buffer the DOCX to avoid stream reuse issues
        processed = pre_process_docx(file_stream)
        buffer = io.BytesIO(processed.read())
        buffer.seek(0)

        try:
            result = mammoth.convert_to_html(buffer, style_map=style_map)
            html = result.value
        except KeyError as exc:
            # Known issue: malformed DOCX with missing w:styleId
            logger.warning(
                "DOCX conversion encountered missing style metadata (%s). "
                "Falling back to default style handling.",
                exc,
            )

            buffer.seek(0)
            result = mammoth.convert_to_html(buffer)
            html = result.value

        return self._html_converter.convert_string(html, **kwargs)
