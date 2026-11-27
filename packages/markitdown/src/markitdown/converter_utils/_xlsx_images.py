"""Read spreadsheet drawing images without reloading or resaving the workbook."""

import base64
import io
import mimetypes
import posixpath
import re
import zipfile
import zlib
from typing import Any, BinaryIO, Callable, Optional
from urllib.parse import unquote
from xml.etree.ElementTree import ParseError

from defusedxml import ElementTree as ET
from defusedxml.common import DefusedXmlException

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
# The workbook supplies this value. Only a bare image type belongs in the URI.
_IMAGE_MIME_TYPE = re.compile(r"image/[a-z0-9][a-z0-9.+_-]*", re.ASCII | re.IGNORECASE)
# Missing relationships, malformed XML, and unreadable ZIP parts can leave tables usable.
_IMAGE_READ_ERRORS = (
    KeyError,
    StopIteration,
    ParseError,
    DefusedXmlException,
    zipfile.BadZipFile,
    zlib.error,
    EOFError,
    NotImplementedError,
)


def _image_data_uri(data: bytes, mimetype: Optional[str]) -> str:
    if mimetype and _IMAGE_MIME_TYPE.fullmatch(mimetype):
        media_type = mimetype.lower()
    else:
        media_type = "application/octet-stream"
    return f"data:{media_type};base64,{base64.b64encode(data).decode('ascii')}"


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
                drawing_parts = _relationships(archive, sheet_part, "drawing")
                images = self._sheets.setdefault(sheet.attrib["name"], [])
                for drawing in drawings:
                    drawing_part = drawing_parts[drawing.attrib[_REL_ID]]
                    image_parts = _relationships(archive, drawing_part, "image")
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
            if soup is not None:
                fragments.append(f"<div>{soup}</div>")
            elif options.get("keep_data_uris"):
                uri = _image_data_uri(data, info.mimetype)
                fragments.append(f'<div><img alt="" src="{uri}"></div>')
        if not fragments:
            return ""
        return "<h3>Images in this sheet:</h3>" + "".join(fragments)
