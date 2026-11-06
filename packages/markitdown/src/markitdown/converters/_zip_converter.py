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

# Safeguard limits for archive expansion. ZIP members are decompressed in
# memory, so an archive with a high compression ratio (a "zip bomb"), a very
# large member count, or deep archive-in-archive nesting can exhaust memory
# even when the archive file itself is small. The defaults below are set
# generously for legitimate document archives; every limit can be overridden
# per conversion via the matching ``zip_*`` keyword argument, or per
# converter instance via the constructor.
DEFAULT_MAX_MEMBER_SIZE = 100 * 1024 * 1024  # 100 MiB per member, uncompressed
DEFAULT_MAX_TOTAL_SIZE = 500 * 1024 * 1024  # 500 MiB per archive tree, uncompressed
DEFAULT_MAX_MEMBERS = 1000  # members per archive
DEFAULT_MAX_DEPTH = 5  # levels of archive-in-archive nesting


class ZipLimitExceededException(FileConversionException):
    """Raised when a ZIP archive breaches a ZipConverter safeguard limit.

    This is a hard failure, not a per-member skip: a limit breach means the
    archive as a whole is rejected. It subclasses FileConversionException so
    callers see the usual conversion-failure type, but ZipConverter
    deliberately re-raises it instead of swallowing it the way it swallows
    per-member conversion failures -- silently dropping the offending member
    would produce partial output that looks like a complete conversion.
    """


class _ZipBudget:
    """Shared uncompressed-byte budget for one archive tree.

    A single instance is created for the outermost archive and passed down
    through nested conversions, so the cumulative limit applies to the whole
    tree rather than resetting at each level of nesting.
    """

    def __init__(self, total_limit: int) -> None:
        self.total_limit = total_limit
        self.consumed = 0

    def consume(self, nbytes: int, *, member_name: str) -> None:
        self.consumed += nbytes
        if self.consumed > self.total_limit:
            raise ZipLimitExceededException(
                f"ZIP archive exceeds the cumulative uncompressed size limit "
                f"of {self.total_limit} bytes (breached at member "
                f"'{member_name}'). Raise zip_max_total_size to convert "
                f"larger archives."
            )


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
        max_member_size: int = DEFAULT_MAX_MEMBER_SIZE,
        max_total_size: int = DEFAULT_MAX_TOTAL_SIZE,
        max_members: int = DEFAULT_MAX_MEMBERS,
        max_depth: int = DEFAULT_MAX_DEPTH,
    ):
        super().__init__()
        self._markitdown = markitdown
        self._max_member_size = max_member_size
        self._max_total_size = max_total_size
        self._max_members = max_members
        self._max_depth = max_depth

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

        # Resolve the safeguard limits: per-conversion keyword arguments
        # override the converter-instance defaults.
        max_member_size = int(kwargs.get("zip_max_member_size", self._max_member_size))
        max_total_size = int(kwargs.get("zip_max_total_size", self._max_total_size))
        max_members = int(kwargs.get("zip_max_members", self._max_members))
        max_depth = int(kwargs.get("zip_max_depth", self._max_depth))

        # Nesting depth and the cumulative budget travel with the member
        # kwargs, so nested archives share the outermost archive's limits.
        depth = int(kwargs.get("_zip_depth", 0))
        if depth > max_depth:
            raise ZipLimitExceededException(
                f"ZIP archive nesting exceeds the maximum depth of "
                f"{max_depth}. Raise zip_max_depth to convert more deeply "
                f"nested archives."
            )
        budget = kwargs.get("_zip_budget")
        if budget is None:
            budget = _ZipBudget(max_total_size)

        # Drop the metadata describing the outer *archive*
        member_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key not in ("file_extension", "url")
        }
        member_kwargs["_zip_depth"] = depth + 1
        member_kwargs["_zip_budget"] = budget
        # Pin the resolved limits into the member kwargs so nested archives
        # enforce the same values, including limits set on this instance's
        # constructor rather than passed per call.
        member_kwargs["zip_max_member_size"] = max_member_size
        member_kwargs["zip_max_total_size"] = max_total_size
        member_kwargs["zip_max_members"] = max_members
        member_kwargs["zip_max_depth"] = max_depth

        with zipfile.ZipFile(file_stream, "r") as zipObj:
            entries = zipObj.infolist()
            if len(entries) > max_members:
                raise ZipLimitExceededException(
                    f"ZIP archive contains {len(entries)} members, exceeding "
                    f"the limit of {max_members}. Raise zip_max_members to "
                    f"convert archives with more members."
                )
            for entry in entries:
                name = entry.filename
                try:
                    if entry.is_dir():
                        continue
                    # Fast reject on the declared size, before decompressing.
                    if entry.file_size > max_member_size:
                        raise ZipLimitExceededException(
                            f"ZIP member '{name}' declares an uncompressed "
                            f"size of {entry.file_size} bytes, exceeding the "
                            f"limit of {max_member_size} bytes. Raise "
                            f"zip_max_member_size to convert larger members."
                        )
                    # Stream the member out instead of zipObj.read(), and
                    # count the bytes actually produced: a member whose
                    # header understates its size is still stopped.
                    chunks = []
                    member_size = 0
                    with zipObj.open(entry) as member_stream:
                        while True:
                            chunk = member_stream.read(1024 * 1024)
                            if not chunk:
                                break
                            member_size += len(chunk)
                            if member_size > max_member_size:
                                raise ZipLimitExceededException(
                                    f"ZIP member '{name}' exceeds the "
                                    f"uncompressed size limit of "
                                    f"{max_member_size} bytes while being "
                                    f"read. Raise zip_max_member_size to "
                                    f"convert larger members."
                                )
                            chunks.append(chunk)
                    budget.consume(member_size, member_name=name)
                    z_file_stream = io.BytesIO(b"".join(chunks))
                    z_file_stream_info = StreamInfo(
                        extension=os.path.splitext(name)[1],
                        filename=os.path.basename(name),
                    )
                    result = self._markitdown.convert_stream(
                        stream=z_file_stream,
                        stream_info=z_file_stream_info,
                        **member_kwargs,
                    )
                    if result is not None:
                        md_content += f"## File: {name}\n\n"
                        md_content += result.markdown + "\n\n"
                except UnsupportedFormatException:
                    pass
                except ZipLimitExceededException:
                    # A limit breach rejects the whole archive. It must not
                    # be swallowed like an ordinary per-member failure, or
                    # the caller would receive silently truncated output.
                    raise
                except FileConversionException as e:
                    # A breach in a NESTED archive reaches this loop wrapped
                    # in a plain FileConversionException, because
                    # MarkItDown._convert() aggregates converter failures
                    # into .attempts instead of propagating the original
                    # exception. Unwrap it: a breach anywhere in the tree
                    # rejects the whole archive, at every level.
                    if e.attempts and any(
                        attempt.exc_info is not None
                        and isinstance(attempt.exc_info[1], ZipLimitExceededException)
                        for attempt in e.attempts
                    ):
                        raise ZipLimitExceededException(
                            f"Nested archive member '{name}' breached a ZIP "
                            f"safeguard limit; rejecting the whole archive."
                        ) from e
                    pass

        return DocumentConverterResult(markdown=md_content.strip())
