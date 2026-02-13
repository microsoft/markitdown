"""
Enhanced DOCX Converter with OCR support for embedded images.
Extracts images from Word documents and performs OCR while maintaining context.
"""

import sys
import io
import re
from typing import BinaryIO, Any, Optional

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from ._ocr_service import MultiBackendOCRService

# Try loading dependencies
_dependency_exc_info = None
try:
    import mammoth
    from docx import Document
except ImportError:
    _dependency_exc_info = sys.exc_info()


class DocxConverterWithOCR(HtmlConverter):
    """
    Enhanced DOCX Converter with OCR support for embedded images.
    Maintains document flow while extracting text from images inline.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

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

        # Get OCR service if available
        ocr_service: Optional[MultiBackendOCRService] = kwargs.get("ocr_service")

        if ocr_service:
            # Extract and OCR images before mammoth processing
            file_stream.seek(0)
            image_ocr_map = self._extract_and_ocr_images(file_stream, ocr_service)

            # Process with mammoth
            file_stream.seek(0)
            pre_process_stream = pre_process_docx(file_stream)
            html_result = mammoth.convert_to_html(
                pre_process_stream, style_map=kwargs.get("style_map")
            ).value

            # Inject OCR results into HTML
            html_with_ocr = self._inject_ocr_into_html(html_result, image_ocr_map)

            return self._html_converter.convert_string(html_with_ocr, **kwargs)
        else:
            # Standard conversion without OCR
            style_map = kwargs.get("style_map", None)
            pre_process_stream = pre_process_docx(file_stream)
            return self._html_converter.convert_string(
                mammoth.convert_to_html(pre_process_stream, style_map=style_map).value,
                **kwargs,
            )

    def _extract_and_ocr_images(
        self, file_stream: BinaryIO, ocr_service: MultiBackendOCRService
    ) -> dict[str, str]:
        """
        Extract images from DOCX and OCR them.

        Args:
            file_stream: DOCX file stream
            ocr_service: OCR service to use

        Returns:
            Dict mapping image relationship IDs to OCR text
        """
        ocr_map = {}

        try:
            file_stream.seek(0)
            doc = Document(file_stream)

            # Extract images from document relationships
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref.lower():
                    try:
                        image_part = rel.target_part
                        image_bytes = image_part.blob

                        # Create stream for OCR
                        image_stream = io.BytesIO(image_bytes)

                        # Perform OCR
                        ocr_result = ocr_service.extract_text(image_stream)

                        if ocr_result.text.strip():
                            # Store with relationship ID using consistent format
                            ocr_text = f"\n[Image OCR: {rel.rId}]\n{ocr_result.text}\n[End Image OCR]\n"
                            ocr_map[rel.rId] = ocr_text

                    except Exception:
                        continue

        except Exception:
            pass

        return ocr_map

    def _inject_ocr_into_html(self, html: str, ocr_map: dict[str, str]) -> str:
        """
        Replace image tags with OCR text inline (no base64 images).

        Args:
            html: HTML content from mammoth
            ocr_map: Map of image IDs to OCR text

        Returns:
            HTML with images replaced by OCR text
        """
        if not ocr_map:
            return html

        # Create a list of OCR texts and track which ones we've used
        ocr_texts = list(ocr_map.values())
        ocr_keys = list(ocr_map.keys())
        used_indices = []

        def replace_img(match):
            # Replace the entire image tag with OCR text (no base64!)
            for i, ocr_text in enumerate(ocr_texts):
                if i not in used_indices:
                    used_indices.append(i)
                    # Return just the OCR text as a paragraph, no image
                    return f"<p><em>{ocr_text}</em></p>"
            return ""  # Remove image if no OCR text available

        # Replace ALL img tags (including base64) with OCR text
        result = re.sub(r"<img[^>]*>", replace_img, html)

        # If there are remaining OCR texts (images that weren't in HTML), append them
        remaining_ocr = [
            ocr_texts[i] for i in range(len(ocr_texts)) if i not in used_indices
        ]
        if remaining_ocr:
            result += f"<p><em>{''.join(remaining_ocr)}</em></p>"

        return result
