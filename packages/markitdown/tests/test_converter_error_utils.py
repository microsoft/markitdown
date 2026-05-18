"""Unit tests for _converter_error_utils.py — shared error-handling utilities.

Covers:
- report_missing_dependency() import error reporting
- conversion_error_handler() decorator
- safe_read / safe_seek / safe_tell helpers
- stream_position_guard() context manager
"""

import io
import sys
import pytest

from markitdown._exceptions import (
    FileConversionException,
    MissingDependencyException,
    MISSING_DEPENDENCY_MESSAGE,
)
from markitdown._base_converter import DocumentConverterResult
from markitdown._stream_info import StreamInfo
from markitdown.converters._converter_error_utils import (
    report_missing_dependency,
    conversion_error_handler,
    safe_read,
    safe_seek,
    safe_tell,
    stream_position_guard,
)


# ============================================================
# report_missing_dependency
# ============================================================


def test_report_missing_dependency_raises_with_formatted_message():
    with pytest.raises(MissingDependencyException) as exc:
        report_missing_dependency("DocxConverter", ".docx", "docx")
    msg = str(exc.value)
    assert "DocxConverter" in msg
    assert ".docx" in msg
    assert "docx" in msg


def test_report_missing_dependency_with_exc_info_preserves_traceback():
    try:
        raise ImportError("No module named 'python-docx'")
    except ImportError:
        exc_info = sys.exc_info()

    with pytest.raises(MissingDependencyException) as exc:
        report_missing_dependency(
            "PptxConverter", ".pptx", "pptx", exc_info=exc_info
        )
    assert "PptxConverter" in str(exc.value)
    assert exc.value.__traceback__ is not None


def test_report_missing_dependency_raises_exception():
    """verify report_missing_dependency always raises (never returns)."""
    with pytest.raises(MissingDependencyException):
        report_missing_dependency("TestConverter", ".test", "test")


# ============================================================
# conversion_error_handler decorator
# ============================================================


class _FakeConverter:
    def __init__(self):
        self._stream = io.BytesIO(b"fake")

    @conversion_error_handler("FakeConverter")
    def convert_ok(self, file_stream, stream_info, **kwargs):
        return DocumentConverterResult(markdown="success")

    @conversion_error_handler("FakeConverter")
    def convert_raises_random(self, file_stream, stream_info, **kwargs):
        raise RuntimeError("something went wrong")

    @conversion_error_handler(
        "FakeConverter", reraise_on=(ValueError,)
    )
    def convert_raises_reraisable(self, file_stream, stream_info, **kwargs):
        raise ValueError("reraisable error")

    @conversion_error_handler("FakeConverter")
    def convert_raises_fce(self, file_stream, stream_info, **kwargs):
        raise FileConversionException("already wrapped")

    @conversion_error_handler(
        "FakeConverter", reraise_on=(MissingDependencyException,)
    )
    def convert_raises_missing_dep(self, file_stream, stream_info, **kwargs):
        raise MissingDependencyException("missing dep")


def test_conversion_error_handler_success():
    conv = _FakeConverter()
    si = StreamInfo(extension=".fake")
    result = conv.convert_ok(io.BytesIO(b"data"), si)
    assert result.markdown == "success"


def test_conversion_error_handler_wraps_random_error():
    conv = _FakeConverter()
    si = StreamInfo(extension=".fake")
    with pytest.raises(FileConversionException) as exc:
        conv.convert_raises_random(io.BytesIO(b"data"), si)
    assert "FakeConverter failed" in str(exc.value)
    assert "something went wrong" in str(exc.value)


def test_conversion_error_handler_reraise_on_bypasses_wrap():
    conv = _FakeConverter()
    si = StreamInfo(extension=".fake")
    with pytest.raises(ValueError, match="reraisable error"):
        conv.convert_raises_reraisable(io.BytesIO(b"data"), si)


def test_conversion_error_handler_passes_through_fce():
    """FileConversionException should not be double-wrapped."""
    conv = _FakeConverter()
    si = StreamInfo(extension=".fake")
    with pytest.raises(FileConversionException, match="already wrapped"):
        conv.convert_raises_fce(io.BytesIO(b"data"), si)


def test_conversion_error_handler_reraise_missing_dependency():
    conv = _FakeConverter()
    si = StreamInfo(extension=".fake")
    with pytest.raises(MissingDependencyException, match="missing dep"):
        conv.convert_raises_missing_dep(io.BytesIO(b"data"), si)


# ============================================================
# safe_read / safe_seek / safe_tell
# ============================================================


def test_safe_read_normal():
    stream = io.BytesIO(b"hello world")
    assert safe_read(stream, 5) == b"hello"
    assert safe_read(stream) == b" world"


def test_safe_read_empty():
    stream = io.BytesIO(b"")
    assert safe_read(stream) == b""


def test_safe_read_closed_stream():
    stream = io.BytesIO(b"data")
    stream.close()
    result = safe_read(stream)
    assert result == b""
    assert isinstance(result, bytes)


def test_safe_read_none_stream():
    """safe_read on None should return empty bytes (AttributeError caught)."""
    result = safe_read(None, 10)
    assert result == b""


def test_safe_seek_normal():
    stream = io.BytesIO(b"hello world")
    assert safe_seek(stream, 6) is True
    assert stream.tell() == 6


def test_safe_seek_closed():
    stream = io.BytesIO(b"data")
    stream.close()
    assert safe_seek(stream, 0) is False


def test_safe_tell_normal():
    stream = io.BytesIO(b"hello")
    stream.read(3)
    assert safe_tell(stream) == 3


def test_safe_tell_closed():
    stream = io.BytesIO(b"data")
    stream.close()
    assert safe_tell(stream) == 0


# ============================================================
# stream_position_guard
# ============================================================


def test_stream_position_guard_restores_on_success():
    stream = io.BytesIO(b"hello world")
    stream.read(6)  # position at 6
    with stream_position_guard(stream):
        stream.read(5)  # read to 11
        assert stream.tell() == 11
    # should be restored to 6
    assert stream.tell() == 6


def test_stream_position_guard_restores_on_exception():
    stream = io.BytesIO(b"hello world")
    stream.read(3)  # position at 3
    try:
        with stream_position_guard(stream):
            stream.read(5)
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    # should be restored to 3
    assert stream.tell() == 3


def test_stream_position_guard_does_not_suppress_exception():
    stream = io.BytesIO(b"data")
    with pytest.raises(ValueError):
        with stream_position_guard(stream):
            stream.read(1)
            raise ValueError("should propagate")


def test_stream_position_guard_zero_start():
    stream = io.BytesIO(b"hello")
    with stream_position_guard(stream):
        stream.read(5)
    assert stream.tell() == 0


# ============================================================
# MISSING_DEPENDENCY_MESSAGE format string validation
# ============================================================


def test_missing_dependency_message_format_works():
    msg = MISSING_DEPENDENCY_MESSAGE.format(
        converter="XlsxConverter",
        extension=".xlsx",
        feature="xlsx",
    )
    assert "XlsxConverter" in msg
    assert ".xlsx" in msg
    assert "xlsx" in msg
    assert "pip install" in msg
