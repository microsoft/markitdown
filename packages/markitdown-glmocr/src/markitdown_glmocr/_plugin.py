"""Plugin registration for markitdown-glmocr."""

import logging
from typing import Any

from markitdown import MarkItDown

from ._converter import GlmOcrConverter

__plugin_interface_version__ = 1

logger = logging.getLogger(__name__)


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """
    Register markitdown-glmocr converter.

    Config sources (priority high to low):
    1. kwargs parameters
    2. Environment variables (ZHIPU_API_KEY)
    3. .env file
    4. Built-in defaults
    """
    logger.info("markitdown-glmocr: 开始注册插件")

    # Register converter
    # Priority -2.0: higher priority than PaddleOcrConverter (-1.0),
    # so glmocr is tried first and paddleocr serves as fallback.
    PRIORITY_GLMOCR = -2.0

    try:
        converter = GlmOcrConverter(
            api_key=kwargs.get("api_key"),
            timeout=kwargs.get("timeout", 1800),
            enable_layout=kwargs.get("enable_layout", False),
            force_ai=kwargs.get("force_ai", False),
        )
        markitdown.register_converter(
            converter,
            priority=PRIORITY_GLMOCR,
        )
        logger.info("markitdown-glmocr: 插件注册成功, priority=%.1f", PRIORITY_GLMOCR)
    except Exception as e:
        logger.error("markitdown-glmocr: 插件注册失败, 错误=%s", e)
        raise
