"""GlmOcr PDF Converter - Intelligent PDF to Markdown conversion."""

import io
import sys
from typing import Any, BinaryIO, Optional

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo
from markitdown._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

from ._page_analyzer import PageType, analyze_page
from ._page_renderer import render_page_to_image
from ._ai_service import AIService

# Import dependencies
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


class GlmOcrPdfConverter(DocumentConverter):
    """
    Intelligent PDF converter using glm-ocr.
    
    Features:
    - Auto-detect page content type (plain text vs images/tables)
    - Plain text pages use default parser (pdfplumber/pdfminer)
    - Complex pages use AI screenshot conversion to Markdown
    """

    def __init__(
        self,
        ai_service: Optional[AIService] = None,
        dpi: int = 150,
        force_ai: bool = False,
    ):
        """
        Initialize converter.

        Args:
            ai_service: AI service instance
            dpi: Screenshot DPI (default: 150)
            force_ai: Force all pages to use AI (default: False)
        """
        self.ai_service = ai_service
        self.dpi = dpi
        self.force_ai = force_ai

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

        # Get AI service (from kwargs or instance)
        ai_service = kwargs.get("ai_service") or self.ai_service

        # Read PDF
        pdf_stream = io.BytesIO(file_stream.read())
        markdown_parts = []

        try:
            with pdfplumber.open(pdf_stream) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Analyze page type
                    page_type = analyze_page(page)

                    # Choose processing method based on type
                    if self.force_ai or page_type != PageType.PLAIN_TEXT:
                        # Complex content: screenshot + AI
                        if ai_service:
                            markdown = self._convert_with_ai(
                                page, page_num, ai_service
                            )
                        else:
                            # No AI service, fallback to default
                            markdown = self._extract_text_with_tables(page)
                    else:
                        # Plain text: default parser
                        markdown = self._extract_text_with_tables(page)

                    if markdown.strip():
                        markdown_parts.append(f"## Page {page_num + 1}\n\n{markdown}")

                    # Release page resources
                    page.close()

            markdown = "\n\n".join(markdown_parts).strip()

        except Exception:
            # Exception: fallback to pdfminer
            pdf_stream.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_stream) or ""

        # Final fallback
        if not markdown:
            pdf_stream.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_stream) or ""

        return DocumentConverterResult(markdown=markdown)

    def _convert_with_ai(
        self,
        page: Any,
        page_num: int,
        ai_service: AIService,
    ) -> str:
        """
        Convert page using AI.

        Args:
            page: pdfplumber page object
            page_num: Page number
            ai_service: AI service

        Returns:
            str: Markdown content
        """
        try:
            # Screenshot
            img_stream = render_page_to_image(page, self.dpi)

            # Call AI (filename uses page number)
            filename = f"page_{page_num + 1}.png"
            result = ai_service.image_to_markdown(img_stream, filename=filename)

            if result.success and result.text.strip():
                return result.text
            else:
                # AI failed, fallback to default
                return self._extract_text_with_tables(page)

        except Exception:
            # Exception, fallback to default
            return self._extract_text_with_tables(page)

    def _extract_text_with_tables(self, page: Any) -> str:
        """
        Extract text and tables.

        Args:
            page: pdfplumber page object

        Returns:
            str: Markdown content
        """
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
        """
        Convert table to Markdown.

        Args:
            table: 2D list

        Returns:
            str: Markdown table
        """
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
            # Pad columns
            padded_row = row + [""] * (len(col_widths) - len(row))
            line = "| " + " | ".join(
                str(cell).ljust(width) for cell, width in zip(padded_row, col_widths)
            ) + " |"
            lines.append(line)

            # Add separator
            if row_idx == 0:
                sep = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
                lines.append(sep)

        return "\n".join(lines)