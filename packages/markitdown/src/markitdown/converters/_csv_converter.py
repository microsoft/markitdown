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
    "text/tsv"
]
ACCEPTED_FILE_EXTENSIONS = [".csv", ".tsv", ".psv", ".ssv"]


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
        
        SAMPLE_SNIFF_SIZE = 8192
        try:
            sample_chunk = content[:SAMPLE_SNIFF_SIZE]
        except IndexError:
            sample_chunk = content
            
        delimiter = self.get_delimiter(stream_info, kwargs.get("delimiter", ""), sample_chunk) # Option to specify delimiter.

        # Parse CSV content using the determined delimiter
        reader = csv.reader(io.StringIO(content), delimiter=delimiter) 
        rows = list(reader)

        if not rows:
            return DocumentConverterResult(markdown="")

        # Create markdown table
        markdown_table = []

        # Add header row
        safe_header = [self.sanitize_cell(cell) for cell in rows[0]]
        markdown_table.append("| " + " | ".join(safe_header) + " |")

        # Add separator row
        markdown_table.append("| " + " | ".join(["---"] * len(safe_header)) + " |")
        # Add data rows
        for row in rows[1:]:
            # Make sure row has the same number of columns as header
            while len(row) < len(safe_header):
                row.append("")
            # Truncate if row has more columns than header
            row = row[: len(safe_header)]
            markdown_table.append("| " + " | ".join([self.sanitize_cell(cell) for cell in row]) + " |")
        result = "\n".join(markdown_table)

        return DocumentConverterResult(markdown=result)
    
    # Determine the delimiter using the provided option, CSV sniffer, or file extension and MIME type as fallbacks.
    def get_delimiter(self, stream_info: StreamInfo, delimiter: str, sample_chunk: str) -> str:
        if delimiter:
            return delimiter
        try:
            dialect = csv.Sniffer().sniff(sample_chunk or "", delimiters=",\t|;")
            return dialect.delimiter
        except csv.Error:
            if stream_info.mimetype == "text/tab-separated-values" or stream_info.extension.lower() == ".tsv":
                return "\t"
            if stream_info.extension.lower() == ".psv":
                return "|"
            if stream_info.extension.lower() == ".ssv":
                return ";"
            return ","
        
    # makes sure to escape pipes and newlines in cell values to prevent breaking the markdown table format
    def sanitize_cell(self, cell_value: Any) -> str:
            val = str(cell_value)
            val = val.replace("|", "\\|")
            val = val.replace("\n", " ").replace("\r", "")
            return val
            