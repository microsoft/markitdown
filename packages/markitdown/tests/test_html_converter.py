import io

import pytest

from markitdown import MarkItDown


def _convert_html(html: str) -> str:
    result = MarkItDown().convert_stream(
        io.BytesIO(html.encode("utf-8")),
        file_extension=".html",
    )
    return result.markdown


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


@pytest.mark.parametrize("attributes", ["", 'name="bookmark"', 'href=""'])
@pytest.mark.parametrize("text", [" middle ", " "])
def test_html_anchor_without_destination_preserves_word_boundaries(
    attributes: str, text: str
) -> None:
    markdown = _convert_html(f"<p>before<a {attributes}>{text}</a>after</p>")

    assert markdown == f"before{text}after"


@pytest.mark.parametrize("href", ["", 'href="https://example.com"'])
def test_html_anchor_in_pre_preserves_whitespace(href: str) -> None:
    markdown = _convert_html(f"<pre>before<a {href}>  middle\n </a>after</pre>")

    assert markdown == "```\nbefore  middle\n after\n```"


def test_html_autolink_preserves_surrounding_spaces() -> None:
    markdown = _convert_html(
        '<p>before<a href="https://example.com"> https://example.com </a>after</p>'
    )

    assert markdown == "before <https://example.com> after"


def test_html_link_with_whitespace_only_text_preserves_word_boundary() -> None:
    markdown = _convert_html('<p>before<a href="https://example.com"> </a>after</p>')

    assert markdown == "before after"


@pytest.mark.parametrize(
    "href, expected",
    [
        ("https://example.com", "before [middle](https://example.com) after"),
        ("javascript:void(0)", "before middle after"),
    ],
)
def test_html_link_preserves_surrounding_spaces(href: str, expected: str) -> None:
    markdown = _convert_html(f'<p>before<a href="{href}"> middle </a>after</p>')

    assert markdown == expected
