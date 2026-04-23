#!/usr/bin/env python3 -m pytest
"""Tests for PDF heading detection via font-size analysis."""

import io
import pytest

from markitdown.converters._pdf_converter import _extract_text_with_headings


def _make_pdf_with_headings():
    """Create a simple PDF with H1 (24pt), H2 (18pt), and body text (12pt)."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab not available")

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # H1 heading (24pt)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(72, 720, "Chapter One")

    # Body text (12pt) — repeated to become the "mode" font size
    c.setFont("Helvetica", 12)
    c.drawString(72, 690, "This is body text describing the chapter.")
    c.drawString(72, 675, "More body text that continues the description.")
    c.drawString(72, 660, "Yet more body content for good measure.")

    # H2 heading (18pt)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, 630, "Section Overview")

    # Body text (12pt)
    c.setFont("Helvetica", 12)
    c.drawString(72, 605, "Section body text goes here with details.")
    c.drawString(72, 590, "Additional section content follows.")

    c.save()
    buf.seek(0)
    return buf


class TestPdfHeadingDetection:
    """Tests for heading detection via font-size analysis."""

    def test_headings_detected_in_pdf_with_varied_font_sizes(self):
        """Headings with larger font sizes should become Markdown headings."""
        buf = _make_pdf_with_headings()
        result = _extract_text_with_headings(buf)

        # Largest font (24pt) should be H1
        assert "# Chapter One" in result, (
            "Expected '# Chapter One' in output, got:\n" + result
        )
        # Second-largest font (18pt) should be H2
        assert "## Section Overview" in result, (
            "Expected '## Section Overview' in output, got:\n" + result
        )

    def test_body_text_not_converted_to_heading(self):
        """Body text (most common font size) should not receive heading markers."""
        buf = _make_pdf_with_headings()
        result = _extract_text_with_headings(buf)

        # Body text lines must not start with '#'
        for line in result.splitlines():
            if "body text" in line.lower():
                assert not line.startswith("#"), (
                    f"Body text line should not be a heading: {line!r}"
                )

    def test_uniform_font_size_pdf_produces_no_headings(self):
        """A PDF where all text has the same font size should have no headings."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            pytest.skip("reportlab not available")

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(72, 720, "All text is the same size here.")
        c.drawString(72, 705, "No headings should be detected.")
        c.drawString(72, 690, "Every line is twelve points.")
        c.save()
        buf.seek(0)

        result = _extract_text_with_headings(buf)
        assert "#" not in result, (
            "Uniform-font PDF should produce no headings, got:\n" + result
        )

    def test_extract_text_with_headings_returns_string(self):
        """_extract_text_with_headings should always return a string."""
        buf = _make_pdf_with_headings()
        result = _extract_text_with_headings(buf)
        assert isinstance(result, str)
        assert len(result) > 0
