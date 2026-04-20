import io
import os
import zipfile
from typing import Any, BinaryIO, TYPE_CHECKING

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import FileConversionException, UnsupportedFormatException
from .._stream_info import StreamInfo

# Break otherwise circular import for type hinting
if TYPE_CHECKING:
    from .._markitdown import MarkItDown

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/zip",
]

ACCEPTED_FILE_EXTENSIONS = [".zip"]

# Default safety limits
_DEFAULT_MAX_FILE_COUNT = 100
_DEFAULT_MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB per file
_DEFAULT_MAX_TOTAL_SIZE = 200 * 1024 * 1024  # 200 MB total uncompressed


class ZipConverter(DocumentConverter):
    """Converts ZIP files to markdown by extracting and converting all contained files.

    The converter iterates over ZIP entries, processes each file using appropriate
    converters based on file extensions, and combines the results into a single
    markdown document.

    Safety limits guard against zip bombs and excessively large archives:

    - ``max_file_count``: maximum number of files to process (default 100).
      Files beyond this limit are silently skipped with a notice appended.
    - ``max_file_size``: maximum uncompressed size in bytes per individual file
      (default 50 MB). Files that exceed this limit are skipped with a notice.
    - ``max_total_size``: maximum total uncompressed bytes across all processed
      files (default 200 MB). Processing stops when this budget is exhausted.

    Example output format::

        Content from the zip file `example.zip`:

        ## File: docs/readme.txt

        This is the content of readme.txt

        ## File: data/report.xlsx

        ## Sheet1
        | Column1 | Column2 |
        |---------|---------|
        | data1   | data2   |
    """

    def __init__(
        self,
        *,
        markitdown: "MarkItDown",
        max_file_count: int = _DEFAULT_MAX_FILE_COUNT,
        max_file_size: int = _DEFAULT_MAX_FILE_SIZE,
        max_total_size: int = _DEFAULT_MAX_TOTAL_SIZE,
    ):
        super().__init__()
        self._markitdown = markitdown
        self._max_file_count = max_file_count
        self._max_file_size = max_file_size
        self._max_total_size = max_total_size

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

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        file_path = stream_info.url or stream_info.local_path or stream_info.filename
        md_content = f"Content from the zip file `{file_path}`:\n\n"

        files_processed = 0
        total_bytes = 0

        with zipfile.ZipFile(file_stream, "r") as zipObj:
            for info in zipObj.infolist():
                name = info.filename

                # Skip directory entries
                if name.endswith("/"):
                    continue

                # Guard against zip slip: skip entries with absolute paths or traversal sequences.
                # Check for both Unix-style ("/") and OS-level absolute paths so the guard
                # works correctly on Windows as well as POSIX.
                if (
                    name.startswith("/")
                    or os.path.isabs(name)
                    or ".." in name.split("/")
                ):
                    continue

                if files_processed >= self._max_file_count:
                    md_content += (
                        f"_Remaining files not processed: file count limit "
                        f"({self._max_file_count}) reached._\n"
                    )
                    break

                uncompressed_size = info.file_size
                if uncompressed_size > self._max_file_size:
                    md_content += (
                        f"## File: {name}\n\n"
                        f"_Skipped: uncompressed size ({uncompressed_size:,} bytes) "
                        f"exceeds per-file limit ({self._max_file_size:,} bytes)._\n\n"
                    )
                    continue

                if total_bytes + uncompressed_size > self._max_total_size:
                    md_content += (
                        f"_Remaining files not processed: total size limit "
                        f"({self._max_total_size:,} bytes) reached._\n"
                    )
                    break

                try:
                    z_file_stream = io.BytesIO(zipObj.read(name))
                    z_file_stream_info = StreamInfo(
                        extension=os.path.splitext(name)[1],
                        filename=os.path.basename(name),
                    )
                    result = self._markitdown.convert_stream(
                        stream=z_file_stream,
                        stream_info=z_file_stream_info,
                    )
                    if result is not None:
                        md_content += f"## File: {name}\n\n"
                        md_content += result.markdown + "\n\n"
                except UnsupportedFormatException:
                    pass
                except FileConversionException:
                    pass

                files_processed += 1
                total_bytes += uncompressed_size

        return DocumentConverterResult(markdown=md_content.strip())
