import csv
import io
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/csv",
    "application/csv",
    "text/tab-separated-values",
    "text/tsv",
]
ACCEPTED_FILE_EXTENSIONS = [".csv", ".tsv"]

SNIFF_SAMPLE_SIZE = 8192


class CsvConverter(DocumentConverter):
    """
    Converts CSV and TSV files to Markdown tables.
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

        # Auto-detect the delimiter
        extension = (stream_info.extension or "").lower()
        delimiter = self._detect_delimiter(content, extension)

        # Parse content
        reader = csv.reader(io.StringIO(content), delimiter=delimiter)
        rows = list(reader)

        if not rows:
            return DocumentConverterResult(markdown="")

        # Create markdown table
        markdown_table = []

        # Add header row (with pipe escaping)
        header = [self._escape_cell(cell) for cell in rows[0]]
        markdown_table.append("| " + " | ".join(header) + " |")

        # Add separator row
        markdown_table.append("| " + " | ".join(["---"] * len(rows[0])) + " |")

        # Add data rows
        for row in rows[1:]:
            # Make sure row has the same number of columns as header
            while len(row) < len(rows[0]):
                row.append("")
            # Truncate if row has more columns than header
            row = row[: len(rows[0])]
            escaped = [self._escape_cell(cell) for cell in row]
            markdown_table.append("| " + " | ".join(escaped) + " |")

        result = "\n".join(markdown_table)

        return DocumentConverterResult(markdown=result)

    def _detect_delimiter(self, content: str, extension: str) -> str:
        """Auto-detect the delimiter using csv.Sniffer, with sensible fallbacks."""
        try:
            sample = content[:SNIFF_SAMPLE_SIZE]
            dialect = csv.Sniffer().sniff(sample)
            return dialect.delimiter
        except csv.Error:
            if extension == ".tsv":
                return "\t"
            return ","

    def _escape_cell(self, cell: str) -> str:
        """Escape characters that would break a Markdown table."""
        return cell.replace("|", "\\|").replace("\n", " ").replace("\r", "")
