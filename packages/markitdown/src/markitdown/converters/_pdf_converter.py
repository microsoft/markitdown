import sys
import io
from typing import BinaryIO, Any, List, Optional


from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE


# pdfminer is required for basic PDF text extraction
_dependency_exc_info = None  # Holds exception info if pdfminer missing
try:  # pragma: no cover - dependency import
    import pdfminer  # type: ignore
    import pdfminer.high_level  # type: ignore
except ImportError:  # pragma: no cover
    _dependency_exc_info = sys.exc_info()

# Optional: pdfplumber for table extraction
try:  # pragma: no cover - optional dependency
    import pdfplumber  # type: ignore
    _pdfplumber_available = True
except Exception:  # pragma: no cover
    _pdfplumber_available = False

# Optional: camelot for table extraction (only works on stream-based pages or lattice with ghostscript)
try:  # pragma: no cover - optional dependency
    import camelot  # type: ignore
    _camelot_available = True
except Exception:  # pragma: no cover
    _camelot_available = False


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


def _format_md_table(rows: List[List[Optional[str]]]) -> str:
    """Render a 2D list into GitHub-flavored markdown table.

    Very small formatting helper: left-align all columns, normalize None/whitespace.
    """
    if not rows:
        return ""
    norm = [[(c or "").strip() for c in r] for r in rows]
    # Drop completely empty trailing rows that sometimes appear from extractors
    while len(norm) > 1 and all(len(c) == 0 for c in norm[-1]):
        norm.pop()
    if not norm or len(norm[0]) == 0:
        return ""
    widths = [max(len(r[i]) for r in norm) for i in range(len(norm[0]))]

    def fmt_row(r: List[str]) -> str:
        return "| " + " | ".join(r[i].ljust(widths[i]) for i in range(len(widths))) + " |"

    header = fmt_row(norm[0])
    separator = "| " + " | ".join("-" * max(3, widths[i]) for i in range(len(widths))) + " |"
    body = [fmt_row(r) for r in norm[1:]]
    # Ensure at least header + separator; if only one row, duplicate header as a body row copy
    if len(body) == 0:
        body.append(fmt_row(["" for _ in widths]))
    return "\n".join([header, separator, *body])


class PdfConverter(DocumentConverter):
    """Convert PDFs to Markdown.

    Table extraction (when enabled) is best-effort and relies on optional dependencies:
    - pdfplumber: generic table detection using pdfminer layout analysis
    - camelot: stronger detection for ruling-line (lattice) or stream tables

    Modes (selectable via kwarg `pdf_tables` passed through from CLI):
        none (default): Plain text via pdfminer
        plumber: Use pdfplumber only
        camelot: Use camelot only
        auto: Try pdfplumber first, then camelot, else fallback
    """

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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Dependency check for baseline pdfminer
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__, extension=".pdf", feature="pdf"
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        mode = (kwargs.get("pdf_tables") or "none").lower()
        if mode not in {"none", "auto", "plumber", "camelot"}:
            mode = "none"

        # Ensure we can seek back after optional libs consume the stream
        if not file_stream.seekable():
            # Should normally be seekable by the time we get here, but safeguard
            buffer = io.BytesIO(file_stream.read())
            file_stream = buffer
        cur_pos = file_stream.tell()

        extracted_tables: List[str] = []
        body_chunks: List[str] = []

        def append_tables(tables: List[List[List[Optional[str]]]]):
            for t in tables:
                md = _format_md_table(t)
                if md.strip():
                    extracted_tables.append(md)

        tried_any = False

        # Try pdfplumber if requested/auto
        if mode in {"plumber", "auto"} and _pdfplumber_available:
            tried_any = True
            try:  # pragma: no cover - logic covered indirectly
                file_stream.seek(cur_pos)
                with pdfplumber.open(file_stream) as pdf:  # type: ignore
                    for page in pdf.pages:
                        page_text = page.extract_text() or ""
                        tables = page.extract_tables() or []
                        if page_text.strip():
                            body_chunks.append(page_text.rstrip())
                        if tables:
                            append_tables(tables)  # type: ignore[arg-type]
                # Success path: combine text + tables appended in order encountered
                if extracted_tables:
                    markdown = "\n\n".join(
                        [c for c in body_chunks if c] + extracted_tables
                    )
                else:
                    markdown = "\n\n".join([c for c in body_chunks if c])
                if markdown.strip():
                    return DocumentConverterResult(markdown=markdown)
            except Exception:
                # Swallow and fall through to other options
                pass

        # Try camelot if requested/auto
        if mode in {"camelot", "auto"} and _camelot_available:
            tried_any = True
            try:  # pragma: no cover - optional dependency path
                file_stream.seek(cur_pos)
                # Camelot expects a file path; if we have a local_path in stream_info use it
                if stream_info.local_path:
                    # Try both lattice then stream to maximize recall
                    tables_all: List[Any] = []
                    try:
                        tables_all.extend(camelot.read_pdf(stream_info.local_path, pages="all", flavor="lattice"))  # type: ignore
                    except Exception:
                        pass
                    try:
                        tables_all.extend(camelot.read_pdf(stream_info.local_path, pages="all", flavor="stream"))  # type: ignore
                    except Exception:
                        pass
                    for tbl in tables_all:
                        try:
                            data = tbl.df.values.tolist()  # pandas DataFrame
                            append_tables(data)  # type: ignore[arg-type]
                        except Exception:
                            continue
                    if extracted_tables:
                        # Fallback body text via pdfminer
                        file_stream.seek(cur_pos)
                        plain = pdfminer.high_level.extract_text(file_stream)
                        markdown = plain.strip()
                        markdown = "\n\n".join(
                            [markdown] + [t for t in extracted_tables if t]
                        )
                        return DocumentConverterResult(markdown=markdown)
            except Exception:
                pass

        # Final fallback to plain pdfminer text
        file_stream.seek(cur_pos)
        plain_text = pdfminer.high_level.extract_text(file_stream)
        if tried_any and extracted_tables:
            plain_text = "\n\n".join([plain_text.strip()] + extracted_tables)
        return DocumentConverterResult(markdown=plain_text)
