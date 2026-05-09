"""Plugin registration for markitdown-glmocr."""

from typing import Any
from markitdown import MarkItDown

from ._config import GlmOcrConfig
from ._ai_service import AIService
from ._converter import GlmOcrPdfConverter


__plugin_interface_version__ = 1


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """
    Register markitdown-glmocr converter.
    
    Config sources (priority high to low):
    1. kwargs parameters
    2. Environment variables
    3. Config file (pyproject.toml)
    4. Default values
    """
    # Load config
    config = GlmOcrConfig.load()
    
    # kwargs override config
    api_key = kwargs.get("api_key") or config.api_key
    model = kwargs.get("model", config.model)
    dpi = kwargs.get("dpi", config.dpi)
    force_ai = kwargs.get("force_ai", config.force_ai)
    timeout = kwargs.get("timeout", config.timeout)
    
    # Create AI service
    ai_service = None
    if api_key:
        try:
            ai_service = AIService(
                api_key=api_key,
                model=model,
                timeout=timeout,
            )
        except Exception:
            pass
    
    # Register converter
    PRIORITY_GLMOCR = -1.0
    
    markitdown.register_converter(
        GlmOcrPdfConverter(
            ai_service=ai_service,
            dpi=dpi,
            force_ai=force_ai,
        ),
        priority=PRIORITY_GLMOCR,
    )