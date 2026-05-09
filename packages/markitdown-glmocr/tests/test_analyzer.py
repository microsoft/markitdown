"""Tests for page analyzer."""

import pytest
from unittest.mock import MagicMock

from markitdown_glmocr._page_analyzer import (
    PageType,
    detect_images,
    detect_tables,
    analyze_page,
)


class TestDetectImages:
    """图片检测测试"""

    def test_no_images(self):
        """无图片页面"""
        page = MagicMock()
        page.images = []
        page.objects = {}

        assert detect_images(page) is False

    def test_has_images_via_images_attr(self):
        """通过 page.images 检测图片"""
        page = MagicMock()
        page.images = [MagicMock(x0=0, y0=0, x1=100, y1=100)]

        assert detect_images(page) is True

    def test_has_images_via_objects(self):
        """通过 page.objects 检测图片"""
        page = MagicMock()
        page.images = []
        page.objects = {"image": [MagicMock()]}

        assert detect_images(page) is True

    def test_has_xobject_image(self):
        """通过 XObject 检测图片"""
        page = MagicMock()
        page.images = []
        page.objects = {
            "xobject": [{"subtype": "Image"}]
        }

        assert detect_images(page) is True


class TestDetectTables:
    """表格检测测试"""

    def test_no_tables(self):
        """无表格页面"""
        page = MagicMock()
        page.extract_tables.return_value = []

        assert detect_tables(page) is False

    def test_has_tables_via_extract_tables(self):
        """通过 extract_tables 检测表格"""
        page = MagicMock()
        page.extract_tables.return_value = [
            [["A", "B", "C"], ["1", "2", "3"]]
        ]

        assert detect_tables(page) is True

    def test_empty_table_not_detected(self):
        """空表格不应被检测"""
        page = MagicMock()
        page.extract_tables.return_value = [
            [["", "", ""], ["", "", ""]]
        ]

        assert detect_tables(page) is False

    def test_has_table_lines(self):
        """通过线条检测表格"""
        page = MagicMock()
        page.extract_tables.return_value = []

        # 模拟网格线条
        lines = []
        for i in range(5):
            # 水平线
            lines.append({"height": 0.5, "width": 100})
            # 垂直线
            lines.append({"height": 100, "width": 0.5})

        page.objects = {"line": lines}

        assert detect_tables(page) is True


class TestAnalyzePage:
    """页面分析测试"""

    def test_plain_text_page(self):
        """纯文本页面"""
        page = MagicMock()
        page.images = []
        page.objects = {}
        page.extract_tables.return_value = []

        assert analyze_page(page) == PageType.PLAIN_TEXT

    def test_page_with_images(self):
        """仅包含图片"""
        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_tables.return_value = []

        assert analyze_page(page) == PageType.HAS_IMAGES

    def test_page_with_tables(self):
        """仅包含表格"""
        page = MagicMock()
        page.images = []
        page.extract_tables.return_value = [[["A", "B"]]]

        assert analyze_page(page) == PageType.HAS_TABLES

    def test_complex_page(self):
        """同时包含图片和表格"""
        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_tables.return_value = [[["A", "B"]]]

        assert analyze_page(page) == PageType.COMPLEX