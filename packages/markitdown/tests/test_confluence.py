#!/usr/bin/env python3 -m pytest
"""Tests for the Confluence converters (URL-based and Storage Format XML)."""

import io
import os

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import ConfluenceConverter, ConfluenceStorageConverter

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

# ---------------------------------------------------------------------------
# Expected strings for the HTML fixture (Confluence Cloud page)
# ---------------------------------------------------------------------------
CLOUD_MUST_CONTAIN = [
    "Design Decisions",          # title / h1
    "## Overview",               # h2 preserved
    "## Goals",
    "## Decision Log",
    "**architecture**",          # bold preserved
    "Simplicity",                # list item
    "Reliability",
    "Extensibility",
    "Use Python",                # table content
    "Use REST API",
    "Accepted",
]

CLOUD_MUST_NOT_CONTAIN = [
    "Header chrome",
    "Footer chrome",
    "Sidebar content",
    "12 likes",
    "A comment that should not appear.",
    "Home",                      # breadcrumb/nav link text
]

# ---------------------------------------------------------------------------
# Expected strings for the XML fixture (Confluence Storage Format)
# ---------------------------------------------------------------------------
STORAGE_MUST_CONTAIN = [
    "API Guidelines",            # page title / h1
    "def get_user",              # code block body
    "user_id",
    "Info:",                     # info panel label
    "/v1/",                      # info panel body
    "Note:",                     # note panel label
    "Rate limiting",
    "Warning:",                  # warning panel label
    "Never expose internal IDs",
    "Authentication Docs",       # ac:link resolved to page title
    "architecture-diagram.png",  # ac:image resolved to filename
    "Write API spec",            # completed task
    "Add pagination support",    # incomplete task
    "[x]",                       # checked checkbox
    "[ ]",                       # unchecked checkbox
]

STORAGE_MUST_NOT_CONTAIN = [
    "ac:structured-macro",       # raw Confluence XML must not leak through
    "ac:task-list",
    "ac:emoticon",
    "ri:attachment",
    # TOC macro should be fully removed — no heading containing "toc"
    ">toc<",
]


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_text(result) -> str:
    return result.text_content.replace("\\", "")


# ---------------------------------------------------------------------------
# ConfluenceConverter (URL / HTML)
# ---------------------------------------------------------------------------

