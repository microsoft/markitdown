import io
import re
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException

try:
    import pdfplumber
except ImportError as e:
    raise MissingDependencyException(
        "PDF conversion with layout support requires: pip install 'markitdown[pdf]'"
    ) from e

ACCEPTED_MIME_TYPE_PREFIXES = ["application/pdf", "application/x-pdf"]
ACCEPTED_FILE_EXTENSIONS = [".pdf"]


class PdfConverter(DocumentConverter):
    def accepts(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()
        return extension in ACCEPTED_FILE_EXTENSIONS or any(
            mimetype.startswith(prefix) for prefix in ACCEPTED_MIME_TYPE_PREFIXES
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        remove_headers_footers: bool = True,   # We turn this ON by default!
        **kwargs: Any,
    ) -> DocumentConverterResult:
        assert isinstance(file_stream, io.IOBase)

        file_stream.seek(0)  # Important: reset stream position
        with pdfplumber.open(file_stream) as pdf:
            pages_text = []

            # === Smart header/footer detection (only on multi-page docs) ===
            header = footer = None
            if remove_headers_footers and len(pdf.pages) > 3:
                top_lines = {}
                bottom_lines = {}
                sample_pages = pdf.pages[:min(20, len(pdf.pages))]
                for page in sample_pages:
                    lines = page.extract_text_lines() or []
                    if not lines:
                        continue
                    top_text = lines[0]["text"].strip()
                    bottom_text = lines[-1]["text"].strip()
                    top_lines[top_text] = top_lines.get(top_text, 0) + 1
                    bottom_lines[bottom_text] = bottom_lines.get(bottom_text, 0) + 1

                if top_lines:
                    header = max(top_lines, key=top_lines.get) if max(top_lines.values()) > 2 else None
                if bottom_lines:
                    footer = max(bottom_lines, key=bottom_lines.get) if max(bottom_lines.values()) > 2 else None

            # Common page number patterns
            page_number_re = re.compile(
                r"^\s*\d+\s*$|^Page\s*\d+.*|^-\s*\d+\s*-$|^\d+\s+of\s+\d+$"
            )

            for page in pdf.pages:
                lines = page.extract_text_lines() or []
                clean = []

                for line in lines:
                    text = line["text"].rstrip()
                    if not text.strip():
                        continue

                    skip = False
                    if remove_headers_footers:
                        # Remove detected header/footer
                        if text.strip() == header or text.strip() == footer:
                            skip = True
                        # Remove obvious page numbers
                        elif page_number_re.match(text.strip()):
                            skip = True
                        # Remove by position (top/bottom 8% of page)
                        elif line["top"] < page.height * 0.08 or line["top"] > page.height * 0.92:
                            skip = True

                    if not skip:
                        clean.append(text)

                page_text = "\n".join(clean).strip()
                if page_text:
                    pages_text.append(page_text)

            final_markdown = "\n\n---\n\n".join(pages_text) if pages_text else "No text extracted."
            return DocumentConverterResult(markdown=final_markdown)
