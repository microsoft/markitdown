"""markitdown-paddleocr: PDF/Image to Markdown converter using PaddleOCR cloud API."""

from ._plugin import register_converters
from ._config import PaddleOcrConfig
from ._converter import PaddleOcrConverter
from ._paddle_client import PaddleClient
from ._dual_converter import DualOcrConverter

__plugin_interface_version__ = 1
__all__ = [
    "register_converters",
    "PaddleOcrConfig",
    "PaddleOcrConverter",
    "PaddleClient",
    "DualOcrConverter",
]
