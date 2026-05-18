"""
Shared error-handling utilities for MarkItDown converters.

Provides consistent patterns for:
- Wrapping conversion logic with standardized error handling
- Reporting import/dependency errors
- Handling corrupt or unreadable input gracefully
"""

import functools
import logging
import sys
from typing import Callable, Any, Optional, Type

from .._base_converter import DocumentConverterResult
from .._exceptions import (
    FileConversionException,
    MissingDependencyException,
    MISSING_DEPENDENCY_MESSAGE,
)

logger = logging.getLogger(__name__)

# ── Import error reporting ────────────────────────────────────────────


def report_missing_dependency(
    converter_name: str,
    extension: str,
    feature: str,
    exc_info: Optional[tuple] = None,
) -> None:
    """Raise a MissingDependencyException with a clear installation hint.

    Args:
        converter_name: Human-readable converter name (e.g. "DocxConverter").
        extension: The file extension this converter handles (e.g. ".docx").
        feature: The pip extra name for the missing dependency (e.g. "docx").
        exc_info: Optional sys.exc_info() tuple from the original ImportError.
    """
    message = MISSING_DEPENDENCY_MESSAGE.format(
        converter=converter_name,
        extension=extension,
        feature=feature,
    )
    exc = MissingDependencyException(message)
    if exc_info:
        exc = exc.with_traceback(exc_info[2])
    raise exc


# ── Conversion error wrapper ──────────────────────────────────────────


def conversion_error_handler(
    converter_name: str,
    *,
    reraise_on: tuple = (),
) -> Callable:
    """Decorator that wraps converter.convert() with consistent error handling.

    By default, unexpected errors are caught and re-raised as
    FileConversionException so the caller (MarkItDown engine) can
    handle them uniformly.

    Specify `reraise_on` to let certain exceptions propagate unchanged
    (e.g., MissingDependencyException should bubble up directly).

    Example:
        @conversion_error_handler("CsvConverter", reraise_on=(MissingDependencyException,))
        def convert(self, file_stream, stream_info, **kwargs):
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, file_stream, stream_info, **kwargs: Any) -> Any:
            try:
                return func(self, file_stream, stream_info, **kwargs)
            except reraise_on:
                raise  # Let these propagate unchanged
            except FileConversionException:
                raise  # Already wrapped, don't double-wrap
            except Exception as e:
                logger.warning(
                    "%s.convert() failed for %s: %s",
                    converter_name,
                    getattr(stream_info, "filename", stream_info.extension or "?"),
                    e,
                )
                raise FileConversionException(
                    f"{converter_name} failed: {e}"
                ) from e

        return wrapper

    return decorator


# ── Safe stream read helpers ──────────────────────────────────────────


def safe_read(stream, size: int = -1) -> bytes:
    """Read from a stream, returning empty bytes on failure instead of raising."""
    try:
        return stream.read(size)
    except (OSError, ValueError, AttributeError) as e:
        logger.warning("safe_read: stream read failed: %s", e)
        return b""


def safe_seek(stream, position: int) -> bool:
    """Seek a stream, returning True on success, False on failure."""
    try:
        stream.seek(position)
        return True
    except (OSError, ValueError, AttributeError) as e:
        logger.warning("safe_seek: stream seek failed: %s", e)
        return False


def safe_tell(stream) -> int:
    """Tell stream position, returning 0 on failure."""
    try:
        return stream.tell()
    except (OSError, ValueError, AttributeError) as e:
        logger.warning("safe_tell: stream tell failed: %s", e)
        return 0


def stream_position_guard(stream):
    """Context manager that saves/restores stream position on exception.

    Usage:
        with stream_position_guard(file_stream):
            data = file_stream.read(100)
            # ... do something with peeked data ...
        # stream position is restored even on error
    """
    return _StreamPositionGuard(stream)


class _StreamPositionGuard:
    def __init__(self, stream):
        self._stream = stream
        self._pos = None

    def __enter__(self):
        self._pos = safe_tell(self._stream)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._pos is not None:
            safe_seek(self._stream, self._pos)
        return False  # Don't suppress exceptions
