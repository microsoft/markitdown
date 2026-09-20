"""Converts OpenDocument files (ODT / ODS / ODP) to Markdown.

Why this belongs in the repository rather than in a plugin
---------------------------------------------------------
New formats are added sparingly, and the stated reason is dependencies: a
converter that pulls in a parser makes the base install heavier for everyone.
This one adds **no dependency at all**. OpenDocument is a ZIP of XML parts, so it
is read with :mod:`zipfile` from the standard library and :mod:`defusedxml`,
which ``markitdown`` already requires. ``defusedxml`` is the right parser here
rather than a convenience: ``content.xml`` arrives from an untrusted file, and
the hardened parser blocks entity expansion and external entity resolution that
plain :mod:`xml.dom.minidom` allows.

OpenDocument is what LibreOffice, OpenOffice and most public-sector suites write
by default, and it is the one common office format MarkItDown could not read.
The flat variants (``.fodt``, ``.fods``, ``.fodp``) are the same XML with the ZIP
removed and are handled by the same code.

Three properties of the format drive most of the code below, and all three are
things a straightforward implementation gets wrong:

1. **Repetition is a compression scheme, not data.** Every row of a spreadsheet
   ends with something like
   ``<table:table-cell table:number-columns-repeated="16384"/>`` for the empty
   tail of the sheet, and a *populated* cell can be repeated too. Expanding
   repeats blindly turns a three-column file into a 16384-column Markdown table,
   so the width of a table is the last column that holds a *value* and repeats are
   capped (:data:`MAX_REPEATED_CELLS`, :data:`MAX_COLUMNS`) so a hostile file
   cannot exhaust memory.
2. **Whitespace is markup.** ``<text:s text:c="3"/>`` is three spaces and
   ``<text:tab/>`` is a tab; runs of literal whitespace between elements are not
   significant. Reading ``nodeValue`` alone silently drops both.
3. **A cell is a container, not a string.** A cell holds ``text:p`` paragraphs and
   a table holds cells; flattening either one to text produces a table whose rows
   do not line up with its header.

Where the format has a choice, this converter follows :class:`XlsxConverter` so
that ``.ods`` and ``.xlsx`` of the same data produce the same Markdown: each sheet
becomes a ``##`` heading followed by one table, and the first row is treated as
the header, which is what ``pandas.DataFrame.to_html(index=False)`` does.

Limitations, stated rather than implied:

- Embedded images are not extracted. Their ``xlink:href`` values are
  package-internal paths (``Pictures/1000000000000001.png``) that mean nothing
  outside the file, and a Markdown link to one would be a broken link.
- Footnotes and endnotes are dropped rather than emitted as ``[^n]`` references
  with no definition. Losing a footnote is better than producing a document that
  does not render.
- Change tracking is not resolved: revisions are rendered as they appear in
  ``content.xml``.
- Ordered lists render as bullets. Whether a list is numbered is a *style*
  property stored in ``styles.xml``, not an attribute of the list itself, so
  resolving it would mean resolving the whole style cascade.
"""

import io
import re
import zipfile
from typing import Any, BinaryIO, Iterator, List, Optional, Sequence, Tuple
from xml.dom import Node

from defusedxml import minidom

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

# ---------------------------------------------------------------------------
# Namespaces.  Matching on namespace URI rather than on the literal prefix is
# what makes this work on files written by something other than LibreOffice:
# the prefix is arbitrary, the URI is not.
# ---------------------------------------------------------------------------

OFFICE_NS = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
TABLE_NS = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
DRAW_NS = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
PRESENTATION_NS = "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
DC_NS = "http://purl.org/dc/elements/1.1/"
XLINK_NS = "http://www.w3.org/1999/xlink"

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.oasis.opendocument",
]

ACCEPTED_FILE_EXTENSIONS = [".odt", ".ods", ".odp", ".fodt", ".fods", ".fodp"]

#: Flat OpenDocument: the same document as a single uncompressed XML file.
FLAT_EXTENSIONS = frozenset({".fodt", ".fods", ".fodp"})

#: Cap on one ``number-columns-repeated`` / ``number-rows-repeated`` value. A
#: populated cell legitimately repeats a handful of times; a value in the
#: thousands is a compression artefact of the empty tail, and honouring it is how
#: a converter turns a 4 KiB file into a 200 MiB string.
MAX_REPEATED_CELLS = 256
MAX_REPEATED_ROWS = 64

#: Cap on the width of a generated table, applied after repeats are resolved.
MAX_COLUMNS = 1024

