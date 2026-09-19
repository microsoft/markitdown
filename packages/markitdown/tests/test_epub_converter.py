import io
import zipfile

from markitdown import StreamInfo
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


if __name__ == "__main__":
    test_percent_encoded_href_resolves_to_zip_entry()
    test_non_ascii_percent_encoded_href_resolves()
    test_literally_encoded_zip_entry_still_resolves()
    test_parent_relative_href_resolves()
    print("All tests passed")
