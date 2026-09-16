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


# The separators a spreadsheet actually writes into a file named ".csv".
# Excel writes the list separator of the machine's locale, which is a semicolon
# across most of Europe, and a tab-separated export is routinely saved as .csv.
_CANDIDATE_DELIMITERS = (",", ";", "\t")

# Some producers, Excel among them, write a "sep=" line ahead of the header to
# declare the separator. Excel honours it and hides the line.
_SEP_DIRECTIVE_RE = re.compile(r"^sep=(.)\r?\n", re.IGNORECASE)

# How much of the file the detection looks at. A separator that holds for the
# first rows holds for the file; reading all of a large export to decide would
# not change the answer.
_DETECTION_SAMPLE_CHARS = 64 * 1024
_DETECTION_SAMPLE_ROWS = 20


def _consistent_column_count(content: str, delimiter: str) -> int:
    """Columns per row under `delimiter`, or 0 when the rows disagree.

    A separator the file was not written with either does not occur at all (one
    column) or occurs by accident, and then the rows do not line up. Requiring
    the same count on every row is what keeps a comma inside a sentence from
    being read as a separator.
    """
    count = 0
    reader = csv.reader(io.StringIO(content, newline=""), delimiter=delimiter)
    for index, row in enumerate(reader):
        if index >= _DETECTION_SAMPLE_ROWS:
            break
        if not row:  # a blank line says nothing about the separator
            continue
        if count and len(row) != count:
            return 0
        count = len(row)
    return count if count > 1 else 0


def _detect_delimiter(content: str) -> str:
    """The separator the file was written with, defaulting to a comma.

    Parsing a semicolon-separated export with a comma does not fail -- it yields
    one column holding the whole row, separators and all.
    """
    sample = content[:_DETECTION_SAMPLE_CHARS]
    best_delimiter, best_columns = ",", 0
    for delimiter in _CANDIDATE_DELIMITERS:
        columns = _consistent_column_count(sample, delimiter)
        if columns > best_columns:
            best_delimiter, best_columns = delimiter, columns
    return best_delimiter


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

        # A "sep=" line declares the separator and is not part of the table.
        directive = _SEP_DIRECTIVE_RE.match(content)
        if directive:
            delimiter = directive.group(1)
            content = content[directive.end() :]
        else:
            delimiter = _detect_delimiter(content)

        # Parse CSV content
        reader = csv.reader(io.StringIO(content, newline=""), delimiter=delimiter)
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
