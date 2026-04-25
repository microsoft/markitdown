"""Tests for the RTF converter."""

import io
import pytest

from markitdown.converters._rtf_converter import RtfConverter, _rtf_to_markdown
from markitdown._base_converter import DocumentConverterResult
from markitdown._stream_info import StreamInfo


@pytest.fixture
def converter():
    return RtfConverter()


def _make_stream_info(extension=".rtf", mimetype="text/rtf", charset=None):
    return StreamInfo(extension=extension, mimetype=mimetype, charset=charset)


# ---- Basic acceptance tests ----

class TestRtfConverterAccepts:
    def test_accepts_rtf_extension(self, converter):
        stream = io.BytesIO(b"")
        info = _make_stream_info(extension=".rtf")
        assert converter.accepts(stream, info) is True

    def test_accepts_rtf_mimetype(self, converter):
        stream = io.BytesIO(b"")
        info = _make_stream_info(extension="", mimetype="text/rtf")
        assert converter.accepts(stream, info) is True

    def test_accepts_application_rtf_mimetype(self, converter):
        stream = io.BytesIO(b"")
        info = _make_stream_info(extension="", mimetype="application/rtf")
        assert converter.accepts(stream, info) is True

    def test_rejects_txt_extension(self, converter):
        stream = io.BytesIO(b"")
        info = _make_stream_info(extension=".txt", mimetype="")
        assert converter.accepts(stream, info) is False

    def test_rejects_html_mimetype(self, converter):
        stream = io.BytesIO(b"")
        info = _make_stream_info(extension="", mimetype="text/html")
        assert converter.accepts(stream, info) is False


# ---- Conversion tests ----

MINIMAL_RTF = rb"{\rtf1 Hello World}"
BOLD_RTF = rb"{\rtf1 {\b Bold Text}}"
ITALIC_RTF = rb"{\rtf1 {\i Italic Text}}"
UNDERLINE_RTF = rb"{\rtf1 {\ul Underline Text}}"
BOLD_ITALIC_RTF = rb"{\rtf1 {\b\i Bold Italic}}"
PARA_RTF = rb"{\rtf1 First\par Second}"
UNICODE_RTF = rb"{\rtf1 Euro sign: \u8364?}"
HEX_RTF = rb"{\rtf1 caf\'e9}"
TABLE_RTF = rb"{\rtf1 \trowd Cell1\cell Cell2\cell\row}"


class TestRtfConversion:
    def test_minimal_rtf(self, converter):
        result = converter.convert(io.BytesIO(MINIMAL_RTF), _make_stream_info())
        assert isinstance(result, DocumentConverterResult)
        assert "Hello World" in result.markdown

    def test_bold_text(self, converter):
        result = converter.convert(io.BytesIO(BOLD_RTF), _make_stream_info())
        assert "**Bold Text**" in result.markdown

    def test_italic_text(self, converter):
        result = converter.convert(io.BytesIO(ITALIC_RTF), _make_stream_info())
        assert "*Italic Text*" in result.markdown

    def test_underline_text(self, converter):
        result = converter.convert(io.BytesIO(UNDERLINE_RTF), _make_stream_info())
        assert "<u>Underline Text</u>" in result.markdown

    def test_bold_italic_text(self, converter):
        result = converter.convert(io.BytesIO(BOLD_ITALIC_RTF), _make_stream_info())
        assert "***Bold Italic***" in result.markdown

    def test_paragraph_break(self, converter):
        result = converter.convert(io.BytesIO(PARA_RTF), _make_stream_info())
        assert "First" in result.markdown
        assert "Second" in result.markdown

    def test_unicode_escape(self, converter):
        result = converter.convert(io.BytesIO(UNICODE_RTF), _make_stream_info())
        assert "\u20ac" in result.markdown  # Euro sign €

    def test_hex_escape(self, converter):
        result = converter.convert(io.BytesIO(HEX_RTF), _make_stream_info())
        assert "café" in result.markdown

    def test_table_conversion(self, converter):
        result = converter.convert(io.BytesIO(TABLE_RTF), _make_stream_info())
        assert "Cell1" in result.markdown
        assert "Cell2" in result.markdown
        assert "|" in result.markdown

    def test_empty_rtf(self, converter):
        result = converter.convert(io.BytesIO(rb"{\rtf1 }"), _make_stream_info())
        assert result.markdown == ""

    def test_skip_fonttbl_group(self, converter):
        rtf = rb"{\rtf1 {\fonttbl{\f0 Times New Roman;}}Hello}"
        result = converter.convert(io.BytesIO(rtf), _make_stream_info())
        # Font table content should not appear
        assert "Times New Roman" not in result.markdown
        assert "Hello" in result.markdown

    def test_skip_colortbl_group(self, converter):
        rtf = rb"{\rtf1 {\colortbl;\red255\green0\blue0;}Colored text}"
        result = converter.convert(io.BytesIO(rtf), _make_stream_info())
        assert "red255" not in result.markdown
        assert "Colored text" in result.markdown

    def test_latin1_fallback_encoding(self, converter):
        # Create RTF with bytes that are valid latin-1 but not valid UTF-8
        rtf = b"{\\rtf1 caf\\'\xe9}"  # é in latin-1
        result = converter.convert(io.BytesIO(rtf), _make_stream_info())
        assert "caf" in result.markdown

    def test_charset_specified_in_stream_info(self, converter):
        info = _make_stream_info(charset="latin-1")
        result = converter.convert(io.BytesIO(MINIMAL_RTF), info)
        assert "Hello World" in result.markdown

    def test_nested_groups(self, converter):
        rtf = rb"{\rtf1 {Outer {Inner text} Outer2}}"
        result = converter.convert(io.BytesIO(rtf), _make_stream_info())
        assert "Outer" in result.markdown
        assert "Inner text" in result.markdown
        assert "Outer2" in result.markdown

    def test_nonbreaking_space(self, converter):
        rtf = rb"{\rtf1 word\~word}"
        result = converter.convert(io.BytesIO(rtf), _make_stream_info())
        assert "word\u00a0word" in result.markdown

    def test_tab_control_word(self, converter):
        rtf = rb"{\rtf1 col1\tab col2}"
        result = converter.convert(io.BytesIO(rtf), _make_stream_info())
        assert "col1\tcol2" in result.markdown


# ---- Low-level function tests ----

class TestRtfToMarkdown:
    def test_plain_text(self):
        assert _rtf_to_markdown("{\\rtf1 plain text}") == "plain text"

    def test_multiple_paragraphs(self):
        md = _rtf_to_markdown("{\\rtf1 A\\par B\\par C}")
        assert "A" in md
        assert "B" in md
        assert "C" in md

    def test_style_reset_with_plain(self):
        md = _rtf_to_markdown("{\\rtf1 \\b bold\\plain normal}")
        assert "**bold**" in md
        assert "normal" in md
        # "normal" should not be bold
        assert "**normal**" not in md

    def test_negative_unicode_codepoint(self):
        # RTF uses negative numbers for codepoints > 32767
        md = _rtf_to_markdown("{\\rtf1 \\u-10179?}")
        # -10179 + 65536 = 55357 which is a surrogate, chr() may produce \ufffd
        assert len(md) > 0
