import io
import sys
from typing import Any, BinaryIO

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo
from markitdown._exceptions import (
    MISSING_DEPENDENCY_MESSAGE,
    MissingDependencyException,
)
from markitdown.converters import PdfConverter

from ._ocr_service import PaddleOCRService

_dependency_exc_info = None
try:
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()


class PdfConverterWithPaddleOCR(DocumentConverter):
    """
    Keep the built-in PDF behavior for normal PDFs and use PaddleOCR only as a
    scanned-PDF fallback when extracted text is empty.
    """

    def __init__(
        self,
        *,
        ocr_service: PaddleOCRService | None = None,
        pdf_converter: DocumentConverter | None = None,
    ) -> None:
        self.ocr_service = ocr_service
        self.pdf_converter = pdf_converter or PdfConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()
        return extension == ".pdf" or mimetype.startswith("application/pdf") or mimetype.startswith(
            "application/x-pdf"
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
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        file_stream.seek(0)
        pdf_bytes = file_stream.read()

        built_in_result = self.pdf_converter.convert(
            io.BytesIO(pdf_bytes),
            stream_info,
            **kwargs,
        )
        if built_in_result.markdown.strip():
            return built_in_result

        ocr_service = kwargs.get("ocr_service") or self.ocr_service
        if ocr_service is None:
            return built_in_result

        markdown = self._ocr_full_pages(io.BytesIO(pdf_bytes), ocr_service)
        if markdown.strip():
            return DocumentConverterResult(markdown=markdown)

        return built_in_result

    def _ocr_full_pages(
        self,
        pdf_bytes: io.BytesIO,
        ocr_service: PaddleOCRService,
    ) -> str:
        markdown_parts: list[str] = []

        try:
            pdf_bytes.seek(0)
            with pdfplumber.open(pdf_bytes) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    markdown_parts.append(f"## Page {page_num}")

                    page_image = page.to_image(resolution=300)
                    image_stream = io.BytesIO()
                    page_image.original.save(image_stream, format="PNG")
                    image_stream.seek(0)

                    ocr_result = ocr_service.extract_text(image_stream)
                    if ocr_result.text.strip():
                        markdown_parts.append(
                            f"*[Image OCR]\n{ocr_result.text.strip()}\n[End OCR]*"
                        )
                    else:
                        markdown_parts.append("*[No text could be extracted from this page]*")
        except Exception:
            markdown_parts = self._ocr_full_pages_with_pymupdf(pdf_bytes, ocr_service)

        return "\n\n".join(markdown_parts).strip()

    def _ocr_full_pages_with_pymupdf(
        self,
        pdf_bytes: io.BytesIO,
        ocr_service: PaddleOCRService,
    ) -> list[str]:
        markdown_parts: list[str] = []
        try:
            import fitz

            pdf_bytes.seek(0)
            doc = fitz.open(stream=pdf_bytes.read(), filetype="pdf")
            try:
                for page_num in range(1, doc.page_count + 1):
                    markdown_parts.append(f"## Page {page_num}")
                    page = doc[page_num - 1]
                    mat = fitz.Matrix(300 / 72, 300 / 72)
                    pix = page.get_pixmap(matrix=mat)
                    image_stream = io.BytesIO(pix.tobytes("png"))
                    ocr_result = ocr_service.extract_text(image_stream)
                    if ocr_result.text.strip():
                        markdown_parts.append(
                            f"*[Image OCR]\n{ocr_result.text.strip()}\n[End OCR]*"
                        )
                    else:
                        markdown_parts.append("*[No text could be extracted from this page]*")
            finally:
                doc.close()
        except Exception:
            return ["*[Error: Could not process scanned PDF]*"]

        return markdown_parts
