# SPDX-FileCopyrightText: 2025-present Contributors
# SPDX-License-Identifier: MIT

"""
markitdown-ocr: OCR plugin for MarkItDown

Adds text extraction from images embedded in PDF, DOCX, PPTX, and XLSX files.
Supports multiple OCR providers:
- LLM Vision (OpenAI-compatible: GPT-4o, Gemini, etc.)
- glm-ocr (ZhiPu AI layout parsing: better table recognition, lower cost)
"""

from ._plugin import __plugin_interface_version__, register_converters
from .__about__ import __version__
from ._ocr_service import (
    OCRResult,
    LLMVisionOCRService,
    GlmOcrService,
)
from ._glmocr_config import GlmOcrConfig
from ._pdf_converter_with_ocr import PdfConverterWithOCR
from ._docx_converter_with_ocr import DocxConverterWithOCR
from ._pptx_converter_with_ocr import PptxConverterWithOCR
from ._xlsx_converter_with_ocr import XlsxConverterWithOCR

__all__ = [
    "__version__",
    "__plugin_interface_version__",
    "register_converters",
    "OCRResult",
    "LLMVisionOCRService",
    "GlmOcrService",
    "GlmOcrConfig",
    "PdfConverterWithOCR",
    "DocxConverterWithOCR",
    "PptxConverterWithOCR",
    "XlsxConverterWithOCR",
]
