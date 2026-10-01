import io

import pytest
from bs4 import BeautifulSoup

from markitdown import MarkItDown
from markitdown.converters._markdownify import _CustomMarkdownify


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
        ("<br>", "First\nLast"),
        ("word", "First<u>word</u>Last"),
        (" word ", "First <u>word</u> Last"),
    ],
)
def test_html_underlined_content_is_preserved(content: str, expected: str) -> None:
    assert _convert_html(f"<p>First<u>{content}</u>Last</p>") == expected


@pytest.mark.parametrize(
    "tag",
    [
        "b",
        "code",
        "del",
        "em",
        "i",
        "kbd",
        "s",
        "samp",
        "strike",
        "strong",
        "sub",
        "sup",
        "u",
    ],
)
def test_html_whitespace_only_inline_tag_keeps_its_whitespace(tag: str) -> None:
    assert _convert_html(f"<p>First<{tag}> </{tag}>Last</p>") == "First Last"


def test_html_whitespace_only_inline_tag_keeps_the_exact_character() -> None:
    assert _convert_html("<p>First<b>&#160;</b>Last</p>") == "First\u00a0Last"


def test_html_empty_inline_tag_still_adds_nothing() -> None:
    assert _convert_html("<p>First<b></b>Last</p>") == "FirstLast"


def test_html_styled_runs_are_not_glued_together() -> None:
    """Editors that emit one element per styled run put the space in its own element.

    Losing it merges the two words and joins the emphasis markers into `****`.
    """
    assert (
        _convert_html("<p><b>First</b><b> </b><b>Last</b></p>") == "**First** **Last**"
    )


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("b", "First **word** Last"),
        ("code", "First `word` Last"),
        ("em", "First *word* Last"),
        ("s", "First ~~word~~ Last"),
        ("u", "First <u>word</u> Last"),
    ],
)
def test_html_inline_tag_with_content_is_still_converted(
    tag: str, expected: str
) -> None:
    assert _convert_html(f"<p>First <{tag}>word</{tag}> Last</p>") == expected


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
