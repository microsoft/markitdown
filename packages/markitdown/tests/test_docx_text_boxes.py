"""A DrawingML text box keeps its text in the document and must not be dropped.

Mammoth reaches a ``w:txbxContent`` only through the legacy VML path
(``w:pict`` -> ``v:shape`` -> ``v:textbox``). A modern text box is a DrawingML
shape instead, and the element that holds it is read as a picture, so its text is
dropped silently. ``_pre_process_text_boxes`` rewrites it into the form Mammoth
reads.
"""

import io
import re
import zipfile
from pathlib import Path

from markitdown import MarkItDown

TEST_DOCX = Path(__file__).parent / "test_files" / "test.docx"

DRAWING_TEXT_BOX = (
    "<w:r><w:drawing><wp:inline distT='0' distB='0' distL='0' distR='0'>"
    "<wp:extent cx='2743200' cy='914400'/><wp:docPr id='9001' name='Text Box 1'/>"
    "<a:graphic><a:graphicData "
    "uri='http://schemas.microsoft.com/office/word/2010/wordprocessingShape'>"
    "<wps:wsp><wps:txbx><w:txbxContent>"
    "<w:p><w:r><w:t>CALLOUT MARKER</w:t></w:r></w:p>"
    "</w:txbxContent></wps:txbx></wps:wsp>"
    "</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>"
)

VML_TEXT_BOX = (
    "<w:pict><v:shape><v:textbox><w:txbxContent>"
    "<w:p><w:r><w:t>CALLOUT MARKER</w:t></w:r></w:p>"
    "</w:txbxContent></v:textbox></v:shape></w:pict>"
)

ALTERNATE_CONTENT_TEXT_BOX = (
    "<w:r><mc:AlternateContent>"
    f"<mc:Choice Requires='wps'>{DRAWING_TEXT_BOX}</mc:Choice>"
    f"<mc:Fallback>{VML_TEXT_BOX}</mc:Fallback>"
    "</mc:AlternateContent></w:r>"
)


def _docx_with(markup: str) -> io.BytesIO:
    """Return test.docx with `markup` appended to its first paragraph."""
    fixture = io.BytesIO()
    with zipfile.ZipFile(TEST_DOCX) as source, zipfile.ZipFile(fixture, "w") as target:
        for item in source.infolist():
            content = source.read(item)
            if item.filename == "word/document.xml":
                document = content.decode()
                paragraph = re.search(r"<w:p\b[^>]*>.*?</w:p>", document, re.DOTALL)
                assert paragraph is not None
                patched = paragraph.group(0).replace(
                    "</w:p>", markup.replace("'", '"') + "</w:p>", 1
                )
                document = document.replace(paragraph.group(0), patched, 1)
                content = document.encode()
            target.writestr(item, content)
    fixture.seek(0)
    return fixture


def test_a_drawing_text_box_is_read() -> None:
    markdown = MarkItDown().convert(_docx_with(DRAWING_TEXT_BOX)).markdown

    assert markdown.count("CALLOUT MARKER") == 1


def test_an_alternate_content_text_box_is_read_once() -> None:
    """Word writes the same text twice, as a choice and as a VML fallback.

    Mammoth reads the fallback, so promoting the choice as well would double it.
    """
    markdown = MarkItDown().convert(_docx_with(ALTERNATE_CONTENT_TEXT_BOX)).markdown

    assert markdown.count("CALLOUT MARKER") == 1


def test_a_document_without_a_text_box_is_unchanged() -> None:
    expected = MarkItDown().convert(TEST_DOCX).markdown

    assert MarkItDown().convert(_docx_with("")).markdown == expected
