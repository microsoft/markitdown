import zipfile
import io
import os

from typing import BinaryIO, Any, TYPE_CHECKING

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

# Limits that protect against zip bombs (tiny archives that expand to gigabytes)
# and deeply nested archives. They can be overridden per call via kwargs:
# zip_max_entry_bytes, zip_max_total_bytes, zip_max_entries, zip_max_depth.
DEFAULT_MAX_ENTRY_BYTES = 100 * 1024 * 1024  # 100 MB per member
DEFAULT_MAX_TOTAL_BYTES = 500 * 1024 * 1024  # 500 MB for the whole archive
DEFAULT_MAX_ENTRIES = 10_000
DEFAULT_MAX_DEPTH = 3  # zip inside zip inside zip

_CHUNK = 1024 * 1024


class _LimitExceeded(Exception):
    pass


def _read_capped(zip_obj: zipfile.ZipFile, entry: zipfile.ZipInfo, cap: int) -> bytes:
    """Read a member, stopping as soon as it exceeds `cap` bytes.

    The size in the zip header can lie, so the real decompressed size is
    counted while reading instead of trusting entry.file_size.
    """
    buf = io.BytesIO()
    with zip_obj.open(entry) as fh:
        while True:
            chunk = fh.read(_CHUNK)
            if not chunk:
                break
            if buf.tell() + len(chunk) > cap:
                raise _LimitExceeded()
            buf.write(chunk)
    return buf.getvalue()


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
        file_path = (
            stream_info.url
            or stream_info.local_path
            or stream_info.filename
            or "(unknown)"
        )
        md_content = f"Content from the zip file `{file_path}`:\n\n"

        max_entry = int(kwargs.get("zip_max_entry_bytes", DEFAULT_MAX_ENTRY_BYTES))
        max_total = int(kwargs.get("zip_max_total_bytes", DEFAULT_MAX_TOTAL_BYTES))
        max_entries = int(kwargs.get("zip_max_entries", DEFAULT_MAX_ENTRIES))
        max_depth = int(kwargs.get("zip_max_depth", DEFAULT_MAX_DEPTH))
        depth = int(kwargs.get("_zip_depth", 0)) + 1

        if depth > max_depth:
            return DocumentConverterResult(
                markdown=f"Skipped zip file `{file_path}`: nested deeper than {max_depth} levels."
            )

        # Drop the metadata describing the outer *archive*, and pass the
        # current nesting depth down so nested zips are counted.
        member_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key not in ("file_extension", "url", "_zip_depth")
        }
        member_kwargs["_zip_depth"] = depth

        skipped = []
        total = 0
        with zipfile.ZipFile(file_stream, "r") as zipObj:
            entries = [e for e in zipObj.infolist() if not e.is_dir()]
            if len(entries) > max_entries:
                skipped.append(
                    f"{len(entries) - max_entries} files beyond the limit of {max_entries}"
                )
                entries = entries[:max_entries]

            for entry in entries:
                name = entry.filename
                remaining = max_total - total
                if remaining <= 0:
                    skipped.append(f"`{name}` (archive total limit reached)")
                    continue
                try:
                    data = _read_capped(zipObj, entry, min(max_entry, remaining))
                except _LimitExceeded:
                    skipped.append(f"`{name}` (too large once decompressed)")
                    continue
                except (zipfile.BadZipFile, RuntimeError, NotImplementedError):
                    # Corrupt, encrypted or unsupported compression
                    skipped.append(f"`{name}` (could not be read)")
                    continue
                total += len(data)
                try:
                    result = self._markitdown.convert_stream(
                        stream=io.BytesIO(data),
                        stream_info=StreamInfo(
                            extension=os.path.splitext(name)[1],
                            filename=os.path.basename(name),
                        ),
                        **member_kwargs,
                    )
                    if result is not None:
                        md_content += f"## File: {name}\n\n"
                        md_content += result.markdown + "\n\n"
                except UnsupportedFormatException:
                    pass
                except FileConversionException:
                    pass

        if skipped:
            md_content += "## Skipped\n\n" + "".join(f"- {s}\n" for s in skipped)

        return DocumentConverterResult(markdown=md_content.strip())
