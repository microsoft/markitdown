import io
import sys
import os
from pathlib import Path
from typing import BinaryIO, Any, Optional

from markitdown import (
    MarkItDown,
    DocumentConverter,
    DocumentConverterResult,
    StreamInfo,
    MissingDependencyException,
)

MISSING_DEPENDENCY_MESSAGE = """{converter} recognized the input as a potential {extension} file, but the dependencies needed to read {extension} files have not been installed. To resolve this error, include the optional dependency [{feature}] or [all] when installing MarkItDown. For example:

* pip install markitdown[{feature}]
* pip install markitdown[all]
* pip install markitdown[{feature}, ...]
* etc."""

__plugin_interface_version__ = 1

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import fitz as pymupdf
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


def register_converters(markitdown: MarkItDown, **kwargs):
    """
    Called during construction of MarkItDown instances to register converters provided by plugins.
    """
    markitdown.register_converter(PyMuPdfConverter(), override=True)


class PyMuPdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown using PyMuPDF.
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
        images_output_dir: Optional[str] = None,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Check the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        assert isinstance(file_stream, io.IOBase)  # for mypy

        doc = pymupdf.open(stream=file_stream.read(), filetype="pdf")
        text = ""
        extracted_image_paths = []

        # Determine output directory for images
        output_dir = None
        if images_output_dir:
            output_dir = Path(images_output_dir)
        elif stream_info.local_path:
            source_path = Path(stream_info.local_path)
            output_dir = source_path.parent / "img"

        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)

        for page_num, page in enumerate(doc):
            text += page.get_text()
            extracted_image_paths.extend(self._extract_images_from_page(doc, page, page_num, output_dir))

        doc.close()

        result = DocumentConverterResult(markdown=text)
        result.extracted_image_paths = extracted_image_paths
        return result

    def _extract_images_from_page(self, doc: pymupdf.Document, page: pymupdf.Page, page_num: int, output_dir: Optional[Path]) -> list[str]:
        """
        Extracts images from a single PyMuPDF page and saves them to the specified output directory.
        Returns a list of paths to the extracted images.
        """
        extracted_paths = []
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            if output_dir:
                image_filename = f"page_{page_num + 1}_image_{img_index + 1}.{image_ext}"
                image_path = output_dir / image_filename
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                extracted_paths.append(str(image_path))
        return extracted_paths
