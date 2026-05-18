import csv
import io
import logging
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import FileConversionException

logger = logging.getLogger(__name__)

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/csv",
    "application/csv",
]
ACCEPTED_FILE_EXTENSIONS = [".csv"]


class CsvConverter(DocumentConverter):
    """
    Converts CSV files to Markdown tables.
    """

    def __init__(self):
        super().__init__()

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
        # Read the file content
        try:
            raw_bytes = file_stream.read()
            if not raw_bytes:
                return DocumentConverterResult(markdown="")
            if stream_info.charset:
                content = raw_bytes.decode(stream_info.charset)
            else:
                content = str(from_bytes(raw_bytes).best())
        except (UnicodeDecodeError, LookupError) as e:
            logger.warning("CSV encoding detection failed: %s", e)
            raise FileConversionException(
                f"CsvConverter: unable to decode file with charset={stream_info.charset}: {e}"
            ) from e

        # Parse CSV content
        try:
            reader = csv.reader(io.StringIO(content))
            rows = list(reader)
        except csv.Error as e:
            logger.warning("CSV parsing failed: %s", e)
            raise FileConversionException(
                f"CsvConverter: malformed CSV content: {e}"
            ) from e

        if not rows:
            return DocumentConverterResult(markdown="")

        # Create markdown table
        try:
            markdown_table = []

            # Add header row
            markdown_table.append("| " + " | ".join(rows[0]) + " |")

            # Add separator row
            markdown_table.append("| " + " | ".join(["---"] * len(rows[0])) + " |")

            # Add data rows
            for row in rows[1:]:
                # Make sure row has the same number of columns as header
                while len(row) < len(rows[0]):
                    row.append("")
                # Truncate if row has more columns than header
                row = row[: len(rows[0])]
                markdown_table.append("| " + " | ".join(row) + " |")

            result = "\n".join(markdown_table)
        except (IndexError, TypeError) as e:
            logger.warning("CSV table generation failed: %s", e)
            raise FileConversionException(
                f"CsvConverter: unable to generate table from CSV: {e}"
            ) from e

        return DocumentConverterResult(markdown=result)
