"""HTML conversion, link handling, and Wikipedia pages."""

import io

import pytest
from bs4 import BeautifulSoup

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import WikipediaConverter
from markitdown.converters._markdownify import _CustomMarkdownify


# HTML rendering


def _convert_html(html: str, **kwargs) -> str:
    result = MarkItDown().convert_stream(
        io.BytesIO(html.encode("utf-8")),
        file_extension=".html",
        **kwargs,
    )
    return result.markdown


@pytest.mark.parametrize(
    "whitespace", ["", " ", "  ", "\t", "\n", "\r\n", "\u00a0", " \t\n\u00a0 "]
)
def test_underline_preserves_whitespace_verbatim(whitespace: str) -> None:
    element = BeautifulSoup("<u></u>", "html.parser").u

    assert _CustomMarkdownify().convert_u(element, whitespace) == whitespace


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("", "FirstLast"),
        (" ", "First Last"),
        ("\t", "First Last"),
        ("&#160;", "First\u00a0Last"),
        ("<br>", "First  \nLast"),
        ("word", "First<u>word</u>Last"),
        (" word ", "First <u>word</u> Last"),
    ],
)
def test_html_underlined_content_is_preserved(content: str, expected: str) -> None:
    assert _convert_html(f"<p>First<u>{content}</u>Last</p>") == expected


def test_preserves_non_utf8_percent_encoded_href_path() -> None:
    href = "https://abc.com/hist/" "%a5%c8%a5%c3%a5%d7%a5%da%a1%bc%a5%b8"
    html = f'<a href="{href}">example</a>'

    markdown = _convert_html(html)

    assert f"[example]({href})" in markdown
    assert "%EF%BF%BD" not in markdown


def test_html_href_still_quotes_raw_unicode_and_spaces() -> None:
    href = "https://example.com/a path/日本語"
    expected_href = "https://example.com/a%20path/" "%E6%97%A5%E6%9C%AC%E8%AA%9E"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_html_href_quotes_literal_percent_sign() -> None:
    href = "https://example.com/100% complete"
    expected_href = "https://example.com/100%25%20complete"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_html_href_quotes_malformed_percent_escape() -> None:
    href = "https://example.com/items/%ZZ/%2F"
    expected_href = "https://example.com/items/%25ZZ/%2F"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_html_href_preserves_encoded_slash() -> None:
    href = "https://example.com/items/a%2Fb"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({href})" in markdown


def test_html_href_does_not_quote_query_or_fragment() -> None:
    href = "https://example.com/a path?query=a b%20c#fragment with spaces"
    expected_href = "https://example.com/a%20path?query=a b%20c#fragment with spaces"

    markdown = _convert_html(f'<a href="{href}">example</a>')

    assert f"[example]({expected_href})" in markdown


def test_img_prefers_data_src_over_placeholder_data_uri() -> None:
    placeholder = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
    )
    real_src = "https://example.com/photo.jpg"
    html = (
        f'<img src="{placeholder}" data-src="{real_src}" alt="A photo" loading="lazy">'
    )

    markdown = _convert_html(html)

    assert f"![A photo]({real_src})" in markdown
    assert placeholder not in markdown


def test_img_uses_real_src_over_data_src_when_both_present() -> None:
    real_src = "https://example.com/photo.jpg"
    other_src = "https://example.com/photo-alt.jpg"
    html = f'<img src="{real_src}" data-src="{other_src}" alt="A photo">'

    markdown = _convert_html(html)

    assert f"![A photo]({real_src})" in markdown


def test_img_falls_back_to_data_src_when_src_missing() -> None:
    real_src = "https://example.com/photo.jpg"
    html = f'<img data-src="{real_src}" alt="A photo">'

    markdown = _convert_html(html)

    assert f"![A photo]({real_src})" in markdown


def test_img_keeps_truncated_data_uri_when_no_data_src() -> None:
    placeholder = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
    )
    html = f'<img src="{placeholder}" alt="A photo">'

    markdown = _convert_html(html)

    assert "![A photo](data:image/gif;base64...)" in markdown


def test_img_keeps_embedded_data_uri_over_data_src_when_keeping_data_uris() -> None:
    embedded = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
    )
    other_src = "https://example.com/photo.jpg"
    html = f'<img src="{embedded}" data-src="{other_src}" alt="A photo">'

    markdown = _convert_html(html, keep_data_uris=True)

    assert f"![A photo]({embedded})" in markdown
    assert other_src not in markdown


# Wikipedia article titles

STREAM_INFO = StreamInfo(
    url="https://en.wikipedia.org/wiki/Example",
    mimetype="text/html",
    extension=".html",
)


def _page(heading: str, document_title: str) -> io.BytesIO:
    """Build a page shaped like the article HTML Wikipedia actually serves."""
    return io.BytesIO(
        f"""<html><head><title>{document_title} - Wikipedia</title></head><body>
<h1 id="firstHeading" class="firstHeading mw-first-heading">{heading}</h1>
<div id="mw-content-text"><p>Body text.</p></div>
</body></html>""".encode()
    )


def test_plain_title_is_read_from_the_title_span() -> None:
    """A plain title keeps being read from mw-page-title-main."""
    page = _page(
        '<span lang="en" dir="ltr"><span class="mw-page-title-main">Paris</span></span>',
        "Paris",
    )

    result = WikipediaConverter().convert(page, STREAM_INFO)

    assert result.title == "Paris"
    assert result.markdown.lstrip().startswith("# Paris")


