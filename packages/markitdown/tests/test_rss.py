"""RSS and Atom conversion, metadata, and link resolution."""

import io
import sys
import warnings
from typing import Final

import pytest
from bs4 import Tag
from markitdown import MarkItDown, StreamInfo
from markitdown.converters import RssConverter

# Feed bodies and links


@pytest.mark.parametrize(
    "root_prefix, child_prefix",
    [("", ""), ("a:", "a:"), ("a:", "b:"), ("a:", ""), ("", "a:")],
)
def test_atom_namespace_prefixes(root_prefix: str, child_prefix: str) -> None:
    # Fully prefixed feeds do not need a default namespace declaration.
    default_namespace = (
        "" if root_prefix and child_prefix else "http://www.w3.org/2005/Atom"
    )
    feed = f"""<?xml version="1.0" encoding="utf-8"?>
<{root_prefix}feed xmlns="{default_namespace}"
    xmlns:a="http://www.w3.org/2005/Atom"
    xmlns:b="http://www.w3.org/2005/Atom">
  <{child_prefix}title>Example feed</{child_prefix}title>
  <{child_prefix}subtitle>Feed subtitle</{child_prefix}subtitle>
  <{child_prefix}id>urn:example:feed</{child_prefix}id>
  <{child_prefix}updated>2026-01-01T00:00:00Z</{child_prefix}updated>
  <{child_prefix}author><{child_prefix}name>Example author</{child_prefix}name></{child_prefix}author>
  <{child_prefix}entry>
    <{child_prefix}title>Example entry</{child_prefix}title>
    <{child_prefix}id>urn:example:entry</{child_prefix}id>
    <{child_prefix}updated>2026-01-02T00:00:00Z</{child_prefix}updated>
    <{child_prefix}summary type="html">&lt;p&gt;An &lt;em&gt;entry summary&lt;/em&gt;.&lt;/p&gt;</{child_prefix}summary>
    <{child_prefix}content type="xhtml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p>Read the <strong>important details</strong>.</p>
      </div>
    </{child_prefix}content>
  </{child_prefix}entry>
</{root_prefix}feed>
""".encode()
    stream_info = StreamInfo(mimetype="application/xml", extension=".xml")
    converter = RssConverter()
    stream = io.BytesIO(feed)

    assert converter.accepts(stream, stream_info)
    assert stream.tell() == 0
    result = converter.convert(stream, stream_info)

    assert result.title == "Example feed"
    assert result.markdown.startswith("# Example feed\nFeed subtitle\n")
    assert "## Example entry\nUpdated on: 2026-01-02T00:00:00Z" in result.markdown
    assert "An *entry summary*." in result.markdown
    assert "Read the **important details**." in result.markdown

    # The public API must recognize the feed instead of falling back to raw XML.
    converted = MarkItDown().convert_stream(io.BytesIO(feed), stream_info=stream_info)
    assert converted.title == result.title
    assert converted.markdown == result.markdown.strip()


def test_atom_without_namespace_is_still_supported() -> None:
    feed = b"""<feed>
  <title>Example feed</title>
  <entry><title>Example entry</title><content>Entry content.</content></entry>
</feed>"""
    converter = RssConverter()
    stream_info = StreamInfo(extension=".xml")

    assert converter.accepts(io.BytesIO(feed), stream_info)
    result = converter.convert(io.BytesIO(feed), stream_info)

    assert result.title == "Example feed"
    assert "## Example entry" in result.markdown
    assert "Entry content." in result.markdown


def test_atom_ignores_elements_from_other_namespaces() -> None:
    feed = b"""<a:feed xmlns:a="http://www.w3.org/2005/Atom" xmlns="urn:example:other">
  <title>Unrelated title</title>
  <a:title>Example feed</a:title>
  <entry><title>Unrelated entry</title><content>Unrelated content.</content></entry>
  <a:entry>
    <a:title>Example entry</a:title>
    <content>Unrelated content.</content>
    <a:content>Entry content.</a:content>
  </a:entry>
</a:feed>"""
    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".atom"))

    assert result.title == "Example feed"
    assert "## Example entry" in result.markdown
    assert "Entry content." in result.markdown
    assert "Unrelated" not in result.markdown


