"""EXPERIMENTAL: slide-by-slide streaming conversion for PPTX documents."""

from __future__ import annotations

import sys
from typing import Any, BinaryIO, Iterator

from .._exceptions import MISSING_DEPENDENCY_MESSAGE, MissingDependencyException
from .._stream_info import StreamInfo
from ..converters._pptx_converter import (
    ACCEPTED_FILE_EXTENSIONS,
    ACCEPTED_MIME_TYPE_PREFIXES,
    PptxConverter,
)
from ._base import StreamingDocumentConverter

_dependency_exc_info = None
try:
    import pptx
except ImportError:
    _dependency_exc_info = sys.exc_info()

_ZIP_MAGIC = b"PK\x03\x04"


class PptxStreamingConverter(StreamingDocumentConverter):
    """EXPERIMENTAL: Converts PPTX presentations to Markdown one slide at a
    time.

    Delegates per-slide conversion to the standard
    :class:`markitdown.converters.PptxConverter`, so each fragment matches
    the standard converter's output for that slide exactly.
    """

    def __init__(self) -> None:
        self._converter = PptxConverter()

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

        # PPTX files are ZIP archives; verify the magic bytes so mislabeled
        # content falls back to the standard conversion path.
        cur_pos = file_stream.tell()
        magic = file_stream.read(len(_ZIP_MAGIC))
        file_stream.seek(cur_pos)
        return magic == _ZIP_MAGIC

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
                    extension=".pptx",
                    feature="pptx",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        presentation = pptx.Presentation(file_stream)
        for slide_num, slide in enumerate(presentation.slides, start=1):
            yield self._converter._convert_slide(slide, slide_num, **kwargs)
