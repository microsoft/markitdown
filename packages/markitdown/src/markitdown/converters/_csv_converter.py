import csv
import io
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ..converter_utils._markdown import _escape_table_cell

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/csv",
    "application/csv",
]
ACCEPTED_FILE_EXTENSIONS = [".csv"]


def _trim_outer_blank_rows(rows: list[list[str]]) -> None:
    """Remove empty rows from the beginning and end, and immediately after the header. This operation is performed in-place."""
    start = 0
    while start < len(rows) and not rows[start]:
        start += 1

    if start == len(rows):
        rows.clear()
        return

    header_index = start
    start += 1
    while start < len(rows) and not rows[start]:
        start += 1

    end = len(rows)
    while end > start and not rows[end - 1]:
        end -= 1

    # Remove each blank run at once, rather than shifting the list per row.
    del rows[end:]
    del rows[header_index + 1 : start]
    del rows[:header_index]


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
            data = file_stream.read()
            detected = from_bytes(data).best()
            content = (
                str(detected)
                if detected is not None
                else data.decode("utf-8", errors="ignore")
            )

        # Excel and other tools prepend a UTF-8 BOM to CSV exports; strip it so
        # it does not end up inside the first header cell.
        content = content.lstrip("\ufeff")

        # Parse CSV content
        reader = csv.reader(io.StringIO(content, newline=""))
        rows = list(reader)
        _trim_outer_blank_rows(rows)

        if not rows:
            return DocumentConverterResult(markdown="")

        # Pad all rows, including the header, to preserve the widest row.
        num_columns = max(len(row) for row in rows)
        for row in rows:
            row.extend([""] * (num_columns - len(row)))

        # Create markdown table
        markdown_table = []

        # Add header row
        header = [_escape_table_cell(cell) for cell in rows[0]]
        markdown_table.append("| " + " | ".join(header) + " |")

        # Add separator row
        markdown_table.append("| " + " | ".join(["---"] * num_columns) + " |")

        # Add data rows
        for row in rows[1:]:
            markdown_table.append(
                "| " + " | ".join(_escape_table_cell(cell) for cell in row) + " |"
            )

        result = "\n".join(markdown_table)

        return DocumentConverterResult(markdown=result)
