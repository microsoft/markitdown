#!/usr/bin/env python3
"""Regression tests for RSS metadata / crash fixes and ZIP option forwarding."""

import io
import zipfile

from markitdown import MarkItDown, StreamInfo
from markitdown.converters._rss_converter import RssConverter


def test_rss_no_channel_title_does_not_crash_or_leak_item_title():
    """Feeds without a channel <title> must not crash or steal an item title."""
    xml = (
        b'<?xml version="1.0"?><rss version="2.0"><channel>'
        b"<description>Only desc</description>"
        b"<item><title>Item One</title><description>body</description></item>"
        b"</channel></rss>"
    )
    result = RssConverter().convert(io.BytesIO(xml), StreamInfo(extension=".rss"))
    assert result.title is None
    # Channel heading must not be the nested item title
    assert not result.markdown.startswith("# Item One")
    assert "Only desc" in result.markdown
    assert "## Item One" in result.markdown


def test_rss_no_titles_at_all_does_not_raise():
    """Missing channel title + no item titles previously raised UnboundLocalError."""
    xml = (
        b'<?xml version="1.0"?><rss version="2.0"><channel>'
        b"<description>Only desc</description>"
        b"<item><description>body</description></item>"
        b"</channel></rss>"
    )
    result = RssConverter().convert(io.BytesIO(xml), StreamInfo(extension=".rss"))
    assert "Only desc" in result.markdown
    assert result.title is None


def test_rss_channel_title_still_preferred():
    xml = (
        b'<?xml version="1.0"?><rss version="2.0"><channel>'
        b"<title>Feed Title</title><description>Desc</description>"
        b"<item><title>Item</title></item>"
        b"</channel></rss>"
    )
    result = RssConverter().convert(io.BytesIO(xml), StreamInfo(extension=".rss"))
    assert result.title == "Feed Title"
    assert result.markdown.startswith("# Feed Title")
    assert "## Item" in result.markdown


def test_atom_missing_feed_title():
    xml = (
        b'<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">'
        b"<entry><title>Entry</title></entry>"
        b"</feed>"
    )
    result = RssConverter().convert(io.BytesIO(xml), StreamInfo(extension=".atom"))
    assert result.title is None
    assert not result.markdown.startswith("# Entry")
    assert "## Entry" in result.markdown


def test_zip_propagates_keep_data_uris_and_skips_directories():
    html = b'<html><body><img src="data:image/png;base64,aaaa"/></body></html>'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("folder/", "")
        zf.writestr("folder/x.html", html)
    buf.seek(0)

    kept = MarkItDown().convert_stream(
        buf, stream_info=StreamInfo(extension=".zip"), keep_data_uris=True
    )
    assert "data:image/png;base64,aaaa" in kept.markdown
    assert "## File: folder/x.html" in kept.markdown
    # Directory-only entries must not get their own section heading.
    assert "\n## File: folder/\n" not in ("\n" + kept.markdown + "\n")

    buf.seek(0)
    truncated = MarkItDown().convert_stream(
        buf, stream_info=StreamInfo(extension=".zip"), keep_data_uris=False
    )
    assert "data:image/png;base64,aaaa" not in truncated.markdown
    assert "data:image" in truncated.markdown
    assert "aaaa" not in truncated.markdown


if __name__ == "__main__":
    test_rss_no_channel_title_does_not_crash_or_leak_item_title()
    test_rss_no_titles_at_all_does_not_raise()
    test_rss_channel_title_still_preferred()
    test_atom_missing_feed_title()
    test_zip_propagates_keep_data_uris_and_skips_directories()
    print("all passed")
