"""Unified logging facade for MarkItDown.

This module provides a consistent logging interface used throughout MarkItDown.
"""
import logging
import sys
from typing import Optional

# Create package logger
_logger = logging.getLogger("markitdown")
_logger.addHandler(logging.NullHandler())  # Default to no output

# Track if user has configured logging
_user_configured = False


def get_logger() -> logging.Logger:
    """Get the MarkItDown package logger."""
    return _logger


def configure_logging(
    level: int = logging.INFO,
    format: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
) -> None:
    """Configure MarkItDown logging.

    Args:
        level: Log level (default: logging.INFO)
        format: Custom log format (default: "%(levelname)s:%(name)s:%(message)s")
        handler: Custom log handler (default: StreamHandler to stderr)
    """
    global _user_configured

    if format is None:
        format = "%(levelname)s:%(name)s:%(message)s"

    if handler is None:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(format))

    # Clear existing handlers
    _logger.handlers.clear()
    _logger.addHandler(handler)
    _logger.setLevel(level)
    _user_configured = True


def is_configured() -> bool:
    """Check if logging has been explicitly configured."""
    return _user_configured


# Convenience methods
def debug(msg: str, *args, **kwargs) -> None:
    _logger.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
    _logger.info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
    _logger.warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
    _logger.error(msg, *args, **kwargs)