#: Cap on the uncompressed size of ``content.xml``. ``defusedxml`` blocks entity
#: expansion but not a plain 10 GiB member, and the ZIP central directory is
#: attacker-controlled.
MAX_CONTENT_XML_BYTES = 64 * 1024 * 1024

#: A pipe together with any run of backslashes in front of it, so the run can be
#: doubled before the pipe is escaped. Same rule as the CSV converter, because a
#: cell is a cell whichever format it came from.
_PIPE_ESCAPE_RE = re.compile(r"(?<!\\)(\\*)\|")

_WHITESPACE_RE = re.compile(r"\s+")
_REPEATED_SPACE_RE = re.compile(r" {2,}")

_TOC_ELEMENTS = frozenset(
    {
        "table-of-content",
        "table-of-content-source",
        "index-body",
        "sequence-decls",
        "tracked-changes",
        "variable-decls",
    }
)


# ---------------------------------------------------------------------------
# DOM helpers
# ---------------------------------------------------------------------------


def _elements(node: Node) -> Iterator[Node]:
    """Element children of ``node``, in document order."""
    for child in node.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            yield child


def _children(node: Node, namespace: str, local_name: str) -> List[Node]:
    return [
        child
        for child in _elements(node)
        if child.namespaceURI == namespace and child.localName == local_name
    ]


def _first(node: Node, namespace: str, local_name: str) -> Optional[Node]:
    for child in _elements(node):
        if child.namespaceURI == namespace and child.localName == local_name:
            return child
    return None


def _attr(node: Node, namespace: str, local_name: str, default: str = "") -> str:
    value = node.getAttributeNS(namespace, local_name)
    return value if value else default


