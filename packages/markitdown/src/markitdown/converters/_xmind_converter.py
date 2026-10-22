"""Convert modern and classic XMind workbooks into Markdown outlines."""

import json
import zipfile
from typing import Any, BinaryIO, Iterator
from xml.etree.ElementTree import Element

from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo


ACCEPTED_FILE_EXTENSIONS = [".xmind"]
ACCEPTED_MIME_TYPES = {
    "application/vnd.xmind.workbook",
    "application/xmind",
    "application/x-xmind",
}
MAX_CONTENT_SIZE = 20 * 1024 * 1024


class XMindConverter(DocumentConverter):
    """Render the topic hierarchy in an XMind archive as a Markdown outline.

    XMind 2020+ workbooks store their sheets in ``content.json``.  XMind 8
    uses ``content.xml`` instead.  A few workbooks contain both, so JSON is
    deliberately preferred as the current format.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        return (stream_info.extension or "").lower() in ACCEPTED_FILE_EXTENSIONS or (
            (stream_info.mimetype or "").lower() in ACCEPTED_MIME_TYPES
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        try:
            with zipfile.ZipFile(file_stream) as archive:
                name = (
                    "content.json"
                    if "content.json" in archive.NameToInfo
                    else "content.xml"
                    if "content.xml" in archive.NameToInfo
                    else None
                )
                if name is None:
                    raise ValueError(
                        "XMind archive is missing content.json or content.xml"
                    )

                info = archive.getinfo(name)
                if info.flag_bits & 1:
                    raise ValueError(f"XMind archive entry {name} is encrypted")
                if info.is_dir() or info.file_size == 0:
                    raise ValueError(f"XMind archive entry {name} is empty")
                if info.file_size > MAX_CONTENT_SIZE:
                    raise ValueError(
                        f"XMind archive entry {name} exceeds the {MAX_CONTENT_SIZE // 1024 // 1024} MiB limit"
                    )
                with archive.open(info) as entry:
                    content = entry.read(MAX_CONTENT_SIZE + 1)
                if len(content) > MAX_CONTENT_SIZE:
                    raise ValueError(
                        f"XMind archive entry {name} exceeds the {MAX_CONTENT_SIZE // 1024 // 1024} MiB limit"
                    )
        except zipfile.BadZipFile as exc:
            raise ValueError("Invalid XMind archive") from exc

        sheets = (
            self._parse_json(content)
            if name == "content.json"
            else self._parse_xml(content)
        )
        if not sheets:
            raise ValueError("XMind archive contains no sheets")

        markdown = self._render_sheets(sheets)
        if not markdown:
            raise ValueError("XMind archive contains no topics")
        title = sheets[0][0] if len(sheets) == 1 else None
        return DocumentConverterResult(markdown=markdown, title=title)

    @staticmethod
    def _parse_json(content: bytes) -> list[tuple[str, dict[str, Any]]]:
        try:
            data = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid XMind content.json") from exc
        if not isinstance(data, list):
            raise ValueError("XMind content.json must contain a sheet list")

        sheets = []
        for sheet in data:
            if not isinstance(sheet, dict):
                continue
            root = sheet.get("rootTopic")
            if isinstance(root, dict):
                sheets.append((XMindConverter._text(sheet.get("title")), root))
        return sheets

    @staticmethod
    def _parse_xml(content: bytes) -> list[tuple[str, dict[str, Any]]]:
        try:
            root = ElementTree.fromstring(content)
        except (DefusedXmlException, ElementTree.ParseError) as exc:
            raise ValueError("Invalid XMind content.xml") from exc

        sheets = []
        for sheet in XMindConverter._children(root, "sheet"):
            topic = next(XMindConverter._children(sheet, "topic"), None)
            if topic is not None:
                sheet_title = next(XMindConverter._children(sheet, "title"), None)
                sheets.append(
                    (
                        XMindConverter._element_text(sheet_title),
                        XMindConverter._xml_topic(topic),
                    )
                )
        return sheets

    @staticmethod
    def _xml_topic(topic: Element) -> dict[str, Any]:
        title = next(XMindConverter._children(topic, "title"), None)
        plain = None
        for notes in XMindConverter._children(topic, "notes"):
            plain = next(XMindConverter._children(notes, "plain"), None)
            if plain is not None:
                break
        children = [
            XMindConverter._xml_topic(child)
            for children in XMindConverter._children(topic, "children")
            for topics in XMindConverter._children(children, "topics")
            for child in XMindConverter._children(topics, "topic")
        ]
        return {
            "title": XMindConverter._element_text(title),
            "note": XMindConverter._element_text(plain),
            "children": children,
        }

    @staticmethod
    def _children(element: Element, local_name: str) -> Iterator[Element]:
        return (
            child for child in element if child.tag.rsplit("}", 1)[-1] == local_name
        )

    @staticmethod
    def _text(value: Any) -> str:
        return value.strip() if isinstance(value, str) else ""

    @staticmethod
    def _element_text(element: Element | None) -> str:
        """Return all textual content, including text in nested XML elements."""
        return "" if element is None else "".join(element.itertext()).strip()

    @classmethod
    def _render_sheets(cls, sheets: list[tuple[str, dict[str, Any]]]) -> str:
        parts = []
        for index, (title, root) in enumerate(sheets, start=1):
            heading = title or f"Sheet {index}"
            lines = [f"# {heading}", ""]
            lines.extend(cls._render_topic(root, depth=0))
            parts.append("\n".join(lines).rstrip())
        return "\n\n".join(parts)

    @classmethod
    def _render_topic(cls, topic: dict[str, Any], depth: int) -> list[str]:
        title = cls._text(topic.get("title"))
        indent = "  " * depth
        lines = [f"{indent}- {title}"] if title else []
        notes = topic.get("notes")
        plain = notes.get("plain") if isinstance(notes, dict) else None
        note = plain.get("content") if isinstance(plain, dict) else None
        if not isinstance(note, str):
            note = topic.get("note")
        note = cls._text(note)
        if note and title:
            lines.extend(
                f"{indent}  > {line}" if line else f"{indent}  >"
                for line in note.splitlines()
            )

        children = topic.get("children", {})
        if isinstance(children, dict):
            children = children.get("attached", [])
        if not isinstance(children, list):
            children = []
        for child in children:
            if isinstance(child, dict):
                lines.extend(cls._render_topic(child, depth + 1 if title else depth))
        return lines
