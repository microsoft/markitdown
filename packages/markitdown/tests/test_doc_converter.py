"""Tests for DocConverter (.doc file support)."""

import io
from unittest.mock import MagicMock, patch

import pytest

from markitdown.converters._doc_converter import DocConverter
from markitdown._stream_info import StreamInfo


def test_doc_converter_accepts_doc_extension():
    """Test that DocConverter accepts .doc files."""
    converter = DocConverter()
    stream_info = StreamInfo(extension=".doc")
    assert converter.accepts(io.BytesIO(), stream_info) is True


def test_doc_converter_accepts_doc_mimetype():
    """Test that DocConverter accepts application/msword MIME type."""
    converter = DocConverter()
    stream_info = StreamInfo(mimetype="application/msword")
    assert converter.accepts(io.BytesIO(), stream_info) is True


def test_doc_converter_rejects_other_extensions():
    """Test that DocConverter rejects non-.doc files."""
    converter = DocConverter()
    stream_info = StreamInfo(extension=".docx")
    assert converter.accepts(io.BytesIO(), stream_info) is False


@patch("markitdown.converters._doc_converter.unword")
def test_doc_converter_convert(mock_unword):
    """Test that DocConverter converts .doc files correctly."""
    # Mock the unword.parse_doc function
    mock_doc = MagicMock()
    mock_doc.body_text = "This is test content from a .doc file"
    mock_unword.parse_doc.return_value = mock_doc

    converter = DocConverter()
    stream_info = StreamInfo(extension=".doc")
    file_content = b"fake .doc file content"

    result = converter.convert(io.BytesIO(file_content), stream_info)

    assert result.markdown == "This is test content from a .doc file"
    mock_unword.parse_doc.assert_called_once_with(file_content)
