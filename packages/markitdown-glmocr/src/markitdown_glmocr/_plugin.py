"""Plugin registration for markitdown-glmocr."""

from typing import Any
from markitdown import MarkItDown

from ._converter import GlmOcrConverter


__plugin_interface_version__ = 1


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """
    Register markitdown-glmocr converter.
    
    Config sources (priority high to low):
    1. kwargs parameters
    2. Environment variables (ZHIPU_API_KEY)
    3. .env file
    4. Built-in defaults
    """
    # Register converter
    PRIORITY_GLMOCR = -1.0
    
    markitdown.register_converter(
        GlmOcrConverter(
            api_key=kwargs.get("api_key"),
            timeout=kwargs.get("timeout", 1800),
            enable_layout=kwargs.get("enable_layout", False),
            force_ai=kwargs.get("force_ai", False),
        ),
        priority=PRIORITY_GLMOCR,
    )