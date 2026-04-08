#!/usr/bin/env python3 -m pytest
"""Tests for PDF converter memory optimization.

Verifies that:
- page.close() is called after processing each page (frees cached data)
- Plain-text PDFs fall back to pdfminer when no form pages are found
- Mixed PDFs use form extraction only on form-style pages
- Memory stays constant regardless of page count
"""

import gc
import io
import os
import tracemalloc

import pytest
from unittest.mock import patch, MagicMock

from markitdown import MarkItDown

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


def _has_fpdf2() -> bool:
    try:
        import fpdf  # noqa: F401

        return True
    except ImportError:
        return False


def _make_form_page():
    """Create a mock page with 3-column table-like word positions."""
    page = MagicMock()
    page.width = 612
    page.close = MagicMock()
    page.extract_words.return_value = [
        {"text": "Name", "x0": 50, "x1": 100, "top": 10, "bottom": 20},
        {"text": "Value", "x0": 250, "x1": 300, "top": 10, "bottom": 20},
        {"text": "Unit", "x0": 450, "x1": 500, "top": 10, "bottom": 20},
        {"text": "Alpha", "x0": 50, "x1": 100, "top": 30, "bottom": 40},
        {"text": "100", "x0": 250, "x1": 280, "top": 30, "bottom": 40},
        {"text": "kg", "x0": 450, "x1": 470, "top": 30, "bottom": 40},
        {"text": "Beta", "x0": 50, "x1": 100, "top": 50, "bottom": 60},
        {"text": "200", "x0": 250, "x1": 280, "top": 50, "bottom": 60},
        {"text": "lb", "x0": 450, "x1": 470, "top": 50, "bottom": 60},
    ]
    return page


def _make_plain_page():
    """Create a mock page with single-line paragraph (no table structure)."""
    page = MagicMock()
    page.width = 612
    page.close = MagicMock()
    page.extract_words.return_value = [
        {
            "text": "This is a long paragraph of plain text.",
            "x0": 50,
            "x1": 550,
            "top": 10,
            "bottom": 20,
        },
    ]
    page.extract_text.return_value = "This is a long paragraph of plain text."
    return page


def _mock_pdfplumber_open(pages):
    """Return a mock pdfplumber.open that yields the given pages."""

    def mock_open(stream):
        mock_pdf = MagicMock()
        mock_pdf.pages = pages
        mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
        mock_pdf.__exit__ = MagicMock(return_value=False)
        return mock_pdf

    return mock_open


