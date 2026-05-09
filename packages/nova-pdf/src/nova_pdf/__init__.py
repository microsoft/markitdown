from ._plugin import register_converters
from ._config import NovaPdfConfig
from ._ai_service import AIService, AIResult
from ._converter import NovaPdfConverter

__plugin_interface_version__ = 1
__all__ = [
    "register_converters",
    "NovaPdfConfig",
    "AIService",
    "AIResult",
    "NovaPdfConverter",
]