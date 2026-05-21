"""Tests for scan detection optimization."""

import pytest
from unittest.mock import MagicMock, patch

from markitdown_paddleocr._config import PaddleOcrConfig, ScanDetectionMode
from markitdown_paddleocr._converter import PaddleOcrConverter


class TestScanDetectionMode:
    """扫描检测模式配置测试"""

    def test_default_mode_is_sampling(self):
        """默认模式应为 SAMPLING"""
        config = PaddleOcrConfig()
        assert config.scan_detection_mode == ScanDetectionMode.SAMPLING

    def test_custom_mode_from_config(self):
        """从配置对象读取自定义模式"""
        config = PaddleOcrConfig(scan_detection_mode=ScanDetectionMode.FIRST_PAGE_HINT)
        converter = PaddleOcrConverter(config=config, token="test_token")
        assert converter.scan_detection_mode == ScanDetectionMode.FIRST_PAGE_HINT

    def test_custom_mode_from_constructor(self):
        """从构造函数传入自定义模式"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.PAGE_BY_PAGE,
        )
        assert converter.scan_detection_mode == ScanDetectionMode.PAGE_BY_PAGE

    def test_constructor_overrides_config(self):
        """构造函数参数优先于配置对象"""
        config = PaddleOcrConfig(scan_detection_mode=ScanDetectionMode.FIRST_PAGE_HINT)
        converter = PaddleOcrConverter(
            config=config,
            token="test_token",
            scan_detection_mode=ScanDetectionMode.PAGE_BY_PAGE,
        )
        assert converter.scan_detection_mode == ScanDetectionMode.PAGE_BY_PAGE


class TestIsScannedPage:
    """扫描页面检测测试"""

    def test_page_without_images_not_scanned(self):
        """无图片的页面不是扫描件"""
        converter = PaddleOcrConverter(token="test_token")

        page = MagicMock()
        page.images = []
        page.extract_text.return_value = "Some text content here"

        assert converter._is_scanned_page(page) is False

    def test_page_with_images_and_text_not_scanned(self):
        """有图片但有足够文本的页面不是扫描件"""
        converter = PaddleOcrConverter(token="test_token", scan_text_threshold=50)

        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_text.return_value = "This is more than 50 characters of text content that should be extracted"

        assert converter._is_scanned_page(page) is False

    def test_page_with_images_no_text_is_scanned(self):
        """有图片但无文本的页面是扫描件"""
        converter = PaddleOcrConverter(token="test_token", scan_text_threshold=50)

        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_text.return_value = ""

        assert converter._is_scanned_page(page) is True

    def test_page_with_images_little_text_is_scanned(self):
        """有图片但文本少于阈值的页面是扫描件"""
        converter = PaddleOcrConverter(token="test_token", scan_text_threshold=50)

        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_text.return_value = "Short text"  # Only 10 chars

        assert converter._is_scanned_page(page) is True

    def test_text_extraction_error_assumes_scanned(self):
        """文本提取失败时假定是扫描件"""
        converter = PaddleOcrConverter(token="test_token")

        page = MagicMock()
        page.images = [MagicMock()]
        page.extract_text.side_effect = Exception("Extraction failed")

        assert converter._is_scanned_page(page) is True

    def test_custom_threshold(self):
        """自定义阈值生效"""
        converter = PaddleOcrConverter(token="test_token", scan_text_threshold=100)

        # Text below threshold
        page1 = MagicMock()
        page1.images = [MagicMock()]
        page1.extract_text.return_value = "This is exactly 50 characters"  # ~30 chars

        assert converter._is_scanned_page(page1) is True

        # Text above threshold
        page2 = MagicMock()
        page2.images = [MagicMock()]
        page2.extract_text.return_value = "This is definitely more than 100 characters of text content here for testing and verification purposes"  # 106 chars

        assert converter._is_scanned_page(page2) is False


class TestDetectAllScanned:
    """全文档扫描检测测试"""

    def test_page_by_page_mode_returns_false(self):
        """PAGE_BY_PAGE 模式永远返回 False"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.PAGE_BY_PAGE,
        )

        # Even with all scanned pages
        pdf = MagicMock()
        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""
        scanned_page.close = MagicMock()
        pdf.pages = [scanned_page, scanned_page, scanned_page]

        assert converter._detect_all_scanned(pdf) is False

    def test_first_page_hint_first_page_scanned(self):
        """FIRST_PAGE_HINT 模式，首页扫描则全文档扫描"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.FIRST_PAGE_HINT,
        )

        # First page scanned
        pdf = MagicMock()
        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""
        scanned_page.close = MagicMock()

        normal_page = MagicMock()
        normal_page.images = []
        normal_page.extract_text.return_value = "Normal text"

        pdf.pages = [scanned_page, normal_page, normal_page]

        assert converter._detect_all_scanned(pdf) is True

    def test_first_page_hint_first_page_not_scanned(self):
        """FIRST_PAGE_HINT 模式，首页非扫描则不判定全扫描"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.FIRST_PAGE_HINT,
        )

        # First page not scanned
        pdf = MagicMock()
        normal_page = MagicMock()
        normal_page.images = []
        normal_page.extract_text.return_value = "Normal text"

        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""

        pdf.pages = [normal_page, scanned_page, scanned_page]

        assert converter._detect_all_scanned(pdf) is False

    def test_sampling_mode_majority_scanned(self):
        """SAMPLING 模式，多数页面扫描则全文档扫描"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=3,
        )

        # 3 pages, 2 scanned, 1 normal -> majority scanned
        pdf = MagicMock()

        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""

        normal_page = MagicMock()
        normal_page.images = []
        normal_page.extract_text.return_value = "Normal text"

        pdf.pages = [scanned_page, scanned_page, normal_page]

        assert converter._detect_all_scanned(pdf) is True

    def test_sampling_mode_minority_scanned(self):
        """SAMPLING 模式，少数页面扫描则不判定全扫描"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=3,
        )

        # 3 pages, 1 scanned, 2 normal -> minority scanned
        pdf = MagicMock()

        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""

        normal_page = MagicMock()
        normal_page.images = []
        normal_page.extract_text.return_value = "Normal text"

        pdf.pages = [normal_page, normal_page, scanned_page]

        assert converter._detect_all_scanned(pdf) is False

    def test_sampling_mode_all_scanned(self):
        """SAMPLING 模式，所有抽样页扫描则全文档扫描"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=3,
        )

        pdf = MagicMock()
        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""

        pdf.pages = [scanned_page, scanned_page, scanned_page, scanned_page]

        assert converter._detect_all_scanned(pdf) is True

    def test_sampling_mode_custom_sample_count(self):
        """SAMPLING 模式，自定义抽样页数"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=5,
        )

        # 5 pages sampled, 3 scanned -> majority
        pdf = MagicMock()

        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""

        normal_page = MagicMock()
        normal_page.images = []
        normal_page.extract_text.return_value = "Normal text"

        pdf.pages = [scanned_page, scanned_page, scanned_page, normal_page, normal_page]

        assert converter._detect_all_scanned(pdf) is True

    def test_empty_pdf_returns_false(self):
        """空 PDF 返回 False"""
        converter = PaddleOcrConverter(token="test_token")

        pdf = MagicMock()
        pdf.pages = []

        assert converter._detect_all_scanned(pdf) is False

    def test_pdf_with_less_pages_than_sample_count(self):
        """PDF 页数少于抽样数时使用实际页数"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=5,
        )

        # Only 2 pages, both scanned -> majority
        pdf = MagicMock()
        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""

        pdf.pages = [scanned_page, scanned_page]

        assert converter._detect_all_scanned(pdf) is True


class TestConvertPdfWithScanDetection:
    """PDF 转换中的扫描检测集成测试"""

    def test_all_scanned_uses_batch_mode(self):
        """全扫描模式优先使用批量上传"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=3,
        )

        # Mock _detect_all_scanned to return True
        converter._detect_all_scanned = MagicMock(return_value=True)
        converter._convert_pdf_batch = MagicMock(return_value="Batch OCR result")
        converter._convert_with_paddleocr = MagicMock(return_value="Page OCR result")

        # Mock PDF
        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""
        scanned_page.close = MagicMock()

        pdf = MagicMock()
        pdf.pages = [scanned_page, scanned_page]

        with patch("markitdown_paddleocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = pdf

            import io
            stream = io.BytesIO(b"%PDF-1.4")
            result = converter._convert_pdf(stream)

        # Should call batch mode (1 API call)
        converter._convert_pdf_batch.assert_called_once()
        # Should NOT call per-page OCR
        converter._convert_with_paddleocr.assert_not_called()
        assert "Batch OCR result" in result.markdown

    def test_batch_failure_fallback_to_per_page(self):
        """批量OCR失败后降级为逐页处理"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=3,
        )

        # Mock _detect_all_scanned to return True
        converter._detect_all_scanned = MagicMock(return_value=True)
        converter._convert_pdf_batch = MagicMock(side_effect=RuntimeError("Batch API error"))
        converter._convert_with_paddleocr = MagicMock(return_value="Page OCR result")

        # Mock PDF
        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""
        scanned_page.close = MagicMock()

        pdf = MagicMock()
        pdf.pages = [scanned_page, scanned_page]

        with patch("markitdown_paddleocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = pdf

            import io
            stream = io.BytesIO(b"%PDF-1.4")
            result = converter._convert_pdf(stream)

        # Should have tried batch first
        converter._convert_pdf_batch.assert_called_once()
        # Should fall back to per-page OCR
        assert converter._convert_with_paddleocr.call_count == 2

    def test_all_scanned_skips_per_page_analysis(self):
        """全扫描模式跳过逐页分析"""
        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.SAMPLING,
            scan_sample_pages=3,
        )

        # Mock _detect_all_scanned to return True
        converter._detect_all_scanned = MagicMock(return_value=True)
        converter._convert_pdf_batch = MagicMock(return_value="Batch OCR result")
        converter._analyze_page = MagicMock(return_value="plain_text")

        # Mock PDF
        scanned_page = MagicMock()
        scanned_page.images = [MagicMock()]
        scanned_page.extract_text.return_value = ""
        scanned_page.close = MagicMock()

        pdf = MagicMock()
        pdf.pages = [scanned_page, scanned_page]

        with patch("markitdown_paddleocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = pdf

            import io
            stream = io.BytesIO(b"%PDF-1.4")
            result = converter._convert_pdf(stream)

        # Should call batch mode, not _analyze_page
        converter._convert_pdf_batch.assert_called_once()
        converter._analyze_page.assert_not_called()

    def test_page_by_page_mode_analyzes_each_page(self):
        """PAGE_BY_PAGE 模式分析每页"""

        converter = PaddleOcrConverter(
            token="test_token",
            scan_detection_mode=ScanDetectionMode.PAGE_BY_PAGE,
        )

        # Mock _analyze_page to return different results
        converter._analyze_page = MagicMock(side_effect=["plain_text", "complex"])
        converter._convert_with_paddleocr = MagicMock(return_value="OCR result")
        converter._extract_text_with_tables = MagicMock(return_value="Text result")

        # Mock PDF
        page1 = MagicMock()
        page1.close = MagicMock()
        page2 = MagicMock()
        page2.close = MagicMock()

        pdf = MagicMock()
        pdf.pages = [page1, page2]

        with patch("markitdown_paddleocr._converter.pdfplumber.open") as mock_open:
            mock_open.return_value.__enter__.return_value = pdf

            import io
            stream = io.BytesIO(b"%PDF-1.4")
            result = converter._convert_pdf(stream)

        # Should analyze each page
        assert converter._analyze_page.call_count == 2
        # Should use different methods for different pages
        converter._extract_text_with_tables.assert_called_once()
        converter._convert_with_paddleocr.assert_called_once()