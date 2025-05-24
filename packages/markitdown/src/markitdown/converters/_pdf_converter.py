import sys
import io
from typing import BinaryIO, Any, List

from .._base_converter import DocumentConverter, DocumentConverterResult, PageInfo
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE


# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
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

        # Check if page-level extraction is requested
        extract_pages = kwargs.get("extract_pages", False)

        if extract_pages:
            # Extract text page by page
            pages = self._extract_pages(file_stream)
            # Combine all pages for the main markdown content
            markdown = "\n\n".join([page.content for page in pages])
            return DocumentConverterResult(
                markdown=markdown,
                pages=pages,
            )
        else:
            # Default behavior - extract all text at once
            return DocumentConverterResult(
                markdown=pdfminer.high_level.extract_text(file_stream),
            )

    def _extract_pages(self, file_stream: BinaryIO) -> List[PageInfo]:
        """Extract text from each page separately."""
        pages = []

        try:
            # Reset stream position
            file_stream.seek(0)

            # Create resource manager
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()

            # Get all pages
            pdf_pages = list(PDFPage.get_pages(file_stream))

            for page_num, page in enumerate(pdf_pages, 1):
                output_string = None
                device = None
                try:
                    # Create a new StringIO for each page
                    output_string = io.StringIO()
                    device = TextConverter(rsrcmgr, output_string, laparams=laparams)
                    interpreter = PDFPageInterpreter(rsrcmgr, device)

                    # Process the page
                    interpreter.process_page(page)

                    # Get the text content
                    text = output_string.getvalue()

                    # Add page info
                    pages.append(PageInfo(page_number=page_num, content=text.strip()))

                finally:
                    # Clean up resources
                    if device:
                        device.close()
                    if output_string:
                        output_string.close()

        except Exception:
            # If page-by-page extraction fails, fall back to full document extraction
            file_stream.seek(0)
            full_text = pdfminer.high_level.extract_text(file_stream)
            pages = [PageInfo(page_number=1, content=full_text.strip())]

        return pages
