from __future__ import annotations

import zipfile
from dataclasses import dataclass
from typing import Any, BinaryIO

from defusedxml import ElementTree as ET

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_FILE_EXTENSIONS = [".udf"]
ZIP_MIME_TYPE_PREFIXES = [
    "application/zip",
    "application/x-zip-compressed",
    "application/octet-stream",
]
IMAGE_PLACEHOLDER = "[embedded image omitted]"


@dataclass(frozen=True)
class _TextStyle:
    bold: bool = False
    italic: bool = False
    underline: bool = False


@dataclass(frozen=True)
class _TextRun:
    text: str
    style: _TextStyle


@dataclass(frozen=True)
class _ImageRun:
    pass


@dataclass(frozen=True)
class _ListInfo:
    ordered: bool
    level: int
    list_id: str | None


@dataclass(frozen=True)
class _Paragraph:
    runs: list[_TextRun | _ImageRun]
    list_info: _ListInfo | None


@dataclass(frozen=True)
class _TableCell:
    blocks: list[_Block]


@dataclass(frozen=True)
class _TableRow:
    cells: list[_TableCell]


@dataclass(frozen=True)
class _Table:
    rows: list[_TableRow]


_Block = _Paragraph | _Table
_InlineRun = _TextRun | _ImageRun


class UdfConverter(DocumentConverter):
    """Convert UYAP UDF documents into Markdown."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        extension = (stream_info.extension or "").lower()
        mimetype = (stream_info.mimetype or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        if extension not in ("", ".zip"):
            return False

        if mimetype and not any(
            mimetype.startswith(prefix) for prefix in ZIP_MIME_TYPE_PREFIXES
        ):
            return False

        return self._looks_like_udf(file_stream)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        content_xml = self._read_content_xml(file_stream)
        root = ET.fromstring(content_xml)
        if self._local_name(root.tag) != "template":
            raise ValueError("Invalid UDF file: missing <template> root element")

        content_element = self._find_child(root, "content")
        if content_element is None:
            raise ValueError("Invalid UDF file: missing <content> element")

        elements_element = self._find_child(root, "elements")
        if elements_element is None:
            return DocumentConverterResult(markdown="")

        runes = list(content_element.text or "")
        blocks = self._parse_blocks(elements_element, runes)
        markdown = self._render_blocks(blocks)
        return DocumentConverterResult(markdown=markdown.strip())

    def _looks_like_udf(self, file_stream: BinaryIO) -> bool:
        cur_pos = file_stream.tell()
        try:
            with zipfile.ZipFile(file_stream, "r") as archive:
                if "content.xml" not in archive.namelist():
                    return False
                content_xml = archive.read("content.xml")
                root = ET.fromstring(content_xml)
                return self._local_name(root.tag) == "template"
        except Exception:
            return False
        finally:
            file_stream.seek(cur_pos)

    def _read_content_xml(self, file_stream: BinaryIO) -> bytes:
        try:
            with zipfile.ZipFile(file_stream, "r") as archive:
                return archive.read("content.xml")
        except zipfile.BadZipFile as exc:
            raise ValueError("Invalid UDF file: expected a ZIP archive") from exc
        except KeyError as exc:
            raise ValueError("Invalid UDF file: missing content.xml") from exc

    def _parse_blocks(self, parent: ET.Element, runes: list[str]) -> list[_Block]:
        blocks: list[_Block] = []
        for child in self._child_elements(parent):
            tag = self._local_name(child.tag)
            if tag == "paragraph":
                blocks.append(self._parse_paragraph(child, runes))
            elif tag == "table":
                blocks.append(self._parse_table(child, runes))
        return blocks

    def _parse_paragraph(self, element: ET.Element, runes: list[str]) -> _Paragraph:
        runs: list[_InlineRun] = []
        for child in self._child_elements(element):
            tag = self._local_name(child.tag)
            if tag == "content":
                text = self._extract_text(child, runes)
                if text:
                    runs.append(
                        _TextRun(
                            text=text,
                            style=_TextStyle(
                                bold=self._attr_bool(child, "bold"),
                                italic=self._attr_bool(child, "italic"),
                                underline=self._attr_bool(child, "underline"),
                            ),
                        )
                    )
            elif tag == "tab":
                runs.append(_TextRun(text="    ", style=_TextStyle()))
            elif tag == "image":
                runs.append(_ImageRun())

        merged_runs: list[_InlineRun] = []
        for run in runs:
            if isinstance(run, _TextRun):
                if not run.text:
                    continue
                if (
                    merged_runs
                    and isinstance(merged_runs[-1], _TextRun)
                    and merged_runs[-1].style == run.style
                ):
                    previous = merged_runs[-1]
                    merged_runs[-1] = _TextRun(
                        text=previous.text + run.text,
                        style=run.style,
                    )
                else:
                    merged_runs.append(run)
            else:
                merged_runs.append(run)

        list_info = self._parse_list_info(element)
        return _Paragraph(runs=merged_runs, list_info=list_info)

    def _parse_list_info(self, element: ET.Element) -> _ListInfo | None:
        is_numbered = self._attr_bool(element, "Numbered")
        is_bulleted = self._attr_bool(element, "Bulleted")
        if not is_numbered and not is_bulleted:
            return None

        return _ListInfo(
            ordered=is_numbered,
            level=max(self._attr_int(element, "ListLevel"), 0),
            list_id=element.attrib.get("ListId"),
        )

    def _parse_table(self, element: ET.Element, runes: list[str]) -> _Table:
        rows: list[_TableRow] = []
        for row_element in self._child_elements(element):
            if self._local_name(row_element.tag) != "row":
                continue

            cells: list[_TableCell] = []
            for cell_element in self._child_elements(row_element):
                if self._local_name(cell_element.tag) != "cell":
                    continue
                cells.append(
                    _TableCell(blocks=self._parse_blocks(cell_element, runes))
                )

            rows.append(_TableRow(cells=cells))

        return _Table(rows=rows)

    def _extract_text(self, element: ET.Element, runes: list[str]) -> str:
        start_offset = self._attr_int(
            element, "startOffset", fallback=self._attr_int(element, "offset")
        )
        length = max(self._attr_int(element, "length"), 0)

        if start_offset < 0:
            start_offset = 0
        end_offset = min(start_offset + length, len(runes))
        if start_offset >= len(runes) or start_offset >= end_offset:
            return ""

        text = "".join(runes[start_offset:end_offset])
        return (
            text.replace("\u200b", "")
            .replace("\t", "    ")
            .replace("\r", "")
            .replace("\n", " ")
            .replace("\xa0", " ")
        )

    def _render_blocks(self, blocks: list[_Block]) -> str:
        sections: list[str] = []
        index = 0
        while index < len(blocks):
            block = blocks[index]
            if isinstance(block, _Paragraph) and block.list_info is not None:
                list_group: list[_Paragraph] = []
                while (
                    index < len(blocks)
                    and isinstance(blocks[index], _Paragraph)
                    and blocks[index].list_info is not None
                ):
                    list_group.append(blocks[index])
                    index += 1
                sections.append(self._render_list_group(list_group))
                continue

            if isinstance(block, _Paragraph):
                sections.append(self._render_paragraph(block))
            else:
                sections.append(self._render_table(block))
            index += 1

        return "\n\n".join(sections)

    def _render_paragraph(self, paragraph: _Paragraph) -> str:
        return self._render_runs(paragraph.runs)

    def _render_list_group(self, paragraphs: list[_Paragraph]) -> str:
        counters: dict[int, int] = {}
        level_keys: dict[int, tuple[bool, str | None]] = {}
        lines: list[str] = []

        for paragraph in paragraphs:
            assert paragraph.list_info is not None
            list_info = paragraph.list_info
            level = max(list_info.level, 0)

            for depth in list(counters):
                if depth > level:
                    del counters[depth]
            for depth in list(level_keys):
                if depth > level:
                    del level_keys[depth]

            key = (list_info.ordered, list_info.list_id)
            if list_info.ordered:
                current = counters.get(level)
                if level_keys.get(level) != key or current is None:
                    counters[level] = 1
                else:
                    counters[level] = current + 1
                marker = f"{counters[level]}."
            else:
                counters.pop(level, None)
                marker = "-"

            level_keys[level] = key
            content = self._render_runs(paragraph.runs).strip()
            line = f"{'  ' * level}{marker} {content}".rstrip()
            lines.append(line if line.strip() else f"{'  ' * level}{marker}")

        return "\n".join(lines)

    def _render_table(self, table: _Table) -> str:
        rows = [self._render_table_row(row) for row in table.rows if row.cells]
        if not rows:
            return ""

        column_count = max(len(row) for row in rows)
        normalized_rows = [
            row + [""] * (column_count - len(row))
            for row in rows
        ]

        separator = ["---"] * column_count
        lines = [
            self._format_table_row(normalized_rows[0]),
            self._format_table_row(separator),
        ]
        for row in normalized_rows[1:]:
            lines.append(self._format_table_row(row))
        return "\n".join(lines)

    def _render_table_row(self, row: _TableRow) -> list[str]:
        return [self._render_table_cell(cell) for cell in row.cells]

    def _render_table_cell(self, cell: _TableCell) -> str:
        text = self._flatten_blocks(cell.blocks, in_table=True).strip()
        return text or " "

    def _flatten_blocks(self, blocks: list[_Block], *, in_table: bool) -> str:
        pieces: list[str] = []
        for block in blocks:
            if isinstance(block, _Paragraph):
                text = self._render_runs(block.runs, in_table=in_table).strip()
            else:
                text = self._flatten_table(block, in_table=in_table)
            if text:
                pieces.append(text)
        return " ".join(pieces)

    def _flatten_table(self, table: _Table, *, in_table: bool) -> str:
        row_texts: list[str] = []
        for row in table.rows:
            cell_texts = [
                self._render_table_cell(cell).strip() for cell in row.cells if row.cells
            ]
            if cell_texts:
                row_texts.append(" / ".join(cell_texts))
        return "; ".join(row_texts)

    def _render_runs(self, runs: list[_InlineRun], *, in_table: bool = False) -> str:
        rendered: list[str] = []
        for index, run in enumerate(runs):
            if isinstance(run, _ImageRun):
                chunk = IMAGE_PLACEHOLDER
                if rendered and not rendered[-1].endswith((" ", "\t", "\n")):
                    chunk = " " + chunk

                next_run = runs[index + 1] if index + 1 < len(runs) else None
                if next_run is not None:
                    if isinstance(next_run, _ImageRun):
                        chunk = chunk + " "
                    elif next_run.text and not next_run.text[0].isspace():
                        chunk = chunk + " "

                rendered.append(chunk)
            else:
                rendered.append(self._render_text_run(run, in_table=in_table))
        return "".join(rendered)

    def _render_text_run(self, run: _TextRun, *, in_table: bool) -> str:
        text = self._escape_text(run.text, in_table=in_table)
        if not text:
            return ""
        return self._apply_style(text, run.style)

    def _escape_text(self, text: str, *, in_table: bool) -> str:
        escaped = text.replace("\\", "\\\\")
        if in_table:
            escaped = escaped.replace("|", "\\|")
        return escaped

    def _apply_style(self, text: str, style: _TextStyle) -> str:
        leading_length = len(text) - len(text.lstrip())
        trailing_length = len(text) - len(text.rstrip())
        leading = text[:leading_length]
        trailing = text[len(text) - trailing_length :] if trailing_length else ""
        core_end = len(text) - trailing_length if trailing_length else len(text)
        core = text[leading_length:core_end]

        if not core:
            return text

        if style.bold and style.italic:
            core = f"***{core}***"
        elif style.bold:
            core = f"**{core}**"
        elif style.italic:
            core = f"*{core}*"

        if style.underline:
            core = f"<u>{core}</u>"

        return f"{leading}{core}{trailing}"

    def _format_table_row(self, cells: list[str]) -> str:
        return "| " + " | ".join(cells) + " |"

    def _child_elements(self, parent: ET.Element) -> list[ET.Element]:
        return [child for child in list(parent) if isinstance(child.tag, str)]

    def _find_child(self, parent: ET.Element, name: str) -> ET.Element | None:
        for child in self._child_elements(parent):
            if self._local_name(child.tag) == name:
                return child
        return None

    def _local_name(self, tag: str) -> str:
        if "}" in tag:
            return tag.rsplit("}", 1)[-1]
        return tag

    def _attr_bool(self, element: ET.Element, name: str) -> bool:
        value = element.attrib.get(name, "")
        return value.lower() in {"1", "true", "yes"}

    def _attr_int(
        self, element: ET.Element, name: str, fallback: int = 0
    ) -> int:
        value = element.attrib.get(name)
        if value in (None, ""):
            return fallback
        try:
            return int(value)
        except ValueError:
            try:
                return int(float(value))
            except ValueError:
                return fallback