def test_atom_xhtml_content_is_preserved() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="xhtml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p>Read the <strong>important details</strong>.</p>
      </div>
    </content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "Read the **important details**." in result.markdown


def test_atom_xhtml_summary_is_preserved() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <summary type="xhtml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p>A <em>structured</em> summary.</p>
      </div>
    </summary>
    <content type="text">Plain text content.</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "A *structured* summary." in result.markdown
    assert "Plain text content." in result.markdown


def test_atom_prefixed_xhtml_content_is_preserved() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:x="http://www.w3.org/1999/xhtml">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="xhtml">
      <x:div>
        <x:p>Hello <x:strong>bold</x:strong> and <x:em>italic</x:em>.</x:p>
        <x:a href="https://example.com">link</x:a>
      </x:div>
    </content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "Hello **bold** and *italic*." in result.markdown
    assert "[link](https://example.com)" in result.markdown


def test_atom_plain_text_content_is_not_parsed_as_html() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="text">Run &lt;job_id&gt; with &amp;lt;literal&amp;gt;.</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "Run <job_id> with &lt;literal&gt;." in result.markdown


def test_atom_untyped_summary_is_not_parsed_as_html() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <summary>A &lt;placeholder&gt; summary.</summary>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "A <placeholder> summary." in result.markdown


def test_atom_html_content_is_still_converted() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="html">&lt;p&gt;Read the &lt;strong&gt;important details&lt;/strong&gt;.&lt;/p&gt;</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "Read the **important details**." in result.markdown


def test_atom_text_media_type_content_is_not_parsed_as_html() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="text/plain">Run &lt;job_id&gt; to start.</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "Run <job_id> to start." in result.markdown


def test_atom_html_media_type_content_is_still_converted() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="text/html; charset=utf-8">&lt;p&gt;Read the &lt;strong&gt;important details&lt;/strong&gt;.&lt;/p&gt;</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "Read the **important details**." in result.markdown


def test_atom_xml_media_type_content_is_preserved() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="application/xhtml+xml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p>Read the <strong>important details</strong>.</p>
      </div>
    </content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "Read the **important details**." in result.markdown


def test_atom_binary_content_is_skipped() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="application/octet-stream">iVBORw0KGgoAAAANSUhEUg==</content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "iVBORw0KGgo" not in result.markdown


def test_atom_summary_media_type_is_treated_as_text() -> None:
    """Atom text constructs do not admit media types; treat one as plain text."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <summary type="text/plain">A &lt;placeholder&gt; summary.</summary>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "A <placeholder> summary." in result.markdown


def test_atom_plain_text_layout_whitespace_is_removed() -> None:
    """Feed indentation must not survive as a Markdown code block."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <content type="text">
      Run the job with &lt;job_id&gt;.

      Then check status.
    </content>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert result.markdown.splitlines()[-3:] == [
        "Run the job with <job_id>.",
        "",
        "Then check status.",
    ]


def _feed_with_body(field: str, payload: str, *, atom_type: str = "html") -> bytes:
    if field.startswith("rss-"):
        tag = "description" if field == "rss-description" else "content:encoded"
        return (
            '<rss version="2.0" '
            'xmlns:content="http://purl.org/rss/1.0/modules/content/">'
            "<channel><title>Feed</title><description>About the feed.</description>"
            f"<item><title>Entry</title><{tag}>{payload}</{tag}></item>"
            "</channel></rss>"
        ).encode()
    tag = field.removeprefix("atom-")
    return (
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        "<title>Feed</title><entry><title>Entry</title>"
        f'<{tag} type="{atom_type}">{payload}</{tag}>'
        "</entry></feed>"
    ).encode()


