from typing import Any

from markitdown import MarkItDown

from ._ocr_service import PaddleOCRService
from ._pdf_converter import PdfConverterWithPaddleOCR

__plugin_interface_version__ = 1


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    ocr_service = None
    if kwargs.get("paddleocr_enabled"):
        ocr_service = PaddleOCRService(
            lang=kwargs.get("paddleocr_lang", "ch"),
            paddleocr_kwargs=kwargs.get("paddleocr_kwargs"),
        )

    markitdown.register_converter(
        PdfConverterWithPaddleOCR(ocr_service=ocr_service),
        priority=-1.0,
    )
