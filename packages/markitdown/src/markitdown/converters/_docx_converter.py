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
    file_stream.seek(0)
    try:
        return mammoth.read_embedded_style_map(file_stream)
    finally:
        file_stream.seek(position)


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

        pre_process_stream = pre_process_docx(file_stream)

        caller_style_map = kwargs.get("style_map")
        embedded_style_map = _read_embedded_style_map(pre_process_stream)

        style_map = "\n".join(
            part
            for part in (
                caller_style_map,
                embedded_style_map,
                _UNDERLINE_STYLE_MAP,
            )
            if part
        )

        image_adapter = None
        mammoth_kwargs: dict[str, Any] = {}
        if type(self)._image_to_html is not DocxConverter._image_to_html:
            from ..converter_utils.docx._images import _DocxImages

            image_adapter = _DocxImages(self._image_to_html, kwargs)
            mammoth_kwargs["convert_image"] = image_adapter.convert_image

        html_result = mammoth.convert_to_html(
            pre_process_stream,
            style_map=style_map,
            include_embedded_style_map=False,
            **mammoth_kwargs,
        ).value

        if image_adapter is not None:
            html_result = image_adapter.replace_images(html_result)

        return self._html_converter.convert_string(html_result, **kwargs)

    def _image_to_html(
        self,
        image_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Optional[str]:
        """Override to render an embedded image as an HTML fragment.

        The stream is borrowed, seekable, and positioned at zero; do not close
        or retain it. StreamInfo describes the image, not the document. Existing
        conversion options are forwarded through kwargs.

        Return None or blank text to retain the native image representation.
        Otherwise return HTML, escaping any literal text. Inline HTML stays
        inline; block HTML splits enclosing paragraph/inline wrappers but stays
        inside its table cell or list item. Hook failures propagate through the
        normal conversion failure path.
        """
        return None
