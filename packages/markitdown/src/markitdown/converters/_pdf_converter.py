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

# Try to import pytesseract and pdf2image for OCR
_ocr_dependency_exc_info = None
try:
    import pytesseract
    from pdf2image import convert_from_bytes
except ImportError:
    _ocr_dependency_exc_info = sys.exc_info()

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
        # Check dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(_dependency_exc_info[2])

        # Try to extract text with pdfminer
        file_stream.seek(0)
        text = pdfminer.high_level.extract_text(file_stream)
        if text and text.strip():
            return DocumentConverterResult(markdown=text)

        # If no text found, fall back to OCR
        if _ocr_dependency_exc_info is not None:
            raise MissingDependencyException(
                "OCR dependencies are missing. Please install pytesseract and pdf2image for OCR support."
            ) from _ocr_dependency_exc_info[1].with_traceback(_ocr_dependency_exc_info[2])

        file_stream.seek(0)
        images = convert_from_bytes(file_stream.read())
        ocr_text = []
        for img in images:
            ocr_text.append(pytesseract.image_to_string(img))
        ocr_output = "\n\n".join(ocr_text)
        return DocumentConverterResult(markdown=ocr_output)
