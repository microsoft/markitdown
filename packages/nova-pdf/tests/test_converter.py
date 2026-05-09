"""Tests for nova-pdf converter."""

import io
import pytest
from unittest.mock import MagicMock, patch

from nova_pdf._converter import NovaPdfConverter
from nova_pdf._ai_service import AIService, AIResult
from nova_pdf._page_analyzer import PageType


class TestNovaPdfConverter:
    """转换器测试"""

    def test_accepts_pdf_extension(self):
        """接受 .pdf 扩展名"""
        converter = NovaPdfConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=".pdf", mimetype=None)

        assert converter.accepts(stream, stream_info) is True

    def test_accepts_pdf_mimetype(self):
        """接受 PDF MIME 类型"""
        converter = NovaPdfConverter()
        stream = io.BytesIO(b"%PDF-1.4")
        stream_info = MagicMock(extension=None, mimetype="application/pdf")

        assert converter.accepts(stream, stream_info) is True

    def test_rejects_non_pdf(self):
        """拒绝非 PDF 文件"""
        converter = NovaPdfConverter()
        stream = io.BytesIO(b"not a pdf")
        stream_info = MagicMock(extension=".txt", mimetype="text/plain")

        assert converter.accepts(stream, stream_info) is False

    def test_table_to_markdown(self):
        """表格转 Markdown"""
        converter = NovaPdfConverter()
        table = [
            ["Name", "Age", "City"],
            ["Alice", "25", "Beijing"],
            ["Bob", "30", "Shanghai"],
        ]

        result = converter._table_to_markdown(table)
        
        assert "|" in result
        assert "Name" in result
        assert "Alice" in result
        assert "---" in result  # 分隔行

    def test_plain_text_page_without_ai(self):
        """纯文本页面不使用 AI"""
        converter = NovaPdfConverter()

        # 模拟页面
        page = MagicMock()
        page.images = []
        page.objects = {}
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Hello World"
        page.close = MagicMock()

        # 模拟 PDF
        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("nova_pdf._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        assert "Hello World" in result.markdown

    def test_complex_page_with_ai(self):
        """复杂页面使用 AI"""
        # 模拟 AI 服务
        ai_service = MagicMock(spec=AIService)
        ai_service.image_to_markdown.return_value = AIResult(
            success=True,
            text="# AI Generated\n\nThis is from AI."
        )

        converter = NovaPdfConverter(ai_service=ai_service)

        # 模拟页面
        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Plain text"
        page.to_image.return_value.original = MagicMock()
        page.close = MagicMock()

        # 模拟图片保存
        img_stream = io.BytesIO()
        page.to_image.return_value.original.save = lambda s, format: s.write(b"fake")

        # 模拟 PDF
        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("nova_pdf._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        # 应该调用 AI
        ai_service.image_to_markdown.assert_called_once()
        assert "AI Generated" in result.markdown

    def test_force_ai_mode(self):
        """强制 AI 模式"""
        ai_service = MagicMock(spec=AIService)
        ai_service.image_to_markdown.return_value = AIResult(
            success=True,
            text="AI result"
        )

        converter = NovaPdfConverter(ai_service=ai_service, force_ai=True)

        # 即使是纯文本页面
        page = MagicMock()
        page.images = []
        page.objects = {}
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Plain text"
        page.to_image.return_value.original = MagicMock()
        page.close = MagicMock()

        img_stream = io.BytesIO()
        page.to_image.return_value.original.save = lambda s, format: s.write(b"fake")

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("nova_pdf._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        # 应该调用 AI（因为 force_ai=True）
        ai_service.image_to_markdown.assert_called_once()

    def test_fallback_on_ai_failure(self):
        """AI 失败时回退到默认解析"""
        ai_service = MagicMock(spec=AIService)
        ai_service.image_to_markdown.return_value = AIResult(
            success=False,
            text="",
            error="API error"
        )

        converter = NovaPdfConverter(ai_service=ai_service)

        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_tables.return_value = []
        page.extract_text.return_value = "Fallback text"
        page.to_image.return_value.original = MagicMock()
        page.close = MagicMock()

        img_stream = io.BytesIO()
        page.to_image.return_value.original.save = lambda s, format: s.write(b"fake")

        mock_pdf = MagicMock()
        mock_pdf.pages = [page]

        with patch("nova_pdf._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = mock_pdf

            stream = io.BytesIO(b"%PDF-1.4")
            result = converter.convert(stream, MagicMock())

        # 应该回退到默认文本
        assert "Fallback text" in result.markdown
