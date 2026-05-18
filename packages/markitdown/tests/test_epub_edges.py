"""Edge-case tests for EpubConverter — corrupt archives, missing spine.

Tests EPUB parsing robustness.
"""

import io
import zipfile
import pytest

from markitdown import MarkItDown, StreamInfo, FileConversionException


def _make_epub_bytes(files: dict) -> bytes:
    """Build a minimal EPUB in memory from {path: content} dict."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        for path, content in files.items():
            zf.writestr(path, content)
    return buf.getvalue()


def _convert_epub(data: bytes) -> str:
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(data),
        stream_info=StreamInfo(extension=".epub", mimetype="application/epub+zip"),
    )
    return result.markdown


# Minimal EPUB mimetype file
MIMETYPE_CONTENT = "application/epub+zip"

# Minimal container.xml
CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""


def _make_content_opf(spine_items: list = None) -> str:
    """Build a minimal content.opf with given spine items."""
    items_xml = ""
    spine_xml = ""
    if spine_items:
        for i, item in enumerate(spine_items):
            items_xml += f'<item id="item{i}" href="{item}" media-type="application/xhtml+xml"/>\n'
            spine_xml += f'<itemref idref="item{i}"/>\n'

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid">
  <metadata>
    <dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">Test EPUB</dc:title>
  </metadata>
  <manifest>
    {items_xml}
  </manifest>
  <spine>
    {spine_xml}
  </spine>
</package>"""


# ============================================================
# Valid minimal EPUB
# ============================================================


def test_minimal_epub():
    epub = _make_epub_bytes({
        "mimetype": MIMETYPE_CONTENT,
        "META-INF/container.xml": CONTAINER_XML,
        "content.opf": _make_content_opf(["chapter1.xhtml"]),
        "chapter1.xhtml": "<html><body><h1>Chapter One</h1><p>Hello EPUB!</p></body></html>",
    })
    result = _convert_epub(epub)
    assert "Chapter One" in result
    assert "Hello EPUB!" in result


def test_epub_with_multiple_chapters():
    epub = _make_epub_bytes({
        "mimetype": MIMETYPE_CONTENT,
        "META-INF/container.xml": CONTAINER_XML,
        "content.opf": _make_content_opf(["ch1.xhtml", "ch2.xhtml"]),
        "ch1.xhtml": "<html><body><h1>Chapter 1</h1><p>First</p></body></html>",
        "ch2.xhtml": "<html><body><h1>Chapter 2</h1><p>Second</p></body></html>",
    })
    result = _convert_epub(epub)
    assert "Chapter 1" in result
    assert "Chapter 2" in result


# ============================================================
# Missing spine / empty EPUB
# ============================================================


def test_epub_with_no_spine_items():
    epub = _make_epub_bytes({
        "mimetype": MIMETYPE_CONTENT,
        "META-INF/container.xml": CONTAINER_XML,
        "content.opf": _make_content_opf([]),
    })
    result = _convert_epub(epub)
    # Should not crash, produces some output (title at minimum)
    assert isinstance(result, str)


# ============================================================
# Corrupt EPUB
# ============================================================


def test_corrupt_epub_not_a_zip():
    md = MarkItDown()
    # Falls through when EPUB parsing fails
    result = md.convert(
        io.BytesIO(b"not an epub file"),
        stream_info=StreamInfo(extension=".epub", mimetype="application/epub+zip"),
    )
    assert isinstance(result.markdown, str)


def test_epub_missing_mimetype():
    epub = _make_epub_bytes({
        "META-INF/container.xml": CONTAINER_XML,
        "content.opf": _make_content_opf(["ch.xhtml"]),
        "ch.xhtml": "<html><body><p>content</p></body></html>",
    })
    result = _convert_epub(epub)
    # Should handle gracefully
    assert isinstance(result, str)


def test_epub_missing_container():
    epub = _make_epub_bytes({
        "mimetype": MIMETYPE_CONTENT,
        "content.opf": _make_content_opf(["ch.xhtml"]),
        "ch.xhtml": "<html><body><p>content</p></body></html>",
    })
    with pytest.raises(FileConversionException):
        _convert_epub(epub)


def test_epub_truncated():
    truncated = b"PK\x03\x04\x00\x00\x00\x00"
    md = MarkItDown()
    # Truncated ZIP → may raise FileConversionException
    try:
        result = md.convert(
            io.BytesIO(truncated),
            stream_info=StreamInfo(extension=".epub", mimetype="application/epub+zip"),
        )
        assert isinstance(result.markdown, str)
    except FileConversionException:
        pass  # Also acceptable


# ============================================================
# EPUB with HTML content variations
# ============================================================


def test_epub_with_xhtml_content():
    epub = _make_epub_bytes({
        "mimetype": MIMETYPE_CONTENT,
        "META-INF/container.xml": CONTAINER_XML,
        "content.opf": _make_content_opf(["chapter.xhtml"]),
        "chapter.xhtml": (
            '<html xmlns="http://www.w3.org/1999/xhtml">'
            "<body><h1>XHTML Title</h1><p>XHTML paragraph</p></body></html>"
        ),
    })
    result = _convert_epub(epub)
    assert "XHTML Title" in result


def test_epub_with_css_linked():
    """EPUB with CSS reference — should not crash."""
    epub = _make_epub_bytes({
        "mimetype": MIMETYPE_CONTENT,
        "META-INF/container.xml": CONTAINER_XML,
        "content.opf": _make_content_opf(["chapter.xhtml"]),
        "chapter.xhtml": (
            '<html><head><link rel="stylesheet" href="style.css"/></head>'
            "<body><p>Styled content</p></body></html>"
        ),
        "style.css": "body { color: red; }",
    })
    result = _convert_epub(epub)
    assert "Styled content" in result