class TestPdfMemoryOptimization:
    """Test that PDF conversion cleans up per-page caches to limit memory."""

    def test_page_close_called_on_every_page(self):
        """Verify page.close() is called on every page during conversion.

        This ensures cached word/layout data is freed after each page,
        preventing O(n) memory growth with page count.
        """
        num_pages = 20
        pages = [_make_form_page() for _ in range(num_pages)]

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(pages)

            md = MarkItDown()
            buf = io.BytesIO(b"fake pdf content")
            from markitdown import StreamInfo

            md.convert_stream(
                buf,
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        # page.close() must be called on ALL pages
        for i, page in enumerate(pages):
            assert page.close.called, (
                f"page.close() was NOT called on page {i} — "
                "this would cause memory to accumulate"
            )

    def test_plain_text_pdf_falls_back_to_pdfminer(self):
        """Verify all-plain-text PDFs fall back to pdfminer.

        When no page has form-style content, the converter should discard
        pdfplumber results and use pdfminer for the whole document (better
        text spacing for prose).
        """
        num_pages = 50
        pages = [_make_plain_page() for _ in range(num_pages)]

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber, patch(
            "markitdown.converters._pdf_converter.pdfminer"
        ) as mock_pdfminer:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(pages)
            mock_pdfminer.high_level.extract_text.return_value = "Plain text content"

            md = MarkItDown()
            buf = io.BytesIO(b"fake pdf content")
            from markitdown import StreamInfo

            result = md.convert_stream(
                buf,
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        # pdfminer should be used for the final text extraction
        assert mock_pdfminer.high_level.extract_text.called, (
            "pdfminer.high_level.extract_text was not called — "
            "plain-text PDFs should fall back to pdfminer"
        )
        assert result.text_content is not None

    def test_plain_text_pdf_still_closes_all_pages(self):
        """Even for plain-text PDFs, page.close() must be called on every page."""
        num_pages = 30
        pages = [_make_plain_page() for _ in range(num_pages)]

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber, patch(
            "markitdown.converters._pdf_converter.pdfminer"
        ) as mock_pdfminer:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(pages)
            mock_pdfminer.high_level.extract_text.return_value = "text"

            md = MarkItDown()
            buf = io.BytesIO(b"fake pdf content")
            from markitdown import StreamInfo

            md.convert_stream(
                buf,
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        for i, page in enumerate(pages):
            assert (
                page.close.called
            ), f"page.close() was NOT called on plain-text page {i}"

    def test_mixed_pdf_uses_form_extraction_per_page(self):
        """In a mixed PDF, form pages get table extraction while plain pages don't.

        Ensures we don't miss form-style pages and don't waste work
        running form extraction on plain-text pages.
        """
        # Pages 0,2,4 are form-style; pages 1,3 are plain text
        pages = [
            _make_form_page(),  # 0 - form
            _make_plain_page(),  # 1 - plain
            _make_form_page(),  # 2 - form
            _make_plain_page(),  # 3 - plain
            _make_form_page(),  # 4 - form
        ]

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(pages)

            md = MarkItDown()
            buf = io.BytesIO(b"fake pdf content")
            from markitdown import StreamInfo

            result = md.convert_stream(
                buf,
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        # All pages should have close() called
        for i, page in enumerate(pages):
            assert page.close.called, f"page.close() not called on page {i}"

        # Form pages (0,2,4) should have extract_words called
        for i in [0, 2, 4]:
            assert pages[
                i
            ].extract_words.called, f"extract_words not called on form page {i}"

        # Result should contain table content from form pages
        assert result.text_content is not None
        assert (
            "|" in result.text_content
        ), "Expected markdown table pipes in output from form-style pages"

    def test_only_one_pdfplumber_open_call(self):
        """Verify pdfplumber.open is called exactly once (single pass)."""
        pages = [_make_form_page() for _ in range(10)]

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(pages)

            md = MarkItDown()
            buf = io.BytesIO(b"fake pdf content")
            from markitdown import StreamInfo

            md.convert_stream(
                buf,
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        assert mock_pdfplumber.open.call_count == 1, (
            f"Expected 1 pdfplumber.open call (single pass), "
            f"got {mock_pdfplumber.open.call_count}"
        )

    @pytest.mark.skipif(
        not os.path.exists(os.path.join(TEST_FILES_DIR, "test.pdf")),
        reason="test.pdf not available",
    )
    def test_real_pdf_page_cleanup(self):
        """Integration test: verify page.close() is called with a real PDF."""
        import pdfplumber

        close_call_count = 0
        original_close = pdfplumber.page.Page.close

        def tracking_close(self):
            nonlocal close_call_count
            close_call_count += 1
            original_close(self)

        with patch.object(pdfplumber.page.Page, "close", tracking_close):
            md = MarkItDown()
            pdf_path = os.path.join(TEST_FILES_DIR, "test.pdf")
            md.convert(pdf_path)

        assert (
            close_call_count > 0
        ), "page.close() was never called during PDF conversion"


def _generate_table_pdf(num_pages: int) -> bytes:
    """Generate a PDF with table-like content on every page."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    for page_num in range(num_pages):
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)
        pdf.set_xy(10, 10)
        pdf.cell(60, 8, "Parameter", border=1)
        pdf.cell(60, 8, "Value", border=1)
        pdf.cell(60, 8, "Unit", border=1)
        pdf.ln()
        for row in range(20):
            y = 18 + row * 8
            if y > 270:
                break
            pdf.set_xy(10, y)
            pdf.cell(60, 8, f"Param_{page_num}_{row}", border=1)
            pdf.cell(60, 8, f"{(page_num * 100 + row) * 1.23:.2f}", border=1)
            pdf.cell(60, 8, "kg/m2", border=1)
    return pdf.output()


@pytest.mark.skipif(
    not _has_fpdf2(),
    reason="fpdf2 not installed",
)
class TestPdfMemoryBenchmark:
    """Benchmark: verify memory stays constant with page.close() fix."""

    def test_memory_does_not_grow_linearly(self):
        """Peak memory for 200 pages should be far less than without the fix.

        Without page.close(), 200 pages uses ~225 MiB (linear growth).
        With the fix, peak memory should stay under 30 MiB.
        """
        from markitdown import StreamInfo

        num_pages = 200
        pdf_bytes = _generate_table_pdf(num_pages)

        gc.collect()
        tracemalloc.start()

        md = MarkItDown()
        buf = io.BytesIO(pdf_bytes)
        md.convert_stream(buf, stream_info=StreamInfo(extension=".pdf"))

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_mib = peak / 1024 / 1024
        # Without the fix this would be ~225 MiB. With the fix it should
        # be well under 30 MiB. Use a generous threshold to avoid flaky
        # failures on different machines.
        assert peak_mib < 30, (
            f"Peak memory {peak_mib:.1f} MiB for {num_pages} pages is too high. "
            f"Expected < 30 MiB with page.close() fix."
        )

    def test_memory_constant_across_page_counts(self):
        """Peak memory should not scale linearly with page count.

        Converts 50-page and 200-page PDFs and asserts the peak memory
        ratio is much less than the 4x page count ratio.
        """
        from markitdown import StreamInfo

        results = {}
        for num_pages in [50, 200]:
            pdf_bytes = _generate_table_pdf(num_pages)

            gc.collect()
            tracemalloc.start()

            md = MarkItDown()
            buf = io.BytesIO(pdf_bytes)
            md.convert_stream(buf, stream_info=StreamInfo(extension=".pdf"))

            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            results[num_pages] = peak

        ratio = results[200] / results[50]
        # With O(n) memory growth the ratio would be ~4x.
        # With the fix it should be close to 1x (well under 2x).
        assert ratio < 2.0, (
            f"Memory ratio 200p/50p = {ratio:.2f}x — "
            f"expected < 2.0x (constant memory). "
            f"50p={results[50] / 1024 / 1024:.1f} MiB, "
            f"200p={results[200] / 1024 / 1024:.1f} MiB"
        )