def test_fully_italicised_title_keeps_its_text() -> None:
    """Wikipedia drops the title span for italicised titles, e.g. species names."""
    page = _page("<i>Escherichia coli</i>", "Escherichia coli")

    result = WikipediaConverter().convert(page, STREAM_INFO)

    # Without the first-heading fallback this became "Escherichia coli - Wikipedia".
    assert result.title == "Escherichia coli"
    assert result.markdown.lstrip().startswith("# Escherichia coli")


def test_title_mixing_markup_and_plain_text_keeps_both_parts() -> None:
    """A disambiguated italic title spans several children, so .string is None."""
    page = _page("<i>Titanic</i> (1997 film)", "Titanic (1997 film)")

    result = WikipediaConverter().convert(page, STREAM_INFO)

    assert result.title == "Titanic (1997 film)"
    assert result.markdown.lstrip().startswith("# Titanic (1997 film)")


# Conversion regressions


def test_wikipedia_converter_no_title() -> None:
    """WikipediaConverter should not render '# None' when page has no title."""
    converter = WikipediaConverter()
    html = b"<html><body><div id='mw-content-text'><p>Hello</p></div></body></html>"
    stream_info = StreamInfo(
        mimetype="text/html", url="https://en.wikipedia.org/wiki/Test"
    )
    result = converter.convert(io.BytesIO(html), stream_info)
    assert "# None" not in result.markdown
    assert "Hello" in result.markdown
    assert result.markdown.strip() == "Hello"


def test_wikipedia_converter_blank_title() -> None:
    """WikipediaConverter should not render an empty heading for a blank title."""
    converter = WikipediaConverter()
    html = b"<html><head><title>   </title></head><body><div id='mw-content-text'><p>Hello</p></div></body></html>"
    stream_info = StreamInfo(
        mimetype="text/html", url="https://en.wikipedia.org/wiki/Test"
    )
    result = converter.convert(io.BytesIO(html), stream_info)
    assert not result.markdown.lstrip().startswith("#")
    assert result.title is None
    assert result.text_content.strip() == "Hello"


def test_uppercase_data_image_uri_is_truncated_by_default() -> None:
    markitdown = MarkItDown()
    html = b'<html><body><img alt="dot" src="DATA:image/png;base64,AAAA"></body></html>'
    stream_info = StreamInfo(mimetype="text/html", extension=".html")

    result = markitdown.convert_stream(io.BytesIO(html), stream_info=stream_info)
    assert result.markdown == "![dot](DATA:image/png;base64...)"
    assert "AAAA" not in result.markdown

    result = markitdown.convert_stream(
        io.BytesIO(html), stream_info=stream_info, keep_data_uris=True
    )
    assert result.markdown == "![dot](DATA:image/png;base64,AAAA)"


def test_html_strikethrough_variants(tmp_path) -> None:
    html = """<!doctype html>
<html><body>
<p>Plain <s>s element</s> after.</p>
<p>Plain <del>del element</del> after.</p>
<p>Plain <strike>strike element</strike> after.</p>
<p>Spaces A<strike> B </strike>C.</p>
<p>Runs D<strike>  E  </strike>F.</p>
<p>Empty G<strike></strike>H.</p>
<p>Newline I<strike>J
K</strike>L.</p>
<p>Break M<strike>N<br>O</strike>P.</p>
</body></html>
"""
    path = tmp_path / "strike.html"
    path.write_text(html, encoding="utf-8")
    markdown = MarkItDown().convert(str(path)).markdown

    assert markdown == "\n\n".join(
        [
            # <s>, <del> and the obsolete <strike> all mean strikethrough
            "Plain ~~s element~~ after.",
            "Plain ~~del element~~ after.",
            "Plain ~~strike element~~ after.",
            # Surrounding whitespace stays outside of the markup ...
            "Spaces A ~~B~~ C.",
            # ... and runs of it collapse to a single space
            "Runs D ~~E~~ F.",
            # An empty element contributes nothing
            "Empty GH.",
            # A line break inside the element is kept, and the markup
            # survives it because strikethrough may span a single newline
            "Newline I~~J\nK~~L.",
            "Break M~~N  \nO~~P.",
        ]
    )


def test_deeply_nested_html_fallback() -> None:
    """Large, deeply nested HTML should fall back to plain-text extraction
    instead of silently returning unconverted HTML (issue #1636).

    Note: This test uses sys.setrecursionlimit to guarantee a RecursionError
    regardless of the host environment's default limit, making it deterministic
    across different platforms and CI configurations.
    """
    import sys
    import warnings

    markitdown = MarkItDown()

    # Use a small recursion limit so the test is environment-independent.
    # We restore the original limit in a finally block to avoid side-effects.
    original_limit = sys.getrecursionlimit()
    low_limit = 200  # well below markdownify's traversal depth for depth=500

    # Build HTML with nesting deep enough to trigger RecursionError
    depth = 500
    html = "<html><body>"
    for _ in range(depth):
        html += '<div style="margin-left:10px">'
    html += "<p>Deep content with <b>bold text</b></p>"
    for _ in range(depth):
        html += "</div>"
    html += "</body></html>"

    try:
        sys.setrecursionlimit(low_limit)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = markitdown.convert_stream(
                io.BytesIO(html.encode("utf-8")),
                file_extension=".html",
            )

            # Should have emitted a warning about the fallback
            recursion_warnings = [x for x in w if "deeply nested" in str(x.message)]
            assert len(recursion_warnings) > 0

    finally:
        sys.setrecursionlimit(original_limit)

    # The output should contain the text content, not raw HTML
    assert "Deep content" in result.markdown
    assert "bold text" in result.markdown
    assert "<div" not in result.markdown
    assert "<p>" not in result.markdown


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
