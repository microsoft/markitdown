import re
import struct
import sys
from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

_dependency_exc_info = None
olefile = None
try:
    import olefile  # type: ignore[no-redef]
except ImportError:
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/doc",
    "application/ms-doc",
    "application/msword",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """Converts legacy Word .doc files to Markdown."""

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

        if any(mimetype.startswith(prefix) for prefix in ACCEPTED_MIME_TYPE_PREFIXES):
            return True

        cur_pos = file_stream.tell()
        try:
            if olefile is None or not olefile.isOleFile(file_stream):
                return False

            doc = olefile.OleFileIO(file_stream)
            try:
                return doc.exists("WordDocument")
            finally:
                doc.close()
        except Exception:
            return False
        finally:
            file_stream.seek(cur_pos)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__, extension=".doc", feature="doc"
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        assert olefile is not None
        doc = olefile.OleFileIO(file_stream)
        try:
            text = _WordDocTextExtractor(doc).extract()
        finally:
            doc.close()

        return DocumentConverterResult(markdown=text)


class _WordDocTextExtractor:
    def __init__(self, doc: Any):
        self._doc = doc

    def extract(self) -> str:
        word_stream = self._read_stream("WordDocument")
        if len(word_stream) < 0x20 or self._u16(word_stream, 0) != 0xA5EC:
            raise ValueError("Not a supported Word binary document")

        chunks = self._extract_from_piece_table(word_stream)
        if not chunks:
            chunks = [self._decode_fallback_text(word_stream)]

        return self._clean_text("\n".join(chunk for chunk in chunks if chunk))

    def _extract_from_piece_table(self, word_stream: bytes) -> list[str]:
        if len(word_stream) < 0x1AA:
            return []

        table_name = "1Table" if (self._u16(word_stream, 0x0A) & 0x0200) else "0Table"
        if not self._doc.exists(table_name):
            return []

        table_stream = self._read_stream(table_name)
        fc_clx = self._u32(word_stream, 0x01A2)
        lcb_clx = self._u32(word_stream, 0x01A6)
        if fc_clx < 0 or lcb_clx <= 0 or fc_clx + lcb_clx > len(table_stream):
            return []

        clx = table_stream[fc_clx : fc_clx + lcb_clx]
        plc_pcd = self._find_plc_pcd(clx)
        if not plc_pcd:
            return []

        if (len(plc_pcd) - 4) % 12 != 0:
            return []

        piece_count = (len(plc_pcd) - 4) // 12
        cp_offsets = [self._u32(plc_pcd, i * 4) for i in range(piece_count + 1)]
        pcd_offset = 4 * (piece_count + 1)
        chunks: list[str] = []

        for i in range(piece_count):
            char_count = cp_offsets[i + 1] - cp_offsets[i]
            if char_count <= 0:
                continue

            pcd = plc_pcd[pcd_offset + i * 8 : pcd_offset + (i + 1) * 8]
            fc_raw = self._u32(pcd, 2)
            compressed = bool(fc_raw & 0x40000000)
            fc = fc_raw & 0x3FFFFFFF

            if compressed:
                start = fc // 2
                data = word_stream[start : start + char_count]
                chunks.append(data.decode("cp1252", errors="ignore"))
            else:
                start = fc
                data = word_stream[start : start + char_count * 2]
                chunks.append(data.decode("utf-16-le", errors="ignore"))

        return chunks

    def _decode_fallback_text(self, word_stream: bytes) -> str:
        fc_min = self._u32(word_stream, 0x18)
        fc_mac = self._u32(word_stream, 0x1C)
        data = word_stream[fc_min:fc_mac]
        if not data:
            data = word_stream
        return data.decode("utf-16-le", errors="ignore")

    def _find_plc_pcd(self, clx: bytes) -> bytes | None:
        offset = 0
        while offset < len(clx):
            marker = clx[offset]
            offset += 1
            if marker == 0x01:
                if offset + 2 > len(clx):
                    return None
                offset += 2 + self._u16(clx, offset)
            elif marker == 0x02:
                if offset + 4 > len(clx):
                    return None
                size = self._u32(clx, offset)
                offset += 4
                if offset + size > len(clx):
                    return None
                return clx[offset : offset + size]
            else:
                return None
        return None

    def _read_stream(self, name: str) -> bytes:
        return self._doc.openstream(name).read()

    def _clean_text(self, text: str) -> str:
        text = text.replace("\r", "\n")
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]+", "", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _u16(self, data: bytes, offset: int) -> int:
        return struct.unpack_from("<H", data, offset)[0]

    def _u32(self, data: bytes, offset: int) -> int:
        return struct.unpack_from("<I", data, offset)[0]
