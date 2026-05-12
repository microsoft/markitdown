"""GlmOcr PDF/Image Converter - Intelligent PDF and Image to Markdown conversion."""

import io
import sys
from typing import Any, BinaryIO, Optional

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo
from markitdown._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

from ._config import GlmOcrConfig

# Import dependencies
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()

# glmocr SDK
try:
    import glmocr
    from glmocr import GlmOcr
except ImportError:
    glmocr = None
    GlmOcr = None


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
    "image/jpeg",
    "image/png",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]


class GlmOcrConverter(DocumentConverter):
    """
    Intelligent PDF/Image converter using glmocr SDK.
    
    Features:
    - Auto-detect page content type (plain text vs images/tables)
    - Plain text pages use pdfplumber/pdfminer (fast, free)
    - Complex pages use glmocr SDK for AI-powered OCR
    - Image files (PNG, JPG) use glmocr SDK directly
    - One-liner: glmocr.parse("document.pdf") handles everything
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 1800,
        enable_layout: bool = False,
        force_ai: bool = False,
        config: Optional[GlmOcrConfig] = None,
    ):
        """
        Initialize converter.

        Args:
            api_key: Zhipu API key (reads from ZHIPU_API_KEY env var if not provided)
            timeout: Request timeout in seconds (default: 1800)
            enable_layout: Enable layout detection (default: False)
            force_ai: Force all pages to use AI (default: False)
            config: Optional GlmOcrConfig instance
        """
        if glmocr is None:
            raise ImportError(
                "glmocr is required. Install with: pip install markitdown-glmocr[glmocr]"
            )
        
        # Use config if provided
        if config:
            self.api_key = api_key or config.api_key
            self.timeout = timeout if timeout != 1800 else config.timeout
            self.enable_layout = enable_layout if enable_layout else config.enable_layout
            self.force_ai = force_ai or config.force_ai
        else:
            self.api_key = api_key
            self.timeout = timeout
            self.enable_layout = enable_layout
            self.force_ai = force_ai
        
        # Lazy init GlmOcr instance
        self._glmocr: Optional[GlmOcr] = None

    def _get_glmocr(self) -> GlmOcr:
        """Get or create GlmOcr instance."""
        if self._glmocr is None:
            kwargs = {"timeout": self.timeout, "enable_layout": self.enable_layout}
            if self.api_key:
                kwargs["api_key"] = self.api_key
            self._glmocr = GlmOcr(**kwargs)
        return self._glmocr

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
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )

        extension = (stream_info.extension or "").lower()

        # Image files: use glmocr directly
        if extension in (".jpg", ".jpeg", ".png"):
            return self._convert_image(file_stream, extension)

        # PDF files: use hybrid approach
        return self._convert_pdf(file_stream)

    def _convert_image(self, file_stream: BinaryIO, extension: str = ".png") -> DocumentConverterResult:
        """Convert image file using glmocr SDK."""
        img_bytes = file_stream.read()

        try:
            result = self._get_glmocr().parse(img_bytes)

            # Check for errors
            d = result.to_dict()
            if "error" in d:
                return DocumentConverterResult(markdown="")

            return DocumentConverterResult(
                markdown=result.markdown_result or ""
            )
        except Exception as e:
            return DocumentConverterResult(
                markdown=f"<!-- Error converting image: {e} -->"
            )

    def _convert_pdf(self, file_stream: BinaryIO) -> DocumentConverterResult:
        pdf_stream = io.BytesIO(file_stream.read())
        markdown_parts = []

        try:
            with pdfplumber.open(pdf_stream) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Analyze page type
                    page_type = self._analyze_page(page)

                    # Choose processing method
                    if self.force_ai or page_type != "plain_text":
                        # Complex content: use glmocr
                        markdown = self._convert_with_glmocr(page, page_num)
                    else:
                        # Plain text: use pdfplumber
                        markdown = self._extract_text_with_tables(page)

                    if markdown.strip():
                        markdown_parts.append(f"## Page {page_num + 1}\n\n{markdown}")

                    page.close()

            markdown = "\n\n".join(markdown_parts).strip()

        except Exception:
            # Fallback to pdfminer
            pdf_stream.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_stream) or ""

        # Final fallback
        if not markdown:
            pdf_stream.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_stream) or ""

        return DocumentConverterResult(markdown=markdown)

    def _analyze_page(self, page: Any) -> str:
        """Analyze page content type."""
        # Check for images
        if hasattr(page, "images") and page.images:
            return "complex"
        
        # Check for tables
        tables = page.find_tables()
        if tables:
            return "complex"
        
        # Check for graphics/curves
        if hasattr(page, "curves") and page.curves:
            return "complex"
        
        return "plain_text"

    def _convert_with_glmocr(self, page: Any, page_num: int) -> str:
        """Convert page using glmocr SDK."""
        try:
            # Render page to image
            img = page.to_image(resolution=150)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            result = self._get_glmocr().parse(img_bytes.getvalue())
            
            # Check for errors
            d = result.to_dict()
            if "error" in d:
                return self._extract_text_with_tables(page)
            
            return result.markdown_result or ""
            
        except Exception:
            return self._extract_text_with_tables(page)

    def _extract_text_with_tables(self, page: Any) -> str:
        """Extract text and tables from page."""
        parts = []

        # Extract text
        text = page.extract_text() or ""
        if text.strip():
            parts.append(text.strip())

        # Extract tables
        try:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table:
                        md_table = self._table_to_markdown(table)
                        if md_table.strip():
                            parts.append(md_table)
        except Exception:
            pass

        return "\n\n".join(parts)

    def _table_to_markdown(self, table: list[list[str]]) -> str:
        """Convert table to Markdown."""
        if not table:
            return ""

        # Filter None values
        table = [[cell if cell is not None else "" for cell in row] for row in table]

        # Filter empty rows
        table = [row for row in table if any(cell.strip() for cell in row)]

        if not table:
            return ""

        # Calculate column widths
        col_widths = [
            max(len(str(row[i])) if i < len(row) else 0 for row in table)
            for i in range(max(len(row) for row in table))
        ]

        # Format table
        lines = []
        for row_idx, row in enumerate(table):
            padded_row = row + [""] * (len(col_widths) - len(row))
            line = "| " + " | ".join(
                str(cell).ljust(width) for cell, width in zip(padded_row, col_widths)
            ) + " |"
            lines.append(line)

            if row_idx == 0:
                sep = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
                lines.append(sep)

        return "\n".join(lines)
    
    def close(self):
        """Close the GlmOcr instance."""
        if self._glmocr:
            self._glmocr.close()
            self._glmocr = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()