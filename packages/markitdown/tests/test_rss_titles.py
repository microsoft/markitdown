#!/usr/bin/env python3 -m pytest
"""Feed and entry titles must survive a pretty-printed feed."""

import io
import sys

import pytest

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


@pytest.mark.parametrize("extension", [".rss", ".atom"])
@pytest.mark.parametrize(
    "payload, expected",
    [
        ("Quarterly <![CDATA[R&D]]> report", "Quarterly R&D report"),
        ("<![CDATA[Quarterly ]]><![CDATA[R&D]]> report", "Quarterly R&D report"),
        ("\n  <![CDATA[Example]]>\n", "Example"),
        ("<b>nested</b> trailing", "nested trailing"),
        ("leading <b>nested</b> trailing", "leading nested trailing"),
        ("leading <b>nested</b>", "leading nested"),
        ("<b><i>nested</i></b>", "nested"),
        (
            " \n<!--ignore--><?instruction ignore?><b>nested</b> trailing",
            "nested trailing",
        ),
        ("co<b>op</b>erate", "cooperate"),
        ("<p>First</p><p>Second</p>", "First Second"),
        (
            "Use &lt;slot&gt; and &amp;lt;literal&amp;gt;",
            "Use <slot> and &lt;literal&gt;",
        ),
        ("", None),
        ("   \n", None),
        ("<b/>", None),
        ("<!--ignore--><?instruction ignore?>", None),
    ],
)
def test_complete_feed_and_entry_titles(
    extension: str, payload: str, expected: str | None
) -> None:
    if extension == ".rss":
        xml = (
            f"<rss><channel><title>{payload}</title>"
            f"<item><title>{payload}</title><description>Body.</description></item>"
            "</channel></rss>"
        )
    else:
        xml = (
            f'<feed xmlns="http://www.w3.org/2005/Atom"><title>{payload}</title>'
            f"<entry><title>{payload}</title><content>Body.</content></entry></feed>"
        )
    result = RssConverter().convert(
        io.BytesIO(xml.encode()), StreamInfo(extension=extension)
    )

    assert result.title == expected
    assert result.markdown == (
        f"# {expected}\n\n## {expected}\nBody." if expected else "Body."
    )


@pytest.mark.parametrize("prefix", ["", "a:"])
@pytest.mark.parametrize(
    "content_type, payload, expected",
    [
        ("html", "&lt;b&gt;nested&lt;/b&gt; trailing", "nested trailing"),
        ("html", "<![CDATA[<b>nes]]><![CDATA[ted</b>]]> trailing", "nested trailing"),
        ("html", "<b>nested</b> trailing", "nested trailing"),
        ("html", "&lt;p&gt;First&lt;/p&gt;&lt;p&gt;Second&lt;/p&gt;", "First Second"),
        ("html", "Use &amp;lt;slot&amp;gt;", "Use <slot>"),
        (
            "xhtml",
            '<x:div xmlns:x="http://www.w3.org/1999/xhtml">co<x:b>op</x:b>erate'
            " <![CDATA[<slot> &lt;literal&gt;]]></x:div>",
            "cooperate <slot> &lt;literal&gt;",
        ),
        ("text/plain", "Use &lt;slot&gt;", "Use <slot>"),
    ],
)
def test_atom_typed_titles_and_subtitles(
    prefix: str, content_type: str, payload: str, expected: str
) -> None:
    xml = (
        f'<{prefix}feed xmlns="http://www.w3.org/2005/Atom" '
        'xmlns:a="http://www.w3.org/2005/Atom">'
        f'<{prefix}title type="{content_type}">{payload}</{prefix}title>'
        f'<{prefix}subtitle type="{content_type}">{payload}</{prefix}subtitle>'
        f'<{prefix}entry><{prefix}title type="{content_type}">{payload}</{prefix}title>'
        f"<{prefix}content>Body.</{prefix}content></{prefix}entry></{prefix}feed>"
    )
    result = RssConverter().convert(
        io.BytesIO(xml.encode()), StreamInfo(extension=".atom")
    )

    assert result.title == expected
    assert result.markdown == f"# {expected}\n{expected}\n\n## {expected}\nBody."


@pytest.mark.parametrize("extension", [".rss", ".atom"])
def test_feed_does_not_borrow_nested_metadata(extension: str) -> None:
    if extension == ".rss":
        xml = (
            "<rss><channel><image><title>Wrong feed title</title></image>"
            "<item><title>Entry</title><description>Body.</description></item>"
            "<item><extension><title>Wrong entry title</title></extension>"
            "<description>Second body.</description></item></channel></rss>"
        )
    else:
        xml = (
            '<feed xmlns="http://www.w3.org/2005/Atom">'
            "<entry><title>Entry</title><content>Body.</content></entry>"
            "<entry><source><title>Wrong entry title</title><summary>Wrong body.</summary>"
            "</source><content>Second body.</content></entry></feed>"
        )
    result = RssConverter().convert(
        io.BytesIO(xml.encode()), StreamInfo(extension=extension)
    )

    assert result.title is None
    assert result.markdown.count("## Entry") == 1
    assert "Wrong" not in result.markdown
    assert not result.markdown.startswith("# ")
    assert "Body.\n\nSecond body." in result.markdown


@pytest.mark.parametrize("content_type", ["rss", "text", "html", "xhtml"])
def test_deeply_nested_title_is_read_without_recursion(content_type: str) -> None:
    payload = "<b>" * 500 + "Deep title" + "</b>" * 500
    if content_type == "rss":
        xml = f"<rss><channel><title>{payload}</title></channel></rss>".encode()
        extension = ".rss"
    else:
        if content_type == "html":
            payload = f"<![CDATA[{payload}]]>"
        elif content_type == "xhtml":
            payload = f'<div xmlns="http://www.w3.org/1999/xhtml">{payload}</div>'
        xml = (
            f'<feed xmlns="http://www.w3.org/2005/Atom">'
            f'<title type="{content_type}">{payload}</title><entry/></feed>'
        ).encode()
        extension = ".atom"
    original_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(200)
        result = RssConverter().convert(
            io.BytesIO(xml), StreamInfo(extension=extension)
        )
    finally:
        sys.setrecursionlimit(original_limit)

    assert result.title == "Deep title"


def test_rss_channel_description_and_date_preserve_complete_text() -> None:
    xml = b"""<rss><channel><title>Feed</title>
      <description>About <![CDATA[R&D]]> and <b>research</b>.</description>
      <item><title>Entry</title><pubDate>Mon, <![CDATA[01 Jan 2024]]> 00:00:00 GMT</pubDate>
      </item></channel></rss>"""
    result = RssConverter().convert(io.BytesIO(xml), StreamInfo(extension=".rss"))

    assert "About R&D and research." in result.markdown
    assert "Published on: Mon, 01 Jan 2024 00:00:00 GMT" in result.markdown
