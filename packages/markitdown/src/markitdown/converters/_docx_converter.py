import base64
import mimetypes
import os
import re
import sys
import io
from warnings import warn

from bs4 import BeautifulSoup
from typing import BinaryIO, Any

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from ..converter_utils.images import resolve_images_dir
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

# Map mimetypes.guess_extension() quirks to sane extensions
_EXT_FIXES = {".jpe": ".jpg", ".jpeg": ".jpg"}


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
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

        style_map = kwargs.get("style_map", None)
        pre_process_stream = pre_process_docx(file_stream)
        html = mammoth.convert_to_html(pre_process_stream, style_map=style_map).value

        save_images = kwargs.get("save_images", False)
        if save_images:
            actual_images_dir, md_prefix = resolve_images_dir(
                save_images, stream_info, "docx"
            )
            html = self._save_images(html, actual_images_dir, md_prefix)

        return self._html_converter.convert_string(html, **kwargs)

    def _save_images(self, html: str, images_dir: str, md_prefix: str) -> str:
        """Extract base64 data URI images from mammoth HTML, save to *images_dir*,
        and replace each src with a *md_prefix*/filename relative path."""
        soup = BeautifulSoup(html, "html.parser")
        for i, img in enumerate(soup.find_all("img")):
            src = img.get("src", "")
            if not src.startswith("data:"):
                continue
            try:
                header, b64data = src.split(",", 1)
                mime = header.split(":")[1].split(";")[0]
                ext = mimetypes.guess_extension(mime) or ".bin"
                ext = _EXT_FIXES.get(ext, ext)
                filename = f"image_{i + 1}{ext}"
                with open(os.path.join(images_dir, filename), "wb") as f:
                    f.write(base64.b64decode(b64data))
                img["src"] = f"{md_prefix}/{filename}"
            except Exception:
                continue
        return str(soup)
