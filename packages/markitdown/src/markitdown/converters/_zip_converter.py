import zipfile
import io
import os

from typing import BinaryIO, Any, Optional, TYPE_CHECKING

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


def _decode_zip_filename(
    entry: zipfile.ZipInfo,
    metadata_encoding: Optional[str] = None,
) -> str:
    """Decode a ZIP member filename, handling non-ASCII names when flag bit 11 is not set."""
    name = entry.filename
    # If bit 11 is set, Python's zipfile already decoded the filename as UTF-8
    if entry.flag_bits & 0x800:
        return name

    # When bit 11 is not set, zipfile decoded raw bytes as CP437.
    # Re-encode to recover the original raw bytes.
    try:
        raw_bytes = name.encode("cp437")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name

    # 1. Use explicit user/caller provided metadata encoding if given
    if metadata_encoding:
        try:
            return raw_bytes.decode(metadata_encoding)
        except (UnicodeDecodeError, LookupError):
            pass

    # 2. Try UTF-8 first (many archivers write UTF-8 bytes without setting bit 11)
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pass

    # 3. Use charset-normalizer to detect language/encoding
    try:
        from charset_normalizer import from_bytes

        matches = from_bytes(raw_bytes)
        best = matches.best()
        if best is not None:
            if best.encoding in ("cp932", "shift_jis"):
                return str(best)

            gb_match = next(
                (m for m in matches if m.encoding in ("gb18030", "gbk", "cp936")),
                None,
            )
            if gb_match is not None:
                if (
                    best.encoding in ("cp949", "johab")
                    and "CJK Unified Ideographs" in best.alphabets
                ):
                    return str(gb_match)
                if best.encoding in ("gb18030", "gbk", "cp936"):
                    return str(gb_match)

            return str(best)
    except (ValueError, TypeError, LookupError):
        pass

    # 4. Fallback common CJK encodings
    for enc in ("gb18030", "cp932", "big5"):
        try:
            return raw_bytes.decode(enc)
        except (UnicodeDecodeError, LookupError):
            pass

    return name


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

        # Drop the metadata describing the outer *archive*
        member_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key not in ("file_extension", "url")
        }

        with zipfile.ZipFile(file_stream, "r") as zipObj:
            for entry in zipObj.infolist():
                name = _decode_zip_filename(
                    entry,
                    metadata_encoding=kwargs.get("metadata_encoding"),
                )
                try:
                    z_file_stream = io.BytesIO(zipObj.read(entry))
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
                except FileConversionException:
                    pass

        return DocumentConverterResult(markdown=md_content.strip())
