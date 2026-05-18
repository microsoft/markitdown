#!/usr/bin/env python3 -m pytest
"""Tests for markitdown-sample-plugin — covers accepts(), convert(), register_converters(), and edge cases."""

import io
import os

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown_sample_plugin import (
    RtfConverter,
    __plugin_interface_version__,
    register_converters,
)
from markitdown_sample_plugin._plugin import (
    ACCEPTED_FILE_EXTENSIONS,
    ACCEPTED_MIME_TYPE_PREFIXES,
)

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

RTF_TEST_STRINGS = {
    "This is a Sample RTF File",
    "It is included to test if the MarkItDown sample plugin can correctly convert RTF files.",
}


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_plugin_interface_version_is_int(self):
        assert isinstance(__plugin_interface_version__, int)
        assert __plugin_interface_version__ >= 1

    def test_accepted_extensions(self):
        assert ".rtf" in ACCEPTED_FILE_EXTENSIONS
        assert all(ext.startswith(".") for ext in ACCEPTED_FILE_EXTENSIONS)

    def test_accepted_mime_prefixes(self):
        assert "text/rtf" in ACCEPTED_MIME_TYPE_PREFIXES
        assert "application/rtf" in ACCEPTED_MIME_TYPE_PREFIXES


# ---------------------------------------------------------------------------
# accepts() — acceptance logic
# ---------------------------------------------------------------------------

class TestAccepts:
    def setup_method(self):
        self.converter = RtfConverter()
        self.dummy_stream = io.BytesIO(b"dummy")

    def _accepts(self, extension=".rtf", mimetype="text/rtf", charset=None):
        si = StreamInfo(
            mimetype=mimetype,
            extension=extension,
            filename=f"test{extension}",
            charset=charset,
        )
        return self.converter.accepts(self.dummy_stream, si)

    # --- extension matching ---
    @pytest.mark.parametrize("ext", [".rtf", ".RTF", ".Rtf"])
    def test_accepts_by_extension(self, ext):
        assert self._accepts(extension=ext, mimetype="") is True

    def test_rejects_non_rtf_extension(self):
        assert self._accepts(extension=".pdf", mimetype="") is False
        assert self._accepts(extension=".docx", mimetype="") is False

    # --- mimetype matching ---
    @pytest.mark.parametrize("mime", ["text/rtf", "application/rtf"])
    def test_accepts_by_mimetype(self, mime):
        assert self._accepts(extension="", mimetype=mime) is True

    @pytest.mark.parametrize("mime", ["text/plain", "application/pdf", "image/png"])
    def test_rejects_non_rtf_mimetype(self, mime):
        assert self._accepts(extension="", mimetype=mime) is False

    # --- edge cases: None values ---
    def test_accepts_none_mimetype(self):
        """None mimetype should not crash (treated as empty string)."""
        si = StreamInfo(mimetype=None, extension=".rtf", filename="test.rtf")
        assert self.converter.accepts(self.dummy_stream, si) is True

    def test_accepts_none_extension(self):
        """None extension should not crash."""
        si = StreamInfo(mimetype="text/rtf", extension=None, filename="test")
        assert self.converter.accepts(self.dummy_stream, si) is True

    def test_rejects_both_none(self):
        """Both None → no match."""
        si = StreamInfo(mimetype=None, extension=None, filename="test")
        assert self.converter.accepts(self.dummy_stream, si) is False

    # --- extension takes priority ---
    def test_extension_over_mimetype(self):
        """Extension match should return True even with wrong mimetype."""
        assert self._accepts(extension=".rtf", mimetype="application/pdf") is True


# ---------------------------------------------------------------------------
# convert() — conversion logic
# ---------------------------------------------------------------------------

class TestConvert:
    def test_converter_extracts_text(self):
        """Tests the RTF converter directly."""
        with open(os.path.join(TEST_FILES_DIR, "test.rtf"), "rb") as file_stream:
            converter = RtfConverter()
            result = converter.convert(
                file_stream=file_stream,
                stream_info=StreamInfo(
                    mimetype="text/rtf", extension=".rtf", filename="test.rtf"
                ),
            )
            for test_string in RTF_TEST_STRINGS:
                assert test_string in result.text_content

    def test_convert_returns_none_title(self):
        """RTF converter does not extract title."""
        with open(os.path.join(TEST_FILES_DIR, "test.rtf"), "rb") as file_stream:
            result = RtfConverter().convert(
                file_stream=file_stream,
                stream_info=StreamInfo(mimetype="text/rtf", extension=".rtf", filename="test.rtf"),
            )
            assert result.title is None

    def test_convert_empty_rtf(self):
        """Empty/minimal RTF should not crash."""
        minimal_rtf = b"{\\rtf1\\ansi }"
        result = RtfConverter().convert(
            file_stream=io.BytesIO(minimal_rtf),
            stream_info=StreamInfo(mimetype="text/rtf", extension=".rtf", filename="empty.rtf"),
        )
        assert isinstance(result.text_content, str)

    def test_convert_with_charset(self):
        """Explicit charset in StreamInfo should be used."""
        with open(os.path.join(TEST_FILES_DIR, "test.rtf"), "rb") as file_stream:
            result = RtfConverter().convert(
                file_stream=file_stream,
                stream_info=StreamInfo(
                    mimetype="text/rtf", extension=".rtf", filename="test.rtf", charset="utf-8"
                ),
            )
            for test_string in RTF_TEST_STRINGS:
                assert test_string in result.text_content


# ---------------------------------------------------------------------------
# register_converters() — plugin integration
# ---------------------------------------------------------------------------

class TestPluginIntegration:
    def test_markitdown_loads_plugin(self):
        """Tests that MarkItDown correctly loads the plugin via enable_plugins."""
        md = MarkItDown(enable_plugins=True)
        result = md.convert(os.path.join(TEST_FILES_DIR, "test.rtf"))
        for test_string in RTF_TEST_STRINGS:
            assert test_string in result.text_content

    def test_register_converters_attaches_rtf(self):
        """register_converters should attach an RtfConverter to MarkItDown."""
        md = MarkItDown(enable_plugins=False)
        # Manually call register to verify it works
        register_converters(md)
        # Check that RTF files are now accepted
        result = md.convert(os.path.join(TEST_FILES_DIR, "test.rtf"))
        assert "Sample RTF" in result.text_content

    def test_markitdown_without_plugins_ignores_rtf(self):
        """Without enable_plugins, MarkItDown should not handle .rtf files natively."""
        md = MarkItDown(enable_plugins=False)
        result = md.convert(os.path.join(TEST_FILES_DIR, "test.rtf"))
        # Without the plugin, the raw RTF control codes should remain
        assert "\\rtf1" in result.text_content.lower() or "\\" in result.text_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