def _positive_int(value: str, default: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return number if number > 0 else default


def _outline_level(node: Node, default: int = 1) -> int:
    level = _positive_int(_attr(node, TEXT_NS, "outline-level", ""), default)
    return max(1, min(6, level))


# ---------------------------------------------------------------------------
# Inline rendering
# ---------------------------------------------------------------------------


def _render_inline(node: Node) -> str:
    """Render the inline content of a paragraph-like node to Markdown text.

    Whitespace inside a text node is insignificant, so it collapses to a single
    space; ``text:s`` and ``text:tab`` are *not* whitespace, they are elements
    that happen to mean whitespace, so they survive the collapse and are only
    de-duplicated afterwards. That ordering is the whole trick: collapsing the
    assembled string instead would turn ``a<text:s/>b`` and ``ab`` into the same
    output.
    """
    parts: List[str] = []

    for child in node.childNodes:
        if child.nodeType == Node.TEXT_NODE:
            parts.append(_WHITESPACE_RE.sub(" ", child.nodeValue or ""))
            continue
        if child.nodeType != Node.ELEMENT_NODE:
            continue

        namespace, name = child.namespaceURI, child.localName

        if namespace == TEXT_NS:
            if name == "s":
                parts.append(" " * _positive_int(_attr(child, TEXT_NS, "c", "1"), 1))
                continue
            if name == "tab":
                parts.append("\t")
                continue
            if name == "line-break":
                parts.append("<br>")
                continue
            if name == "a":
                inner = _render_inline(child)
                href = _attr(child, XLINK_NS, "href")
                parts.append(f"[{inner}]({href})" if inner and href else inner)
                continue
            if name in (
                "span",
                "bookmark-ref",
                "reference-ref",
                "note-ref",
                "meta-field",
            ):
                parts.append(_render_inline(child))
                continue
            if name in (
                "note",
                "annotation",
                "bookmark",
                "soft-page-break",
                "index-mark",
            ):
                # A footnote reference without its body would render as a broken
                # link; see the module docstring for why they are dropped.
                continue
            parts.append(_render_inline(child))
            continue

        if namespace == OFFICE_NS and name == "annotation":
            continue
        # draw:frame and draw:text-box appear inline in text documents, and their
        # text:p children are the anchor's content.
        parts.append(_render_inline(child))

    return _REPEATED_SPACE_RE.sub(" ", "".join(parts)).strip()


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------


def _escape_cell(value: str) -> str:
    r"""Escape a value so it survives inside a Markdown table cell.

    A pipe is a column separator, so it is escaped; a paragraph break inside a
    cell becomes ``<br>`` rather than a newline, because a newline would end the
    row and shift every following cell by one column.
    """
    value = _PIPE_ESCAPE_RE.sub(lambda match: match.group(1) * 2 + r"\|", value)
    return value.replace("\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")


def _cell_text(cell: Node) -> str:
    """The visible text of one cell.

    A cell is a container: its paragraphs are joined with ``<br>`` so a
    multi-paragraph cell keeps both its lines and its row. When there is no
    display text at all, the stored ``office:value`` is used, which is the only
    content a formula cell carries when the producer omitted the cached text.
    """
    paragraphs = [
        child
        for child in _elements(cell)
        if child.namespaceURI == TEXT_NS and child.localName in ("p", "h")
    ]
    text = "<br>".join(part for part in (_render_inline(p) for p in paragraphs) if part)

    if not text:
        value_type = _attr(cell, OFFICE_NS, "value-type")
        if value_type in ("float", "percentage", "currency"):
            text = _attr(cell, OFFICE_NS, "value")
        elif value_type == "date":
            text = _attr(cell, OFFICE_NS, "date-value")
        elif value_type == "time":
            text = _attr(cell, OFFICE_NS, "time-value")
        elif value_type == "boolean":
            raw = _attr(cell, OFFICE_NS, "boolean-value")
            text = "TRUE" if raw == "true" else "FALSE" if raw else ""

    return _escape_cell(text)


def _iter_rows(node: Node) -> Iterator[Node]:
    """Rows of a table, descending through row groups but never into a nested table.

    Rows live under ``table:table-header-rows`` or ``table:table-row-group`` as
    often as directly under ``table:table``, and a cell can contain a whole nested
    table whose rows are not part of this grid.
    """
    for child in _elements(node):
        if child.namespaceURI != TABLE_NS:
            continue
        if child.localName == "table-row":
            yield child
        elif child.localName in ("table-header-rows", "table-row-group", "table-rows"):
            yield from _iter_rows(child)


def _row_cells(row: Node) -> List[Tuple[str, int]]:
    """``(text, repeat)`` for each cell of a row, in column order."""
    cells: List[Tuple[str, int]] = []
    for child in _elements(row):
        if child.namespaceURI != TABLE_NS:
            continue
        if child.localName == "table-cell":
            repeat = _positive_int(
                _attr(child, TABLE_NS, "number-columns-repeated", "1"), 1
            )
            cells.append((_cell_text(child), repeat))
        elif child.localName == "covered-table-cell":
            # A cell swallowed by a span still occupies a column, so it becomes an
            # empty one. Markdown has no merged cells; leaving the column in place
            # keeps every other row aligned.
            repeat = _positive_int(
                _attr(child, TABLE_NS, "number-columns-repeated", "1"), 1
            )
            cells.append(("", repeat))
    return cells


def _table_width(rows: Sequence[Sequence[Tuple[str, int]]]) -> int:
    """The width of the table: the last column that holds a value, plus its repeat.

    Empty cells contribute nothing. They still *occupy* a column when the row is
    laid out, but they never define the grid, and that is the whole point: every
    LibreOffice row ends with an empty cell repeated to the sheet's maximum width,
    so a rule of "the rightmost cell defines the width" turns a two-column file
    into a 16384-column table. The cost is that a genuinely blank trailing column
    is dropped, which is not information a Markdown table can carry anyway.
    """
    width = 0
    for cells in rows:
        column = 0
        for text, repeat in cells:
            repeat = min(repeat, MAX_REPEATED_CELLS)
            if text:
                width = max(width, column + repeat)
            column += repeat
    return min(width, MAX_COLUMNS)


def _expand_row(cells: Sequence[Tuple[str, int]], width: int) -> List[str]:
    row: List[str] = []
    column = 0
    for text, repeat in cells:
        if column >= width:
            break
        take = min(repeat, width - column, MAX_REPEATED_CELLS)
        row.extend([text] * take)
        column += take
    row.extend([""] * (width - len(row)))
    return row[:width]


def _grid_to_markdown(grid: Sequence[Sequence[str]]) -> List[str]:
    """A GitHub-flavoured Markdown table whose first row is the header."""
    header = list(grid[0])
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for row in grid[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def _render_table(node: Node, title: Optional[str]) -> List[str]:
    """A table as Markdown lines, preceded by ``## title`` when one is given."""
    raw_rows = [
        (
            _row_cells(row),
            _positive_int(_attr(row, TABLE_NS, "number-rows-repeated", "1"), 1),
        )
        for row in _iter_rows(node)
    ]
    if not raw_rows:
        return []

    width = _table_width([cells for cells, _ in raw_rows])
    if width == 0:
        return []

    grid: List[List[str]] = []
    for cells, repeat in raw_rows:
        dense = _expand_row(cells, width)
        if not any(dense):
            # A blank row carries no data and Markdown cannot express one, so it
            # is dropped rather than rendered as a row of empty cells. This also
            # absorbs the "row repeated 1048576 times, all empty" tail.
            continue
        grid.extend([dense] * min(repeat, MAX_REPEATED_ROWS))

    if not grid:
        return []

    lines: List[str] = []
    if title:
        lines.extend([f"## {title}", ""])
    lines.extend(_grid_to_markdown(grid))
    return lines


# ---------------------------------------------------------------------------
# Text documents
# ---------------------------------------------------------------------------


def _render_list(node: Node, indent: int) -> List[str]:
    """A list as Markdown lines, nested two spaces per level."""
    pad = "  " * indent
    lines: List[str] = []

    for item in _children(node, TEXT_NS, "list-item"):
        item_lines: List[str] = []
        for child in _elements(item):
            namespace, name = child.namespaceURI, child.localName
            if namespace == TEXT_NS and name in ("p", "h"):
                text = _render_inline(child)
                if text:
                    # A paragraph after the first is a continuation of the same
                    # item, so it is indented under the bullet instead of getting
                    # a bullet of its own.
                    item_lines.append(text if not item_lines else f"{pad}  {text}")
            elif namespace == TEXT_NS and name == "list":
                item_lines.extend(_render_list(child, indent + 1))
            elif namespace == TABLE_NS and name == "table":
                item_lines.extend(_render_table(child, None))
            elif namespace == TEXT_NS and name in ("soft-page-break", "bookmark"):
                continue
            else:
                for block in _render_blocks(child):
                    item_lines.extend(block.split("\n"))

        if not item_lines:
            lines.append(f"{pad}-")
        elif item_lines[0].startswith((" ", "#")):
            # The item opened with something that carries its own layout (a nested
            # list, a heading): prefixing a bullet would produce "- - ...".
            lines.extend(item_lines)
        else:
            lines.append(f"{pad}- {item_lines[0]}")
            lines.extend(item_lines[1:])

    return lines


def _render_blocks(node: Node) -> List[str]:
    """Render a container's block-level children as a list of Markdown blocks."""
    blocks: List[str] = []

    for child in _elements(node):
        namespace, name = child.namespaceURI, child.localName

        if namespace == TEXT_NS:
            if name == "h":
                text = _render_inline(child)
                if text:
                    blocks.append("#" * _outline_level(child) + " " + text)
                continue
            if name == "p":
                text = _render_inline(child)
                if text:
                    blocks.append(text)
                continue
            if name == "list":
                lines = _render_list(child, 0)
                if lines:
                    blocks.append("\n".join(lines))
                continue
            if name in _TOC_ELEMENTS:
                # A table of contents is derived from the headings, which are
                # already in the output; emitting the stale copy as well would
                # duplicate every heading.
                continue
            if name == "section":
                blocks.extend(_render_blocks(child))
                continue
            blocks.extend(_render_blocks(child))
            continue

        if namespace == TABLE_NS and name == "table":
            lines = _render_table(child, None)
            if lines:
                blocks.append("\n".join(lines))
            continue

        if namespace == DRAW_NS and name == "frame":
            text = _render_inline(child)
            if text:
                blocks.append(text)
            continue

        blocks.extend(_render_blocks(child))

    return blocks


def _render_spreadsheet(body: Node) -> List[str]:
    blocks: List[str] = []
    for sheet in _children(body, TABLE_NS, "table"):
        lines = _render_table(sheet, _attr(sheet, TABLE_NS, "name") or "Sheet")
        if lines:
            blocks.append("\n".join(lines))
    return blocks


def _iter_slide_text(node: Node) -> Iterator[Node]:
    """``text:p`` / ``text:h`` under a slide, in order, skipping speaker notes.

    A ``text:p`` is not descended into: its nested frames would otherwise be
    emitted twice.
    """
    for child in _elements(node):
        if child.namespaceURI == PRESENTATION_NS and child.localName == "notes":
            continue
        if child.namespaceURI == TEXT_NS and child.localName in ("p", "h"):
            yield child
        else:
            yield from _iter_slide_text(child)


def _render_presentation(body: Node) -> List[str]:
    blocks: List[str] = []
    for index, page in enumerate(_children(body, DRAW_NS, "page"), start=1):
        name = _attr(page, DRAW_NS, "name")
        blocks.append(f"## {name}" if name else f"## Slide {index}")

        for node in _iter_slide_text(page):
            text = _render_inline(node)
            if not text:
                continue
            if node.localName == "h":
                # A slide's own heading level would compete with the slide title,
                # so content headings start below it.
                level = max(3, _outline_level(node))
                blocks.append("#" * level + " " + text)
            else:
                blocks.append(text)

        notes = _first(page, PRESENTATION_NS, "notes")
        if notes is not None:
            note_text = "\n".join(
                text
                for text in (_render_inline(node) for node in _iter_slide_text(notes))
                if text
            )
            if note_text:
                blocks.append("\n".join("> " + line for line in note_text.split("\n")))

    return blocks


# ---------------------------------------------------------------------------
# Package access
# ---------------------------------------------------------------------------


def _parse_xml(data: Any, origin: str) -> Node:
    """Parse XML from bytes, text or an open stream, with a named error.

    ``minidom.parse`` takes a *file object or a filename*, so bytes have to be
    wrapped: passing them straight through makes expat interpret the payload as a
    path and report a confusing I/O error instead of the XML problem.
    """
    if isinstance(data, bytes):
        source: Any = io.BytesIO(data)
    elif isinstance(data, str):
        source = io.StringIO(data)
    else:
        source = data
    try:
        return minidom.parse(source)
    except Exception as exc:
        raise ValueError(f"{origin} is not well-formed XML: {exc}") from exc


def _root_element(document: Node) -> Node:
    """The root element of a parsed document.

    ``minidom.parse`` returns a ``Document``, whose only child is the root
    element; every lookup below wants the element, not the wrapper.
    """
    return getattr(document, "documentElement", None) or document


def _document_title(root: Node) -> Optional[str]:
    meta = _first(root, OFFICE_NS, "meta")
    if meta is None:
        return None
    title = _first(meta, DC_NS, "title")
    if title is None:
        return None
    text = "".join(
        child.nodeValue or ""
        for child in title.childNodes
        if child.nodeType == Node.TEXT_NODE
    ).strip()
    return text or None


class OdfConverter(DocumentConverter):
    """Converts OpenDocument text, spreadsheet and presentation files to Markdown.

    Handles the packaged (``.odt`` / ``.ods`` / ``.odp``) and flat
    (``.fodt`` / ``.fods`` / ``.fodp``) variants. The body is dispatched on which
    of ``office:text``, ``office:spreadsheet`` or ``office:presentation`` the
    document actually has, not on the file extension, so a mislabelled file still
    converts.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        extension = (stream_info.extension or "").lower()

        if extension in FLAT_EXTENSIONS:
            # Flat ODF is the same document as one uncompressed XML file, so there
            # is no package to open and the root element is office:document rather
            # than office:document-content.
            document = _root_element(
                _parse_xml(file_stream, "the flat OpenDocument file")
            )
        else:
            document = self._read_packaged(file_stream)

        body = _first(document, OFFICE_NS, "body")
        if body is None:
            raise ValueError(
                "not an OpenDocument file: no office:body element was found"
            )

        blocks: List[str] = []
        if _first(body, OFFICE_NS, "text") is not None:
            blocks = _render_blocks(_first(body, OFFICE_NS, "text"))
        elif _first(body, OFFICE_NS, "spreadsheet") is not None:
            blocks = _render_spreadsheet(_first(body, OFFICE_NS, "spreadsheet"))
        elif _first(body, OFFICE_NS, "presentation") is not None:
            blocks = _render_presentation(_first(body, OFFICE_NS, "presentation"))
        else:
            raise ValueError(
                "unsupported OpenDocument body: expected office:text, "
                "office:spreadsheet or office:presentation"
            )

        markdown = "\n\n".join(block for block in blocks if block.strip()).strip()
        return DocumentConverterResult(
            markdown=markdown, title=_document_title(document)
        )

    def _read_packaged(self, file_stream: BinaryIO) -> Node:
        """Parse ``content.xml`` out of an OpenDocument ZIP, with the title if present."""
        try:
            with zipfile.ZipFile(file_stream, "r") as archive:
                names = set(archive.namelist())
                if "content.xml" not in names:
                    raise ValueError(
                        "not an OpenDocument file: the package has no content.xml"
                    )

                info = archive.getinfo("content.xml")
                if info.file_size > MAX_CONTENT_XML_BYTES:
                    raise ValueError(
                        f"refusing to parse a {info.file_size} byte content.xml "
                        f"(limit {MAX_CONTENT_XML_BYTES})"
                    )

                document = _root_element(
                    _parse_xml(archive.read("content.xml"), "content.xml")
                )

                # meta.xml carries dc:title. It is a separate part, so the title is
                # grafted onto the body document to keep _document_title() simple.
                if "meta.xml" in names:
                    try:
                        meta_document = _parse_xml(archive.read("meta.xml"), "meta.xml")
                    except ValueError:
                        meta_document = None
                    if meta_document is not None:
                        meta = _first(_root_element(meta_document), OFFICE_NS, "meta")
                        if meta is not None:
                            document.appendChild(meta)
        except zipfile.BadZipFile as exc:
            raise ValueError(f"not a valid OpenDocument package: {exc}") from exc

        return document
