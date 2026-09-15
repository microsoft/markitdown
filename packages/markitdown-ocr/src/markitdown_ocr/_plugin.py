"""
Plugin registration for markitdown-ocr.
Registers OCR-enhanced converters with priority-based replacement strategy.
"""

import os
from typing import Any
from markitdown import MarkItDown

from ._ocr_service import (
    LLMVisionOCRService,
    OCR_API_KEY_ENV,
    OCR_API_BASE_ENV,
    OCR_MODEL_ENV,
)
from ._pdf_converter_with_ocr import PdfConverterWithOCR
from ._docx_converter_with_ocr import DocxConverterWithOCR
from ._pptx_converter_with_ocr import PptxConverterWithOCR
from ._xlsx_converter_with_ocr import XlsxConverterWithOCR


__plugin_interface_version__ = 1


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """
    Register OCR-enhanced converters with MarkItDown.

    This plugin provides OCR support for PDF, DOCX, PPTX, and XLSX files.
    The converters are registered with priority -1.0 to run BEFORE built-in
    converters (which have priority 0.0), effectively replacing them when
    the plugin is enabled.

    OCR service can be configured in three ways (in order of priority):
    1. Explicit kwargs: llm_client, llm_model, llm_prompt
    2. Environment variables: MARKITDOWN_OCR_API_KEY, MARKITDOWN_OCR_API_BASE, MARKITDOWN_OCR_MODEL
    3. No OCR service (text-only extraction)

    Args:
        markitdown: MarkItDown instance to register converters with
        **kwargs: Additional keyword arguments that may include:
            - llm_client: OpenAI-compatible client for LLM-based OCR
            - llm_model: Model name (e.g., 'gpt-4o')
            - llm_prompt: Custom prompt for text extraction
    """
    # Create OCR service — reads the same llm_client/llm_model kwargs
    # that MarkItDown itself already accepts for image descriptions
    llm_client = kwargs.get("llm_client")
    llm_model = kwargs.get("llm_model")
    llm_prompt = kwargs.get("llm_prompt")

    ocr_service: LLMVisionOCRService | None = None

    # Priority 1: Use explicit kwargs if provided
    if llm_client and llm_model:
        ocr_service = LLMVisionOCRService(
            client=llm_client,
            model=llm_model,
            default_prompt=llm_prompt,
        )
    # Priority 2: Try to create from environment variables
    elif os.environ.get(OCR_API_KEY_ENV) and os.environ.get(OCR_MODEL_ENV):
        try:
            ocr_service = LLMVisionOCRService.from_env(default_prompt=llm_prompt)
        except Exception:
            # If environment config is incomplete or invalid, proceed without OCR
            pass

    # Register converters with priority -1.0 (before built-ins at 0.0)
    # This effectively "replaces" the built-in converters when plugin is installed
    # Pass the OCR service to each converter's constructor
    PRIORITY_OCR_ENHANCED = -1.0

    markitdown.register_converter(
        PdfConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )

    markitdown.register_converter(
        DocxConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )

    markitdown.register_converter(
        PptxConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )

    markitdown.register_converter(
        XlsxConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )
