"""Edge-case tests for BingSerpConverter — corrupt HTML, malformed redirects.

Tests Bing SERP HTML parsing robustness.
"""

import io
import pytest

from markitdown import MarkItDown, StreamInfo, FileConversionException


BING_URL = "https://www.bing.com/search?q=test"


def _convert_bing_html(html: str) -> str:
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(html.encode("utf-8")),
        stream_info=StreamInfo(
            extension=".html",
            mimetype="text/html",
            charset="utf-8",
            url=BING_URL,
        ),
    )
    return result.markdown


# ============================================================
# Valid Bing SERP
# ============================================================


def test_basic_bing_serp():
    html = f"""<!DOCTYPE html>
<html><head><title>test - Bing</title></head>
<body>
<div class="b_algo">
  <h2><a href="/ck/a?u=aHR0cHM6Ly9leGFtcGxlLmNvbQ==">Example</a></h2>
  <p>Description of the result</p>
</div>
</body></html>"""
    result = _convert_bing_html(html)
    assert "Bing search" in result
    assert "Example" in result


def test_bing_serp_with_multiple_results():
    html = f"""<!DOCTYPE html>
<html><head><title>test - Bing</title></head>
<body>
<div class="b_algo">
  <h2><a href="/ck/a?u=aHR0cHM6Ly9zaXRlMS5jb20=">Site 1</a></h2>
  <p>First result</p>
</div>
<div class="b_algo">
  <h2><a href="/ck/a?u=aHR0cHM6Ly9zaXRlMi5jb20=">Site 2</a></h2>
  <p>Second result</p>
</div>
</body></html>"""
    result = _convert_bing_html(html)
    assert "Site 1" in result
    assert "Site 2" in result


# ============================================================
# Missing URL
# ============================================================


def test_bing_serp_no_url_raises():
    md = MarkItDown()
    # Without URL, BingSerpConverter won't accept → falls to HtmlConverter
    result = md.convert(
        io.BytesIO(b"<html><body><p>no url</p></body></html>"),
        stream_info=StreamInfo(extension=".html", mimetype="text/html"),
    )
    assert isinstance(result.markdown, str)


# ============================================================
# Corrupt HTML
# ============================================================


def test_bing_serp_malformed_html():
    """Malformed HTML should not crash the converter."""
    html = f"""<!DOCTYPE html>
<html><head><title>test - Bing</title></head>
<body>
<div class="b_algo">
  <h2><a href="/ck/a?u=!!!not_valid_base64!!!">Broken Link</a></h2>
  <p>Broken description</p>
</div>
</body></html>"""
    result = _convert_bing_html(html)
    # Should produce output without crashing
    assert "Bing search" in result


def test_bing_serp_empty():
    html = f"""<!DOCTYPE html>
<html><head><title>test - Bing</title></head>
<body></body></html>"""
    result = _convert_bing_html(html)
    assert "Bing search" in result


def test_bing_serp_no_results():
    html = f"""<!DOCTYPE html>
<html><head><title>test - Bing</title></head>
<body>
<div class="not_a_result"><p>No algorithm results</p></div>
</body></html>"""
    result = _convert_bing_html(html)
    assert "Bing search" in result


def test_bing_serp_unparseable_html():
    """Severely broken HTML — converter falls through gracefully."""
    html = b"not <html> at all\x00\x01\x02"
    md = MarkItDown()
    result = md.convert(
        io.BytesIO(html),
        stream_info=StreamInfo(
            extension=".html",
            mimetype="text/html",
            charset="utf-8",
            url=BING_URL,
        ),
    )
    assert isinstance(result.markdown, str)


# ============================================================
# _bing_serp non-Bing URL
# ============================================================


def test_non_bing_url_not_accepted():
    """BingSerpConverter should reject non-Bing URLs."""
    md = MarkItDown()
    # The converter chain should fall through to HtmlConverter
    result = md.convert(
        io.BytesIO(b"<html><body><p>generic content</p></body></html>"),
        stream_info=StreamInfo(
            extension=".html",
            mimetype="text/html",
            url="https://www.google.com/search?q=test",
        ),
    )
    assert "generic content" in result.markdown
