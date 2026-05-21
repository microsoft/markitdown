"""GlmOcr PDF/Image Converter - Intelligent PDF and Image to Markdown conversion."""

import io
import logging
import sys
from typing import Any, BinaryIO, Optional

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo
from markitdown._exceptions import (
    MISSING_DEPENDENCY_MESSAGE,
    MissingDependencyException,
)

from ._config import GlmOcrConfig, ScanDetectionMode

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


logger = logging.getLogger(__name__)


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
        scan_detection_mode: Optional[ScanDetectionMode] = None,
        scan_sample_pages: Optional[int] = None,
        scan_text_threshold: Optional[int] = None,
        config: Optional[GlmOcrConfig] = None,
    ):
        """
        Initialize converter.

        Args:
            api_key: Zhipu API key (reads from ZHIPU_API_KEY env var if not provided)
            timeout: Request timeout in seconds (default: 1800)
            enable_layout: Enable layout detection (default: False)
            force_ai: Force all pages to use AI (default: False)
            scan_detection_mode: 扫描检测模式，优化扫描PDF处理
            scan_sample_pages: SAMPLING模式下抽样页数 (default: 3)
            scan_text_threshold: 判定为扫描件的最小文本长度阈值 (default: 50)
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
            self.enable_layout = (
                enable_layout if enable_layout else config.enable_layout
            )
            self.force_ai = force_ai or config.force_ai
            self.scan_detection_mode = (
                scan_detection_mode
                if scan_detection_mode is not None
                else config.scan_detection_mode
            )
            self.scan_sample_pages = (
                scan_sample_pages
                if scan_sample_pages is not None
                else config.scan_sample_pages
            )
            self.scan_text_threshold = (
                scan_text_threshold
                if scan_text_threshold is not None
                else config.scan_text_threshold
            )
        else:
            self.api_key = api_key
            self.timeout = timeout
            self.enable_layout = enable_layout
            self.force_ai = force_ai
            self.scan_detection_mode = (
                scan_detection_mode
                if scan_detection_mode is not None
                else ScanDetectionMode.SAMPLING
            )
            self.scan_sample_pages = scan_sample_pages if scan_sample_pages is not None else 3
            self.scan_text_threshold = (
                scan_text_threshold if scan_text_threshold is not None else 50
            )

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
            ) from _dependency_exc_info[1].with_traceback(_dependency_exc_info[2])

        extension = (stream_info.extension or "").lower()

        logger.info("GlmOcrConverter: 开始转换, 文件类型=%s", extension)

        # Image files: use glmocr directly
        if extension in (".jpg", ".jpeg", ".png"):
            return self._convert_image(file_stream, extension)

        # PDF files: use hybrid approach
        return self._convert_pdf(file_stream)

    def _convert_image(
        self, file_stream: BinaryIO, extension: str = ".png"
    ) -> DocumentConverterResult:
        """Convert image file using glmocr SDK."""
        img_bytes = file_stream.read()

        logger.info("GlmOcrConverter: 开始 OCR 识别图片, 格式=%s", extension)
        try:
            result = self._get_glmocr().parse(img_bytes)
        except Exception as e:
            logger.error(
                "GlmOcrConverter: 图片 OCR 识别异常, 格式=%s, 错误=%s", extension, e
            )
            raise

        # Check for errors
        d = result.to_dict()
        if "error" in d:
            logger.error(
                "GlmOcrConverter: 图片 OCR 返回错误, 格式=%s, 错误=%s",
                extension,
                d["error"],
            )
            raise RuntimeError(
                f"GlmOcrConverter: glmocr SDK returned error: {d['error']}"
            )

        markdown = result.markdown_result or ""
        logger.info("GlmOcrConverter: 图片 OCR 识别完成, 输出长度=%d", len(markdown))
        return DocumentConverterResult(markdown=markdown)

    def _convert_pdf(self, file_stream: BinaryIO) -> DocumentConverterResult:
        pdf_stream = io.BytesIO(file_stream.read())
        pdf_bytes = pdf_stream.getvalue()  # Keep original bytes for batch OCR
        markdown_parts = []

        with pdfplumber.open(pdf_stream) as pdf:
            total_pages = len(pdf.pages)
            logger.info("GlmOcrConverter: 开始处理 PDF, 总页数=%d", total_pages)

            # Optimization: detect if entire PDF is scanned
            all_scanned = self._detect_all_scanned(pdf)

            if all_scanned and not self.force_ai:
                # Batch mode: upload entire PDF to glmocr SDK (single API call)
                logger.info(
                    "GlmOcrConverter: 全文档扫描模式, 批量上传PDF, 页数=%d",
                    total_pages,
                )
                try:
                    markdown = self._convert_pdf_batch(pdf_bytes)
                    if markdown.strip():
                        logger.info(
                            "GlmOcrConverter: 批量OCR完成, 输出长度=%d",
                            len(markdown),
                        )
                        return DocumentConverterResult(markdown=markdown)
                except Exception as e:
                    logger.warning(
                        "GlmOcrConverter: 批量OCR失败, 降级为逐页处理, 错误=%s",
                        e,
                    )
                    # Fall through to per-page processing

            # Per-page processing (PAGE_BY_PAGE mode or batch failed)
            for page_num, page in enumerate(pdf.pages):
                # Choose processing method
                if self.force_ai or all_scanned:
                    # All scanned (after batch failed) or force_ai
                    logger.info(
                        "GlmOcrConverter: 第 %d/%d 页, 使用 glmocr OCR",
                        page_num + 1,
                        total_pages,
                    )
                    try:
                        markdown = self._convert_with_glmocr(page, page_num)
                    except Exception as e:
                        logger.error(
                            "GlmOcrConverter: 第 %d/%d 页识别异常, 错误=%s",
                            page_num + 1,
                            e,
                        )
                        raise
                else:
                    # Per-page analysis (PAGE_BY_PAGE mode or non-scanned doc)
                    page_type = self._analyze_page(page)

                    if page_type != "plain_text":
                        logger.info(
                            "GlmOcrConverter: 第 %d/%d 页, 类型=%s, 使用 glmocr OCR",
                            page_num + 1,
                            total_pages,
                            page_type,
                        )
                        try:
                            markdown = self._convert_with_glmocr(page, page_num)
                        except Exception as e:
                            logger.error(
                                "GlmOcrConverter: 第 %d/%d 页识别异常, 错误=%s",
                                page_num + 1,
                                e,
                            )
                            raise
                    else:
                        logger.info(
                            "GlmOcrConverter: 第 %d/%d 页, 类型=%s, 使用 pdfplumber",
                            page_num + 1,
                            total_pages,
                            page_type,
                        )
                        markdown = self._extract_text_with_tables(page)

                if markdown.strip():
                    markdown_parts.append(f"## Page {page_num + 1}\n\n{markdown}")

                page.close()

        markdown = "\n\n".join(markdown_parts).strip()
        logger.info("GlmOcrConverter: PDF 转换完成, 输出长度=%d", len(markdown))
        return DocumentConverterResult(markdown=markdown)

    def _convert_pdf_batch(self, pdf_bytes: bytes) -> str:
        """Convert entire PDF in a single API call.

        More efficient for scanned PDFs: one API call instead of N calls for N pages.

        Args:
            pdf_bytes: Raw PDF file content.

        Returns:
            Markdown text from all pages.
        """
        logger.info("GlmOcrConverter: 批量上传PDF到glmocr SDK, 大小=%d bytes", len(pdf_bytes))
        result = self._get_glmocr().parse(pdf_bytes)

        # Check for errors
        d = result.to_dict()
        if "error" in d:
            logger.error(
                "GlmOcrConverter: 批量OCR返回错误, 错误=%s",
                d["error"],
            )
            raise RuntimeError(
                f"GlmOcrConverter: glmocr SDK batch OCR error: {d['error']}"
            )

        markdown = result.markdown_result or ""
        return markdown

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

    def _is_scanned_page(self, page: Any) -> bool:
        """Check if a page is likely a scanned image.

        A page is considered scanned if:
        1. It contains images, AND
        2. It has very little extractable text (below threshold)

        Args:
            page: pdfplumber page object

        Returns:
            True if the page appears to be a scanned image
        """
        # Must have images to be a scan
        has_images = hasattr(page, "images") and bool(page.images)
        if not has_images:
            return False

        # Check extractable text length
        try:
            text = page.extract_text() or ""
            text_len = len(text.strip())
            # If there's substantial text, it might be a mixed page or
            # a digital PDF with embedded images
            if text_len >= self.scan_text_threshold:
                return False
        except Exception:
            # If text extraction fails, assume it's a scan
            return True

        return True

    def _detect_all_scanned(self, pdf: Any) -> bool:
        """Detect if entire PDF is scanned based on scan_detection_mode.

        Optimization: When first few pages are scanned, we can assume
        all pages are scanned and skip per-page analysis.

        Args:
            pdf: pdfplumber PDF object

        Returns:
            True if entire PDF should be treated as scanned
        """
        if self.scan_detection_mode == ScanDetectionMode.PAGE_BY_PAGE:
            return False

        total_pages = len(pdf.pages)
        if total_pages == 0:
            return False

        if self.scan_detection_mode == ScanDetectionMode.FIRST_PAGE_HINT:
            # Check only first page
            first_page = pdf.pages[0]
            is_scanned = self._is_scanned_page(first_page)
            first_page.close()
            if is_scanned:
                logger.info(
                    "GlmOcrConverter: 首页检测为扫描件, 模式=FIRST_PAGE_HINT, 全文档使用OCR"
                )
            return is_scanned

        if self.scan_detection_mode == ScanDetectionMode.SAMPLING:
            # Sample first N pages
            sample_count = min(self.scan_sample_pages, total_pages)
            scanned_count = 0

            for i in range(sample_count):
                page = pdf.pages[i]
                if self._is_scanned_page(page):
                    scanned_count += 1

            # If majority of sampled pages are scanned, treat all as scanned
            majority_threshold = sample_count // 2 + 1
            all_scanned = scanned_count >= majority_threshold

            if all_scanned:
                logger.info(
                    "GlmOcrConverter: 抽样检测 %d/%d 页为扫描件, 模式=SAMPLING, 全文档使用OCR",
                    scanned_count,
                    sample_count,
                )

            return all_scanned

        return False

    def _convert_with_glmocr(self, page: Any, page_num: int) -> str:
        """Convert page using glmocr SDK.

        Raises RuntimeError on OCR failure so the framework can try the next converter.
        """
        # Render page to image
        img = page.to_image(resolution=150)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")

        logger.info("GlmOcrConverter: glmocr SDK 开始识别第 %d 页", page_num + 1)
        try:
            result = self._get_glmocr().parse(img_bytes.getvalue())
        except Exception as e:
            logger.error(
                "GlmOcrConverter: glmocr SDK 第 %d 页识别异常, 错误=%s", page_num + 1, e
            )
            raise

        # Check for errors
        d = result.to_dict()
        if "error" in d:
            logger.error(
                "GlmOcrConverter: glmocr SDK 第 %d 页返回错误, 错误=%s",
                page_num + 1,
                d["error"],
            )
            raise RuntimeError(
                f"GlmOcrConverter: glmocr SDK returned error on page {page_num + 1}: {d['error']}"
            )

        markdown = result.markdown_result or ""
        logger.info(
            "GlmOcrConverter: glmocr SDK 第 %d 页识别完成, 输出长度=%d",
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
        """Close the GlmOcr instance."""
        if self._glmocr:
            self._glmocr.close()
            self._glmocr = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
