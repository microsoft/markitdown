# File: packages/markitdown/csv_converter.py

import csv
import io
from .document_converter import DocumentConverter, DocumentConverterResult

class CsvConverter(DocumentConverter):
    def accepts(self, stream_info):
        return (
            stream_info.extension == ".csv"
            or stream_info.mime_type in ["text/csv", "application/csv"]
        )

    def convert(self, stream_info):
        content = stream_info.read_text()
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

        if not rows:
            return DocumentConverterResult("")

        header = rows[0]
        table = []
        table.append("| " + " | ".join(header) + " |")
        table.append("| " + " | ".join(["---"] * len(header)) + " |")

        for row in rows[1:]:
            row += [""] * (len(header) - len(row))  # Pad missing cells
            table.append("| " + " | ".join(row[:len(header)]) + " |")

        markdown_output = "\n".join(table)
        return DocumentConverterResult(markdown_output)
