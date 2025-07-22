import sys
import io

from typing import BinaryIO, Any


from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE


# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown. Most style information is ignored, so the results are essentially plain-text.
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
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        assert isinstance(file_stream, io.IOBase)  # for mypy
        return DocumentConverterResult(
            markdown=pdfminer.high_level.extract_text(file_stream),
        )

        # ========== Custom Addition: Pagewise Markdown Output (Non-invasive) ==========

def convert_pagewise(file_stream: BinaryIO) -> list[str]:
    """
    Converts each page of a PDF to a separate Markdown string using pdfminer.
    This function is non-invasive and does not modify the original PdfConverter class.
    """
    from pdfminer.pdfpage import PDFPage
    from pdfminer.high_level import extract_text_to_fp
    from pdfminer.layout import LAParams

    output_pages = []
    laparams = LAParams()
    for page in PDFPage.get_pages(file_stream):
        buffer = io.StringIO()
        extract_text_to_fp(io.BytesIO(page.__self__.read(page.length)), buffer, laparams=laparams, page_numbers=[page.pageid])
        markdown_text = buffer.getvalue().strip()
        output_pages.append(f"<!-- Page {page.pageid} -->\n\n{markdown_text}")
        buffer.close()

    return output_pages

