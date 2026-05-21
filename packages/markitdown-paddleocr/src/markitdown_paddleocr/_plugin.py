"""Plugin registration for markitdown-paddleocr."""

import logging
from typing import Any

from markitdown import MarkItDown

from ._converter import PaddleOcrConverter

__plugin_interface_version__ = 1

logger = logging.getLogger(__name__)


def register_converters(markitdown: MarkItDown, **kwargs: Any) -> None:
    """Register markitdown-paddleocr converter.

    Config sources (priority high to low):
    1. kwargs parameters
    2. Environment variables (BAIDU_PADDLE_TOKEN)
    3. Built-in defaults
    """
    logger.info("markitdown-paddleocr: 开始注册插件")

    # Register converter with higher priority than default PDF converter
    PRIORITY_PADDLEOCR = -1.0

    try:
        converter = PaddleOcrConverter(
            token=kwargs.get("token"),
            model=kwargs.get("model", "PaddleOCR-VL-1.5"),
            poll_interval=kwargs.get("poll_interval", 2.0),
            poll_timeout=kwargs.get("poll_timeout", 300.0),
            force_ai=kwargs.get("force_ai", False),
            use_doc_orientation_classify=kwargs.get(
                "use_doc_orientation_classify", False
            ),
            use_doc_unwarping=kwargs.get("use_doc_unwarping", False),
            use_chart_recognition=kwargs.get("use_chart_recognition", False),
        )
        markitdown.register_converter(
            converter,
            priority=PRIORITY_PADDLEOCR,
        )
        logger.info(
            "markitdown-paddleocr: 插件注册成功, priority=%.1f", PRIORITY_PADDLEOCR
        )
    except Exception as e:
        logger.error("markitdown-paddleocr: 插件注册失败, 错误=%s", e)
        raise
