"""Tests for the unified logging facade module."""
import logging
import io
import sys

import pytest

from markitdown import _logging


def setup_function():
    """Reset logging state before each test."""
    _logging._logger.handlers.clear()
    _logging._logger.addHandler(logging.NullHandler())
    _logging._logger.setLevel(logging.NOTSET)
    _logging._user_configured = False


def test_get_logger_returns_logger():
    """Test that get_logger returns a logger instance."""
    logger = _logging.get_logger()
    assert isinstance(logger, logging.Logger)
    assert logger.name == "markitdown"


def test_default_logging_has_null_handler():
    """Test that default logging has a NullHandler (no output)."""
    logger = _logging.get_logger()
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.NullHandler)


def test_is_configured_initially_false():
    """Test that is_configured returns False initially."""
    assert _logging.is_configured() is False


def test_configure_logging_sets_level():
    """Test that configure_logging sets the correct log level."""
    _logging.configure_logging(level=logging.DEBUG)
    assert _logging._logger.level == logging.DEBUG
    assert _logging.is_configured() is True


def test_configure_logging_with_custom_format():
    """Test that configure_logging accepts custom format."""
    custom_format = "%(levelname)s - %(message)s"
    _logging.configure_logging(format=custom_format)

    handler = _logging._logger.handlers[0]
    assert handler.formatter._fmt == custom_format


def test_configure_logging_with_custom_handler():
    """Test that configure_logging accepts custom handler."""
    stream = io.StringIO()
    custom_handler = logging.StreamHandler(stream)

    _logging.configure_logging(handler=custom_handler)

    assert len(_logging._logger.handlers) == 1
    assert _logging._logger.handlers[0] is custom_handler


def test_configure_logging_clears_existing_handlers(tmp_path):
    """Test that configure_logging clears existing handlers before adding new one."""
    # Add some handlers manually
    _logging._logger.handlers.clear()
    _logging._logger.addHandler(logging.StreamHandler())
    # Use a temp file instead of /dev/null for cross-platform compatibility
    temp_file = tmp_path / "test.log"
    _logging._logger.addHandler(logging.FileHandler(str(temp_file)))
    assert len(_logging._logger.handlers) == 2

    # Configure should clear and add one
    _logging.configure_logging()
    assert len(_logging._logger.handlers) == 1


def test_convenience_methods_debug():
    """Test that debug convenience method works."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    _logging.configure_logging(level=logging.DEBUG, handler=handler)

    _logging.debug("test debug message")
    handler.flush()

    assert "test debug message" in stream.getvalue()


def test_convenience_methods_info():
    """Test that info convenience method works."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    _logging.configure_logging(level=logging.INFO, handler=handler)

    _logging.info("test info message")
    handler.flush()

    assert "test info message" in stream.getvalue()


def test_convenience_methods_warning():
    """Test that warning convenience method works."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    _logging.configure_logging(level=logging.WARNING, handler=handler)

    _logging.warning("test warning message")
    handler.flush()

    assert "test warning message" in stream.getvalue()


def test_convenience_methods_error():
    """Test that error convenience method works."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    _logging.configure_logging(level=logging.ERROR, handler=handler)

    _logging.error("test error message")
    handler.flush()

    assert "test error message" in stream.getvalue()


def test_log_level_filtering():
    """Test that messages below the log level are filtered out."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    _logging.configure_logging(level=logging.WARNING, handler=handler)

    _logging.debug("debug message")  # Should be filtered
    _logging.info("info message")  # Should be filtered
    _logging.warning("warning message")  # Should pass

    handler.flush()
    output = stream.getvalue()

    assert "debug message" not in output
    assert "info message" not in output
    assert "warning message" in output


def test_multiple_configure_calls():
    """Test that multiple configure calls work correctly."""
    stream1 = io.StringIO()
    handler1 = logging.StreamHandler(stream1)
    _logging.configure_logging(level=logging.DEBUG, handler=handler1)

    _logging.debug("first message")
    handler1.flush()
    assert "first message" in stream1.getvalue()

    # Reconfigure with different handler and level
    stream2 = io.StringIO()
    handler2 = logging.StreamHandler(stream2)
    _logging.configure_logging(level=logging.ERROR, handler=handler2)

    _logging.debug("second debug")  # Should be filtered
    _logging.error("second error")  # Should pass

    handler2.flush()
    assert "second debug" not in stream2.getvalue()
    assert "second error" in stream2.getvalue()


def test_convenience_methods_with_args():
    """Test that convenience methods support format arguments."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    _logging.configure_logging(level=logging.INFO, handler=handler)

    _logging.info("Hello %s, you are %d years old", "Alice", 30)
    handler.flush()

    assert "Hello Alice, you are 30 years old" in stream.getvalue()


def test_convenience_methods_with_kwargs():
    """Test that convenience methods support keyword arguments (exc_info, etc.)."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    _logging.configure_logging(level=logging.ERROR, handler=handler)

    try:
        raise ValueError("test error")
    except ValueError:
        _logging.error("An error occurred", exc_info=True)

    handler.flush()
    output = stream.getvalue()
    assert "An error occurred" in output
    assert "ValueError" in output  # Should include traceback


def test_null_handler_by_default():
    """Test that without configuration, logging uses NullHandler (no output)."""
    # This should not produce any output even though we call error
    original_stderr = sys.stderr
    sys.stderr = io.StringIO()

    try:
        # Before configure, only NullHandler is present
        _logging.error("This should not appear anywhere")
        output = sys.stderr.getvalue()
        assert output == ""
    finally:
        sys.stderr = original_stderr
