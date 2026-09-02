#!/usr/bin/env python3 -m pytest
import io
import zipfile

from markitdown import MarkItDown

_W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def _paragraph(text: str, num_id: str | None = None, ilvl: int = 0) -> str:
    num_pr = (
        f'<w:numPr><w:ilvl w:val="{ilvl}"/><w:numId w:val="{num_id}"/></w:numPr>'
        if num_id is not None
        else ""
    )
    return f"<w:p><w:pPr>{num_pr}</w:pPr>" f"<w:r><w:t>{text}</w:t></w:r></w:p>"


def _level(ilvl: int, num_fmt: str, left: int) -> str:
    return (
        f'<w:lvl w:ilvl="{ilvl}">'
        f'<w:start w:val="1"/><w:numFmt w:val="{num_fmt}"/>'
        '<w:lvlText w:val="%1)"/><w:lvlJc w:val="left"/>'
        f'<w:pPr><w:ind w:left="{left}" w:hanging="360"/></w:pPr>'
        "</w:lvl>"
    )


def _numbering(levels: dict[tuple[int, int], tuple[str, int]]) -> str:
    """Builds a numbering part.

    Args:
        levels: Maps (numId, ilvl) to (numFmt, left indent) definitions; each
            numId gets its own abstractNum.
    """
    abstracts = []
    nums = []
    for abstract_id, ((num_id, _), _) in enumerate(levels.items()):
        lvl_xml = "".join(
            _level(ilvl, fmt, left)
            for (nid, ilvl), (fmt, left) in levels.items()
            if nid == num_id
        )
        abstracts.append(
            f'<w:abstractNum w:abstractNumId="{abstract_id}">'
            '<w:multiLevelType w:val="hybridMultilevel"/>'
            f"{lvl_xml}</w:abstractNum>"
        )
        nums.append(
            f'<w:num w:numId="{num_id}">'
            f'<w:abstractNumId w:val="{abstract_id}"/></w:num>'
        )
    return (
        '<?xml version="1.0"?>'
        f"<w:numbering {_W_NS}>{''.join(abstracts)}{''.join(nums)}</w:numbering>"
    )


def _docx(paragraphs: list[str], numbering: str | None = None) -> io.BytesIO:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            "</Types>",
        )
        z.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            "</Relationships>",
        )
        z.writestr(
            "word/document.xml",
            '<?xml version="1.0"?>'
            f"<w:document {_W_NS}><w:body>{''.join(paragraphs)}</w:body></w:document>",
        )
        if numbering is not None:
            z.writestr("word/numbering.xml", numbering)
    buf.seek(0)
    return buf


def test_nested_list_with_separate_numbering():
    """A visually-nested sub-list that uses its own numbering definition
    (as in issue #2323) must be converted as a nested list."""
    docx = _docx(
        [
            _paragraph("Item 1", num_id="1"),
            _paragraph("Item 2", num_id="1"),
            _paragraph("Item 2.1", num_id="2"),
            _paragraph("Item 2.2", num_id="2"),
            _paragraph("Item 3", num_id="1"),
        ],
        numbering=_numbering(
            {
                ("1", 0): ("decimal", 720),
                ("1", 1): ("bullet", 1440),
                ("2", 0): ("lowerLetter", 1080),
            }
        ),
    )
    result = MarkItDown(enable_plugins=False).convert(docx).text_content
    assert "Item 2.1" in result and "Item 3" in result
    # The sub-list must be nested (indented), not flattened to the top level.
    assert "   * Item 2.1" in result
    assert "\n3. Item 2.1" not in result


def test_sibling_lists_with_same_indent_are_not_nested():
    """Consecutive lists at the same indent must keep their own numbering
    definitions; the nesting rewrite must not trigger."""
    docx = _docx(
        [
            _paragraph("A", num_id="1"),
            _paragraph("B", num_id="2"),
        ],
        numbering=_numbering(
            {
                ("1", 0): ("decimal", 720),
                ("2", 0): ("decimal", 720),
            }
        ),
    )
    result = MarkItDown(enable_plugins=False).convert(docx).text_content
    assert "   * B" not in result


def test_lists_separated_by_text_are_not_nested():
    """A deeper-indented list that does not directly follow another list
    paragraph must not be rewritten."""
    docx = _docx(
        [
            _paragraph("A", num_id="1"),
            _paragraph("plain text"),
            _paragraph("B", num_id="2"),
        ],
        numbering=_numbering(
            {
                ("1", 0): ("decimal", 720),
                ("2", 0): ("lowerLetter", 1080),
            }
        ),
    )
    result = MarkItDown(enable_plugins=False).convert(docx).text_content
    assert "   * B" not in result
