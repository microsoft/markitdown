import re
import sys
import io
from warnings import warn

from typing import BinaryIO, Any, Optional

from bs4 import BeautifulSoup

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

_FOOTNOTE_DEF_ID = re.compile(r"^footnote-(\d+)$")
_FOOTNOTE_REF_HREF = re.compile(r"^#footnote-(\d+)$")


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

        html_result = self._convert_footnotes_to_gfm(html_result)

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

    def _convert_footnotes_to_gfm(self, html: str) -> str:
        """Rewrite mammoth's footnote HTML into GFM footnote syntax.

        mammoth emits references as
        ``<sup><a href="#footnote-N" id="footnote-ref-N">[N]</a></sup>``
        and definitions as ``<li id="footnote-N">...``, anchored by ids that
        the Markdown step cannot express, so the links arrive dead. Replace
        both ends with GFM footnotes, which need no anchors.
        """
        if "footnote-" not in html:
            return html

        soup = BeautifulSoup(html, "html.parser")
        definitions = soup.find_all("li", id=_FOOTNOTE_DEF_ID)
        if not definitions:
            return html

        for anchor in soup.find_all("a", href=_FOOTNOTE_REF_HREF):
            number = _FOOTNOTE_REF_HREF.match(anchor["href"]).group(1)
            (anchor.find_parent("sup") or anchor).replace_with("[^%s]" % number)

        blocks = []
        for item in definitions:
            number = _FOOTNOTE_DEF_ID.match(item["id"]).group(1)
            for backlink in item.find_all("a", href="#footnote-ref-%s" % number):
                backlink.extract()
            body = self._html_converter.convert_string(
                item.decode_contents()
            ).markdown.strip()
            lines = body.split("\n") if body else [""]
            content = "".join(
                line if index == 0 else ("\n" if not line else "\n    " + line)
                for index, line in enumerate(lines)
            )
            blocks.append("[^%s]: %s" % (number, content))
            list_holder = item.find_parent("ol")
            item.decompose()
            if list_holder is not None and list_holder.find("li") is None:
                list_holder.decompose()

        return str(soup) + "\n\n" + "\n".join(blocks)
