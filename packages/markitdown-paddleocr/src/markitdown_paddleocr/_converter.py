"""PaddleOcr Converter - PDF/Image to Markdown using PaddleOCR cloud API."""

import io
import logging
import sys
from typing import Any, BinaryIO, Optional

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo
from markitdown._exceptions import (
    MISSING_DEPENDENCY_MESSAGE,
    MissingDependencyException,
)

from ._config import PaddleOcrConfig
from ._paddle_client import PaddleClient

# Import PDF dependencies
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
    "image/jpeg",
    "image/png",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]


logger = logging.getLogger(__name__)


class PaddleOcrConverter(DocumentConverter):
    """Intelligent PDF/Image converter using PaddleOCR cloud API.

    Features:
    - Auto-detect page content type (plain text vs images/tables)
    - Plain text pages use pdfplumber/pdfminer (fast, free)
    - Complex pages use PaddleOCR API for AI-powered OCR
    - Image files (PNG, JPG) use PaddleOCR API directly
    - Asynchronous job model: submit → poll → fetch result
    """

    def __init__(
        self,
        token: Optional[str] = None,
        model: str = "PaddleOCR-VL-1.5",
        poll_interval: float = 2.0,
        poll_timeout: float = 300.0,
        force_ai: bool = False,
        use_doc_orientation_classify: bool = False,
        use_doc_unwarping: bool = False,
        use_chart_recognition: bool = False,
        config: Optional[PaddleOcrConfig] = None,
    ):
        """Initialize converter.

        Args:
            token: Baidu PaddleOCR token (reads from BAIDU_PADDLE_TOKEN env var if not provided)
            model: OCR model name (default: PaddleOCR-VL-1.5)
            poll_interval: Seconds between status polls (default: 2.0)
            poll_timeout: Max seconds to wait for job completion (default: 300.0)
            force_ai: Force all pages to use OCR (default: False)
            use_doc_orientation_classify: Enable document orientation classification
            use_doc_unwarping: Enable document unwarping
            use_chart_recognition: Enable chart recognition
            config: Optional PaddleOcrConfig instance
        """
        # Build config from explicit params or provided config
        if config:
            self.token = token or config.token
            self.model = model if model != "PaddleOCR-VL-1.5" else config.model
            self.poll_interval = (
                poll_interval if poll_interval != 2.0 else config.poll_interval
            )
            self.poll_timeout = (
                poll_timeout if poll_timeout != 300.0 else config.poll_timeout
            )
            self.force_ai = force_ai or config.force_ai
            self.use_doc_orientation_classify = (
                use_doc_orientation_classify or config.use_doc_orientation_classify
            )
            self.use_doc_unwarping = use_doc_unwarping or config.use_doc_unwarping
            self.use_chart_recognition = (
                use_chart_recognition or config.use_chart_recognition
            )
        else:
            self.token = token
            self.model = model
            self.poll_interval = poll_interval
            self.poll_timeout = poll_timeout
            self.force_ai = force_ai
            self.use_doc_orientation_classify = use_doc_orientation_classify
            self.use_doc_unwarping = use_doc_unwarping
            self.use_chart_recognition = use_chart_recognition

        # Lazy init client
        self._client: Optional[PaddleClient] = None

    def _get_client(self) -> PaddleClient:
        """Get or create PaddleClient instance."""
        if self._client is None:
            config = PaddleOcrConfig(
                token=self.token or "",
                model=self.model,
                poll_interval=self.poll_interval,
                poll_timeout=self.poll_timeout,
                force_ai=self.force_ai,
                use_doc_orientation_classify=self.use_doc_orientation_classify,
                use_doc_unwarping=self.use_doc_unwarping,
                use_chart_recognition=self.use_chart_recognition,
            )
            self._client = PaddleClient(config=config)
        return self._client

    def _has_token(self) -> bool:
        """Check if a valid token is available."""
        if self.token:
            return True
        import os

        return bool(os.environ.get("BAIDU_PADDLE_TOKEN", ""))

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        # Without a token, PaddleOCR API cannot work — decline so other
        # converters (e.g. GlmOcrConverter) get a chance.
        if not self._has_token():
            return False

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
            ) from _dependency_exc_info[1].with_traceback(_dependency_exc_info[2])

        extension = (stream_info.extension or "").lower()

        logger.info("PaddleOcrConverter: 开始转换, 文件类型=%s", extension)

        # Image files: use PaddleOCR directly
        if extension in (".jpg", ".jpeg", ".png"):
            return self._convert_image(file_stream, extension)

        # PDF files: use hybrid approach
        return self._convert_pdf(file_stream)

    def _convert_image(
        self, file_stream: BinaryIO, extension: str = ".png"
    ) -> DocumentConverterResult:
        """Convert image file using PaddleOCR API."""
        img_bytes = file_stream.read()
        filename = f"image{extension}"

        logger.info("PaddleOcrConverter: 开始 OCR 识别图片, 格式=%s", extension)
        try:
            markdown = self._get_client().ocr(file_bytes=img_bytes, filename=filename)
        except Exception as e:
            logger.error(
                "PaddleOcrConverter: 图片 OCR 识别异常, 格式=%s, 错误=%s", extension, e
            )
            raise

        logger.info("PaddleOcrConverter: 图片 OCR 识别完成, 输出长度=%d", len(markdown))
        return DocumentConverterResult(markdown=markdown)

    def _convert_pdf(self, file_stream: BinaryIO) -> DocumentConverterResult:
        """Convert PDF using hybrid approach (pdfplumber for text, PaddleOCR for complex pages)."""
        pdf_stream = io.BytesIO(file_stream.read())
        markdown_parts = []
        ocr_failed = False

        try:
            with pdfplumber.open(pdf_stream) as pdf:
                total_pages = len(pdf.pages)
                logger.info("PaddleOcrConverter: 开始处理 PDF, 总页数=%d", total_pages)

                for page_num, page in enumerate(pdf.pages):
                    # Analyze page type
                    page_type = self._analyze_page(page)

                    # Choose processing method
                    if self.force_ai or page_type != "plain_text":
                        # Complex content: try PaddleOCR, fallback to pdfplumber on failure
                        logger.info(
                            "PaddleOcrConverter: 第 %d/%d 页, 类型=%s, 使用 PaddleOCR",
                            page_num + 1,
                            total_pages,
                            page_type,
                        )
                        try:
                            markdown = self._convert_with_paddleocr(page, page_num)
                        except Exception as e:
                            logger.warning(
                                "PaddleOcrConverter: 第 %d/%d 页 OCR 失败, 降级为 pdfplumber, 错误=%s",
                                page_num + 1,
                                total_pages,
                                e,
                            )
                            ocr_failed = True
                            markdown = self._extract_text_with_tables(page)
                    else:
                        # Plain text: use pdfplumber
                        logger.info(
                            "PaddleOcrConverter: 第 %d/%d 页, 类型=%s, 使用 pdfplumber",
                            page_num + 1,
                            total_pages,
                            page_type,
                        )
                        markdown = self._extract_text_with_tables(page)

                    if markdown.strip():
                        markdown_parts.append(f"## Page {page_num + 1}\n\n{markdown}")

                    page.close()

            markdown = "\n\n".join(markdown_parts).strip()

        except Exception as e:
            logger.error(
                "PaddleOcrConverter: PDF 处理异常, 降级为 pdfminer, 错误=%s", e
            )
            # Fallback to pdfminer
            pdf_stream.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_stream) or ""

        # Final fallback
        if not markdown:
            pdf_stream.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_stream) or ""

        # If OCR failed and result is empty, raise so the framework can try
        # the next converter (e.g. GlmOcrConverter) instead of returning empty.
        if ocr_failed and not markdown.strip():
            logger.error("PaddleOcrConverter: OCR 失败且所有兜底结果为空, 抛出异常")
            raise RuntimeError(
                "PaddleOcrConverter: OCR failed and all fallbacks returned empty"
            )

        logger.info("PaddleOcrConverter: PDF 转换完成, 输出长度=%d", len(markdown))
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

    def _convert_with_paddleocr(self, page: Any, page_num: int) -> str:
        """Convert page using PaddleOCR API."""
        # Render page to image
        img = page.to_image(resolution=150)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")

        logger.info("PaddleOcrConverter: PaddleOCR API 开始识别第 %d 页", page_num + 1)
        try:
            markdown = self._get_client().ocr(
                file_bytes=img_bytes.getvalue(),
                filename=f"page_{page_num + 1}.png",
            )
        except Exception as e:
            logger.error(
                "PaddleOcrConverter: PaddleOCR API 第 %d 页识别异常, 错误=%s",
                page_num + 1,
                e,
            )
            raise

        logger.info(
            "PaddleOcrConverter: PaddleOCR API 第 %d 页识别完成, 输出长度=%d",
            page_num + 1,
            len(markdown),
        )
        return markdown

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
            line = (
                "| "
                + " | ".join(
                    str(cell).ljust(width)
                    for cell, width in zip(padded_row, col_widths)
                )
                + " |"
            )
            lines.append(line)

            if row_idx == 0:
                sep = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
                lines.append(sep)

        return "\n".join(lines)

    def close(self):
        """Close the client."""
        self._client = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