@pytest.mark.parametrize(
    "field", ["rss-description", "rss-content", "atom-summary", "atom-content"]
)
@pytest.mark.parametrize(
    "payload, expected",
    [
        ("Plain body.", "Plain body."),
        ("<![CDATA[<p>Only CDATA.</p>]]>", "Only CDATA."),
        (
            "\n    <![CDATA[<p>The <strong>body</strong>.</p>]]>\n  ",
            "The **body**.",
        ),
        (
            "Before <![CDATA[<str]]><![CDATA[ong>middle</strong>]]> after.",
            "Before **middle** after.",
        ),
        ("<b>nested</b> trailing", "**nested** trailing"),
        ("leading <b>nested</b> trailing", "leading **nested** trailing"),
        ("leading <b>nested</b>", "leading **nested**"),
        ("First<br/>Second", "First  \nSecond"),
        ("<pre>line 1\n  line 2</pre>", "```\nline 1\n  line 2\n```"),
        (
            "\n <!--ignore--><?instruction ignore?><b>nested<!--ignore--></b> trailing",
            "**nested** trailing",
        ),
        (
            (
                '<p>Read <a href="https://example.com/?a=1&amp;b=2">this</a>.</p>'
                "<p>Then <em>continue</em>.</p>"
            ),
            "Read [this](https://example.com/?a=1&b=2).\n\nThen *continue*.",
        ),
        (
            "<p>Use &lt;slot&gt; and &amp;lt;literal&amp;gt;.</p>",
            "Use <slot> and &lt;literal&gt;.",
        ),
    ],
)
def test_feed_body_preserves_complete_content(
    field: str, payload: str, expected: str
) -> None:
    feed = _feed_with_body(field, payload)
    stream_info = StreamInfo(extension=".rss" if field.startswith("rss-") else ".atom")
    result = RssConverter().convert(io.BytesIO(feed), stream_info)

    assert result.markdown.split("## Entry\n", 1)[1] == expected


@pytest.mark.parametrize("field", ["atom-summary", "atom-content"])
@pytest.mark.parametrize("atom_type", ["text", "text/plain"])
def test_atom_plain_mixed_content_stays_literal(field: str, atom_type: str) -> None:
    feed = _feed_with_body(
        field,
        "Run <![CDATA[<job_id>]]> with <b>&amp;lt;literal&amp;gt;</b>."
        "<!--ignore--><?instruction ignore?>",
        atom_type=atom_type,
    )
    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".atom"))

    assert result.markdown.split("## Entry\n", 1)[1] == (
        "Run <job_id> with &lt;literal&gt;."
    )


@pytest.mark.parametrize("atom_type", ["xhtml", "application/xhtml+xml"])
def test_atom_xhtml_preserves_literal_text_and_surrounding_content(
    atom_type: str,
) -> None:
    feed = _feed_with_body(
        "atom-content",
        'Before &lt;slot&gt; <x:div xmlns:x="http://www.w3.org/1999/xhtml">'
        "<x:p>Use <![CDATA[<slot> &lt;literal&gt;]]> and <x:b>bold</x:b>.</x:p>"
        "<!--ignore--><?instruction ignore?>"
        "<x:pre>line 1\n  line 2</x:pre></x:div> after.",
        atom_type=atom_type,
    )
    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".atom"))

    body = result.markdown.split("## Entry\n", 1)[1]
    assert body.startswith("Before <slot>")
    assert "Use <slot> &lt;literal&gt; and **bold**." in body
    assert "```\nline 1\n  line 2\n```" in body
    assert body.endswith("after.")
    assert "ignore" not in body


@pytest.mark.parametrize("extension", [".rss", ".atom"])
def test_feed_body_fields_are_separated(extension: str) -> None:
    if extension == ".rss":
        feed = _feed_with_body("rss-description", "Summary.").replace(
            b"</item>", b"<content:encoded>Body.</content:encoded></item>"
        )
    else:
        feed = _feed_with_body("atom-summary", "Summary.", atom_type="text").replace(
            b"</entry>", b'<content type="text">Body.</content></entry>'
        )
    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=extension))

    assert result.markdown.split("## Entry\n", 1)[1] == "Summary.\n\nBody."


