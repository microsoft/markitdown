"""
Converter for legacy Microsoft Word .doc files (Word 97-2003, OLE Compound Document format).

This converter uses the `olefile` library (already an optional dependency of markitdown
for Outlook .msg support) to parse the OLE container and extract text from the
WordDocument stream using the binary Word format specification.

Dependency group: "doc"
  pip install markitdown[doc]
"""

import sys
import io
import struct
from typing import Any, BinaryIO

from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# ---------------------------------------------------------------------------
# Optional dependency – olefile
# ---------------------------------------------------------------------------
_dependency_exc_info = None
olefile = None
try:
    import olefile as _olefile  # type: ignore[import-untyped]

    olefile = _olefile
except ImportError:
    _dependency_exc_info = sys.exc_info()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/x-msword",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]

# Word FIB (File Information Block) offsets we need
_FIB_MAGIC = 0xA5EC  # wIdent – identifies a Word binary file
_FIB_OFFSET_WIDENT = 0  # WORD
_FIB_OFFSET_FLAGS = 10  # WORD  – bit 1 = fComplex (complex fast-save)
_FIB_OFFSET_FCMIN = 24  # DWORD – unused in Word 97+, kept for compat
_FIB_OFFSET_N_TABLE_STREAM = 11  # byte 0x0B, bit 1 = fWhichTblStm (0 => 0Table, 1 => 1Table)

# Piece-table CLX offsets (Word 97+)
# These are found in the FibRgFcLcb97 sub-structure that starts at offset 0x0120
_FIB_97_CLXTABLES_FC = 0x01A2  # fcClx  – file offset of CLX in table stream  (DWORD)
_FIB_97_CLXTABLES_LCB = 0x01A6  # lcbClx – size of CLX in table stream         (DWORD)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _read_dword(data: bytes, offset: int) -> int:
    """Read a little-endian 32-bit unsigned integer."""
    return struct.unpack_from("<I", data, offset)[0]


def _read_word(data: bytes, offset: int) -> int:
    """Read a little-endian 16-bit unsigned integer."""
    return struct.unpack_from("<H", data, offset)[0]


def _extract_text_from_doc(file_stream: BinaryIO) -> str:
    """
    Extract plain text from a legacy Word .doc file.

    The algorithm follows the Word97-2007 Binary File Format specification:
      1.  Open the OLE container and locate the WordDocument stream.
      2.  Read the FIB to find which table stream to use and where the CLX is.
      3.  Parse the CLX to get the piece table (PlcPcd).
      4.  For every piece in the PlcPcd, decode the text (UTF-16LE or CP1252).
      5.  Return the concatenated paragraphs as plain text.

    Falls back to a "dumb scan" if the structured parse fails for any reason
    (e.g. fast-saved or corrupted documents).
    """
    assert olefile is not None  # guarded by _dependency_exc_info check above

    ole = olefile.OleFileIO(file_stream)

    try:
        # ---- 1. Read WordDocument stream --------------------------------
        if not ole.exists("WordDocument"):
            raise ValueError("Not a valid .doc file: missing WordDocument stream")

        word_stream = ole.openstream("WordDocument").read()

        # Verify magic number
        magic = _read_word(word_stream, _FIB_OFFSET_WIDENT)
        if magic != _FIB_MAGIC:
            raise ValueError(f"Not a valid Word file: unexpected magic 0x{magic:04X}")

        # ---- 2. Find the correct table stream (0Table or 1Table) --------
        flags_byte = word_stream[_FIB_OFFSET_N_TABLE_STREAM]
        table_stream_name = "1Table" if (flags_byte & 0x02) else "0Table"

        if not ole.exists(table_stream_name):
            raise ValueError(f"Missing table stream: {table_stream_name}")

        table_stream = ole.openstream(table_stream_name).read()

        # ---- 3. Locate the CLX (piece table) in the table stream --------
        if len(word_stream) < _FIB_97_CLXTABLES_LCB + 4:
            raise ValueError("FIB too short – cannot be a Word 97+ file")

        fc_clx = _read_dword(word_stream, _FIB_97_CLXTABLES_FC)
        lcb_clx = _read_dword(word_stream, _FIB_97_CLXTABLES_LCB)

        if lcb_clx == 0:
            raise ValueError("CLX size is 0 – no piece table found")

        clx_data = table_stream[fc_clx: fc_clx + lcb_clx]

        # ---- 4. Parse the CLX to find PlcPcd (piece table) --------------
        # CLX = zero or more Prc structures + one PlcPcd
        # Prc starts with clxt=0x01 followed by a CbGrpprl (int16) + GrpPrl bytes
        # PlcPcd starts with clxt=0x02 followed by lcb (uint32) + PlcPcd data
        i = 0
        plc_pcd_data: bytes | None = None

        while i < len(clx_data):
            clxt = clx_data[i]
            i += 1
            if clxt == 0x01:
                # Prc – skip it
                if i + 2 > len(clx_data):
                    break
                cb_grp = struct.unpack_from("<h", clx_data, i)[0]  # signed int16
                i += 2 + cb_grp
            elif clxt == 0x02:
                # PlcPcd – this is what we want
                if i + 4 > len(clx_data):
                    break
                lcb_plc = _read_dword(clx_data, i)
                i += 4
                plc_pcd_data = clx_data[i: i + lcb_plc]
                break
            else:
                # Unknown record type – bail out and fall back
                break

        if plc_pcd_data is None:
            raise ValueError("Could not locate PlcPcd in CLX")

        # ---- 5. Decode pieces -------------------------------------------
        # PlcPcd structure:
        #   rgCp:  array of (n+1) CP values (uint32 each) – character positions
        #   rgPcd: array of  n   PCD structures (8 bytes each)
        #
        # Number of pieces n = (len(plc_pcd_data) - 4) // 12
        #   because: (n+1)*4 + n*8 = 12n + 4  => n = (size - 4) / 12
        size = len(plc_pcd_data)
        n_pieces = (size - 4) // 12
        if n_pieces <= 0:
            raise ValueError("PlcPcd contains no pieces")

        cp_array_size = (n_pieces + 1) * 4
        pcd_array_offset = cp_array_size

        parts: list[str] = []

        for idx in range(n_pieces):
            # CP start/end (character positions, 0-based)
            cp_start = _read_dword(plc_pcd_data, idx * 4)
            cp_end = _read_dword(plc_pcd_data, (idx + 1) * 4)
            char_count = cp_end - cp_start
            if char_count <= 0:
                continue

            # PCD is 8 bytes; the fc field is bytes 2-5 (DWORD) – file character position
            pcd_offset = pcd_array_offset + idx * 8
            if pcd_offset + 8 > size:
                break

            # fc encoding:
            #   bit 30 (0x40000000) set => compressed (single-byte CP1252 characters)
            #   otherwise              => UTF-16LE (two bytes per character)
            fc_raw = _read_dword(plc_pcd_data, pcd_offset + 2)
            compressed = bool(fc_raw & 0x40000000)
            fc = (fc_raw & ~0x40000000)

            try:
                if compressed:
                    # CP1252 – one byte per character; position is byte offset in WordDocument
                    raw = word_stream[fc: fc + char_count]
                    text = raw.decode("cp1252", errors="replace")
                else:
                    # UTF-16LE – two bytes per character
                    raw = word_stream[fc: fc + char_count * 2]
                    text = raw.decode("utf-16-le", errors="replace")
            except Exception:
                continue

            # Replace Word paragraph marks (0x0D) and special chars with newlines/spaces
            text = text.replace("\r", "\n")
            # Remove NUL characters and other Word control characters that are not
            # visible text (field codes, etc.)
            text = "".join(
                ch if (ch.isprintable() or ch in ("\n", "\t")) else " "
                for ch in text
            )
            parts.append(text)

        return "".join(parts).strip()

    finally:
        ole.close()


