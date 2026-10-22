"""Tests for the OpenDocument converter (``_odf_converter.py``).

Fixtures are assembled in memory rather than checked in as binaries, because the
interesting cases are all *structural* and a hand-written XML fragment shows what
is being asserted. Two of them are worth reading before the assertions:

* the ``number-columns-repeated="16384"`` tail that every LibreOffice row carries,
  which is what a naive implementation turns into a 16384-column table;
* a cell whose text contains a pipe, which silently adds a column if it is not
  escaped.
"""

import io
import zipfile

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import OdfConverter

OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
TABLE_NS = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
DRAW_NS = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
PRESENTATION_NS = "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"

DOCUMENT_HEADER = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    "<office:document-content"
    f' xmlns:office="{OFFICE_NS}"'
    f' xmlns:text="{TEXT_NS}"'
    f' xmlns:table="{TABLE_NS}"'
    f' xmlns:draw="{DRAW_NS}"'
    f' xmlns:presentation="{PRESENTATION_NS}"'
    ' xmlns:dc="http://purl.org/dc/elements/1.1/"'
    ' xmlns:xlink="http://www.w3.org/1999/xlink"'
    ' xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"'
    ' office:version="1.3">'
)


def _package(
    body: str, *, title: str = "Test Document", meta: bool = True
) -> io.BytesIO:
    """Build a minimal but structurally valid OpenDocument package."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("mimetype", "application/vnd.oasis.opendocument.text")
        archive.writestr(
            "content.xml", DOCUMENT_HEADER + body + "</office:document-content>"
        )
        if meta:
            archive.writestr(
                "meta.xml",
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<office:document-meta xmlns:office="{OFFICE_NS}"'
                ' xmlns:dc="http://purl.org/dc/elements/1.1/">'
                f"<office:meta><dc:title>{title}</dc:title></office:meta>"
                "</office:document-meta>",
            )
    buffer.seek(0)
    return buffer


def _flat(body: str) -> io.BytesIO:
    """Build a flat OpenDocument file: the same XML, no package."""
    text = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<office:document"
        f' xmlns:office="{OFFICE_NS}"'
        f' xmlns:text="{TEXT_NS}"'
        f' xmlns:table="{TABLE_NS}"'
        f' xmlns:draw="{DRAW_NS}"'
        f' xmlns:presentation="{PRESENTATION_NS}"'
        ' xmlns:dc="http://purl.org/dc/elements/1.1/"'
        ' xmlns:xlink="http://www.w3.org/1999/xlink"'
        ' office:version="1.3">'
        "<office:meta><dc:title>Flat</dc:title></office:meta>"
        + body
        + "</office:document>"
    )
    return io.BytesIO(text.encode("utf-8"))


def _text_body(inner: str) -> str:
    return f"<office:body><office:text>{inner}</office:text></office:body>"


def _sheet_body(inner: str) -> str:
    return (
        f"<office:body><office:spreadsheet>{inner}</office:spreadsheet></office:body>"
    )


def _slide_body(inner: str) -> str:
    return (
        f"<office:body><office:presentation>{inner}</office:presentation></office:body>"
    )


def _convert(stream: io.BytesIO, extension: str = ".odt"):
    return OdfConverter().convert(
        stream, StreamInfo(extension=extension, mimetype="application/octet-stream")
    )


class TestAccepts:
    @pytest.mark.parametrize(
        "extension", [".odt", ".ods", ".odp", ".fodt", ".fods", ".fodp"]
    )
    def test_accepts_by_extension(self, extension):
        converter = OdfConverter()
        assert converter.accepts(io.BytesIO(), StreamInfo(extension=extension))

    @pytest.mark.parametrize(
        "mimetype",
        [
            "application/vnd.oasis.opendocument.text",
            "application/vnd.oasis.opendocument.spreadsheet",
            "application/vnd.oasis.opendocument.presentation",
            "application/vnd.oasis.opendocument.text-template",
        ],
    )
    def test_accepts_by_mimetype(self, mimetype):
        assert OdfConverter().accepts(io.BytesIO(), StreamInfo(mimetype=mimetype))

    @pytest.mark.parametrize("extension", [".docx", ".zip", ".epub", ".csv", ""])
    def test_rejects_other_extensions(self, extension):
        assert not OdfConverter().accepts(
            io.BytesIO(), StreamInfo(extension=extension, mimetype="application/zip")
        )

    def test_zip_converter_does_not_steal_odt(self):
        """A .odt is a ZIP; the ODF converter must be tried before the ZIP one."""
        stream = _package(_text_body("<text:p>from the odf converter</text:p>"))
        result = MarkItDown().convert_stream(
            stream, stream_info=StreamInfo(extension=".odt", filename="doc.odt")
        )
        assert "from the odf converter" in result.markdown


class TestTextDocument:
    def test_headings_use_the_outline_level(self):
        body = _text_body(
            '<text:h text:outline-level="1">One</text:h>'
            '<text:h text:outline-level="3">Three</text:h>'
        )
        markdown = _convert(_package(body)).markdown
        assert "# One" in markdown
        assert "### Three" in markdown

    def test_outline_level_is_clamped_and_defaults_to_one(self):
        body = _text_body(
            '<text:h text:outline-level="99">Too deep</text:h><text:h>No level</text:h>'
        )
        markdown = _convert(_package(body)).markdown
        assert "###### Too deep" in markdown
        assert "# No level" in markdown

    def test_paragraphs_are_separated_by_a_blank_line(self):
        body = _text_body("<text:p>first</text:p><text:p>second</text:p>")
        assert _convert(_package(body)).markdown == "first\n\nsecond"

    def test_whitespace_markup_survives_collapsing(self):
        """`text:s` and `text:tab` are elements, not whitespace, so they survive.

        The XML below also contains a newline and indentation between the
        elements, which must *not* survive.
        """
        body = _text_body(
            '<text:p>a<text:s text:c="3"/>b</text:p>\n'
            "  <text:p>c<text:s/>d</text:p>\n"
            "  <text:p>e<text:tab/>f</text:p>\n"
        )
        markdown = _convert(_package(body)).markdown
        assert "a b" in markdown
        assert "c d" in markdown
        assert "e\tf" in markdown

    def test_line_break_becomes_br(self):
        body = _text_body("<text:p>up<text:line-break/>down</text:p>")
        assert "up<br>down" in _convert(_package(body)).markdown

    def test_hyperlink_is_rendered_as_a_markdown_link(self):
        body = _text_body(
            '<text:p><text:a xlink:href="https://example.com/x">the link</text:a></text:p>'
        )
        assert "[the link](https://example.com/x)" in _convert(_package(body)).markdown

    def test_link_without_href_keeps_its_text(self):
        body = _text_body("<text:p><text:a>bare</text:a></text:p>")
        markdown = _convert(_package(body)).markdown
        assert "bare" in markdown
        assert "[](" not in markdown

    def test_footnote_is_dropped_rather_than_dangling(self):
        body = _text_body(
            '<text:p>claim<text:note text:note-class="footnote">'
            "<text:note-body><text:p>the note body</text:p></text:note-body>"
            "</text:note></text:p>"
        )
        markdown = _convert(_package(body)).markdown
        assert markdown == "claim"
        assert "the note body" not in markdown

    def test_table_of_content_is_not_duplicated(self):
        body = _text_body(
            '<text:table-of-content text:name="toc">'
            "<text:table-of-content-source/></text:table-of-content>"
            '<text:h text:outline-level="1">Real heading</text:h>'
        )
        markdown = _convert(_package(body)).markdown
        assert markdown.count("Real heading") == 1

    def test_unknown_inline_element_keeps_its_text(self):
        body = _text_body(
            "<text:p>keep<text:meta-field>this</text:meta-field></text:p>"
        )
        assert "keepthis" in _convert(_package(body)).markdown


class TestLists:
    def test_bullet_list(self):
        body = _text_body(
            '<text:list text:style-name="L1">'
            "<text:list-item><text:p>one</text:p></text:list-item>"
            "<text:list-item><text:p>two</text:p></text:list-item>"
            "</text:list>"
        )
        assert _convert(_package(body)).markdown == "- one\n- two"

    def test_nested_list_is_indented(self):
        body = _text_body(
            '<text:list text:style-name="L1"><text:list-item>'
            "<text:p>outer</text:p>"
            '<text:list text:style-name="L2"><text:list-item><text:p>inner</text:p>'
            "</text:list-item></text:list>"
            "</text:list-item></text:list>"
        )
        assert _convert(_package(body)).markdown == "- outer\n  - inner"

    def test_second_paragraph_of_an_item_is_a_continuation(self):
        body = _text_body(
            '<text:list text:style-name="L1"><text:list-item>'
            "<text:p>first line</text:p><text:p>second line</text:p>"
            "</text:list-item></text:list>"
        )
        assert _convert(_package(body)).markdown == "- first line\n  second line"

    def test_empty_item_does_not_lose_its_bullet(self):
        body = _text_body(
            '<text:list text:style-name="L1">'
            "<text:list-item/><text:list-item><text:p>kept</text:p></text:list-item>"
            "</text:list>"
        )
        assert _convert(_package(body)).markdown == "-\n- kept"


class TestTables:
    def test_text_table_has_no_title(self):
        body = _text_body(
            '<table:table table:name="Table1">'
            "<table:table-row>"
            "<table:table-cell><text:p>h1</text:p></table:table-cell>"
            "<table:table-cell><text:p>h2</text:p></table:table-cell>"
            "</table:table-row>"
            "<table:table-row>"
            "<table:table-cell><text:p>a</text:p></table:table-cell>"
            "<table:table-cell><text:p>b</text:p></table:table-cell>"
            "</table:table-row>"
            "</table:table>"
        )
        markdown = _convert(_package(body)).markdown
        assert markdown == "| h1 | h2 |\n| --- | --- |\n| a | b |"
        assert "Table1" not in markdown

    def test_pipe_in_a_cell_is_escaped(self):
        body = _sheet_body(
            '<table:table table:name="S"><table:table-row>'
            "<table:table-cell><text:p>a|b</text:p></table:table-cell>"
            "<table:table-cell><text:p>c</text:p></table:table-cell>"
            "</table:table-row></table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        row = next(line for line in markdown.split("\n") if "a" in line)
        assert row == r"| a\|b | c |"
        # The escaped pipe must not add a column: the separator row still declares
        # two columns, so the table is not ragged.
        separator = markdown.split("\n")[3]
        assert separator == "| --- | --- |"

    def test_multi_paragraph_cell_stays_on_one_row(self):
        body = _sheet_body(
            '<table:table table:name="S"><table:table-row>'
            "<table:table-cell><text:p>top</text:p><text:p>bottom</text:p></table:table-cell>"
            "<table:table-cell><text:p>x</text:p></table:table-cell>"
            "</table:table-row></table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert "| top<br>bottom | x |" in markdown

    def test_covered_cell_keeps_the_column(self):
        body = _sheet_body(
            '<table:table table:name="S">'
            "<table:table-row>"
            '<table:table-cell table:number-columns-spanned="2"><text:p>merged</text:p>'
            "</table:table-cell>"
            "<table:table-cell><text:p>third</text:p></table:table-cell>"
            "</table:table-row>"
            "<table:table-row>"
            "<table:table-cell><text:p>1</text:p></table:table-cell>"
            '<table:covered-table-cell table:number-columns-repeated="1"/>'
            "<table:table-cell><text:p>3</text:p></table:table-cell>"
            "</table:table-row>"
            "</table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        rows = [line for line in markdown.split("\n") if line.startswith("|")]
        assert rows == [
            "| merged | third |  |",
            "| --- | --- | --- |",
            "| 1 |  | 3 |",
        ]


class TestSpreadsheetRepetition:
    def test_trailing_repeated_empty_cells_do_not_set_the_width(self):
        """The case that makes a naive implementation produce a 16384-column table."""
        body = _sheet_body(
            '<table:table table:name="S">'
            "<table:table-row>"
            "<table:table-cell><text:p>name</text:p></table:table-cell>"
            "<table:table-cell><text:p>count</text:p></table:table-cell>"
            '<table:table-cell table:number-columns-repeated="16384"/>'
            "</table:table-row>"
            "<table:table-row>"
            "<table:table-cell><text:p>widgets</text:p></table:table-cell>"
            "<table:table-cell><text:p>3</text:p></table:table-cell>"
            '<table:table-cell table:number-columns-repeated="16384"/>'
            "</table:table-row>"
            "</table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert markdown == "## S\n\n| name | count |\n| --- | --- |\n| widgets | 3 |"

    def test_repeated_populated_cell_is_expanded(self):
        body = _sheet_body(
            '<table:table table:name="S">'
            "<table:table-row>"
            '<table:table-cell table:number-columns-repeated="3"><text:p>same</text:p>'
            "</table:table-cell>"
            "<table:table-cell><text:p>tail</text:p></table:table-cell>"
            "</table:table-row></table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert markdown.split("\n")[2] == "| same | same | same | tail |"

    def test_repeated_row_is_expanded(self):
        body = _sheet_body(
            '<table:table table:name="S">'
            "<table:table-row><table:table-cell><text:p>h</text:p></table:table-cell>"
            "</table:table-row>"
            '<table:table-row table:number-rows-repeated="3">'
            "<table:table-cell><text:p>r</text:p></table:table-cell></table:table-row>"
            "</table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert markdown.count("| r |") == 3

    def test_repeated_empty_rows_are_dropped(self):
        body = _sheet_body(
            '<table:table table:name="S">'
            "<table:table-row><table:table-cell><text:p>h</text:p></table:table-cell>"
            "</table:table-row>"
            '<table:table-row table:number-rows-repeated="1048576">'
            '<table:table-cell table:number-columns-repeated="16384"/></table:table-row>'
            "</table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert markdown == "## S\n\n| h |\n| --- |"

    def test_row_group_rows_are_included(self):
        body = _sheet_body(
            '<table:table table:name="S"><table:table-header-rows>'
            "<table:table-row><table:table-cell><text:p>header</text:p></table:table-cell>"
            "</table:table-row></table:table-header-rows>"
            "<table:table-row-group>"
            "<table:table-row><table:table-cell><text:p>body</text:p></table:table-cell>"
            "</table:table-row></table:table-row-group>"
            "</table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert "| header |" in markdown
        assert "| body |" in markdown

    def test_empty_sheet_is_skipped(self):
        body = _sheet_body(
            '<table:table table:name="Empty">'
            "<table:table-row>"
            '<table:table-cell table:number-columns-repeated="10"/></table:table-row>'
            "</table:table>"
            '<table:table table:name="Real">'
            "<table:table-row><table:table-cell><text:p>v</text:p></table:table-cell>"
            "</table:table-row></table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert "Empty" not in markdown
        assert "## Real" in markdown

    def test_typed_value_is_used_when_there_is_no_display_text(self):
        body = _sheet_body(
            '<table:table table:name="S"><table:table-row>'
            '<table:table-cell office:value-type="float" office:value="1.5"/>'
            '<table:table-cell office:value-type="date" office:date-value="2024-01-02"/>'
            '<table:table-cell office:value-type="boolean" office:boolean-value="true"/>'
            "</table:table-row></table:table>"
        )
        markdown = _convert(_package(body), ".ods").markdown
        assert markdown.split("\n")[2] == "| 1.5 | 2024-01-02 | TRUE |"


class TestPresentation:
    def test_slides_and_frames(self):
        body = _slide_body(
            '<draw:page draw:name="Intro">'
            "<draw:frame><draw:text-box><text:p>Welcome</text:p></draw:text-box></draw:frame>"
            "</draw:page>"
            '<draw:page draw:name="Details">'
            "<draw:frame><draw:text-box>"
            '<text:h text:outline-level="1">Step one</text:h><text:p>do the thing</text:p>'
            "</draw:text-box></draw:frame>"
            "</draw:page>"
        )
        markdown = _convert(_package(body), ".odp").markdown
        assert "## Intro" in markdown
        assert "Welcome" in markdown
        assert "## Details" in markdown
        # A content heading starts below the slide title, not at the same level.
        assert "### Step one" in markdown
        assert "do the thing" in markdown

    def test_unnamed_slide_gets_a_number(self):
        body = _slide_body(
            "<draw:page>"
            "<draw:frame><draw:text-box><text:p>only</text:p></draw:text-box></draw:frame>"
            "</draw:page>"
        )
        assert "## Slide 1" in _convert(_package(body), ".odp").markdown

    def test_speaker_notes_become_a_blockquote(self):
        body = _slide_body(
            '<draw:page draw:name="S">'
            "<draw:frame><draw:text-box><text:p>slide text</text:p></draw:text-box></draw:frame>"
            "<presentation:notes><draw:frame><draw:text-box>"
            "<text:p>remember this</text:p></draw:text-box></draw:frame></presentation:notes>"
            "</draw:page>"
        )
        markdown = _convert(_package(body), ".odp").markdown
        assert "> remember this" in markdown
        # The note must not also appear as slide content.
        assert markdown.count("remember this") == 1


class TestMetadataAndErrors:
    def test_title_comes_from_meta_xml(self):
        result = _convert(_package(_text_body("<text:p>x</text:p>"), title="Quarterly"))
        assert result.title == "Quarterly"

    def test_missing_meta_is_not_an_error(self):
        result = _convert(_package(_text_body("<text:p>x</text:p>"), meta=False))
        assert result.title is None
        assert result.markdown == "x"

    def test_flat_document_has_no_package(self):
        result = _convert(_flat(_text_body("<text:p>flat body</text:p>")), ".fodt")
        assert result.markdown == "flat body"
        assert result.title == "Flat"

    def test_flat_spreadsheet(self):
        body = _sheet_body(
            '<table:table table:name="S"><table:table-row>'
            "<table:table-cell><text:p>f</text:p></table:table-cell>"
            "</table:table-row></table:table>"
        )
        markdown = _convert(_flat(body), ".fods").markdown
        assert "## S" in markdown and "| f |" in markdown

    def test_body_kind_is_detected_not_assumed(self):
        """A spreadsheet mislabelled as .odt still converts as a spreadsheet."""
        body = _sheet_body(
            '<table:table table:name="S"><table:table-row>'
            "<table:table-cell><text:p>v</text:p></table:table-cell>"
            "</table:table-row></table:table>"
        )
        markdown = _convert(_package(body), ".odt").markdown
        assert "## S" in markdown

    def test_zip_without_content_xml_is_refused(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("something.txt", "hi")
        buffer.seek(0)
        with pytest.raises(ValueError, match="content.xml"):
            _convert(buffer)

    def test_not_a_zip_is_refused(self):
        with pytest.raises(ValueError, match="not a valid OpenDocument package"):
            _convert(io.BytesIO(b"this is not a zip file at all"))

    def test_malformed_xml_is_refused(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("content.xml", "<office:document-content><unclosed>")
        buffer.seek(0)
        with pytest.raises(ValueError, match="well-formed"):
            _convert(buffer)

    def test_unknown_body_is_refused(self):
        body = f"<office:body><office:chart/></office:body>"
        with pytest.raises(ValueError, match="unsupported OpenDocument body"):
            _convert(_package(body))

    def test_oversized_content_xml_is_refused(self, monkeypatch):
        import markitdown.converters._odf_converter as module

        monkeypatch.setattr(module, "MAX_CONTENT_XML_BYTES", 32)
        body = _text_body("<text:p>" + "x" * 200 + "</text:p>")
        with pytest.raises(ValueError, match="refusing to parse"):
            _convert(_package(body))
