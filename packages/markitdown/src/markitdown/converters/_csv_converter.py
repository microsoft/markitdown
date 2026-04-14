import csv
import io
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo


def _escape_cell(value: str) -> str:
    """Escape pipe characters and strip newlines inside CSV cells to keep Markdown table valid."""
    # Replace literal pipe chars to avoid breaking table columns
    value = value.replace("|", "\\|")
    # Collapse newlines to a space so single-cell multi-line values don't break rows
    value = value.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    return value

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
        if stream_info.charset:
            content = file_stream.read().decode(stream_info.charset)
        else:
            content = str(from_bytes(file_stream.read()).best())

        # Parse CSV content
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

        if not rows:
            return DocumentConverterResult(markdown="")

        # Create markdown table
        markdown_table = []

        # Determine column count from header
        col_count = len(rows[0])

        # Add header row (escape special chars)
        markdown_table.append("| " + " | ".join(_escape_cell(c) for c in rows[0]) + " |")

        # Add separator row
        markdown_table.append("| " + " | ".join(["---"] * col_count) + " |")

        # Add data rows
        for row in rows[1:]:
            # Make sure row has the same number of columns as header
            while len(row) < col_count:
                row.append("")
            # Truncate if row has more columns than header
            row = row[:col_count]
            markdown_table.append("| " + " | ".join(_escape_cell(c) for c in row) + " |")

        result = "\n".join(markdown_table)

        return DocumentConverterResult(markdown=result)