@pytest.mark.parametrize("extension", [".rss", ".atom"])
@pytest.mark.parametrize(
    "summary, content, expected",
    [("<b/>", "Body.", "Body."), ("Summary.", "<b/>", "Summary."), ("<b/>", "", "")],
)
def test_empty_markup_fields_do_not_add_body_separators(
    extension: str, summary: str, content: str, expected: str
) -> None:
    if extension == ".rss":
        feed = _feed_with_body("rss-description", summary).replace(
            b"</item>", f"<content:encoded>{content}</content:encoded></item>".encode()
        )
    else:
        feed = _feed_with_body("atom-summary", summary).replace(
            b"</entry>", f'<content type="html">{content}</content></entry>'.encode()
        )
    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=extension))

    assert result.markdown.split("## Entry\n", 1)[1] == expected


@pytest.mark.parametrize("field", ["rss-description", "atom-content"])
def test_complete_feed_content_through_public_api(field: str) -> None:
    feed = _feed_with_body(field, "Before <b>nested</b> <![CDATA[after.]]>")
    result = MarkItDown().convert_stream(
        io.BytesIO(feed), stream_info=StreamInfo(extension=".xml")
    )

    assert result.title == "Feed"
    assert result.markdown.endswith("## Entry\nBefore **nested** after.")


@pytest.mark.parametrize(
    ("field", "atom_type", "cdata"),
    [
        pytest.param("rss-description", "html", False, id="rss-description"),
        pytest.param("rss-content", "html", True, id="rss-content-cdata"),
        pytest.param("atom-content", "html", True, id="atom-html-cdata"),
        pytest.param("atom-content", "xhtml", False, id="atom-xhtml"),
    ],
)
@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="iterative Markdown rendering requires Python 3.11",
)
def test_deep_xml_body_converts(field: str, atom_type: str, *, cdata: bool) -> None:
    payload: Final = "<div>" * 500 + "Deep <b>body</b>." + "</div>" * 500
    feed: Final = _feed_with_body(
        field, f"<![CDATA[{payload}]]>" if cdata else payload, atom_type=atom_type
    )
    stream_info: Final = StreamInfo(
        extension=".rss" if field.startswith("rss-") else ".atom"
    )
    original_limit: Final = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(200)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result: Final = RssConverter().convert(io.BytesIO(feed), stream_info)
    finally:
        sys.setrecursionlimit(original_limit)

    assert result.markdown.endswith("Deep **body**.")


def test_rss_content_namespace_alias_and_field_ownership() -> None:
    feed = b"""<rss xmlns:c="http://purl.org/rss/1.0/modules/content/">
      <channel><title>Feed</title><item><title>Entry</title>
        <extension><description>Wrong body.</description></extension>
        <c:encoded>Before <b>nested</b> <![CDATA[after.]]></c:encoded>
      </item></channel>
    </rss>"""
    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert result.markdown == "# Feed\n\n## Entry\nBefore **nested** after."


@pytest.mark.parametrize(
    "field", ["rss-description", "rss-content", "atom-summary", "atom-content"]
)
@pytest.mark.parametrize("cdata", [False, True])
def test_feed_relative_links_use_document_url(field: str, cdata: bool) -> None:
    payload = '<a href="../stories/café%20notes?x=1&amp;y=2#part">Read</a>'
    if cdata:
        payload = f"<![CDATA[{payload}]]>"
    feed = _feed_with_body(field, payload)
    result = MarkItDown().convert_stream(
        io.BytesIO(feed),
        stream_info=StreamInfo(
            extension=".xml", url="https://example.com/news/feed.xml"
        ),
    )

    assert result.markdown.endswith(
        "[Read](https://example.com/stories/caf%C3%A9%20notes?x=1&y=2#part)"
    )


