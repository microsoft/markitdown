import os
from pathlib import Path
import tempfile
from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

_dependency_exc_info = None
rhwp: Any = None
try:
    import rhwp
except ImportError:
    import sys

    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/x-hwp",
    "application/vnd.hancom.hwp",
    "application/x-hwp-v5",
    "application/haansofthwp",
    "application/vnd.hancom.hwpx",
    "application/hwpx",
    "application/x-hwpx",
]

ACCEPTED_FILE_EXTENSIONS = [".hwp", ".hwpx"]


class HwpConverter(DocumentConverter):
    """Converts HWP and HWPX files to Markdown with rhwp-python."""

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

        return any(
            mimetype.startswith(prefix) for prefix in ACCEPTED_MIME_TYPE_PREFIXES
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".hwp or .hwpx",
                    feature="hwp",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        extension = (stream_info.extension or "").lower()
        if extension not in ACCEPTED_FILE_EXTENSIONS:
            extension = ".hwp"

        with tempfile.TemporaryDirectory(prefix="markitdown-rhwp-") as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / f"input{extension}"

            current_position = file_stream.tell()
            try:
                input_path.write_bytes(file_stream.read())
            finally:
                file_stream.seek(current_position)

            document = rhwp.parse(os.fspath(input_path))
            return DocumentConverterResult(markdown=document.to_ir().to_markdown())
