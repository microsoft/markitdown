"""PPTX image OCR using the core presentation conversion pipeline."""

import hashlib
import html
from typing import Any, BinaryIO, Optional
from warnings import warn

from markitdown import DocumentConverterResult, StreamInfo
from markitdown.converters import PptxConverter

from ._ocr_service import LLMVisionOCRService, _extract_text_with_metadata


class PptxConverterWithOCR(PptxConverter):
    """Recognize embedded images while inheriting native PPTX conversion."""

    def __init__(self, ocr_service: Optional[LLMVisionOCRService] = None):
        super().__init__()
        if not hasattr(PptxConverter, "_image_to_html"):
            raise RuntimeError(
                "PPTX OCR requires markitdown>=0.1.8b3 for the "
                "PptxConverter._image_to_html hook. "
                "Upgrade with: pip install --upgrade 'markitdown>=0.1.8b3'."
            )
        self.ocr_service = ocr_service

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        kwargs["_pptx_ocr_cache"] = {}
        return super().convert(file_stream, stream_info, **kwargs)

    def _image_to_html(
        self,
        image_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Optional[str]:
        ocr_service = kwargs.get("ocr_service") or self.ocr_service
        if ocr_service is None:
            return None

        cache: dict[bytes, Optional[str]] = kwargs.get("_pptx_ocr_cache", {})
        key = hashlib.sha256(image_stream.read()).digest()
        image_stream.seek(0)
        if key in cache:
            return cache[key]

        result = _extract_text_with_metadata(ocr_service, image_stream, stream_info)
        if result.error:
            warn(
                f"PPTX image OCR failed: {result.error}. Keeping the native image.",
                RuntimeWarning,
                stacklevel=2,
            )
            cache[key] = None
            return None
        text = result.text.strip()
        if not text:
            cache[key] = None
            return None

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        content = html.escape(text).replace("\n", "<br>")
        fragment = f"<p><em>[Image OCR]<br>{content}<br>[End OCR]</em></p>"
        cache[key] = fragment
        return fragment
