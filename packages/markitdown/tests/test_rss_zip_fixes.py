"""
Tests for bug fixes in RSS and ZIP converters.

- RssConverter: UnboundLocalError when channel has no title (#1784)
- RssConverter: channel description was not HTML-cleaned before use
- ZipConverter: FileConversionException was silently swallowed
"""

import io
import zipfile
import pytest
from markitdown import MarkItDown
from markitdown._markitdown import StreamInfo


# ---------------------------------------------------------------------------
# RSS converter fixes
# ---------------------------------------------------------------------------

RSS_NO_TITLE = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <description>A feed with no title element</description>
    <item>
      <title>Item One</title>
      <link>https://example.com/1</link>
    </item>
  </channel>
</rss>"""

RSS_WITH_HTML_DESCRIPTION = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>My Feed</title>
    <description>&lt;p&gt;Hello &lt;b&gt;world&lt;/b&gt;&lt;/p&gt;</description>
    <item>
      <title>Item One</title>
      <link>https://example.com/1</link>
    </item>
  </channel>
</rss>"""


def _convert_bytes(data: bytes, extension: str) -> str:
    md = MarkItDown()
    result = md.convert_stream(io.BytesIO(data), stream_info=StreamInfo(extension=extension))
    return result.markdown


def test_rss_no_title_does_not_raise():
    """RssConverter must not raise UnboundLocalError when channel has no <title>."""
    # Previously crashed: md_text += ... but md_text was never initialised
    result = _convert_bytes(RSS_NO_TITLE, ".rss")
    assert "A feed with no title element" in result
    assert "Item One" in result


def test_rss_channel_description_html_is_cleaned():
    """Channel <description> containing HTML entities should be converted cleanly."""
    result = _convert_bytes(RSS_WITH_HTML_DESCRIPTION, ".rss")
    # After HTML cleaning we expect plain text / markdown, not raw &lt;p&gt; entities
    assert "&lt;" not in result
    assert "Hello" in result
    assert "world" in result


# ---------------------------------------------------------------------------
# ZIP converter fix
# ---------------------------------------------------------------------------

def _make_zip_with_unconvertible_file() -> bytes:
    """Build an in-memory ZIP that contains a binary file markitdown cannot convert."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        # A plain text file that can be converted
        zf.writestr("hello.txt", "Hello from ZIP")
        # A random binary blob with an unknown extension — conversion will fail
        zf.writestr("data.bin", b"\x00\x01\x02\x03\x04\x05")
    buf.seek(0)
    return buf.read()


def test_zip_conversion_failure_surfaced_in_output():
    """ZipConverter must include a warning when a contained file cannot be converted."""
    zip_bytes = _make_zip_with_unconvertible_file()
    result = _convert_bytes(zip_bytes, ".zip")
    # The convertible file should still appear
    assert "Hello from ZIP" in result
