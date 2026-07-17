import csv
import io
from typing import BinaryIO, Any
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

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
            data = file_stream.read()
            best_guess = from_bytes(data).best()
            if best_guess is not None:
                content = str(best_guess)
            else:
                # charset_normalizer could not classify the bytes; decode as
                # UTF-8 with replacement rather than stringifying None, which
                # would silently turn the document into the literal "None".
                content = data.decode("utf-8", errors="replace")

        # Parse CSV content
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

        if not rows:
            return DocumentConverterResult(markdown="")

        # Create markdown table
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

        return DocumentConverterResult(markdown=result)
