#!/usr/bin/env python3 -m pytest
import io
import os
import zipfile

from markitdown import MarkItDown

# Word represents a nested list in either of two ways: as a deeper "w:ilvl"
# within the parent's "w:numId", or as an entirely new "w:numId" at "w:ilvl" 0
# that is simply indented further. Both render identically in Word, so both
# must produce a nested list in the Markdown output.

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

_W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

_CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>"""

_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

_DOCUMENT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>"""


def _build_docx(paragraphs, abstract_nums, nums) -> io.BytesIO:
    """
    Builds a minimal DOCX exercising a particular list structure.

    Args:
        paragraphs: (text, num_id, ilvl) tuples. A num_id of None makes the
            paragraph ordinary body text.
        abstract_nums: abstract_num_id -> [(ilvl, num_fmt, indent), ...].
        nums: num_id -> abstract_num_id.

    Returns:
        io.BytesIO: The generated DOCX file.
    """
    body = []
    for text, num_id, ilvl in paragraphs:
        if num_id is None:
            body.append(f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>")
        else:
            body.append(
                f'<w:p><w:pPr><w:numPr><w:ilvl w:val="{ilvl}"/>'
                f'<w:numId w:val="{num_id}"/></w:numPr></w:pPr>'
                f"<w:r><w:t>{text}</w:t></w:r></w:p>"
            )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document {_W_NS}><w:body>{"".join(body)}</w:body></w:document>'
    )

    definitions = []
    for abstract_num_id, levels in abstract_nums.items():
        lvls = []
        for ilvl, num_fmt, indent in levels:
            indentation = (
                f'<w:pPr><w:ind w:left="{indent}" w:hanging="360"/></w:pPr>'
                if indent is not None
                else ""
            )
            lvls.append(
                f'<w:lvl w:ilvl="{ilvl}"><w:numFmt w:val="{num_fmt}"/>'
                f"{indentation}</w:lvl>"
            )
        definitions.append(
            f'<w:abstractNum w:abstractNumId="{abstract_num_id}">'
            f'{"".join(lvls)}</w:abstractNum>'
        )
    for num_id, abstract_num_id in nums.items():
        definitions.append(
            f'<w:num w:numId="{num_id}">'
            f'<w:abstractNumId w:val="{abstract_num_id}"/></w:num>'
        )
    numbering = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:numbering {_W_NS}>{"".join(definitions)}</w:numbering>'
    )

    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as docx:
        docx.writestr("[Content_Types].xml", _CONTENT_TYPES)
        docx.writestr("_rels/.rels", _RELS)
        docx.writestr("word/_rels/document.xml.rels", _DOCUMENT_RELS)
        docx.writestr("word/document.xml", document)
        docx.writestr("word/numbering.xml", numbering)
    output.seek(0)
    return output


def _convert(paragraphs, abstract_nums, nums) -> str:
    markitdown = MarkItDown()
    result = markitdown.convert_stream(
        _build_docx(paragraphs, abstract_nums, nums), file_extension=".docx"
    )
    return result.text_content.strip()


def test_docx_multilevel_lists() -> None:
    # A sub-list that Word stored as a separate numbering definition must still
    # nest, rather than being flattened into its parent and renumbered.
    markitdown = MarkItDown()
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "multilevel_lists.docx"))

    assert (
        "1. Item 1\n"
        "2. Item 2\n"
        "   * Item 2.1\n"
        "   * Item 2.2\n"
        "3. Item 3\n"
        "   1. Item 3.1\n"
        "   2. Item 3.2" in result.text_content
    )
    # Flattening previously renumbered the sub-items as siblings of Item 3.
    assert "4. Item 3.1" not in result.text_content


def test_docx_sub_list_as_new_num_id() -> None:
    # The sub-list is a different w:numId at w:ilvl 0, distinguishable from its
    # parent only by indentation.
    assert _convert(
        [("A", 1, 0), ("B", 1, 0), ("B.1", 2, 0), ("B.2", 2, 0)],
        {0: [(0, "decimal", 720)], 1: [(0, "decimal", 1080)]},
        {1: 0, 2: 1},
    ) == ("1. A\n2. B\n   1. B.1\n   2. B.2")


def test_docx_sub_list_preserves_bullets() -> None:
    # The sub-list's own numbering defines w:ilvl 1 as decimal, so nesting it by
    # raising w:ilvl alone would silently turn these bullets into numbers.
    assert _convert(
        [("A", 1, 0), ("A.1", 2, 0)],
        {0: [(0, "decimal", 720)], 1: [(0, "bullet", 1080), (1, "decimal", 1080)]},
        {1: 0, 2: 1},
    ) == ("1. A\n   * A.1")


def test_docx_nesting_from_declared_levels_is_unchanged() -> None:
    # Lists that already declare their nesting through w:ilvl must be untouched.
    assert _convert(
        [("A", 1, 0), ("A.1", 1, 1), ("B", 1, 0)],
        {0: [(0, "decimal", 720), (1, "bullet", 1440)]},
        {1: 0},
    ) == ("1. A\n   * A.1\n2. B")


def test_docx_equal_level_indents_are_not_flattened() -> None:
    # Both levels carry identical indentation, so indentation alone cannot
    # separate them; the declared w:ilvl has to win within a single w:numId.
    assert _convert(
        [("A", 1, 0), ("A.1", 1, 1)],
        {0: [(0, "decimal", 1080), (1, "bullet", 1080)]},
        {1: 0},
    ) == ("1. A\n   * A.1")


def test_docx_list_interrupted_by_paragraph() -> None:
    # Body text ends the surrounding list, so the following list starts over at
    # the top level even though it is indented further.
    converted = _convert(
        [("A", 1, 0), ("break", None, None), ("B", 2, 0)],
        {0: [(0, "decimal", 720)], 1: [(0, "decimal", 1080)]},
        {1: 0, 2: 1},
    )
    assert "1. A" in converted
    assert "\n1. B" in converted


def test_docx_deep_nesting_keeps_every_item() -> None:
    # mammoth's default style map only maps five levels of list nesting, and a
    # paragraph promoted past the last of them would drop out of the list.
    converted = _convert(
        [(f"L{index}", index + 1, 0) for index in range(7)],
        {index: [(0, "decimal", 720 + 360 * index)] for index in range(7)},
        {index + 1: index for index in range(7)},
    )
    for index in range(7):
        assert f"L{index}" in converted
