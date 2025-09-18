"""MarkItDown API server module."""

from .__about__ import __version__

from .api import app
from .config import Settings

__all__ = ["app", "Settings", "__version__"]