def test_atom_inherits_xml_base_and_scopes_nested_overrides() -> None:
    feed = b"""<a:feed xmlns:a="http://www.w3.org/2005/Atom"
        xmlns:x="http://www.w3.org/1999/xhtml" xml:base="https://example.com/root/">
      <a:title>Feed</a:title>
      <a:entry xml:base="entries/">
        <a:title>Entry</a:title>
        <a:summary type="html" xml:base="../summaries/">
          <![CDATA[<a href="summary">Summary</a>]]>
        </a:summary>
        <a:content type="xhtml" xml:base="../articles/">
          <x:div xml:base="chapter/">
            <x:p xml:base="../appendix/">
              <x:a xml:base="../../assets/" href="story">Story</x:a>
              <x:a href="sibling">Sibling</x:a>
            </x:p>
            <x:a href="after">After</x:a>
            <x:img src="diagram.png" alt="Diagram"/>
            <x:img src="" data-src="../lazy.png" alt="Lazy"/>
          </x:div>
        </a:content>
      </a:entry>
      <a:entry><a:title>Next</a:title>
        <a:content type="html">&lt;a href="next"&gt;Next link&lt;/a&gt;</a:content>
      </a:entry>
    </a:feed>"""
    result = RssConverter().convert(
        io.BytesIO(feed),
        StreamInfo(extension=".atom", url="https://other.example/feed.xml"),
    )

    assert "[Summary](https://example.com/root/summaries/summary)" in result.markdown
    assert "[Story](https://example.com/root/assets/story)" in result.markdown
    assert (
        "[Sibling](https://example.com/root/articles/appendix/sibling)"
        in result.markdown
    )
    assert "[After](https://example.com/root/articles/chapter/after)" in result.markdown
    assert (
        "![Diagram](https://example.com/root/articles/chapter/diagram.png)"
        in result.markdown
    )
    assert "![Lazy](https://example.com/root/articles/lazy.png)" in result.markdown
    assert "[Next link](https://example.com/root/next)" in result.markdown


@pytest.mark.parametrize(
    "document_url, feed_base, entry_base, content_base, expected",
    [
        (
            "https://example.com/news/feed.xml",
            "../stories/",
            "2026/",
            "details/",
            "https://example.com/stories/2026/details/story",
        ),
        (
            "https://example.com/news/feed.xml",
            "https://other.example/base/",
            "section/",
            "",
            "https://other.example/base/section/story",
        ),
        (None, "https://example.com/", "", "", "https://example.com/story"),
        (None, "", "", "", "story"),
    ],
)
def test_atom_relative_and_empty_xml_base(
    document_url: str | None,
    feed_base: str,
    entry_base: str,
    content_base: str,
    expected: str,
) -> None:
    xml = (
        f'<feed xmlns="http://www.w3.org/2005/Atom" xml:base="{feed_base}">'
        f'<entry xml:base="{entry_base}"><content type="html" xml:base="{content_base}">'
        '<![CDATA[<a href="story">Read</a>]]></content></entry></feed>'
    )
    result = RssConverter().convert(
        io.BytesIO(xml.encode()), StreamInfo(extension=".atom", url=document_url)
    )

    assert result.markdown == f"[Read]({expected})"


@pytest.mark.parametrize(
    "href, expected",
    [
        ("#section", "https://example.com/news/feed.xml?lang=en#section"),
        ("?page=2", "https://example.com/news/feed.xml?page=2"),
        ("/story", "https://example.com/story"),
        ("//cdn.example.com/story", "https://cdn.example.com/story"),
        ("https://other.example/story", "https://other.example/story"),
    ],
)
def test_feed_link_reference_forms(href: str, expected: str) -> None:
    feed = _feed_with_body("atom-content", f'<a href="{href}">Read</a>')
    result = RssConverter().convert(
        io.BytesIO(feed),
        StreamInfo(extension=".atom", url="https://example.com/news/feed.xml?lang=en"),
    )

    assert result.markdown.endswith(f"[Read]({expected})")


