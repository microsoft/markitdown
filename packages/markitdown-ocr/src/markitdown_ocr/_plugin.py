"""
Plugin registration for markitdown-ocr.
Registers OCR-enhanced converters with priority-based replacement strategy.
"""

from typing import Any
from markitdown import MarkItDown

from ._ocr_service import (
    AnthropicVisionOCRService,
    LLMVisionOCRService,
    create_ocr_service,
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

    Args:
        markitdown: MarkItDown instance to register converters with
        **kwargs: Additional keyword arguments that may include:
            - llm_client: OpenAI-compatible client for LLM-based OCR (required for OCR to work)
            - llm_model: Model name (e.g., 'gpt-4o')
            - llm_prompt: Custom prompt for text extraction
            - ocr_llm_client: Client to use for OCR instead of llm_client — set
              this to use a backend MarkItDown's own converters do not speak,
              such as an Anthropic client
            - ocr_llm_model: Model name paired with ocr_llm_client
            - ocr_llm_prompt: Prompt override for OCR only
    """
    # Read the same llm_client/llm_model kwargs that MarkItDown itself already
    # accepts for image descriptions, so the common case needs no extra config.
    #
    # MarkItDown's built-in converters call the OpenAI chat-completions shape
    # directly, so a non-OpenAI client cannot be passed as llm_client without
    # breaking them. The ocr_llm_* kwargs give OCR its own client for that case
    # — e.g. OpenAI for image descriptions and Claude for OCR, or Claude alone.
    llm_client = kwargs.get("ocr_llm_client") or kwargs.get("llm_client")
    llm_model = kwargs.get("ocr_llm_model") or kwargs.get("llm_model")
    llm_prompt = kwargs.get("ocr_llm_prompt") or kwargs.get("llm_prompt")

    ocr_service: LLMVisionOCRService | AnthropicVisionOCRService | None = None
    if llm_client and llm_model:
        ocr_service = create_ocr_service(
            client=llm_client,
            model=llm_model,
            default_prompt=llm_prompt,
        )

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
