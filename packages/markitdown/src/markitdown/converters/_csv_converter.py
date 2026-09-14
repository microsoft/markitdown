import csv
import io
import re
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/csv",
    "application/csv",
]
ACCEPTED_FILE_EXTENSIONS = [".csv"]


# Matches a pipe together with the (possibly empty) run of backslashes in front
# of it, so that run can be doubled before the pipe is escaped.
# The lookbehind avoids retrying from each position inside a backslash run.
_PIPE_ESCAPE_RE = re.compile(r"(?<!\\)(\\*)\|")


def _escape_table_cell(value: str) -> str:
    r"""Escape a CSV value so it is safe inside a Markdown table cell.

    A pipe is a column separator, so it must be escaped.
    Line breaks would end the row early, so they collapse to a single space.
    """
    value = _PIPE_ESCAPE_RE.sub(lambda m: m.group(1) * 2 + r"\|", value)
    return value.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")


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


def _looks_like_delimited_csv(file_stream: BinaryIO) -> bool:
    """Return true when extensionless text has a real CSV-style delimiter."""
    cur_pos = file_stream.tell()
    try:
        data = file_stream.read(8192)
    finally:
        file_stream.seek(cur_pos)

    if not data:
        return False

    detected = from_bytes(data).best()
    content = str(detected) if detected is not None else data.decode("utf-8", "ignore")
    sample = content.lstrip("\ufeff")

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return False

    return dialect.delimiter in {",", ";", "\t", "|"}


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
                return _looks_like_delimited_csv(file_stream)
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