def test_link_resolution_preserves_plain_atom_text() -> None:
    feed = _feed_with_body(
        "atom-content",
        '<![CDATA[<a href="story">literal</a>]]>',
        atom_type="text",
    )
    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(extension=".atom", url="https://example.com/feed")
    )

    assert result.markdown.endswith('<a href="story">literal</a>')


def test_link_resolution_retains_existing_invalid_link_handling() -> None:
    feed = _feed_with_body(
        "atom-content",
        '<a href="http://[invalid">Malformed</a> '
        '<a href="javascript:alert(1)">Script</a> '
        '<a href="story">Read</a>',
    )
    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(extension=".atom", url="https://example.com/feed")
    )

    assert result.markdown.endswith(
        "Malformed Script [Read](https://example.com/story)"
    )


def test_document_base_does_not_leak_between_conversions() -> None:
    feed = _feed_with_body("atom-content", '<a href="story">Read</a>')
    converter = RssConverter()
    first = converter.convert(
        io.BytesIO(feed), StreamInfo(extension=".atom"), url="https://example.com/feed"
    )
    second = converter.convert(io.BytesIO(feed), StreamInfo(extension=".atom"))

    assert first.markdown.endswith("[Read](https://example.com/story)")
    assert second.markdown.endswith("[Read](story)")


# Feed and entry titles


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
            (
                '<x:div xmlns:x="http://www.w3.org/1999/xhtml">co<x:b>op</x:b>erate'
                " <![CDATA[<slot> &lt;literal&gt;]]></x:div>"
            ),
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


# Conversion regressions


@pytest.mark.parametrize(
    "extension", [pytest.param(".rss", id="rss"), pytest.param(".atom", id="atom")]
)
@pytest.mark.parametrize(
    "strict", [pytest.param(False, id="default"), pytest.param(True, id="strict")]
)
@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="iterative Markdown rendering requires Python 3.11",
)
def test_deeply_nested_rss_item_converts(extension: str, strict: bool) -> None:
    item_html: Final = (
        "<div>" * 500
        + "<p>Deep feed content with <b>bold text</b></p>"
        + "</div>" * 500
    )
    rss: Final = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/">'
        "<channel>"
        "<title>Test Feed</title>"
        "<description>A test feed</description>"
        "<item>"
        "<title>Deep Item</title>"
        f"<content:encoded><![CDATA[{item_html}]]></content:encoded>"
        "</item>"
        "</channel>"
        "</rss>"
    )
    atom: Final = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        "<title>Test Feed</title>"
        "<entry>"
        "<title>Deep Entry</title>"
        f'<content type="html"><![CDATA[{item_html}]]></content>'
        "</entry>"
        "</feed>"
    )

    original_limit: Final = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(200)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result: Final = RssConverter().convert(
                io.BytesIO((rss if extension == ".rss" else atom).encode()),
                StreamInfo(extension=extension),
                strict=strict,
            )
    finally:
        sys.setrecursionlimit(original_limit)

    assert "Deep feed content with **bold text**" in result.markdown


@pytest.mark.parametrize(
    "extension",
    [pytest.param(".rss", id="rss"), pytest.param(".atom", id="atom")],
)
def test_feed_propagates_language_callback_errors(extension: str) -> None:
    def fail_language(tag: Tag) -> str:
        raise ValueError(f"Cannot classify {tag.get_text()}")

    feed: Final = _feed_with_body(
        "rss-content" if extension == ".rss" else "atom-content",
        "<![CDATA[<pre>Garden</pre>]]>",
    )
    with pytest.raises(ValueError, match="Cannot classify Garden"):
        RssConverter().convert(
            io.BytesIO(feed),
            StreamInfo(extension=extension),
            code_language_callback=fail_language,
        )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
