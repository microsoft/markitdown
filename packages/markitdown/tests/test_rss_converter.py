import io

from markitdown import StreamInfo
from markitdown.converters import RssConverter


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


def test_rss_description_survives_a_cdata_section_on_its_own_line() -> None:
    """A pretty-printed CDATA payload is a later child, not the first one."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
  <title>Example feed</title>
  <description>Example feed description</description>
  <item>
    <title>Example item</title>
    <description>
      <![CDATA[<p>The <strong>body</strong> of the item.</p>]]>
    </description>
  </item>
</channel></rss>
"""

    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert "The **body** of the item." in result.markdown


def test_rss_title_survives_a_cdata_section_in_the_middle() -> None:
    """Text either side of a CDATA section belongs to the same value."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
  <title>Example feed</title>
  <description>Example feed description</description>
  <item>
    <title>Quarterly <![CDATA[R&D]]> report</title>
    <description>Body.</description>
  </item>
</channel></rss>
"""

    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert "## Quarterly R&D report" in result.markdown


def test_atom_summary_survives_a_cdata_section_on_its_own_line() -> None:
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example feed</title>
  <entry>
    <title>Example entry</title>
    <summary type="html">
      <![CDATA[<p>A <em>structured</em> summary.</p>]]>
    </summary>
  </entry>
</feed>
"""

    result = RssConverter().convert(
        io.BytesIO(feed), StreamInfo(mimetype="application/atom+xml")
    )

    assert "A *structured* summary." in result.markdown


def test_rss_cdata_only_description_is_unchanged() -> None:
    """The case that already worked must keep working."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
  <title>Example feed</title>
  <description>Example feed description</description>
  <item>
    <title>Example item</title>
    <description><![CDATA[<p>Only a CDATA section.</p>]]></description>
  </item>
</channel></rss>
"""

    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert "Only a CDATA section." in result.markdown


def test_rss_item_without_a_description_is_still_converted() -> None:
    """An absent element must stay absent, not become an empty string."""
    feed = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
  <title>Example feed</title>
  <description>Example feed description</description>
  <item>
    <title>Example item</title>
  </item>
</channel></rss>
"""

    result = RssConverter().convert(io.BytesIO(feed), StreamInfo(extension=".rss"))

    assert result.title == "Example feed"
    assert "## Example item" in result.markdown
