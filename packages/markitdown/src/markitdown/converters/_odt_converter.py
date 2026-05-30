import zipfile
import xml.etree.ElementTree as ET
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ODT_NS = {
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
}

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.oasis.opendocument.text",
]

ACCEPTED_FILE_EXTENSIONS = [".odt"]


class OdtConverter(DocumentConverter):
    """Converts ODT (Open Document Text) files to Markdown."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        try:
            with zipfile.ZipFile(file_stream) as z:
                if "content.xml" not in z.namelist():
                    raise ValueError("Invalid ODT file: missing content.xml")
                content_xml = z.read("content.xml")
        except (zipfile.BadZipFile, ValueError) as e:
            raise ValueError(f"Invalid ODT file: {e}") from e

        root = ET.fromstring(content_xml)

        body = root.find(".//office:body", ODT_NS)
        if body is None:
            return DocumentConverterResult(markdown="")

        text_elem = body.find("office:text", ODT_NS)
        if text_elem is None:
            return DocumentConverterResult(markdown="")

        md_parts = []
        for child in text_elem:
            tag = _strip_ns(child.tag)
            if tag == "h":
                level = child.get("{%s}outline-level" % ODT_NS["text"], "1")
                text = _extract_text(child)
                if text:
                    md_parts.append(f"{'#' * int(level)} {text}")
            elif tag == "p":
                text = _extract_text(child)
                if text:
                    md_parts.append(text)
            elif tag == "list":
                md_parts.append(_convert_list(child))
            elif tag == "table":
                md_parts.append(_convert_table(child))
            elif tag == "section":
                md_parts.append(f"\n## {_extract_text(child)}\n")

        return DocumentConverterResult(markdown="\n\n".join(md_parts))


def _strip_ns(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def _extract_text(element: ET.Element) -> str:
    parts = []
    for node in element.iter():
        tag = _strip_ns(node.tag)
        if tag == "s" and node.get("{%s}c" % ODT_NS["text"]):
            count = int(node.get("{%s}c" % ODT_NS["text"], "1"))
            parts.append(" " * count)
        elif tag == "tab":
            parts.append("\t")
        elif tag == "line-break":
            parts.append("\n")
        elif node.text:
            parts.append(node.text)
        if node.tail:
            parts.append(node.tail)
    return "".join(parts).strip()


def _convert_list(list_elem: ET.Element) -> str:
    lines = []
    for item in list_elem.iter("{%s}list-item" % ODT_NS["text"]):
        for p in item.findall(".//{%s}p" % ODT_NS["text"]):
            text = _extract_text(p)
            if text:
                lines.append(f"- {text}")
    return "\n".join(lines)


def _convert_table(table_elem: ET.Element) -> str:
    rows = []
    for row in table_elem.findall(".//{%s}table-row" % ODT_NS["table"]):
        cells = []
        for cell in row.findall(".//{%s}table-cell" % ODT_NS["table"]):
            cell_text = " ".join(
                _extract_text(p)
                for p in cell.findall(".//{%s}p" % ODT_NS["text"])
            )
            cells.append(cell_text)
        if cells:
            rows.append("| " + " | ".join(cells) + " |")
    if rows:
        # Add header separator after first row
        if len(rows) > 1:
            col_count = rows[0].count("|") - 1
            rows.insert(1, "|" + " --- |" * col_count)
    return "\n".join(rows)
