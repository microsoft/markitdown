import zipfile
import io
import os
import logging

from typing import BinaryIO, Any, TYPE_CHECKING

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import UnsupportedFormatException, FileConversionException

# Break otherwise circular import for type hinting
if TYPE_CHECKING:
    from .._markitdown import MarkItDown

logger = logging.getLogger(__name__)

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/zip",
]

ACCEPTED_FILE_EXTENSIONS = [".zip"]

# Zip bomb protection limits
MAX_DECOMPRESSED_FILE_SIZE = 100 * 1024 * 1024  # 100 MB per file
MAX_DECOMPRESSION_RATIO = 100  # 100:1 compressed-to-decompressed ratio
MAX_TOTAL_DECOMPRESSED_SIZE = 500 * 1024 * 1024  # 500 MB total across all files


class ZipConverter(DocumentConverter):
    """Converts ZIP files to markdown by extracting and converting all contained files.

    The converter extracts the ZIP contents to a temporary directory, processes each file
    using appropriate converters based on file extensions, and then combines the results
    into a single markdown document. The temporary directory is cleaned up after processing.

    Example output format:
    ```markdown
    Content from the zip file `example.zip`:

    ## File: docs/readme.txt

    This is the content of readme.txt
    Multiple lines are preserved

    ## File: images/example.jpg

    ImageSize: 1920x1080
    DateTimeOriginal: 2024-02-15 14:30:00
    Description: A beautiful landscape photo

    ## File: data/report.xlsx

    ## Sheet1
    | Column1 | Column2 | Column3 |
    |---------|---------|---------|
    | data1   | data2   | data3   |
    | data4   | data5   | data6   |
    ```

    Key features:
    - Maintains original file structure in headings
    - Processes nested files recursively
    - Uses appropriate converters for each file type
    - Preserves formatting of converted content
    - Cleans up temporary files after processing

    Note: Size checks use ``zipfile.ZipInfo.file_size`` from the local file header.
    A deliberately crafted archive can spoof this value, so the protection guards
    against accidental or naive zip bombs but not adversarial archives with falsified
    headers. Streaming decompression with a running byte counter would be needed for
    full protection against crafted bombs.
    """

    def __init__(
        self,
        *,
        markitdown: "MarkItDown",
        max_file_size: int = MAX_DECOMPRESSED_FILE_SIZE,
        max_ratio: int = MAX_DECOMPRESSION_RATIO,
        max_total_size: int = MAX_TOTAL_DECOMPRESSED_SIZE,
    ):
        super().__init__()
        self._markitdown = markitdown
        self._max_file_size = max_file_size
        self._max_ratio = max_ratio
        self._max_total_size = max_total_size

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
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
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        file_path = stream_info.url or stream_info.local_path or stream_info.filename
        md_content = f"Content from the zip file `{file_path}`:\n\n"

        with zipfile.ZipFile(file_stream, "r") as zipObj:
            total_decompressed = 0

            for name in zipObj.namelist():
                info = zipObj.getinfo(name)

                # Skip directories
                if info.is_dir():
                    continue

                # Check individual file size.
                # Files that exceed the per-file limit are skipped but do not
                # count toward total_decompressed: the per-file check already
                # prevents them from being read, so the cumulative cap only
                # tracks data that was actually extracted.
                if info.file_size > self._max_file_size:
                    logger.warning(
                        "Skipping '%s': decompressed size %d bytes exceeds "
                        "limit of %d bytes",
                        name,
                        info.file_size,
                        self._max_file_size,
                    )
                    continue

                # Check decompression ratio (zip bomb detection)
                compressed = max(info.compress_size, 1)
                ratio = info.file_size / compressed
                if ratio > self._max_ratio:
                    logger.warning(
                        "Skipping '%s': decompression ratio %.1f:1 exceeds "
                        "limit of %d:1",
                        name,
                        ratio,
                        self._max_ratio,
                    )
                    continue

                # Check cumulative decompressed size
                total_decompressed += info.file_size
                if total_decompressed > self._max_total_size:
                    logger.warning(
                        "Stopping extraction: cumulative decompressed size "
                        "%d bytes exceeds limit of %d bytes",
                        total_decompressed,
                        self._max_total_size,
                    )
                    md_content += (
                        "\n> **Note:** Extraction stopped early "
                        "because the cumulative size limit was reached. "
                        "Some files were not converted.\n\n"
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

        return DocumentConverterResult(markdown=md_content.strip())
