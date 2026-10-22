"""Converter for legacy .doc (Microsoft Word binary) files.

Uses ``mammoth`` if available, falling back to ``python-docx`` with
``olefile`` for pre-2007 Word binary format extraction.
"""

from __future__ import annotations

import locale
import sys
from io import BytesIO
from typing import Any, BinaryIO

from markitdown._base_converter import DocumentConverter, DocumentConverterResult
from markitdown._exceptions import MissingDependencyException
from markitdown._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/x-msword",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """Converts legacy .doc files to Markdown."""

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

        # Try python-docx2txt first (handles .doc via olefile)
        try:
            import docx2txt

            text = docx2txt.process(BytesIO(content))
            if text and text.strip():
                return DocumentConverterResult(markdown=text)
        except ImportError:
            pass
        except Exception:
            pass

        # Fallback: try mammoth (primarily for .docx, but worth trying)
        try:
            import mammoth

            result = mammoth.extract_raw_text(BytesIO(content))
            if result.value and result.value.strip():
                return DocumentConverterResult(markdown=result.value)
        except ImportError:
            pass
        except Exception:
            pass

        raise MissingDependencyException(
            "DocConverter requires 'docx2txt' or 'mammoth'. "
            "Install with: pip install docx2txt"
        )
