"""EXPERIMENTAL: dispatch controller for streaming converters."""

from __future__ import annotations

import re
from typing import Any, BinaryIO, Iterable, Iterator, List, Optional

from .._stream_info import StreamInfo
from ._base import StreamingDocumentConverter
from ._pdf_streaming_converter import PdfStreamingConverter
from ._pptx_streaming_converter import PptxStreamingConverter


class StreamingConverterController:
    """EXPERIMENTAL: Routes documents to a streaming converter when one
    supports the format, mirroring how `MarkItDown` routes to standard
    converters.

    Unlike `MarkItDown`, there is no mid-stream fallback: once a streaming
    converter starts yielding fragments, output has already been delivered,
    so a later failure surfaces as an error rather than a retry with another
    converter. Callers that need fallback behavior should check
    `converter_for()` first and use the standard conversion path when it
    returns None.
    """

    def __init__(
        self, converters: Optional[List[StreamingDocumentConverter]] = None
    ) -> None:
        if converters is None:
            converters = [PdfStreamingConverter(), PptxStreamingConverter()]
        self._converters = list(converters)

    def converter_for(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Optional[StreamingDocumentConverter]:
        """Return the first converter that accepts the document, or None."""
        for converter in self._converters:
            if converter.accepts(file_stream, stream_info, **kwargs):
                return converter
        return None

    def iter_markdown(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Optional[Iterator[str]]:
        """Stream the document if a converter supports it, else return None.

        Fragments are normalized the same way `MarkItDown._convert`
        normalizes complete results, so joining the fragments with a blank
        line reproduces the standard conversion output.
        """
        converter = self.converter_for(file_stream, stream_info, **kwargs)
        if converter is None:
            return None
        return _normalized(converter.iter_markdown(file_stream, stream_info, **kwargs))


def _normalized(fragments: Iterable[str]) -> Iterator[str]:
    """Apply MarkItDown's result normalization to each fragment.

    Mirrors the post-processing in `MarkItDown._convert`: trailing
    whitespace is removed from every line, and runs of three or more
    newlines collapse to two. Empty fragments are dropped.
    """
    for fragment in fragments:
        fragment = "\n".join(line.rstrip() for line in re.split(r"\r?\n", fragment))
        fragment = re.sub(r"\n{3,}", "\n\n", fragment).strip()
        if fragment:
            yield fragment
