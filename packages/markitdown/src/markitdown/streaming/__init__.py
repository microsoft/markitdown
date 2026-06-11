"""EXPERIMENTAL: incremental (streaming) document conversion.

This package provides converters that yield Markdown fragments while the
source document is still being processed — one fragment per PDF page or
PPTX slide — instead of returning the complete document at once. It reuses
the extraction logic of the standard converters but drives it with its own
controller, so the stable `DocumentConverter` contract (and the plugin API
built on it) is untouched.

The full document is equivalent to joining the stripped fragments with a
blank line. See `PdfStreamingConverter` for the documented output
differences vs the standard PDF converter.

This API is experimental: names and behavior may change between releases.
"""

from ._base import StreamingDocumentConverter
from ._controller import StreamingConverterController
from ._pdf_streaming_converter import PdfStreamingConverter
from ._pptx_streaming_converter import PptxStreamingConverter

__all__ = [
    "StreamingDocumentConverter",
    "StreamingConverterController",
    "PdfStreamingConverter",
    "PptxStreamingConverter",
]
