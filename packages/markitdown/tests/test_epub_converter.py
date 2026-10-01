import io
import zipfile

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import EpubConverter

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


def _build_epub(
    manifest_items,
    spine_ids,
    documents,
    *,
    container_prefix="",
    package_prefix="",
    dc_prefix="dc",
) -> io.BytesIO:
    """Assemble a minimal EPUB from manifest entries and ZIP member names."""
    package_xmlns = f"xmlns:{package_prefix}" if package_prefix else "xmlns"
    dc_xmlns = f"xmlns:{dc_prefix}" if dc_prefix else "xmlns"
    package_tag = f"{package_prefix}:" if package_prefix else ""
    dc_tag = f"{dc_prefix}:" if dc_prefix else ""
    manifest = "\n".join(
        f'<{package_tag}item id="{item_id}" href="{href}" media-type="application/xhtml+xml"/>'
        for item_id, href in manifest_items
    )
    spine = "\n".join(
        f'<{package_tag}itemref idref="{item_id}"/>' for item_id in spine_ids
    )
    opf = f"""<?xml version="1.0"?>
<{package_tag}package {package_xmlns}="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">
  <{package_tag}metadata {dc_xmlns}="http://purl.org/dc/elements/1.1/">
    <{dc_tag}title>Encoded Hrefs</{dc_tag}title>
    <{dc_tag}creator>First Author</{dc_tag}creator>
    <{dc_tag}creator>Second Author</{dc_tag}creator>
  </{package_tag}metadata>
  <{package_tag}manifest>{manifest}</{package_tag}manifest>
  <{package_tag}spine>{spine}</{package_tag}spine>
</{package_tag}package>
"""

    container_xml = CONTAINER_XML
    if container_prefix:
        container_xml = container_xml.replace("xmlns=", f"xmlns:{container_prefix}=")
        for tag in ("container", "rootfiles", "rootfile"):
            container_xml = container_xml.replace(
                f"<{tag} ", f"<{container_prefix}:{tag} "
            )
            container_xml = container_xml.replace(
                f"<{tag}>", f"<{container_prefix}:{tag}>"
            )
            container_xml = container_xml.replace(
                f"</{tag}>", f"</{container_prefix}:{tag}>"
            )

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("mimetype", "application/epub+zip")
        z.writestr("META-INF/container.xml", container_xml)
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


@pytest.mark.parametrize("public_api", [False, True])
@pytest.mark.parametrize(
    "container_prefix, package_prefix, dc_prefix",
    [
        ("", "", "dc"),
        ("ocf", "", "dc"),
        ("", "opf", "dc"),
        ("", "", "meta"),
        ("ocf", "opf", ""),
    ],
)
def test_namespace_prefixes_preserve_metadata_and_spine_order(
    public_api, container_prefix, package_prefix, dc_prefix
) -> None:
    stream = _build_epub(
        manifest_items=[("c1", "first.xhtml"), ("c2", "second.xhtml")],
        spine_ids=["c2", "c1"],
        documents={
            "OEBPS/first.xhtml": ("First", "First chapter body"),
            "OEBPS/second.xhtml": ("Second", "Second chapter body"),
        },
        container_prefix=container_prefix,
        package_prefix=package_prefix,
        dc_prefix=dc_prefix,
    )
    stream_info = StreamInfo(mimetype="application/epub+zip", extension=".epub")
    if public_api:
        result = MarkItDown().convert_stream(stream, stream_info=stream_info)
    else:
        result = EpubConverter().convert(stream, stream_info)

    assert result.title == "Encoded Hrefs"
    assert "**Authors:** First Author, Second Author" in result.markdown
    assert "First chapter body" in result.markdown
    assert "Second chapter body" in result.markdown
    assert result.markdown.index("Second chapter body") < result.markdown.index(
        "First chapter body"
    )


@pytest.mark.parametrize("unqualified", [False, True])
def test_package_elements_ignore_foreign_namespaces(unqualified) -> None:
    stream = _build_epub(
        manifest_items=[("c1", "chapter.xhtml")],
        spine_ids=["c1"],
        documents={"OEBPS/chapter.xhtml": ("Chapter", "Expected chapter body")},
    )
    modified = io.BytesIO()
    with zipfile.ZipFile(stream) as source, zipfile.ZipFile(modified, "w") as target:
        for name in source.namelist():
            data = source.read(name)
            if name == "META-INF/container.xml":
                data = data.replace(
                    b"<rootfiles>",
                    b'<rootfiles><ext:rootfile xmlns:ext="urn:example:extension" '
                    b'full-path="missing.opf"/>',
                )
                if unqualified:
                    data = data.replace(
                        b' xmlns="urn:oasis:names:tc:opendocument:xmlns:container"', b""
                    )
            elif name == "OEBPS/content.opf":
                data = (
                    data.replace(
                        b"</manifest>",
                        b'<ext:item xmlns:ext="urn:example:extension" '
                        b'id="c1" href="missing.xhtml"/></manifest>',
                    )
                    .replace(
                        b"<spine>",
                        b'<spine><ext:itemref xmlns:ext="urn:example:extension" idref="c1"/>',
                    )
                    .replace(
                        b"<dc:title>",
                        b'<ext:title xmlns:ext="urn:example:extension">Wrong title</ext:title><dc:title>',
                    )
                )
                if unqualified:
                    data = data.replace(b' xmlns="http://www.idpf.org/2007/opf"', b"")
            target.writestr(name, data)
    modified.seek(0)

    result = MarkItDown().convert_stream(
        modified, stream_info=StreamInfo(extension=".epub")
    )
    assert result.title == "Encoded Hrefs"
    assert result.markdown.count("Expected chapter body") == 1
    assert "Wrong title" not in result.markdown


if __name__ == "__main__":
    test_percent_encoded_href_resolves_to_zip_entry()
    test_non_ascii_percent_encoded_href_resolves()
    test_literally_encoded_zip_entry_still_resolves()
    test_parent_relative_href_resolves()
    print("All tests passed")
