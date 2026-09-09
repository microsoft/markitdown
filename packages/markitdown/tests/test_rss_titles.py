#!/usr/bin/env python3 -m pytest
"""Feed and entry titles must survive a pretty-printed feed."""

import io

from markitdown import StreamInfo
from markitdown.converters import RssConverter


def test_rss_pretty_printed_titles_still_make_headings() -> None:
    """A title written on its own line must not end the heading before its text."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
  <title>
    Example feed
  </title>
  <description>
    Example feed description
  </description>
  <item>
    <title>
      A story about things
    </title>
    <pubDate>
      Mon, 01 Jan 2024 00:00:00 GMT
    </pubDate>
    <description>Body text.</description>
  </item>
</channel></rss>
"""

    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert result.title == "Example feed"
    # The channel description retains its original whitespace.
    assert result.markdown.splitlines() == [
        "# Example feed",
        "",
        "    Example feed description",
        "  ",
        "",
        "## A story about things",
        "Published on: Mon, 01 Jan 2024 00:00:00 GMT",
        "Body text.",
    ]


def test_atom_pretty_printed_titles_still_make_headings() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>
    Example feed
  </title>
  <subtitle>
    Example subtitle
  </subtitle>
  <entry>
    <title>
      Example entry
    </title>
    <updated>
      2024-01-01T00:00:00Z
    </updated>
    <content type="text">Body text.</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert result.title == "Example feed"
    assert result.markdown.splitlines() == [
        "# Example feed",
        "Example subtitle",
        "",
        "## Example entry",
        "Updated on: 2024-01-01T00:00:00Z",
        "Body text.",
    ]


def test_rss_whitespace_only_title_makes_no_heading() -> None:
    """An empty title must be absent, not an empty '#' line."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
  <title>   </title>
  <description>Example feed description</description>
  <item>
    <title>Example item</title>
    <description>Body text.</description>
  </item>
</channel></rss>
"""

    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert result.title is None
    assert not result.markdown.startswith("#\n")
    assert result.markdown.splitlines()[0] == "Example feed description"


def test_atom_feed_without_any_title_makes_no_heading() -> None:
    """A missing title must not render the word 'None' as the document heading."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>urn:example:feed</id>
  <entry>
    <id>urn:example:entry</id>
    <content type="text">Body text.</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "None" not in result.markdown
    assert "Body text." in result.markdown


def test_rss_single_line_titles_are_unchanged() -> None:
    """The ordinary layout must produce exactly the same markdown as before."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
  <title>Example feed</title>
  <description>Example feed description</description>
  <item>
    <title>Example item</title>
    <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
    <description>Body text.</description>
  </item>
</channel></rss>
"""

    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert result.title == "Example feed"
    assert result.markdown == (
        "# Example feed\n"
        "Example feed description\n"
        "\n"
        "## Example item\n"
        "Published on: Mon, 01 Jan 2024 00:00:00 GMT\n"
        "Body text."
    )
