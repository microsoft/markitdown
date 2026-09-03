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
