"""EPUB conversion, archive paths, metadata, and embedded images."""

import io
import zipfile

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import EpubConverter


# Archive href resolution

CONTAINER_XML = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

CHAPTER_XHTML = """<html xmlns="http://www.w3.org/1999/xhtml">
  <body><h1>{title}</h1><p>{body}</p></body>
</html>
"""


def _build_epub(manifest_items, spine_ids, documents) -> io.BytesIO:
    """Assemble a minimal EPUB from manifest entries and ZIP member names."""
    manifest = "\n".join(
        f'<item id="{item_id}" href="{href}" media-type="application/xhtml+xml"/>'
        for item_id, href in manifest_items
    )
    spine = "\n".join(f'<itemref idref="{item_id}"/>' for item_id in spine_ids)
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Encoded Hrefs</dc:title>
  </metadata>
  <manifest>{manifest}</manifest>
  <spine>{spine}</spine>
</package>
"""

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("mimetype", "application/epub+zip")
        z.writestr("META-INF/container.xml", CONTAINER_XML)
        z.writestr("OEBPS/content.opf", opf)
        for name, (title, body) in documents.items():
            z.writestr(name, CHAPTER_XHTML.format(title=title, body=body))
    buffer.seek(0)
    return buffer


def _convert(stream: io.BytesIO) -> str:
    result = EpubConverter().convert(
        stream, StreamInfo(mimetype="application/epub+zip", extension=".epub")
    )
    # markdownify escapes underscores, so compare against unescaped text
    return result.markdown.replace("\\", "")


def test_percent_encoded_href_resolves_to_zip_entry() -> None:
    """A space in a filename arrives percent-encoded in the manifest href."""
    stream = _build_epub(
        manifest_items=[("c1", "chapter%201.xhtml"), ("c2", "plain.xhtml")],
        spine_ids=["c1", "c2"],
        documents={
            "OEBPS/chapter 1.xhtml": ("First", "SPACED_BODY"),
            "OEBPS/plain.xhtml": ("Second", "PLAIN_BODY"),
        },
    )

    markdown = _convert(stream)

    assert "SPACED_BODY" in markdown, "percent-encoded href must resolve to its entry"
    assert "PLAIN_BODY" in markdown, "unencoded hrefs must keep working"
    assert markdown.index("SPACED_BODY") < markdown.index(
        "PLAIN_BODY"
    ), "spine order is preserved"


def test_non_ascii_percent_encoded_href_resolves() -> None:
    """Non-ASCII filenames are percent-encoded UTF-8 in the manifest href."""
    stream = _build_epub(
        manifest_items=[("c1", "cap%C3%ADtulo.xhtml")],
        spine_ids=["c1"],
        documents={"OEBPS/capítulo.xhtml": ("Capítulo", "ACCENTED_BODY")},
    )

    assert "ACCENTED_BODY" in _convert(stream)


def test_literally_encoded_zip_entry_still_resolves() -> None:
    """An archive storing the encoded name verbatim keeps working."""
    stream = _build_epub(
        manifest_items=[("c1", "chapter%201.xhtml")],
        spine_ids=["c1"],
        documents={"OEBPS/chapter%201.xhtml": ("Literal", "LITERAL_BODY")},
    )

    assert "LITERAL_BODY" in _convert(stream)


def test_parent_relative_href_resolves() -> None:
    """Hrefs may point outside the OPF's own directory."""
    stream = _build_epub(
        manifest_items=[("c1", "../shared/chapter.xhtml")],
        spine_ids=["c1"],
        documents={"shared/chapter.xhtml": ("Shared", "SHARED_BODY")},
    )

    assert "SHARED_BODY" in _convert(stream)


# Conversion regressions


def test_epub_metadata_nodevalue():
    from defusedxml.minidom import parseString
    from markitdown.converters._epub_converter import EpubConverter

    xml_data = (
        '<package xmlns:dc="http://purl.org/dc/elements/1.1/">'
        "<dc:title><span>Structured</span> Title</dc:title>"
        "<dc:creator><name>Author 1</name></dc:creator>"
        "<dc:creator>Author 2</dc:creator>"
        "<dc:publisher></dc:publisher>"
        "<dc:description/>"
        "</package>"
    )
    dom = parseString(xml_data)
    converter = EpubConverter()

    title = converter._get_text_from_node(dom, "dc:title")
    assert title == "Structured Title"

    creators = converter._get_all_texts_from_nodes(dom, "dc:creator")
    assert creators == ["Author 1", "Author 2"]

    publisher = converter._get_text_from_node(dom, "dc:publisher")
    assert publisher is None

    missing = converter._get_text_from_node(dom, "dc:date")
    assert missing is None


_EPUB_CONTAINER = (
    '<?xml version="1.0"?>'
    '<container version="1.0" '
    'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
    '<rootfiles><rootfile full-path="OEBPS/content.opf" '
    'media-type="application/oebps-package+xml"/></rootfiles></container>'
)

_EPUB_OPF = (
    '<?xml version="1.0"?>'
    '<package xmlns="http://www.idpf.org/2007/opf" version="2.0" '
    'unique-identifier="id">'
    '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
    "<dc:title>Example book</dc:title></metadata>"
    '<manifest><item id="c1" href="ch1.xhtml" '
    'media-type="application/xhtml+xml"/></manifest>'
    '<spine><itemref idref="c1"/></spine></package>'
)

_EPUB_CHAPTER = (
    '<html xmlns="http://www.w3.org/1999/xhtml"><body>'
    "<p>Chapter text.</p>"
    '<img alt="diagram" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUg=="/>'
    "</body></html>"
)


