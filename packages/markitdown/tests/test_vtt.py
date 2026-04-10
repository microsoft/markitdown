"""
Unit tests for WebVTT converter.
"""

import io
import pytest
from markitdown import MarkItDown
from markitdown.converters import VttConverter
from markitdown._stream_info import StreamInfo

# Sample WebVTT content for testing
SAMPLE_VTT = """WEBVTT

00:00:01.000 --> 00:00:03.000
Hello, welcome to the meeting.

00:00:04.000 --> 00:00:06.000
<v John> Today we'll discuss the project.

00:00:07.000 --> 00:00:09.000
<v Jane> I've prepared some slides.
"""

VTT_WITH_SPEAKERS = """WEBVTT

NOTE This is a test file

00:00:10.000 --> 00:00:12.000
<c.highlight>Important point here</c>

00:00:13.000 --> 00:00:15.000
<v.bob>Bob: This is what I think.
"""

VTT_MULTILINE = """WEBVTT

00:00:20.000 --> 00:00:25.000
This is the first line
and this continues the same cue
with a third line

00:00:26.000 --> 00:00:28.000
New paragraph here.
"""

VTT_EMPTY = """WEBVTT
"""

VTT_NO_HEADER = """00:00:01.000 --> 00:00:03.000
This file has no WEBVTT header.
"""


def test_vtt_converter_accepts_vtt_extension():
    """Test that VttConverter accepts .vtt files."""
    converter = VttConverter()
    info = StreamInfo(extension=".vtt", mimetype="text/vtt", charset="utf-8")
    stream = io.BytesIO(SAMPLE_VTT.encode())

    assert converter.accepts(stream, info) is True


def test_vtt_converter_accepts_vtt_mimetype():
    """Test that VttConverter accepts text/vtt MIME type."""
    converter = VttConverter()
    info = StreamInfo(extension=".txt", mimetype="text/vtt", charset="utf-8")
    stream = io.BytesIO(SAMPLE_VTT.encode())

    assert converter.accepts(stream, info) is True


def test_vtt_converter_accepts_webvtt_header():
    """Test that VttConverter detects WEBVTT header."""
    converter = VttConverter()
    info = StreamInfo(extension=".txt", mimetype=None, charset="utf-8")
    stream = io.BytesIO(SAMPLE_VTT.encode())

    assert converter.accepts(stream, info) is True


def test_vtt_converter_rejects_non_vtt():
    """Test that VttConverter rejects non-VTT files."""
    converter = VttConverter()
    info = StreamInfo(extension=".pdf", mimetype="application/pdf", charset=None)
    stream = io.BytesIO(b"Not a VTT file")

    assert converter.accepts(stream, info) is False


def test_basic_vtt_conversion():
    """Test basic WebVTT to Markdown conversion."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(SAMPLE_VTT.encode()), ".vtt")

    assert "Hello, welcome to the meeting." in result.markdown
    assert "John:" in result.markdown
    assert "Jane:" in result.markdown
    assert result.markdown.strip()


def test_vtt_speaker_tags():
    """Test handling of speaker voice tags."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(VTT_WITH_SPEAKERS.encode()), ".vtt")

    assert "Bob:" in result.markdown
    assert "Important point here" in result.markdown


def test_vtt_multiline_cues():
    """Test handling of multi-line cue text."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(VTT_MULTILINE.encode()), ".vtt")

    # Multi-line cues should be joined with spaces
    assert "first line" in result.markdown
    assert "continues the same cue" in result.markdown
    assert "third line" in result.markdown


def test_vtt_timestamps_removed():
    """Test that timestamps are not in the output text."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(SAMPLE_VTT.encode()), ".vtt")

    # Timestamps should be in [HH:MM:SS.mmm] format, not raw VTT format
    assert "00:00 -->" not in result.markdown
    assert "00:00:01.000 --> 00:00:03.000" not in result.markdown


def test_vtt_timestamps_in_output():
    """Test that timestamps appear in output in bracket format."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(SAMPLE_VTT.encode()), ".vtt")

    # Timestamps should appear in [HH:MM:SS.mmm] format
    assert "[00:00:01.000]" in result.markdown
    assert "[00:00:04.000]" in result.markdown


def test_vtt_webvtt_header_stripped():
    """Test that WEBVTT header is stripped from output."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(SAMPLE_VTT.encode()), ".vtt")

    assert "WEBVTT" not in result.markdown


def test_vtt_empty_file():
    """Test handling of empty VTT file."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(VTT_EMPTY.encode()), ".vtt")

    # Empty file should return empty or minimal markdown
    assert result.markdown.strip() == "" or "[00:" not in result.markdown


def test_vtt_html_tags_stripped():
    """Test that HTML-like tags are stripped."""
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(VTT_WITH_SPEAKERS.encode()), ".vtt")

    # Tags should be stripped
    assert "<c.highlight>" not in result.markdown
    assert "</c>" not in result.markdown
    assert "<v.bob>" not in result.markdown


def test_vtt_direct_converter():
    """Test using VttConverter directly."""
    converter = VttConverter()
    info = StreamInfo(extension=".vtt", mimetype="text/vtt", charset="utf-8")
    stream = io.BytesIO(SAMPLE_VTT.encode())

    result = converter.convert(stream, info)

    assert "Hello, welcome to the meeting." in result.markdown
    assert "John:" in result.markdown
    assert "[00:00:01.000]" in result.markdown
