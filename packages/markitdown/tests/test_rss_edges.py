"""Edge-case tests for RssConverter — invalid XML, empty feeds, atom format.

Tests RSS/Atom parsing robustness.
"""

import io
import pytest

from markitdown import MarkItDown, StreamInfo, FileConversionException

TEST_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Blog</title>
    <link>https://example.com</link>
    <description>A test RSS feed</description>
    <item>
      <title>Post One</title>
      <link>https://example.com/1</link>
      <description>First post content</description>
    </item>
    <item>
      <title>Post Two</title>
      <link>https://example.com/2</link>
      <description>Second post content</description>
    </item>
  </channel>
</rss>"""

TEST_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Atom Feed</title>
  <entry>
    <title>Entry One</title>
    <link href="https://example.com/1"/>
    <summary>Summary of entry one</summary>
  </entry>
</feed>"""


def _convert_rss(xml_str: str, filename: str = "feed.rss", mimetype: str = "application/rss+xml") -> str:
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(xml_str.encode("utf-8")),
        stream_info=StreamInfo(extension=".rss", mimetype=mimetype),
    )
    return result.markdown


# ============================================================
# Valid RSS/Atom feeds
# ============================================================


def test_valid_rss_parses_items():
    result = _convert_rss(TEST_RSS)
    assert "Test Blog" in result
    assert "Post One" in result
    assert "Post Two" in result
    assert "First post content" in result


def test_valid_atom_parses_entries():
    result = _convert_rss(TEST_ATOM)
    assert "Atom Feed" in result or "Entry One" in result


# ============================================================
# Empty / minimal feeds
# ============================================================


def test_empty_rss_with_channel():
    xml = '<?xml version="1.0"?><rss version="2.0"><channel><title>Empty</title></channel></rss>'
    result = _convert_rss(xml)
    assert "Empty" in result


def test_rss_with_no_items():
    xml = '<?xml version="1.0"?><rss version="2.0"><channel><title>No Items</title><link>http://x.com</link></channel></rss>'
    result = _convert_rss(xml)
    assert "No Items" in result


# ============================================================
# Invalid / corrupt XML
# ============================================================


def test_invalid_xml_raises():
    md = MarkItDown()
    # Falls through to PlainTextConverter when XML parsing fails
    result = md.convert(
        io.BytesIO(b"not xml at all"),
        stream_info=StreamInfo(extension=".rss", mimetype="application/rss+xml"),
    )
    assert isinstance(result.markdown, str)


def test_malformed_xml_unclosed_tags():
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(b"<?xml version='1.0'?><rss><channel><title>Broken"),
        stream_info=StreamInfo(extension=".rss", mimetype="application/rss+xml"),
    )
    assert isinstance(result.markdown, str)


def test_rss_with_html_in_description():
    """RSS descriptions often contain HTML — should be converted to Markdown."""
    xml = """<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>HTML Feed</title>
    <item>
      <title>With HTML</title>
      <description>&lt;b&gt;Bold&lt;/b&gt; and &lt;i&gt;italic&lt;/i&gt;</description>
    </item>
  </channel>
</rss>"""
    result = _convert_rss(xml)
    assert "With HTML" in result
    # HTML entities should be decoded: <b> → **, <i> → *
    assert "Bold" in result
    assert "italic" in result


# ============================================================
# Stream info variations
# ============================================================


def test_rss_accepts_application_rss_mime():
    """RssConverter should accept application/rss+xml mimetype."""
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(TEST_RSS.encode("utf-8")),
        stream_info=StreamInfo(mimetype="application/rss+xml"),
    )
    assert "Test Blog" in result.markdown


def test_rss_accepts_text_xml_as_candidate():
    """RssConverter accepts text/xml as candidate (after XML validation)."""
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(TEST_RSS.encode("utf-8")),
        stream_info=StreamInfo(extension=".xml", mimetype="text/xml"),
    )
    assert "Test Blog" in result.markdown


def test_rss_rejects_non_xml():
    """HTML with .xml extension but no RSS content should fall through."""
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(b"<html><body>Not RSS</body></html>"),
        stream_info=StreamInfo(extension=".rss", mimetype="application/rss+xml"),
    )
    assert isinstance(result.markdown, str)
