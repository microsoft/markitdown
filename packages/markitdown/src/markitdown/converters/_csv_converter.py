import csv
import io
import re
import warnings
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
_PIPE_ESCAPE_RE = re.compile(r"(\\*)\|")


def _escape_table_cell(value: str) -> str:
    r"""Escape a CSV value so it is safe inside a Markdown table cell.

    A pipe is a column separator, so it must be escaped.
    Line breaks would end the row early, so they collapse to a single space.
    """
    value = _PIPE_ESCAPE_RE.sub(lambda m: m.group(1) * 2 + r"\|", value)
    return value.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")


def _trim_outer_blank_rows(rows: list[list[str]]) -> None:
    """Remove empty rows from the beginning and end, and immediately after the header. This operation is performed in-place."""
    # Pop empty rows from the beginning
    while len(rows) > 0 and not rows[0]:
        rows.pop(0)

    # Pop empty rows after the header
    while len(rows) > 1 and not rows[1]:
        rows.pop(1)

    # Pop empty rows from the end
    while len(rows) > 0 and not rows[-1]:
        rows.pop(-1)


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

        # Excel and other tools prepend a UTF-8 BOM to CSV exports; strip it so
        # it does not end up inside the first header cell.
        content = content.lstrip("\ufeff")

        # Parse CSV content
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        _trim_outer_blank_rows(rows)

        if not rows:
            return DocumentConverterResult(markdown="")

        # Issue #2390: the first line is blindly treated as the header, so a
        # narrow preamble line (e.g. a one-field title/comment such as a
        # WizTree export banner) followed by a wider real header silently
        # discards every extra column. Detect that shape: a lone single-field
        # row followed by a wider row. The first line is then emitted as plain
        # text and the second line becomes the header.
        preamble: str | None = None
        if len(rows) >= 2 and len(rows[0]) == 1 and len(rows[1]) > 1:
            preamble = rows[0][0].strip()
            warnings.warn(
                "CSV first row has a single field while the second row has "
                f"{len(rows[1])} fields; treating the first row as a "
                "preamble and using the second row as the header."
            )
            rows = rows[1:]

        # Issue #2390 (core fix): never silently drop columns. Widen the
        # table to the widest row instead of truncating data rows to the
        # header width, and warn so the mismatch is visible.
        max_width = max(len(row) for row in rows)
        if max_width > len(rows[0]):
            warnings.warn(
                f"CSV column count mismatch: header has {len(rows[0])} "
                f"column(s) but the widest row has {max_width}; "
                "expanding the table instead of truncating data."
            )

        # Create markdown table
        markdown_table = []

        if preamble:
            markdown_table.append(preamble)
            markdown_table.append("")

        # Add header row (padded to the widest row so no data is lost)
        header = [_escape_table_cell(cell) for cell in rows[0]]
        header += [""] * (max_width - len(header))
        markdown_table.append("| " + " | ".join(header) + " |")

        # Add separator row
        markdown_table.append("| " + " | ".join(["---"] * max_width) + " |")

        # Add data rows
        for row in rows[1:]:
            # Work on a copy to avoid mutating the parsed rows in place
            row = list(row)
            # Pad short rows so every row has the same width
            while len(row) < max_width:
                row.append("")
            # No truncation: max_width is the widest row, so all fields kept
            row = row[:max_width]
            markdown_table.append(
                "| " + " | ".join(_escape_table_cell(cell) for cell in row) + " |"
            )

        result = "\n".join(markdown_table)

        return DocumentConverterResult(markdown=result)
