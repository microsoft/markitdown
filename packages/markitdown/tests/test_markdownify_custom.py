"""Unit tests for _markdownify._CustomMarkdownify — HTML→Markdown converter.

Covers:
- URL sanitization (javascript: stripped, non-http schemes, path escaping)
- Data URI truncation (keep_data_uris=False default)
- Checkbox rendering [x]/[ ]
- Heading style (ATX #)
- General conversion
"""

from markitdown.converters._markdownify import _CustomMarkdownify
from bs4 import BeautifulSoup


def _convert(html: str, **kwargs) -> str:
    """Helper: convert HTML string to Markdown via _CustomMarkdownify."""
    soup = BeautifulSoup(html, "html.parser")
    converter = _CustomMarkdownify(**kwargs)
    return converter.convert_soup(soup).strip()


# ============================================================
# URL sanitization
# ============================================================


def test_strips_javascript_links():
    result = _convert('<a href="javascript:void(0)">click</a>')
    assert "click" in result
    assert "javascript" not in result


def test_keeps_http_links():
    result = _convert('<a href="https://example.com">Example</a>')
    assert "[Example](https://example.com)" in result


def test_keeps_https_links():
    result = _convert('<a href="https://secure.com/page">Secure</a>')
    assert "[Secure](https://secure.com/page)" in result


def test_strips_ftp_links():
    result = _convert('<a href="ftp://files.com/data">Files</a>')
    assert "Files" in result
    assert "ftp://" not in result


def test_strips_mailto_links():
    result = _convert('<a href="mailto:user@example.com">Email</a>')
    assert "Email" in result
    assert "mailto:" not in result


def test_escapes_url_path_special_chars():
    """URL paths with spaces or special chars should be percent-encoded."""
    result = _convert('<a href="https://example.com/path with spaces">Link</a>')
    assert "path%20with%20spaces" in result


def test_autolink_preserves_url():
    result = _convert(
        '<a href="https://example.com/auto">https://example.com/auto</a>'
    )
    assert "<https://example.com/auto>" in result


# ============================================================
# Data URI truncation
# ============================================================


def test_truncates_data_uri_by_default():
    html = '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA" alt="test">'
    result = _convert(html)
    assert "data:image/png;base64..." in result
    assert "iVBORw0KGgo" not in result


def test_keeps_data_uri_when_enabled():
    html = '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA" alt="test">'
    result = _convert(html, keep_data_uris=True)
    assert "iVBORw0KGgo" in result


def test_keeps_normal_image_src():
    html = '<img src="https://example.com/photo.png" alt="photo">'
    result = _convert(html)
    assert "https://example.com/photo.png" in result


def test_img_with_data_src_fallback():
    html = '<img data-src="https://example.com/lazy.png" alt="lazy">'
    result = _convert(html)
    assert "https://example.com/lazy.png" in result


def test_img_with_alt_and_title():
    html = '<img src="https://example.com/pic.jpg" alt="Alt text" title="Title text">'
    result = _convert(html)
    assert '[Alt text](https://example.com/pic.jpg "Title text")' in result


# ============================================================
# Checkbox rendering
# ============================================================


def test_checkbox_checked():
    result = _convert('<input type="checkbox" checked>')
    assert "[x]" in result


def test_checkbox_unchecked():
    result = _convert('<input type="checkbox">')
    assert "[ ]" in result


def test_other_input_types_ignored():
    result = _convert('<input type="text" value="hello">')
    assert result == ""


# ============================================================
# Heading style
# ============================================================


def test_heading_atx_style():
    result = _convert("<h1>Title</h1><h2>Subtitle</h2>")
    assert result.startswith("# Title")
    assert "## Subtitle" in result


# ============================================================
# General conversion
# ============================================================


def test_plain_text_passthrough():
    result = _convert("Hello World")
    assert "Hello World" in result


def test_paragraphs_separated():
    result = _convert("<p>First</p><p>Second</p>")
    assert "First" in result
    assert "Second" in result


def test_bold_and_italic():
    result = _convert("<strong>bold</strong> <em>italic</em>")
    assert "**bold**" in result
    assert "*italic*" in result


def test_unordered_list():
    result = _convert("<ul><li>A</li><li>B</li></ul>")
    lines = result.split("\n")
    assert any("* A" in line for line in lines)
    assert any("* B" in line for line in lines)


def test_nested_pre_skips_link_conversion():
    """Links inside <pre> tags should not be converted."""
    result = _convert("<pre><a href='http://x.com'>code</a></pre>")
    assert "code" in result
    # Should not produce a markdown link inside pre
    assert "](http://x.com)" not in result
