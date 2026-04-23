#!/usr/bin/env python3 -m pytest
"""Tests for specific bug fixes."""
import io
import os
import tempfile

import pytest

from markitdown import MarkItDown, StreamInfo

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


class TestRssNoTitleBug:
    """Test fix for: RSS converter crashes with NameError when feed has no channel title."""

    def test_rss_no_channel_title(self):
        """An RSS feed with no <title> in <channel> should not crash."""
        rss_no_title = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <description>A feed without a title</description>
    <item>
      <title>Item Title</title>
      <description>Item description</description>
    </item>
  </channel>
</rss>"""
        markitdown = MarkItDown()
        result = markitdown.convert_stream(
            io.BytesIO(rss_no_title.encode("utf-8")),
            file_extension=".rss",
        )
        assert "Item Title" in result.text_content
        assert "Item description" in result.text_content

    def test_rss_no_channel_title_or_description(self):
        """An RSS feed with no title or description should still work."""
        rss_minimal = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>Only Item</title>
    </item>
  </channel>
</rss>"""
        markitdown = MarkItDown()
        result = markitdown.convert_stream(
            io.BytesIO(rss_minimal.encode("utf-8")),
            file_extension=".rss",
        )
        assert "Only Item" in result.text_content


class TestCsvPipeEscape:
    """Test fix for: CSV converter doesn't escape pipe characters in cell values."""

    def test_csv_pipe_in_cell(self):
        """CSV cells containing | should be escaped in markdown output."""
        csv_with_pipe = "Name,Description\nTest,hello | world\n"
        markitdown = MarkItDown()
        result = markitdown.convert_stream(
            io.BytesIO(csv_with_pipe.encode("utf-8")),
            file_extension=".csv",
            mimetype="text/csv",
        )
        # The pipe inside the cell should be escaped
        assert "hello \\| world" in result.text_content
        # Header should be unaffected
        assert "| Name | Description |" in result.text_content


class TestWikipediaLanguageSubdomains:
    """Test fix for: Wikipedia converter rejects valid language subdomains."""

    def test_wikipedia_standard_subdomain(self):
        """Standard 2-letter language codes should still work."""
        from markitdown.converters._wikipedia_converter import WikipediaConverter

        converter = WikipediaConverter()
        stream_info = StreamInfo(
            mimetype="text/html",
            extension=".html",
            url="https://en.wikipedia.org/wiki/Test",
        )
        assert converter.accepts(io.BytesIO(b""), stream_info)

    def test_wikipedia_hyphenated_subdomain(self):
        """Hyphenated language codes like be-tarask should be accepted."""
        from markitdown.converters._wikipedia_converter import WikipediaConverter

        converter = WikipediaConverter()
        stream_info = StreamInfo(
            mimetype="text/html",
            extension=".html",
            url="https://be-tarask.wikipedia.org/wiki/Test",
        )
        assert converter.accepts(io.BytesIO(b""), stream_info)

    def test_wikipedia_multi_char_subdomain(self):
        """Long language codes like zh-classical should be accepted."""
        from markitdown.converters._wikipedia_converter import WikipediaConverter

        converter = WikipediaConverter()
        stream_info = StreamInfo(
            mimetype="text/html",
            extension=".html",
            url="https://zh-classical.wikipedia.org/wiki/Test",
        )
        assert converter.accepts(io.BytesIO(b""), stream_info)

    def test_wikipedia_numeric_subdomain(self):
        """Numeric language codes should be accepted."""
        from markitdown.converters._wikipedia_converter import WikipediaConverter

        converter = WikipediaConverter()
        stream_info = StreamInfo(
            mimetype="text/html",
            extension=".html",
            url="https://roa-rup.wikipedia.org/wiki/Test",
        )
        assert converter.accepts(io.BytesIO(b""), stream_info)


if __name__ == "__main__":
    for test in [
        TestRssNoTitleBug().test_rss_no_channel_title,
        TestRssNoTitleBug().test_rss_no_channel_title_or_description,
        TestCsvPipeEscape().test_csv_pipe_in_cell,
        TestWikipediaLanguageSubdomains().test_wikipedia_standard_subdomain,
        TestWikipediaLanguageSubdomains().test_wikipedia_hyphenated_subdomain,
        TestWikipediaLanguageSubdomains().test_wikipedia_multi_char_subdomain,
        TestWikipediaLanguageSubdomains().test_wikipedia_numeric_subdomain,
    ]:
        print(f"Running {test.__name__}...", end="")
        test()
        print("OK")
    print("All tests passed!")
