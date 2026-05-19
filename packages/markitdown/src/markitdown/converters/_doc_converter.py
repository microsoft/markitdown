"""Legacy .doc (old Word binary) converter.

MarkItDown's DocxConverter only handles the modern .docx (Open XML) format.
Real-world Chinese office environments still produce huge amounts of pre-2007
.doc binary files; without a converter these all explode with
``UnsupportedFormatException``.

This converter tries two strategies, in order:

  1. **Word COM automation** (Windows only, requires MS Word installed)
     Spawns an invisible Word instance, opens the .doc, re-saves it as .docx
     in a temp dir, then delegates to the regular DocxConverter. Highest
     fidelity (preserves headings, tables, images alt-text).

  2. **olefile text extraction** (cross-platform, last-ditch fallback)
     Pulls the raw text stream out of the .doc OLE compound document. Loses
     all formatting and image references, but reliably extracts at least the
     prose text so the user is not completely stuck.

If neither path works (e.g. Linux box without Word, .doc heavily corrupted,
olefile cannot read the WordDocument stream), the converter raises
``MissingDependencyException`` with a clear message pointing the user at
LibreOffice / textract / antiword as remediation.
"""

from __future__ import annotations

import io
import os
import re
import sys
import tempfile
import time
from typing import Any, BinaryIO, Optional

from ._docx_converter import DocxConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/vnd.ms-word",
]
ACCEPTED_FILE_EXTENSIONS = [".doc"]


# ---------------------------------------------------------------------------
# Strategy 1: Word COM (Windows + Word installed)
# ---------------------------------------------------------------------------


def _word_com_available() -> bool:
    if sys.platform != "win32":
        return False
    try:
        import win32com.client  # noqa: F401
        return True
    except ImportError:
        return False


def _convert_with_word_com(input_path: str) -> Optional[str]:
    """Open .doc with Word COM, re-save as .docx, return the new path.

    Returns None if Word COM isn't usable (e.g. Word not installed or
    automation refused). The .docx lives in a tempdir; caller is responsible
    for deleting it.
    """
    if not _word_com_available():
        return None
    try:
        import pythoncom  # type: ignore
        import win32com.client  # type: ignore

        pythoncom.CoInitialize()
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            word.DisplayAlerts = 0  # wdAlertsNone
            try:
                # Use absolute paths; Word COM otherwise resolves relative to
                # cwd of the COM server.
                input_path_abs = os.path.abspath(input_path)
                out_dir = tempfile.mkdtemp(prefix="markitdown_doc_")
                out_path = os.path.join(out_dir, "converted.docx")
                doc = word.Documents.Open(
                    input_path_abs,
                    ConfirmConversions=False,
                    ReadOnly=True,
                )
                try:
                    # wdFormatXMLDocument = 12 (.docx)
                    doc.SaveAs(out_path, FileFormat=12)
                finally:
                    doc.Close(SaveChanges=False)
            finally:
                word.Quit()
        finally:
            pythoncom.CoUninitialize()
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return out_path
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Strategy 2: olefile raw text extraction
# ---------------------------------------------------------------------------

# Word .doc files store the body text in the "WordDocument" OLE stream.
# Inside that stream the text starts at byte offset `fcMin` from the
# FibBase, but a far simpler heuristic that handles most files is to grab
# the entire stream and pull printable runs out. Quality is much lower than
# Word COM (no tables / no headings) but it survives missing Word.

_PRINTABLE_RUN_RE = re.compile(
    # Match runs of CJK + ASCII printable + common whitespace
    rb"[\x09\x0a\x0d\x20-\x7e\xc2-\xf4][\x20-\xff]{2,}"
)


def _extract_text_with_olefile(data: bytes) -> Optional[str]:
    try:
        import olefile  # type: ignore
    except ImportError:
        return None
    try:
        if not olefile.isOleFile(io.BytesIO(data)):
            return None
        ole = olefile.OleFileIO(io.BytesIO(data))
        try:
            if not ole.exists("WordDocument"):
                return None
            stream = ole.openstream("WordDocument").read()
        finally:
            ole.close()
    except Exception:
        return None

    # Heuristic: most readable body text is UTF-16-LE inside .doc.
    # Try that first, fall back to a byte-level printable-run sweep.
    try:
        # Skip the FIB header (~1024 bytes) and decode the rest as UTF-16-LE.
        # Replace errors so we don't crash on stray bytes.
        decoded = stream[1024:].decode("utf-16-le", errors="ignore")
        # Strip ASCII control chars and runs of NULs.
        decoded = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", " ", decoded)
        # Collapse 3+ whitespace into 1 newline for readability.
        decoded = re.sub(r"\s{3,}", "\n\n", decoded).strip()
        # Sanity: enough alphanumeric / CJK to count as text?
        meaningful = re.findall(r"[\w\u4e00-\u9fff]", decoded)
        if len(meaningful) >= 20:
            return decoded
    except Exception:
        pass

    # Last-ditch byte-level extraction
    try:
        chunks = _PRINTABLE_RUN_RE.findall(stream)
        joined = b"\n".join(chunks).decode("latin-1", errors="ignore")
        if len(joined) >= 50:
            return joined
    except Exception:
        pass

    return None


# ---------------------------------------------------------------------------
# DocConverter — orchestrates the two strategies
# ---------------------------------------------------------------------------


class DocConverter(DocumentConverter):
    """Converts legacy .doc binaries via Word COM, falling back to olefile."""

    def __init__(self) -> None:
        super().__init__()
        self._docx_converter = DocxConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        return self._accepted_by_mime_or_ext(
            stream_info, ACCEPTED_MIME_TYPE_PREFIXES, ACCEPTED_FILE_EXTENSIONS
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Snapshot the stream once; both strategies need bytes.
        cur = file_stream.tell()
        data = file_stream.read()
        file_stream.seek(cur)

        # --- Strategy 1: Word COM ---
        tmp_input_path = None
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".doc", delete=False
            ) as tmpf:
                tmpf.write(data)
                tmp_input_path = tmpf.name
            docx_path = _convert_with_word_com(tmp_input_path)
            if docx_path is not None:
                try:
                    with open(docx_path, "rb") as docx_fh:
                        return self._docx_converter.convert(
                            docx_fh,
                            stream_info=StreamInfo(extension=".docx"),
                            **kwargs,
                        )
                finally:
                    try:
                        os.unlink(docx_path)
                        os.rmdir(os.path.dirname(docx_path))
                    except OSError:
                        pass
        finally:
            if tmp_input_path and os.path.exists(tmp_input_path):
                try:
                    os.unlink(tmp_input_path)
                except OSError:
                    pass

        # --- Strategy 2: olefile text extraction ---
        text = _extract_text_with_olefile(data)
        if text:
            return DocumentConverterResult(markdown=text)

        # --- Both strategies failed ---
        raise MissingDependencyException(
            MISSING_DEPENDENCY_MESSAGE.format(
                converter=type(self).__name__,
                extension=".doc",
                feature="doc",
            )
            + " (Tried Word COM and olefile; both unavailable or failed. "
            "Install Microsoft Word + pywin32 on Windows, or convert the .doc "
            "to .docx with LibreOffice (`soffice --headless --convert-to docx`) "
            "before passing it to MarkItDown.)"
        )
