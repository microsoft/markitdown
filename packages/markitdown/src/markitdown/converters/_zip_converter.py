import zipfile
import io
import os

from typing import BinaryIO, Any, List, TYPE_CHECKING

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import UnsupportedFormatException, FileConversionException

# Break otherwise circular import for type hinting
if TYPE_CHECKING:
    from .._markitdown import MarkItDown

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/zip",
]

ACCEPTED_FILE_EXTENSIONS = [".zip"]

# Safety limits applied when extracting untrusted archives, guarding against
# decompression bombs. Each limit can be overridden per conversion via the
# corresponding keyword argument (e.g., convert(..., zip_max_members=500)).
DEFAULT_MAX_MEMBERS = 10000
DEFAULT_MAX_TOTAL_UNCOMPRESSED_SIZE = 500 * 1024 * 1024  # 500 MB
DEFAULT_MAX_COMPRESSION_RATIO = 100.0

# The compression ratio check only applies to members whose declared
# uncompressed size exceeds this floor. Smaller members are cheap to extract
# regardless of ratio, and small files can legitimately compress very well.
COMPRESSION_RATIO_MIN_MEMBER_SIZE = 1024 * 1024  # 1 MB


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

    Resource limits for untrusted archives (configurable via keyword arguments):
    - zip_max_members: maximum number of archive members (default 10000)
    - zip_max_total_uncompressed_size: maximum cumulative uncompressed bytes
      (default 500 MB)
    - zip_max_compression_ratio: maximum per-member compression ratio for
      members larger than 1 MB (default 100)
    Archives exceeding these limits fail with a FileConversionException.
    """

    def __init__(
        self,
        *,
        markitdown: "MarkItDown",
    ):
        super().__init__()
        self._markitdown = markitdown

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
        max_members = kwargs.get("zip_max_members", DEFAULT_MAX_MEMBERS)
        max_total_uncompressed_size = kwargs.get(
            "zip_max_total_uncompressed_size", DEFAULT_MAX_TOTAL_UNCOMPRESSED_SIZE
        )
        max_compression_ratio = kwargs.get(
            "zip_max_compression_ratio", DEFAULT_MAX_COMPRESSION_RATIO
        )

        file_path = stream_info.url or stream_info.local_path or stream_info.filename
        md_content = f"Content from the zip file `{file_path}`:\n\n"

        with zipfile.ZipFile(file_stream, "r") as zipObj:
            infos = zipObj.infolist()
            if len(infos) > max_members:
                raise FileConversionException(
                    f"ZIP archive contains {len(infos)} members, which exceeds the maximum supported ({max_members})."
                )

            total_uncompressed_size = 0
            for info in infos:
                name = info.filename

                # Fast-fail on members with an extreme compression ratio
                if (
                    info.file_size > COMPRESSION_RATIO_MIN_MEMBER_SIZE
                    and info.file_size / max(info.compress_size, 1)
                    > max_compression_ratio
                ):
                    raise FileConversionException(
                        f"ZIP member '{name}' has a compression ratio of {info.file_size / max(info.compress_size, 1):.0f}:1, which exceeds the maximum supported ({max_compression_ratio}:1)."
                    )

                # Fast-fail if the declared sizes alone exceed the budget
                if (
                    total_uncompressed_size + info.file_size
                    > max_total_uncompressed_size
                ):
                    raise FileConversionException(
                        f"Extracting ZIP member '{name}' would exceed the maximum supported total uncompressed size ({max_total_uncompressed_size} bytes)."
                    )

                # Read the member in chunks, tracking the actual decompressed
                # size, since header sizes in crafted archives cannot be trusted
                chunks: List[bytes] = []
                with zipObj.open(info) as z_file:
                    while True:
                        chunk = z_file.read(65536)
                        if not chunk:
                            break
                        total_uncompressed_size += len(chunk)
                        if total_uncompressed_size > max_total_uncompressed_size:
                            raise FileConversionException(
                                f"ZIP archive exceeded the maximum supported total uncompressed size ({max_total_uncompressed_size} bytes) while extracting '{name}'."
                            )
                        chunks.append(chunk)

                try:
                    z_file_stream = io.BytesIO(b"".join(chunks))
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