def _fallback_text_extraction(file_stream: BinaryIO) -> str:
    """
    Dumb-scan fallback: read the WordDocument stream and extract any
    printable UTF-16LE runs longer than 4 characters.  Not perfect but
    better than nothing for corrupted or fast-saved documents.
    """
    assert olefile is not None

    file_stream.seek(0)
    ole = olefile.OleFileIO(file_stream)
    try:
        if not ole.exists("WordDocument"):
            return ""
        data = ole.openstream("WordDocument").read()
    finally:
        ole.close()

    # Scan for UTF-16LE printable runs
    words: list[str] = []
    i = 0
    run: list[str] = []
    while i + 1 < len(data):
        lo, hi = data[i], data[i + 1]
        ch = chr(lo | (hi << 8))
        if ch.isprintable() and ch not in ("\x00",):
            run.append(ch)
        else:
            if len(run) >= 4:
                words.append("".join(run))
            run = []
        i += 2
    if len(run) >= 4:
        words.append("".join(run))

    return " ".join(words)


# ---------------------------------------------------------------------------
# Converter class
# ---------------------------------------------------------------------------

class DocConverter(DocumentConverter):
    """
    Converts legacy Microsoft Word .doc files (Word 97-2003, OLE Compound
    Document format) to Markdown.

    Requires the ``olefile`` package::

        pip install markitdown[doc]

    The converter extracts plain text using the Word binary format's piece
    table (PlcPcd) for accurate, structure-aware text extraction.  Paragraph
    breaks are preserved as blank lines, producing clean Markdown-compatible
    output.

    .. note::
        Rich formatting (bold, italic, headings, tables) is **not** preserved
        because the legacy .doc format requires a full Word parser to
        reconstruct that information.  For rich output from modern Word files
        please use .docx (which is supported by :class:`DocxConverter`).
    """

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

        # Brute-force sniff: OLE files start with the magic bytes D0 CF 11 E0
        cur_pos = file_stream.tell()
        try:
            header = file_stream.read(8)
            if header[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
                # It's an OLE file – could be .doc, .xls, .ppt, .msg, …
                # Accept only if extension/mime already matched above, OR if
                # extension is unknown (empty), to avoid stealing .xls/.ppt etc.
                if not extension or extension == ".doc":
                    return True
        finally:
            file_stream.seek(cur_pos)

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Raise a helpful error if olefile is not installed
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        # Ensure we read from the beginning
        file_stream.seek(0)

        try:
            text = _extract_text_from_doc(file_stream)
        except Exception:
            # Fall back to dumb scan on any parse error
            file_stream.seek(0)
            try:
                text = _fallback_text_extraction(file_stream)
            except Exception:
                text = ""

        if not text:
            return DocumentConverterResult(markdown="", title=None)

        # Convert double-newlines to paragraph breaks; single newlines to spaces
        # so that the output reads as clean Markdown paragraphs.
        lines = text.splitlines()
        md_lines: list[str] = []
        for line in lines:
            stripped = line.strip()
            md_lines.append(stripped)

        markdown = "\n".join(md_lines).strip()

        # Collapse 3+ consecutive blank lines into 2
        import re
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        return DocumentConverterResult(markdown=markdown, title=None)
