"""
Enhanced DOCX Converter with OCR support for embedded images.
Extracts images from Word documents and performs OCR while maintaining context.
"""

import sys
from typing import Any, BinaryIO, Optional

from markitdown.converters import HtmlConverter
from markitdown.converter_utils.docx.pre_process import pre_process_docx
from markitdown import DocumentConverterResult, StreamInfo
from markitdown._exceptions import (
    MissingDependencyException,
    MISSING_DEPENDENCY_MESSAGE,
)
from ._ocr_service import LLMVisionOCRService

# Try loading dependencies
_dependency_exc_info = None
try:
    import mammoth
except ImportError:
    _dependency_exc_info = sys.exc_info()

# Placeholder carried through Mammoth and HTML-to-Markdown conversion.
# It must be a single token with no special markdown characters.
_PLACEHOLDER = "MARKITDOWNOCRBLOCK{}"


class DocxConverterWithOCR(HtmlConverter):
    """
    Enhanced DOCX Converter with OCR support for embedded images.
    Maintains document flow while extracting text from images inline.
    """

    def __init__(self, ocr_service: Optional[LLMVisionOCRService] = None):
        super().__init__()
        self._html_converter = HtmlConverter()
        self.ocr_service = ocr_service

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension == ".docx":
            return True

        if mimetype.startswith(
            "application/vnd.openxmlformats-officedocument.wordprocessingml"
        ):
            return True

        return False

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
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        # Get OCR service if available (from kwargs or instance)
        ocr_service: Optional[LLMVisionOCRService] = (
            kwargs.get("ocr_service") or self.ocr_service
        )

        if ocr_service:
            ocr_text_by_placeholder: dict[str, str] = {}
            image_occurrence = 0

            def convert_image(image: Any) -> dict[str, str]:
                nonlocal image_occurrence

                placeholder = _PLACEHOLDER.format(image_occurrence)
                image_occurrence += 1

                try:
                    with image.open() as image_stream:
                        ocr_result = ocr_service.extract_text(image_stream)
                    text = ocr_result.text.strip()
                    if text:
                        ocr_text_by_placeholder[placeholder] = text
                except Exception:
                    pass

                # Keep every occurrence in the converted output, including empty
                # or failed OCR, so later images cannot shift to an earlier slot.
                return {"src": placeholder, "alt": placeholder}

            # Convert DOCX → HTML while Mammoth visits every image occurrence.
            file_stream.seek(0)
            pre_process_stream = pre_process_docx(file_stream)
            html_result = mammoth.convert_to_html(
                pre_process_stream,
                style_map=kwargs.get("style_map"),
                convert_image=mammoth.images.img_element(convert_image),
            ).value

            # Convert HTML → markdown before adding OCR text so formatting in OCR
            # output is not escaped by the markdown converter.
            md_result = self._html_converter.convert_string(
                html_result, **kwargs
            )
            md = md_result.markdown

            for placeholder, raw_text in ocr_text_by_placeholder.items():
                ocr_block = f"*[Image OCR]\n{raw_text}\n[End OCR]*"
                md = md.replace(
                    f"![{placeholder}]({placeholder})",
                    ocr_block,
                )

            # Remove failed or empty OCR occurrences only after successful
            # placeholders have been substituted at their original positions.
            for occurrence in range(image_occurrence):
                placeholder = _PLACEHOLDER.format(occurrence)
                md = md.replace(f"![{placeholder}]({placeholder})", "")

            return DocumentConverterResult(markdown=md)
        else:
            # Standard conversion without OCR
            style_map = kwargs.get("style_map", None)
            pre_process_stream = pre_process_docx(file_stream)
            return self._html_converter.convert_string(
                mammoth.convert_to_html(pre_process_stream, style_map=style_map).value,
                **kwargs,
            )
