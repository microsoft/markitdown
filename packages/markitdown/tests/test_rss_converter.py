import io

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import RssConverter


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
""".encode(
        "utf-8"
    )
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
