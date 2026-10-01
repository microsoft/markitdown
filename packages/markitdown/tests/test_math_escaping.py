#!/usr/bin/env python3 -m pytest
"""Tests for math escaping fix in _markdownify.py.

Regression tests for the bug where markdownify escapes underscores and
asterisks inside $...$ and $$...$$ math delimiters, producing broken
LaTeX like $v\\_{c}$ instead of $v_{c}$.
"""

import pytest

from markitdown.converters._markdownify import _fix_math_escaping


# ─── Unit tests for _fix_math_escaping ──────────────────────────────


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # Inline math with subscript
        ("$v_{c}$", "$v_{c}$"),
        ("$a_{ij}$", "$a_{ij}$"),
        ("$x_{i}$", "$x_{i}$"),
        # Display math with subscript
        ("$$v_{c} = x^{2}$$", "$$v_{c} = x^{2}$$"),
        # Multiple inline math blocks
        ("For $v_{c}$ and $x_{i}$", "For $v_{c}$ and $x_{i}$"),
        # Inline math with surrounding text
        ("text $v_{c}$ more text", "text $v_{c}$ more text"),
        # Display math (multiline)
        ("$$\nv_{c}\n$$", "$$\nv_{c}\n$$"),
        # Asterisk escaping inside math
        ("$a\\*b\\*c$", "$a*b*c$"),
        # Mixed underscore and asterisk
        ("$v_{c} * a_{ij}$", "$v_{c} * a_{ij}$"),
        # No escaping needed (no math delimiters)
        ("hello world", "hello world"),
        # Escaped underscores OUTSIDE math should NOT be touched
        ("hello\\_world", "hello\\_world"),
        # Superscript (no underscore to fix)
        ("$x^{2}$", "$x^{2}$"),
        # Fraction (no underscore to fix)
        ("$\\frac{a}{b}$", "$\\frac{a}{b}$"),
        # Mixed: escaped inside math, preserved outside
        (
            "hello\\_world $v_{c}$ end",
            "hello\\_world $v_{c}$ end",
        ),
    ],
)
def test_fix_math_escaping(input_text, expected):
    """Test that _fix_math_escaping correctly handles various patterns."""
    assert _fix_math_escaping(input_text) == expected


# ─── Escaped-input tests (simulates markdownify's output) ───────────


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # Simulated markdownify output: escaped underscore inside inline math
        ("$v\\_{c}$", "$v_{c}$"),
        ("$a\\_{ij}$", "$a_{ij}$"),
        # Simulated markdownify output: escaped underscore inside display math
        ("$$v\\_{c} = x^{2}$$", "$$v_{c} = x^{2}$$"),
        # Simulated markdownify output: multiple inline math blocks
        (
            "For $v\\_{c}$ and $x\\_{i}$",
            "For $v_{c}$ and $x_{i}$",
        ),
        # Simulated markdownify output: escaped asterisk inside math
        ("$a\\*b\\*c$", "$a*b*c$"),
        # Mixed: markdownify-escaped math + plain text escaped underscore
        (
            "hello\\_world $v\\_{c}$ end",
            "hello\\_world $v_{c}$ end",
        ),
        # Real-world example from equations.docx (should be unchanged)
        (
            "$$\\frac{m\\lambda}{a}$$",
            "$$\\frac{m\\lambda}{a}$$",
        ),
    ],
)
def test_fix_math_escaping_from_markdownify(input_text, expected):
    """Test _fix_math_escaping on markdownify's actual output patterns."""
    assert _fix_math_escaping(input_text) == expected


# ─── Integration test via _CustomMarkdownify ────────────────────────


def test_convert_soup_preserves_math():
    """Test the full convert_soup path with HTML containing math."""
    from markitdown.converters._markdownify import _CustomMarkdownify
    from bs4 import BeautifulSoup

    md = _CustomMarkdownify()

    # Simulate what DocxConverter produces after pre_process_docx + mammoth
    html = "<p>The velocity $v_{c}$ equals $a_{ij} \\cdot x_{i}$.</p>"
    soup = BeautifulSoup(html, "html.parser")
    result = md.convert_soup(soup)

    # Math should be preserved without escaping
    assert "$v_{c}$" in result
    assert "$a_{ij} \\cdot x_{i}$" in result
    assert r"\_" not in result


def test_convert_soup_display_math():
    """Test convert_soup with display math."""
    from markitdown.converters._markdownify import _CustomMarkdownify
    from bs4 import BeautifulSoup

    md = _CustomMarkdownify()

    html = "<p>$$v_{c} = x^{2}$$</p>"
    soup = BeautifulSoup(html, "html.parser")
    result = md.convert_soup(soup)

    assert "$$v_{c} = x^{2}$$" in result
    assert r"\_" not in result


def test_convert_soup_plain_text_underscore_preserved():
    """Test that plain-text underscores remain escaped (correct behavior)."""
    from markitdown.converters._markdownify import _CustomMarkdownify
    from bs4 import BeautifulSoup

    md = _CustomMarkdownify()

    html = "<p>hello_world</p>"
    soup = BeautifulSoup(html, "html.parser")
    result = md.convert_soup(soup)

    # Plain-text underscore should still be escaped
    assert r"\_" in result
    assert "hello\\_world" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
