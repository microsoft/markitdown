"""
Plugin registration for markitdown-ocr.
Registers OCR-enhanced converters with priority-based replacement strategy.

Provider selection (priority high to low):
1. glm-ocr provider (if glmocr_api_key or GLMOCR_API_KEY provided)
2. LLM Vision provider (if llm_client + llm_model provided)
3. No OCR (converters fall back to standard text extraction)
"""

import os
from typing import Any
from warnings import warn

from markitdown import MarkItDown

from ._ocr_service import LLMVisionOCRService, GlmOcrService
from ._glmocr_config import GlmOcrConfig
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

    Provider selection (priority high to low):
    1. glm-ocr provider — if glmocr_api_key or GLMOCR_API_KEY is provided
    2. LLM Vision provider — if llm_client + llm_model is provided
    3. No OCR — converters fall back to standard text extraction

    Args:
        markitdown: MarkItDown instance to register converters with
        **kwargs: Additional keyword arguments that may include:
            - glmocr_api_key: ZhiPu AI API key for glm-ocr provider
            - glmocr_model: glm-ocr model name (default: 'glm-ocr')
            - glmocr_timeout: Request timeout in seconds (default: 120)
            - llm_client: OpenAI-compatible client for LLM-based OCR
            - llm_model: Model name (e.g., 'gpt-4o')
            - llm_prompt: Custom prompt for text extraction
    """
    ocr_service = None

    # --- Provider 1: glm-ocr (priority) ---
    glmocr_api_key = kwargs.get("glmocr_api_key") or os.environ.get("GLMOCR_API_KEY")

    # If not provided via kwargs or env, try config file
    if not glmocr_api_key:
        try:
            config = GlmOcrConfig.load()
            glmocr_api_key = config.api_key
        except Exception:
            pass

    if glmocr_api_key:
        try:
            glmocr_model = (
                kwargs.get("glmocr_model")
                or os.environ.get("GLMOCR_MODEL")
                or "glm-ocr"
            )
            glmocr_timeout = int(
                kwargs.get("glmocr_timeout")
                or os.environ.get("GLMOCR_TIMEOUT", "120")
            )

            ocr_service = GlmOcrService(
                api_key=glmocr_api_key,
                model=glmocr_model,
                timeout=glmocr_timeout,
            )
        except Exception as e:
            warn(
                f"Failed to initialize glm-ocr provider, falling back to LLM Vision: {e}",
                RuntimeWarning,
                stacklevel=2,
            )
            ocr_service = None  # Fall through to LLM Vision

    # --- Provider 2: LLM Vision (fallback) ---
    if ocr_service is None:
        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model")
        llm_prompt = kwargs.get("llm_prompt")

        if llm_client and llm_model:
            ocr_service = LLMVisionOCRService(
                client=llm_client,
                model=llm_model,
                default_prompt=llm_prompt,
            )

    # --- Register converters with priority -1.0 (before built-ins at 0.0) ---
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
