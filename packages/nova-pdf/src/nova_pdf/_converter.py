"""Nova PDF Converter - Intelligent PDF to Markdown conversion."""

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


class NovaPdfConverter(DocumentConverter):
    """
    智能 PDF 转换器
    
    特性：
    - 自动检测每页内容类型（纯文本 vs 包含图片/表格）
    - 纯文本页面使用默认解析（pdfplumber/pdfminer）
    - 复杂页面截图后调用 AI 转换为 Markdown
    """

    def __init__(
        self,
        ai_service: Optional[AIService] = None,
        dpi: int = 150,
        force_ai: bool = False,
    ):
        """
        初始化转换器

        Args:
            ai_service: AI 服务实例
            dpi: 截图分辨率（默认 150）
            force_ai: 强制所有页面使用 AI（默认 False）
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

        # 获取 AI 服务（从 kwargs 或实例）
        ai_service = kwargs.get("ai_service") or self.ai_service

        # 读取 PDF
        pdf_stream = io.BytesIO(file_stream.read())
        markdown_parts = []

        try:
            with pdfplumber.open(pdf_stream) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # 分析页面类型
                    page_type = analyze_page(page)

                    # 根据类型选择处理方式
                    if self.force_ai or page_type != PageType.PLAIN_TEXT:
                        # 复杂内容：截图 + AI
                        if ai_service:
                            markdown = self._convert_with_ai(
                                page, page_num, ai_service
                            )
                        else:
                            # 无 AI 服务，回退到默认解析
                            markdown = self._extract_text_with_tables(page)
                    else:
                        # 纯文本：默认解析
                        markdown = self._extract_text_with_tables(page)

                    if markdown.strip():
                        markdown_parts.append(f"## Page {page_num + 1}\n\n{markdown}")

                    # 释放页面资源
                    page.close()

            markdown = "\n\n".join(markdown_parts).strip()

        except Exception:
            # 异常情况：回退到 pdfminer
            pdf_stream.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_stream) or ""

        # 最终回退
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
        使用 AI 转换页面

        Args:
            page: pdfplumber 页面对象
            page_num: 页码
            ai_service: AI 服务

        Returns:
            str: Markdown 内容
        """
        try:
            # 截图
            img_stream = render_page_to_image(page, self.dpi)

            # 调用 AI（文件名使用页码）
            filename = f"page_{page_num + 1}.png"
            result = ai_service.image_to_markdown(img_stream, filename=filename)

            if result.success and result.text.strip():
                return result.text
            else:
                # AI 失败，回退到默认解析
                return self._extract_text_with_tables(page)

        except Exception:
            # 异常情况，回退到默认解析
            return self._extract_text_with_tables(page)

    def _extract_text_with_tables(self, page: Any) -> str:
        """
        提取文本和表格

        Args:
            page: pdfplumber 页面对象

        Returns:
            str: Markdown 内容
        """
        parts = []

        # 提取文本
        text = page.extract_text() or ""
        if text.strip():
            parts.append(text.strip())

        # 提取表格
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
        将表格转换为 Markdown

        Args:
            table: 2D 列表

        Returns:
            str: Markdown 表格
        """
        if not table:
            return ""

        # 过滤 None 值
        table = [[cell if cell is not None else "" for cell in row] for row in table]

        # 过滤空行
        table = [row for row in table if any(cell.strip() for cell in row)]

        if not table:
            return ""

        # 计算列宽
        col_widths = [
            max(len(str(row[i])) if i < len(row) else 0 for row in table)
            for i in range(max(len(row) for row in table))
        ]

        # 格式化表格
        lines = []
        for row_idx, row in enumerate(table):
            # 补齐列数
            padded_row = row + [""] * (len(col_widths) - len(row))
            line = "| " + " | ".join(
                str(cell).ljust(width) for cell, width in zip(padded_row, col_widths)
            ) + " |"
            lines.append(line)

            # 添加分隔行
            if row_idx == 0:
                sep = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
                lines.append(sep)

        return "\n".join(lines)