class TestConfluenceConverter:

    def test_accepts_cloud_url_with_html_mimetype(self):
        conv = ConfluenceConverter()
        si = StreamInfo(
            url="https://mycompany.atlassian.net/wiki/spaces/ENG/pages/1/Title",
            mimetype="text/html",
        )
        assert conv.accepts(io.BytesIO(b""), si)

    def test_accepts_server_url_with_html_mimetype(self):
        conv = ConfluenceConverter()
        si = StreamInfo(
            url="https://confluence.example.com/wiki/spaces/PROJ/display/Page",
            mimetype="text/html",
        )
        assert conv.accepts(io.BytesIO(b""), si)

    def test_accepts_cloud_url_with_html_extension(self):
        conv = ConfluenceConverter()
        si = StreamInfo(
            url="https://mycompany.atlassian.net/wiki/spaces/ENG/pages/1/Title",
            extension=".html",
        )
        assert conv.accepts(io.BytesIO(b""), si)

    def test_rejects_non_confluence_url(self):
        conv = ConfluenceConverter()
        for url in [
            "https://en.wikipedia.org/wiki/Python",
            "https://www.google.com",
            "https://mycompany.atlassian.net/jira/browse/TICKET-1",  # Jira, not Confluence
        ]:
            si = StreamInfo(url=url, mimetype="text/html")
            assert not conv.accepts(io.BytesIO(b""), si), f"should not accept: {url}"

    def test_rejects_confluence_url_without_html_content(self):
        conv = ConfluenceConverter()
        si = StreamInfo(
            url="https://mycompany.atlassian.net/wiki/spaces/ENG/pages/1/file.pdf",
            mimetype="application/pdf",
        )
        assert not conv.accepts(io.BytesIO(b""), si)

    def test_convert_strips_noise_and_preserves_content(self):
        conv = ConfluenceConverter()
        fixture = os.path.join(TEST_FILES_DIR, "test_confluence_cloud.html")
        si = StreamInfo(
            url="https://mycompany.atlassian.net/wiki/spaces/ENG/pages/1/Design",
            mimetype="text/html",
            extension=".html",
        )
        with open(fixture, "rb") as f:
            result = conv.convert(f, si)

        text = _get_text(result)
        for s in CLOUD_MUST_CONTAIN:
            assert s in text, f"expected {s!r} in output"
        for s in CLOUD_MUST_NOT_CONTAIN:
            assert s not in text, f"expected {s!r} to be stripped from output"

    def test_convert_extracts_title(self):
        conv = ConfluenceConverter()
        fixture = os.path.join(TEST_FILES_DIR, "test_confluence_cloud.html")
        si = StreamInfo(
            url="https://mycompany.atlassian.net/wiki/spaces/ENG/pages/1/Design",
            mimetype="text/html",
            extension=".html",
        )
        with open(fixture, "rb") as f:
            result = conv.convert(f, si)
        assert result.title is not None
        assert "Design Decisions" in result.title

    def test_markitdown_routes_confluence_cloud_url(self):
        """MarkItDown should pick ConfluenceConverter over HtmlConverter for Confluence URLs."""
        markitdown = MarkItDown()
        fixture = os.path.join(TEST_FILES_DIR, "test_confluence_cloud.html")
        si = StreamInfo(
            url="https://mycompany.atlassian.net/wiki/spaces/ENG/pages/1/Design",
            mimetype="text/html",
            extension=".html",
        )
        with open(fixture, "rb") as f:
            result = markitdown.convert_stream(f, stream_info=si)

        text = _get_text(result)
        for s in CLOUD_MUST_CONTAIN:
            assert s in text, f"expected {s!r} in output"
        for s in CLOUD_MUST_NOT_CONTAIN:
            assert s not in text, f"expected {s!r} to be stripped"


# ---------------------------------------------------------------------------
# ConfluenceStorageConverter (XML / Storage Format)
# ---------------------------------------------------------------------------