def _build_epub_with_data_uri() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip")
        zf.writestr("META-INF/container.xml", _EPUB_CONTAINER)
        zf.writestr("OEBPS/content.opf", _EPUB_OPF)
        zf.writestr("OEBPS/ch1.xhtml", _EPUB_CHAPTER)
    return buf.getvalue()


def test_epub_honors_keep_data_uris() -> None:
    """EPUB chapters must be converted with the options the caller passed."""
    result = MarkItDown().convert_stream(
        io.BytesIO(_build_epub_with_data_uri()),
        stream_info=StreamInfo(extension=".epub"),
        keep_data_uris=True,
    )

    assert (
        "![diagram](data:image/png;base64,iVBORw0KGgoAAAANSUhEUg==)" in result.markdown
    )


def test_epub_truncates_data_uris_by_default() -> None:
    """Without the option, the default truncation must still apply."""
    result = MarkItDown().convert_stream(
        io.BytesIO(_build_epub_with_data_uri()),
        stream_info=StreamInfo(extension=".epub"),
    )

    assert "![diagram](data:image/png;base64...)" in result.markdown
    assert "iVBORw0KGgo" not in result.markdown


def test_epub_metadata_and_text_are_unchanged() -> None:
    """The rest of the conversion must not move."""
    result = MarkItDown().convert_stream(
        io.BytesIO(_build_epub_with_data_uri()),
        stream_info=StreamInfo(extension=".epub"),
    )

    assert result.title == "Example book"
    assert "**Title:** Example book" in result.markdown
    assert "Chapter text." in result.markdown


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))


@pytest.mark.parametrize("container_prefix", ["", "c:"])
@pytest.mark.parametrize("package_prefix", ["", "opf:"])
@pytest.mark.parametrize("metadata_prefix", ["dc:", "metadata:"])
def test_epub_namespace_prefixes_preserve_chapters_and_metadata(
    container_prefix, package_prefix, metadata_prefix
):
    stream = _build_epub(
        [("c1", "chapter.xhtml")],
        ["c1"],
        {"OEBPS/chapter.xhtml": ("Chapter", "NAMESPACEBODY")},
    )
    archive = io.BytesIO()
    with zipfile.ZipFile(stream) as source, zipfile.ZipFile(archive, "w") as target:
        for member in source.namelist():
            content = source.read(member)
            if member == "META-INF/container.xml" and container_prefix:
                xml = content.decode().replace(
                    'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"',
                    'xmlns:c="urn:oasis:names:tc:opendocument:xmlns:container"',
                )
                for name in ("container", "rootfiles", "rootfile"):
                    xml = xml.replace(f"<{name}", f"<{container_prefix}{name}")
                    xml = xml.replace(f"</{name}", f"</{container_prefix}{name}")
                content = xml.encode()
            elif member == "OEBPS/content.opf":
                xml = (
                    content.decode().replace("xmlns:dc=", "xmlns:metadata=")
                    if metadata_prefix == "metadata:"
                    else content.decode()
                )
                if metadata_prefix == "metadata:":
                    xml = xml.replace("<dc:", "<metadata:").replace(
                        "</dc:", "</metadata:"
                    )
                if package_prefix:
                    xml = xml.replace(
                        'xmlns="http://www.idpf.org/2007/opf"',
                        'xmlns:opf="http://www.idpf.org/2007/opf"',
                    )
                    for name in (
                        "package",
                        "metadata",
                        "manifest",
                        "itemref",
                        "item",
                        "spine",
                    ):
                        xml = xml.replace(f"<{name} ", f"<{package_prefix}{name} ")
                        xml = xml.replace(f"<{name}>", f"<{package_prefix}{name}>")
                        xml = xml.replace(f"</{name}>", f"</{package_prefix}{name}>")
                content = xml.encode()
            target.writestr(member, content)
    archive.seek(0)
    result = EpubConverter().convert(archive, StreamInfo(extension=".epub"))
    assert result.title == "Encoded Hrefs"
    assert "NAMESPACEBODY" in result.markdown


def test_epub_legacy_unqualified_xml_preserves_chapter_and_title():
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr(
            "META-INF/container.xml",
            '<container><rootfiles><rootfile full-path="book.opf"/></rootfiles></container>',
        )
        z.writestr(
            "book.opf",
            '<package><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Legacy title</dc:title></metadata>'
            '<manifest><item id="c" href="chapter.xhtml"/></manifest>'
            '<spine><itemref idref="c"/></spine></package>',
        )
        z.writestr("chapter.xhtml", "<html><body>Legacy chapter</body></html>")
    archive.seek(0)
    result = EpubConverter().convert(archive, StreamInfo(extension=".epub"))
    assert result.title == "Legacy title"
    assert "Legacy chapter" in result.markdown


def test_epub_foreign_namespace_names_do_not_override_metadata_or_chapters():
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("META-INF/container.xml", CONTAINER_XML)
        z.writestr(
            "OEBPS/content.opf",
            '<package xmlns="http://www.idpf.org/2007/opf" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:foreign="urn:foreign">'
            "<metadata><foreign:title>Foreign title</foreign:title>"
            "<dc:title>Real title</dc:title></metadata><manifest>"
            '<item id="c" href="chapter.xhtml"/>'
            '<foreign:item id="c" href="foreign.xhtml"/></manifest>'
            '<spine><itemref idref="c"/><foreign:itemref idref="bad"/></spine>'
            "</package>",
        )
        z.writestr("OEBPS/chapter.xhtml", "<html><body>Real chapter</body></html>")
        z.writestr("OEBPS/foreign.xhtml", "<html><body>Foreign chapter</body></html>")
    archive.seek(0)
    result = EpubConverter().convert(archive, StreamInfo(extension=".epub"))
    assert result.title == "Real title"
    assert "Real chapter" in result.markdown
    assert "Foreign" not in result.markdown
