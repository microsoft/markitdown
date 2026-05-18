"""Unit tests for _exceptions.py — exception hierarchy and helpers.

Covers:
- Exception inheritance chains
- FileConversionException with nested attempts
- FailedConversionAttempt construction and exc_info access
"""

import sys
import pytest

from markitdown._exceptions import (
    MarkItDownException,
    MissingDependencyException,
    UnsupportedFormatException,
    FileConversionException,
    FailedConversionAttempt,
    MISSING_DEPENDENCY_MESSAGE,
)
from markitdown._base_converter import DocumentConverter


class _DummyConverter(DocumentConverter):
    pass


# ============================================================
# Hierarchy
# ============================================================


def test_markitdown_exception_is_base():
    assert issubclass(MissingDependencyException, MarkItDownException)
    assert issubclass(UnsupportedFormatException, MarkItDownException)
    assert issubclass(FileConversionException, MarkItDownException)


def test_exception_can_be_caught_as_base():
    with pytest.raises(MarkItDownException):
        raise MissingDependencyException("test")


# ============================================================
# MissingDependencyException
# ============================================================


def test_missing_dependency_message():
    msg = MISSING_DEPENDENCY_MESSAGE.format(
        converter="PdfConverter",
        extension=".pdf",
        feature="pdf",
    )
    assert "PdfConverter" in msg
    assert ".pdf" in msg
    assert "pdf" in msg
    assert "pip install" in msg


def test_missing_dependency_exception():
    exc = MissingDependencyException("Missing: xlsx")
    assert "Missing: xlsx" in str(exc)
    assert isinstance(exc, MarkItDownException)


# ============================================================
# UnsupportedFormatException
# ============================================================


def test_unsupported_format_message():
    exc = UnsupportedFormatException("No converter found")
    assert "No converter found" in str(exc)


# ============================================================
# FileConversionException
# ============================================================


def test_file_conversion_exception_empty():
    exc = FileConversionException()
    assert str(exc) == "File conversion failed."
    assert exc.attempts is None


def test_file_conversion_exception_with_message():
    exc = FileConversionException(message="Custom error")
    assert "Custom error" in str(exc)


def test_file_conversion_exception_with_attempts():
    converter = _DummyConverter()
    attempt = FailedConversionAttempt(
        converter=converter,
        exc_info=(RuntimeError, RuntimeError("boom"), None),
    )
    exc = FileConversionException(attempts=[attempt])
    assert len(exc.attempts) == 1
    assert exc.attempts[0].converter is converter
    # exc_info is a tuple: (type, value, traceback)
    assert exc.attempts[0].exc_info[0] is RuntimeError
    assert "boom" in str(exc.attempts[0].exc_info[1])


def test_file_conversion_exception_multiple_attempts():
    c1 = _DummyConverter()
    c2 = _DummyConverter()
    exc = FileConversionException(attempts=[
        FailedConversionAttempt(converter=c1, exc_info=(ValueError, ValueError("e1"), None)),
        FailedConversionAttempt(converter=c2, exc_info=(TypeError, TypeError("e2"), None)),
    ])
    assert len(exc.attempts) == 2
    assert "2 attempts" in str(exc)
    assert "e1" in str(exc)
    assert "e2" in str(exc)


# ============================================================
# FailedConversionAttempt
# ============================================================


def test_failed_attempt_without_exc_info():
    converter = _DummyConverter()
    attempt = FailedConversionAttempt(converter=converter, exc_info=None)
    assert attempt.converter is converter
    assert attempt.exc_info is None


def test_failed_attempt_with_exc_info():
    converter = _DummyConverter()
    attempt = FailedConversionAttempt(
        converter=converter,
        exc_info=(ValueError, ValueError("test error"), None),
    )
    assert attempt.exc_info[0] is ValueError
    assert "test error" in str(attempt.exc_info[1])


def test_failed_attempt_with_live_exc_info():
    """exc_info from sys.exc_info() should be stored."""
    converter = _DummyConverter()
    try:
        raise RuntimeError("traceback test")
    except RuntimeError:
        exc_info = sys.exc_info()
        attempt = FailedConversionAttempt(converter=converter, exc_info=exc_info)
    assert attempt.exc_info[0] is RuntimeError
    assert "traceback test" in str(attempt.exc_info[1])
    assert attempt.exc_info[2] is not None  # traceback


def test_file_conversion_exception_message_no_exc_info():
    """attempts with None exc_info → different message."""
    exc = FileConversionException(attempts=[
        FailedConversionAttempt(converter=_DummyConverter(), exc_info=None),
    ])
    assert "provided no execution info" in str(exc)


def test_file_conversion_exception_message_with_exc_info():
    """attempts with exc_info → includes exception type and message."""
    exc = FileConversionException(attempts=[
        FailedConversionAttempt(
            converter=_DummyConverter(),
            exc_info=(RuntimeError, RuntimeError("done"), None),
        ),
    ])
    assert "_DummyConverter" in str(exc)
    assert "RuntimeError" in str(exc)
    assert "done" in str(exc)
