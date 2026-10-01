import io
import zipfile

import pytest

from markitdown import MarkItDown, StreamInfo


_CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""


def _docx_with_paragraph(paragraph_xml: str) -> io.BytesIO:
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>{paragraph_xml}</w:p>
  </w:body>
</w:document>"""

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("[Content_Types].xml", _CONTENT_TYPES)
        archive.writestr("_rels/.rels", _RELS)
        archive.writestr("word/document.xml", document_xml)

    buffer.seek(0)
    return buffer


def _run(text: str, formatting: str = "") -> str:
    properties = f"<w:rPr>{formatting}</w:rPr>" if formatting else ""
    return f'<w:r>{properties}<w:t xml:space="preserve">{text}</w:t></w:r>'


def _convert_docx(paragraph_xml: str) -> str:
    result = MarkItDown().convert_stream(
        _docx_with_paragraph(paragraph_xml),
        stream_info=StreamInfo(extension=".docx"),
    )
    return result.markdown


@pytest.mark.parametrize(
    "formatting",
    ["<w:b/>", "<w:i/>", '<w:u w:val="single"/>', "<w:strike/>"],
)
def test_docx_formatted_space_between_words_is_kept(formatting: str) -> None:
    """A space can carry formatting of its own in a Word document.

    Runs are only merged when their formatting matches, so such a space reaches
    the Markdown conversion as an element holding nothing but whitespace. Dropping
    it runs the surrounding words together.
    """
    paragraph = _run("First") + _run(" ", formatting) + _run("Last")

    assert _convert_docx(paragraph) == "First Last"


def test_docx_unformatted_space_between_words_is_kept() -> None:
    paragraph = _run("First") + _run(" ") + _run("Last")

    assert _convert_docx(paragraph) == "First Last"


def test_docx_formatted_words_are_still_formatted() -> None:
    paragraph = _run("First") + _run(" bold ", "<w:b/>") + _run("Last")

    assert _convert_docx(paragraph) == "First **bold** Last"
