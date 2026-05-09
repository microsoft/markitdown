from ._plugin import register_converters
from ._config import GlmOcrConfig
from ._ai_service import AIService, AIResult
from ._converter import GlmOcrPdfConverter

__plugin_interface_version__ = 1
__all__ = [
    "register_converters",
    "GlmOcrConfig",
    "AIService",
    "AIResult",
    "GlmOcrPdfConverter",
]