"""EXPERIMENTAL: page-by-page streaming conversion for PDF documents."""

from __future__ import annotations

import io
import sys
from typing import Any, BinaryIO, Iterator

from .._exceptions import MISSING_DEPENDENCY_MESSAGE, MissingDependencyException
from .._stream_info import StreamInfo
from ..converters._pdf_converter import (
    ACCEPTED_FILE_EXTENSIONS,
    ACCEPTED_MIME_TYPE_PREFIXES,
    _extract_form_content_from_words,
    _merge_partial_numbering_lines,
)
from ._base import StreamingDocumentConverter

_dependency_exc_info = None
try:
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()

_PDF_MAGIC = b"%PDF-"


class PdfStreamingConverter(StreamingDocumentConverter):
    """EXPERIMENTAL: Converts PDFs to Markdown one page at a time.

    Reuses the per-page extraction logic of the standard
    :class:`markitdown.converters.PdfConverter` (form/table detection via
    pdfplumber, plain-text extraction otherwise). Output differences vs the
    standard converter:

    - Pure-prose PDFs: the standard converter re-extracts the whole document
      with pdfminer for better spacing; the streaming converter keeps the
      per-page pdfplumber text so pages can be yielded as they are read.
    - MasterFormat partial-numbering merging is applied per page, so a
      numbering item split exactly across a page boundary is not merged.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        hinted = extension in ACCEPTED_FILE_EXTENSIONS or any(
            mimetype.startswith(prefix) for prefix in ACCEPTED_MIME_TYPE_PREFIXES
        )
        if not hinted:
            return False

        # Verify the magic bytes so mislabeled content falls back to the
        # standard conversion path (which re-detects the actual format).
        cur_pos = file_stream.tell()
        magic = file_stream.read(len(_PDF_MAGIC))
        file_stream.seek(cur_pos)
        return magic == _PDF_MAGIC

    def iter_markdown(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Iterator[str]:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        pdf_bytes = io.BytesIO(file_stream.read())

        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages:
                page_content = _extract_form_content_from_words(page)
                if page_content is None:
                    page_content = page.extract_text() or ""
                page.close()  # Free cached page data immediately

                page_content = _merge_partial_numbering_lines(page_content).strip()
                if page_content:
                    yield page_content
