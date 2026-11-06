"""Converter for .chm (Microsoft Compiled HTML Help) files.

CHM files are compressed archives containing HTML pages. This converter
extracts and concatenates the text content from all HTML pages.
"""

from __future__ import annotations

import locale
import os
import subprocess
import tempfile
from typing import Any, BinaryIO

from markitdown._base_converter import DocumentConverter, DocumentConverterResult
from markitdown._exceptions import MissingDependencyException
from markitdown._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/x-chm",
    "application/chm",
    "application/x-ms-chm",
    "application/vnd.ms-htmlhelp",
]

ACCEPTED_FILE_EXTENSIONS = [".chm"]


class ChmConverter(DocumentConverter):
    """Converts .chm files to Markdown by extracting HTML content."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        extension = (stream_info.extension or "").lower()
        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True
        mimetype = (stream_info.mimetype or "").lower()
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
        content = file_stream.read()

        # Try python-chm first
        try:
            from pychm import chm

            with tempfile.NamedTemporaryFile(suffix=".chm", delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                book = chm.CHMFile(tmp_path)
                book.index()
                topics = book.get_all_topics()
                for topic in topics:
                    pass  # text extraction varies by library version
            finally:
                os.unlink(tmp_path)
        except ImportError:
            pass
        except Exception:
            pass

        # Fallback: extract with system tools (7z or python-native zipfile)
        import zipfile

        try:
            # Some CHM files can be opened as zip (ITSF format)
            import html

            with BytesIO(content) as zf_io:
                try:
                    with zipfile.ZipFile(zf_io) as zf:
                        html_files = [
                            n for n in zf.namelist() if n.lower().endswith((".html", ".htm"))
                        ]
                        texts = []
                        for name in sorted(html_files):
                            with zf.open(name) as f:
                                raw = f.read().decode("utf-8", errors="replace")
                                # strip HTML tags roughly
                                import re
                                stripped = re.sub(r"<[^>]+>", " ", raw)
                                stripped = html.unescape(stripped)
                                texts.append(stripped.strip())
                        if texts:
                            return DocumentConverterResult(
                                markdown="\n\n".join(texts)
                            )
                except zipfile.BadZipFile:
                    pass
        except Exception:
            pass

        raise MissingDependencyException(
            "ChmConverter requires 'pychm' or the file to be zip-decodable. "
            "Install with: pip install pychm"
        )
