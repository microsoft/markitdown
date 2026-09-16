"""Read spreadsheet drawing images without reloading or resaving the workbook."""

import io
import mimetypes
import posixpath
import zipfile
from typing import Any, BinaryIO, Callable, Optional
from urllib.parse import unquote

from defusedxml import ElementTree as ET

from .._stream_info import StreamInfo
from ._image import _parse_image_html


_NS = {
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
_REL_ID = "{" + _NS["r"] + "}id"
_EMBED = "{" + _NS["r"] + "}embed"


def _relationships(
    archive: zipfile.ZipFile, part: str, kind: Optional[str] = None
) -> dict[str, str]:
    directory, filename = posixpath.split(part)
    rels = posixpath.join(directory, "_rels", filename + ".rels")
    if rels not in archive.namelist():
        return {}
    root = ET.fromstring(archive.read(rels))
    return {
        rel.attrib["Id"]: posixpath.normpath(
            posixpath.join(directory, unquote(rel.attrib["Target"]))
        ).lstrip("/")
        for rel in root
        if rel.get("TargetMode") != "External"
        and (kind is None or rel.attrib["Type"].endswith("/" + kind))
    }


class _XlsxImages:
    def __init__(self, file_stream: BinaryIO):
        self._sheets: dict[str, list[tuple[bytes, StreamInfo]]] = {}
        with zipfile.ZipFile(file_stream) as archive:
            workbook = _relationships(archive, "", "officeDocument")
            workbook_part = next(iter(workbook.values()))
            sheets = ET.fromstring(archive.read(workbook_part))
            sheet_parts = _relationships(archive, workbook_part)
            content_types = ET.fromstring(archive.read("[Content_Types].xml"))
            defaults = {
                item.attrib["Extension"].lower(): item.attrib["ContentType"]
                for item in content_types
                if "Extension" in item.attrib
            }
            overrides = {
                unquote(item.attrib["PartName"]).lstrip("/"): item.attrib["ContentType"]
                for item in content_types
                if "PartName" in item.attrib
            }
            for sheet in sheets.findall("s:sheets/s:sheet", _NS):
                sheet_part = sheet_parts[sheet.attrib[_REL_ID]]
                drawings = ET.fromstring(archive.read(sheet_part)).findall(
                    "s:drawing", _NS
                )
                if not drawings:
                    continue
                drawing_parts = _relationships(archive, sheet_part)
                images = self._sheets.setdefault(sheet.attrib["name"], [])
                for drawing in drawings:
                    drawing_part = drawing_parts[drawing.attrib[_REL_ID]]
                    image_parts = _relationships(archive, drawing_part)
                    drawing_root = ET.fromstring(archive.read(drawing_part))
                    # Match openpyxl's image traversal, not its XML serialization order.
                    anchors = [
                        anchor
                        for kind in ("absoluteAnchor", "oneCellAnchor", "twoCellAnchor")
                        for anchor in drawing_root.findall(f"xdr:{kind}", _NS)
                    ]
                    for anchor in anchors:
                        for blip in anchor.findall(".//a:blip", _NS):
                            relationship = blip.get(_EMBED)
                            if relationship is None:
                                # Linked images are not embedded package content.
                                continue
                            image_part = image_parts[relationship]
                            extension = posixpath.splitext(image_part)[1].lower()
                            info = StreamInfo(
                                mimetype=overrides.get(image_part)
                                or defaults.get(extension.lstrip("."))
                                or mimetypes.guess_type(image_part)[0],
                                extension=extension,
                                filename=posixpath.basename(image_part),
                            )
                            images.append((archive.read(image_part), info))

    def to_html(
        self,
        sheet_name: str,
        render: Callable[..., Optional[str]],
        options: dict[str, Any],
    ) -> str:
        fragments = []
        for data, info in self._sheets.get(sheet_name, []):
            with io.BytesIO(data) as image_stream:
                fragment = render(image_stream, info, **options)
            soup = _parse_image_html(fragment)
            if soup is None:
                continue
            fragments.append(f"<div>{soup}</div>")
        if not fragments:
            return ""
        return "<h3>Images in this sheet:</h3>" + "".join(fragments)
