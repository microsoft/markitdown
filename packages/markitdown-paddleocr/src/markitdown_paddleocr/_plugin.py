"""Plugin registration for markitdown-paddleocr."""

from typing import Any
from markitdown import MarkItDown

from ._converter import PaddleOcrConverter


__plugin_interface_version__ = 1


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """Register markitdown-paddleocr converter.

    Config sources (priority high to low):
    1. kwargs parameters
    2. Environment variables (BAIDU_PADDLE_TOKEN)
    3. Built-in defaults
    """
    # Register converter with higher priority than default PDF converter
    PRIORITY_PADDLEOCR = -1.0

    markitdown.register_converter(
        PaddleOcrConverter(
            token=kwargs.get("token"),
            model=kwargs.get("model", "PaddleOCR-VL-1.5"),
            poll_interval=kwargs.get("poll_interval", 2.0),
            poll_timeout=kwargs.get("poll_timeout", 300.0),
            force_ai=kwargs.get("force_ai", False),
            use_doc_orientation_classify=kwargs.get("use_doc_orientation_classify", False),
            use_doc_unwarping=kwargs.get("use_doc_unwarping", False),
            use_chart_recognition=kwargs.get("use_chart_recognition", False),
        ),
        priority=PRIORITY_PADDLEOCR,
    )
