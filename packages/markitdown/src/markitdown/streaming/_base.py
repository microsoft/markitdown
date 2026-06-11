"""Base class for experimental streaming converters."""

from __future__ import annotations

from typing import Any, BinaryIO, Iterator

from .._stream_info import StreamInfo


class StreamingDocumentConverter:
    """EXPERIMENTAL: Abstract superclass of incremental document converters.

    Unlike :class:`markitdown.DocumentConverter`, which returns the complete
    Markdown in one result, a streaming converter yields Markdown fragments
    (e.g. one per page or slide) as the source document is processed. The
    full document is equivalent to joining the stripped fragments with a
    blank line (``"\\n\\n"``).

    This API is experimental and may change between releases.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        """Return True if this converter can stream the given document.

        Implementations may peek at `file_stream` (e.g. to check magic
        bytes) but MUST reset the stream position before returning.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement the accepts() method."
        )

    def iter_markdown(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> Iterator[str]:
        """Yield Markdown fragments in document order.

        Raises:
        - FileConversionException: when the document cannot be converted.
        - MissingDependencyException: when a required optional dependency
          is not installed.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement the iter_markdown() method."
        )
