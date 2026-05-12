"""markitdown-glmocr: Intelligent PDF to Markdown converter using glmocr SDK."""

from ._plugin import register_converters
from ._config import GlmOcrConfig
from ._converter import GlmOcrConverter

__plugin_interface_version__ = 1
__all__ = [
    "register_converters",
    "GlmOcrConfig",
    "GlmOcrConverter",
]