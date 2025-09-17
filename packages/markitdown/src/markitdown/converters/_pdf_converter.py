import sys
import io
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Load dependencies
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


def _to_markdown_table(table: list[list[str]]) -> str:
    """Convert a 2D list (rows/columns) into a nicely aligned Markdown table."""
    if not table:
        return ""

    # Normalize None → ""
    table = [[cell if cell is not None else "" for cell in row] for row in table]

    # Column widths
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]

    def fmt_row(row):
        return "| " + " | ".join(
            str(cell).ljust(width) for cell, width in zip(row, col_widths)
        ) + " |"

    header, *rows = table
    md = [fmt_row(header)]
    md.append("| " + " | ".join("-" * w for w in col_widths) + " |")
    for row in rows:
        md.append(fmt_row(row))

    return "\n".join(md)


class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown.
    Supports extracting tables into aligned Markdown format (via pdfplumber).
    Falls back to pdfminer if pdfplumber is missing or fails.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(_dependency_exc_info[2])  # type: ignore[union-attr]

        assert isinstance(file_stream, io.IOBase)

        markdown_chunks: list[str] = []

        try:
            with pdfplumber.open(file_stream) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    page_tables = page.extract_tables()

                    # Remove table rows from text to avoid duplication
                    for table in page_tables:
                        if not table:
                            continue
                        header_line = " ".join(table[0])
                        if header_line in text:
                            text = text.replace(header_line, "")
                        for row in table[1:]:
                            row_line = " ".join(row)
                            if row_line in text:
                                text = text.replace(row_line, "")

                    # Normalize whitespace: collapse multiple blank lines
                    lines = [line.strip() for line in text.splitlines() if line.strip()]
                    clean_text = "\n".join(lines)
                    if clean_text:
                        markdown_chunks.append(clean_text)

                    # Append tables as aligned Markdown
                    for table in page_tables:
                        md_table = _to_markdown_table(table)
                        if md_table:
                            markdown_chunks.append(md_table)

            markdown = "\n\n".join(markdown_chunks).strip()

        except Exception:
            # Fallback if pdfplumber fails
            markdown = pdfminer.high_level.extract_text(file_stream)

        # Fallback if still empty
        if not markdown:
            markdown = pdfminer.high_level.extract_text(file_stream)

        return DocumentConverterResult(markdown=markdown)
