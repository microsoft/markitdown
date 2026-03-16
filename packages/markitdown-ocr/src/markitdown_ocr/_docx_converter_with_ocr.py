"""
Enhanced DOCX Converter with OCR support for embedded images.
Extracts images from Word documents and performs OCR while maintaining context.
"""

import io
import re
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
    from docx import Document
except ImportError:
    _dependency_exc_info = sys.exc_info()

# Placeholder injected into HTML so that mammoth never sees the OCR markers.
# Must be a single token with no special markdown characters.
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
            # 1. Extract and OCR images — returns raw text per image
            file_stream.seek(0)
            image_ocr_map = self._extract_and_ocr_images(file_stream, ocr_service)

            # 2. Convert DOCX → HTML via mammoth
            file_stream.seek(0)
            pre_process_stream = pre_process_docx(file_stream)
            html_result = mammoth.convert_to_html(
                pre_process_stream, style_map=kwargs.get("style_map")
            ).value

            # 3. Replace <img> tags with plain placeholder tokens so that
            #    mammoth's HTML→markdown step never escapes our OCR markers.
            html_with_placeholders, ocr_texts = self._inject_placeholders(
                html_result, image_ocr_map
            )

            # 4. Convert HTML → markdown
            md_result = self._html_converter.convert_string(
                html_with_placeholders, **kwargs
            )
            md = md_result.markdown

            # 5. Swap placeholders for the actual OCR blocks (post-conversion
            #    so * and _ are never escaped by the markdown converter).
            for i, raw_text in enumerate(ocr_texts):
                placeholder = _PLACEHOLDER.format(i)
                ocr_block = f"*[Image OCR]\n{raw_text}\n[End OCR]*"
                md = md.replace(placeholder, ocr_block)

            return DocumentConverterResult(markdown=md)
        else:
            # Standard conversion without OCR
            style_map = kwargs.get("style_map", None)
            pre_process_stream = pre_process_docx(file_stream)
            return self._html_converter.convert_string(
                mammoth.convert_to_html(pre_process_stream, style_map=style_map).value,
                **kwargs,
            )

    def _extract_and_ocr_images(
        self, file_stream: BinaryIO, ocr_service: LLMVisionOCRService
    ) -> dict[str, str]:
        """
        Extract images from DOCX and OCR them.

        Returns:
            Dict mapping image relationship IDs to raw OCR text (no markers).
        """
        ocr_map = {}

        try:
            file_stream.seek(0)
            doc = Document(file_stream)

            for rel in doc.part.rels.values():
                if "image" in rel.target_ref.lower():
                    try:
                        image_bytes = rel.target_part.blob
                        image_stream = io.BytesIO(image_bytes)
                        ocr_result = ocr_service.extract_text(image_stream)

                        if ocr_result.text.strip():
                            # Store raw text only — markers added later
                            ocr_map[rel.rId] = ocr_result.text.strip()

                    except Exception:
                        continue

        except Exception:
            pass

        return ocr_map

    def _inject_placeholders(
        self, html: str, ocr_map: dict[str, str]
    ) -> tuple[str, list[str]]:
        """
        Replace <img> tags with numbered placeholder tokens.

        Returns:
            (html_with_placeholders, ordered list of raw OCR texts)
        """
        if not ocr_map:
            return html, []

        ocr_texts = list(ocr_map.values())
        used: list[int] = []

        def replace_img(match: re.Match) -> str:  # type: ignore[type-arg]
            for i in range(len(ocr_texts)):
                if i not in used:
                    used.append(i)
                    return f"<p>{_PLACEHOLDER.format(i)}</p>"
            return ""  # remove image if all OCR texts already used

        result = re.sub(r"<img[^>]*>", replace_img, html)

        # Any OCR texts that had no matching <img> tag go at the end
        for i in range(len(ocr_texts)):
            if i not in used:
                result += f"<p>{_PLACEHOLDER.format(i)}</p>"

        return result, ocr_texts
