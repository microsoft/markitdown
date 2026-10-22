"""DOCX field text (w:fldSimple, w:fldChar/w:instrText) must survive conversion.

Word stores field display text in two forms: simple fields (``w:fldSimple``),
whose cached result is held in child runs (or, for MACROBUTTON fields, in the
``w:instr`` attribute), and complex fields, whose result runs sit between the
"separate" and "end" ``w:fldChar`` markers. MACROBUTTON fields — used by
standards-body templates for "Proposal N:"/"Observation N:" lines — have no
result runs at all: their display text is the trailing argument of the field
instruction. Mammoth ignores ``w:fldSimple`` entirely and never emits field
instructions, so this display text silently vanishes (issue #1247).
"""

import io
import zipfile
from pathlib import Path

from markitdown import MarkItDown, StreamInfo

TEST_DOCX = Path(__file__).parent / "test_files" / "test.docx"

FIELDS_XML = (
    # Simple field with a cached display run (Word's usual serialization).
    b"<w:p>"
    b'<w:fldSimple w:instr=" MACROBUTTON NoMacro Proposal 1: Support feature X. ">'
    b'<w:r><w:t xml:space="preserve">Proposal 1: Support feature X.</w:t></w:r>'
    b"</w:fldSimple>"
    b"</w:p>"
    # Simple MACROBUTTON field with no child runs: the display text exists
    # only as the trailing argument of the field instruction.
    b"<w:p>"
    b'<w:fldSimple w:instr=" MACROBUTTON NoMacro Proposal 2: Adopt option B. "/>'
    b"</w:p>"
    # Complex MACROBUTTON field: no "separate"/result runs, display text is
    # split across w:instrText runs after the macro name.
    b"<w:p>"
    b'<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
    b'<w:r><w:instrText xml:space="preserve"> MACROBUTTON NoMacro </w:instrText></w:r>'
    b'<w:r><w:instrText xml:space="preserve">Observation 1: Latency is reduced.</w:instrText></w:r>'
    b'<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    b"</w:p>"
    # Complex field with a separator: the cached result runs must keep
    # converting, and the instruction must stay out of the output.
    b"<w:p>"
    b'<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
    b'<w:r><w:instrText xml:space="preserve"> REF SomeBookmark \\h </w:instrText></w:r>'
    b'<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
    b"<w:r><w:t>Cached field result.</w:t></w:r>"
    b'<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    b"</w:p>"
    # Simple HYPERLINK field: at minimum the display text must survive.
    b"<w:p>"
    b'<w:fldSimple w:instr=" HYPERLINK &quot;https://example.test/&quot; ">'
    b"<w:r><w:t>Example link text</w:t></w:r>"
    b"</w:fldSimple>"
    b"</w:p>"
)


def _docx_with_fields() -> io.BytesIO:
    fixture = io.BytesIO()
    with zipfile.ZipFile(TEST_DOCX) as source, zipfile.ZipFile(fixture, "w") as target:
        for item in source.infolist():
            content = source.read(item)
            if item.filename == "word/document.xml":
                assert content.count(b"<w:body>") == 1
                content = content.replace(b"<w:body>", b"<w:body>" + FIELDS_XML, 1)
            target.writestr(item, content)
    fixture.seek(0)
    return fixture


def test_docx_field_text_is_preserved() -> None:
    markitdown = MarkItDown()
    result = markitdown.convert_stream(
        _docx_with_fields(), stream_info=StreamInfo(extension=".docx")
    ).markdown

    # Field display/result text must appear in the output.
    assert "Proposal 1: Support feature X." in result
    assert "Proposal 2: Adopt option B." in result
    assert "Observation 1: Latency is reduced." in result
    assert "Cached field result." in result
    assert "Example link text" in result

    # Field instructions must not leak into the output.
    assert "MACROBUTTON" not in result
    assert "NoMacro" not in result
    assert "SomeBookmark" not in result
    assert "HYPERLINK" not in result

    # The rest of the document still converts.
    assert "# Abstract" in result


def test_docx_fields_conversion_matches_unmodified_document() -> None:
    markitdown = MarkItDown()
    expected = markitdown.convert(TEST_DOCX).markdown
    actual = markitdown.convert_stream(
        _docx_with_fields(), stream_info=StreamInfo(extension=".docx")
    ).markdown

    # Besides the injected field paragraphs, the output is unchanged.
    assert actual.endswith(expected)


def test_pre_process_fields_returns_fieldless_content_unchanged() -> None:
    from markitdown.converter_utils.docx.pre_process import _pre_process_fields

    with zipfile.ZipFile(TEST_DOCX) as source:
        content = source.read("word/document.xml")

    assert _pre_process_fields(content) == content