class TestConfluenceStorageConverter:

    def test_accepts_xml_with_ac_namespace(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"<root><ac:structured-macro ac:name='code'/></root>"
        assert conv.accepts(io.BytesIO(xml), si)

    def test_accepts_xml_with_ri_namespace(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"<root><ri:page ri:content-title='Home'/></root>"
        assert conv.accepts(io.BytesIO(xml), si)

    def test_rejects_plain_xml(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"<root><item>no confluence tags here</item></root>"
        assert not conv.accepts(io.BytesIO(xml), si)

    def test_rejects_non_xml_extension(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".html", mimetype="text/html")
        xml = b"<root><ac:structured-macro/></root>"
        assert not conv.accepts(io.BytesIO(xml), si)

    def test_accepts_does_not_advance_stream(self):
        """Stream position must be reset after accepts() peeks."""
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"<root><ac:structured-macro/></root>"
        stream = io.BytesIO(xml)
        conv.accepts(stream, si)
        assert stream.tell() == 0, "accepts() must reset stream position"

    def test_code_macro_becomes_fenced_block(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"""<?xml version="1.0"?>
<page><body>
  <ac:structured-macro ac:name="code">
    <ac:parameter ac:name="language">python</ac:parameter>
    <ac:plain-text-body>print("hello")</ac:plain-text-body>
  </ac:structured-macro>
</body></page>"""
        result = conv.convert(io.BytesIO(xml), si)
        assert 'print("hello")' in result.markdown
        assert "ac:structured-macro" not in result.markdown

    def test_code_macro_no_language(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"""<?xml version="1.0"?>
<page><body>
  <ac:structured-macro ac:name="code">
    <ac:plain-text-body>SELECT * FROM users;</ac:plain-text-body>
  </ac:structured-macro>
</body></page>"""
        result = conv.convert(io.BytesIO(xml), si)
        assert "SELECT * FROM users;" in result.markdown

    def test_panel_macros_become_blockquotes(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        for macro_name, expected_label in [
            ("info", "Info:"),
            ("note", "Note:"),
            ("warning", "Warning:"),
            ("tip", "Tip:"),
        ]:
            xml = f"""<?xml version="1.0"?>
<page><body>
  <ac:structured-macro ac:name="{macro_name}">
    <ac:rich-text-body><p>Panel content {macro_name}</p></ac:rich-text-body>
  </ac:structured-macro>
</body></page>""".encode()
            result = conv.convert(io.BytesIO(xml), si)
            assert expected_label in result.markdown, f"label missing for {macro_name}"
            assert f"Panel content {macro_name}" in result.markdown

    def test_toc_macro_is_removed(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"""<?xml version="1.0"?>
<page><body>
  <p>Before TOC</p>
  <ac:structured-macro ac:name="toc"/>
  <p>After TOC</p>
</body></page>"""
        result = conv.convert(io.BytesIO(xml), si)
        assert "Before TOC" in result.markdown
        assert "After TOC" in result.markdown
        assert "ac:structured-macro" not in result.markdown

    def test_ac_link_resolves_to_page_title(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"""<?xml version="1.0"?>
<page><body>
  <p>See <ac:link><ri:page ri:content-title="My Other Page"/></ac:link> for details.</p>
</body></page>"""
        result = conv.convert(io.BytesIO(xml), si)
        assert "My Other Page" in result.markdown
        assert "ac:link" not in result.markdown

    def test_ac_image_attachment_becomes_img(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"""<?xml version="1.0"?>
<page><body>
  <ac:image><ri:attachment ri:filename="diagram.png"/></ac:image>
</body></page>"""
        result = conv.convert(io.BytesIO(xml), si)
        assert "diagram.png" in result.markdown
        assert "ac:image" not in result.markdown

    def test_emoticons_are_removed(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"""<?xml version="1.0"?>
<page><body>
  <p>Status: <ac:emoticon ac:name="tick"/> Done</p>
</body></page>"""
        result = conv.convert(io.BytesIO(xml), si)
        assert "Done" in result.markdown
        assert "ac:emoticon" not in result.markdown

    def test_task_list_becomes_checkboxes(self):
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        xml = b"""<?xml version="1.0"?>
<page><body>
  <ac:task-list>
    <ac:task>
      <ac:task-status>complete</ac:task-status>
      <ac:task-body>Finished task</ac:task-body>
    </ac:task>
    <ac:task>
      <ac:task-status>incomplete</ac:task-status>
      <ac:task-body>Pending task</ac:task-body>
    </ac:task>
  </ac:task-list>
</body></page>"""
        result = conv.convert(io.BytesIO(xml), si)
        assert "[x]" in result.markdown
        assert "[ ]" in result.markdown
        assert "Finished task" in result.markdown
        assert "Pending task" in result.markdown
        assert "ac:task-list" not in result.markdown

    def test_full_fixture_content_and_noise(self):
        """End-to-end test against the full XML fixture file."""
        conv = ConfluenceStorageConverter()
        fixture = os.path.join(TEST_FILES_DIR, "test_confluence_storage.xml")
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        with open(fixture, "rb") as f:
            result = conv.convert(f, si)

        text = _get_text(result)
        for s in STORAGE_MUST_CONTAIN:
            assert s in text, f"expected {s!r} in output"
        for s in STORAGE_MUST_NOT_CONTAIN:
            assert s not in text, f"expected {s!r} to be absent from output"

    def test_markitdown_routes_xml_to_storage_converter(self):
        """MarkItDown should route .xml with ac: tags to ConfluenceStorageConverter."""
        markitdown = MarkItDown()
        fixture = os.path.join(TEST_FILES_DIR, "test_confluence_storage.xml")
        result = markitdown.convert(fixture)

        text = _get_text(result)
        for s in STORAGE_MUST_CONTAIN:
            assert s in text, f"expected {s!r} in output"

    def test_plain_xml_not_routed_to_storage_converter(self):
        """A plain XML file without ac:/ri: tags must not be handled by ConfluenceStorageConverter."""
        conv = ConfluenceStorageConverter()
        si = StreamInfo(extension=".xml", mimetype="text/xml")
        plain = b"<feed><entry><title>RSS item</title></entry></feed>"
        assert not conv.accepts(io.BytesIO(plain), si)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
