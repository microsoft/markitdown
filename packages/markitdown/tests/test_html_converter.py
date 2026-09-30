import io
import sys
import warnings
from typing import Final

import pytest
from markitdown import MarkItDown, StreamInfo


def _convert_html(html: str, **kwargs: bool | str) -> str:
    result = MarkItDown().convert_stream(
        io.BytesIO(html.encode("utf-8")),
        file_extension=".html",
        **kwargs,
    )
    return result.markdown


@pytest.mark.parametrize(
    ("html", "expected", "title"),
    [
        pytest.param(
            "<title>Title</title><h1>Heading</h1><p>body</p>",
            "Title\n\n# Heading\n\nbody",
            "Title",
            id="orphan-title",
        ),
        pytest.param(
            "<template><p>hidden</p></template><p>shown</p>",
            "hidden\n\nshown",
            None,
            id="orphan-template",
        ),
        pytest.param(
            "<head><title>Title</title></head>between<p>shown</p>",
            "Titlebetween\n\nshown",
            "Title",
            id="inline-boundary",
        ),
        pytest.param(
            "<script>secret()</script><style>secret</style><p>shown</p>",
            "shown",
            None,
            id="script-style",
        ),
        pytest.param(
            "<html><head><title>Title</title></head><body><p>shown</p></body></html>",
            "shown",
            "Title",
            id="explicit-body",
        ),
    ],
)
def test_html_fragment_content(html: str, expected: str, title: str | None) -> None:
    result = MarkItDown().convert_stream(io.BytesIO(html.encode()), file_extension=".html")
    assert (result.markdown, result.title) == (expected, title)


def test_html_fragment_sniffs_unknown_charset() -> None:
    result = MarkItDown().convert_stream(
        io.BytesIO("<title>Café</title><p>Résumé</p>".encode("cp1252")),
        stream_info=StreamInfo(extension=".html", charset="utf-8"),
    )
    assert (result.markdown, result.title) == ("Café\n\nRésumé", "Café")


def test_html_table_cell_list_keeps_item_boundaries() -> None:
    html: Final = (
        '<table><tr><th>Traded as</th><td><ul>'
        '<li><a href="/nasdaq">Nasdaq</a></li><li>DJIA</li>'
        '</ul></td></tr></table>'
    )
    assert "| Traded as | * [Nasdaq](/nasdaq) * DJIA |" in _convert_html(html)


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
    ("options", "expected"),
    [
        pytest.param({}, r"[text] `code` \*star\* \_name\_", id="default"),
        pytest.param(
            {"escape_misc": True},
            r"\[text\] \`code\` \*star\* \_name\_",
            id="escape-misc",
        ),
        pytest.param(
            {"escape_asterisks": False},
            r"[text] `code` *star* \_name\_",
            id="keep-asterisks",
        ),
        pytest.param(
            {"escape_underscores": False},
            r"[text] `code` \*star\* _name_",
            id="keep-underscores",
        ),
    ],
)
def test_html_escaping_options(options: dict[str, bool], expected: str) -> None:
    assert _convert_html("<p>[text] `code` *star* _name_</p>", **options) == expected


@pytest.mark.parametrize(
    ("html", "options", "expected"),
    [
        pytest.param('<input type="checkbox" checked>', {}, "[x]", id="checked"),
        pytest.param('<input type="checkbox">', {}, "[ ]", id="unchecked"),
        pytest.param('<input type="text">', {}, "", id="text-input"),
        pytest.param(
            "<p><sub>low</sub><sup>high</sup></p>",
            {"sub_symbol": "<sub>", "sup_symbol": "^"},
            "<sub>low</sub>^high^",
            id="independent-script-symbols",
        ),
    ],
)
def test_html_inline_callbacks(
    html: str, options: dict[str, str], expected: str
) -> None:
    assert _convert_html(html, **options) == expected


@pytest.mark.parametrize(
    ("href", "text", "expected"),
    [
        pytest.param(
            "https://example.com", "word", "[word](https://example.com)", id="link"
        ),
        pytest.param(
            "https://example.com",
            "https://example.com",
            "<https://example.com>",
            id="autolink",
        ),
        pytest.param("javascript:alert(1)", "word", "word", id="unsafe-scheme"),
        pytest.param("https://[", "word", "word", id="invalid-url"),
        pytest.param("", "word", "word", id="empty-href"),
    ],
)
def test_html_link_edge_spaces(href: str, text: str, expected: str) -> None:
    assert (
        _convert_html(f'<p>First<a href="{href}"> {text} </a>Last</p>')
        == f"First {expected} Last"
    )


@pytest.mark.parametrize("tag", ["code", "kbd", "samp"])
@pytest.mark.parametrize(
    ("content", "expected"),
    [
        pytest.param("`value`", "`` `value` ``", id="literal-backticks"),
        pytest.param("one<br>two", "`one two`", id="line-break"),
        pytest.param("", "", id="empty"),
    ],
)
def test_html_code_elements(tag: str, content: str, expected: str) -> None:
    assert _convert_html(f"<p><{tag}>{content}</{tag}></p>") == expected


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        pytest.param("<code><ul><li>one</li><li>two</li></ul></code>", "`one two`", id="list"),
        pytest.param("<code><p>one</p><p>two</p></code>", "`one two`", id="paragraphs"),
        pytest.param("<pre><code><ul><li>one</li><li>two</li></ul></code></pre>", "```\none\ntwo\n```", id="pre"),
        pytest.param(
            "<table><tr><td><code><p>one</p><p>two</p></code></td></tr></table>",
            "|  |\n| --- |\n| `one two` |",
            id="table-cell",
        ),
    ],
)
def test_html_code_block_descendants_keep_boundaries(html: str, expected: str) -> None:
    assert _convert_html(html) == expected


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        pytest.param("Plain <s>s element</s> after.", "Plain ~~s element~~ after.", id="s"),
        pytest.param("Plain <del>del element</del> after.", "Plain ~~del element~~ after.", id="del"),
        pytest.param("Plain <strike>strike element</strike> after.", "Plain ~~strike element~~ after.", id="strike"),
        pytest.param("Spaces A<strike> B </strike>C.", "Spaces A ~~B~~ C.", id="spaces"),
        pytest.param("Runs D<strike>  E  </strike>F.", "Runs D ~~E~~ F.", id="runs"),
        pytest.param("Empty G<strike></strike>H.", "Empty GH.", id="empty"),
        pytest.param("Newline I<strike>J\nK</strike>L.", "Newline I~~J K~~L.", id="newline"),
        pytest.param("Break M<strike>N<br>O</strike>P.", "Break M~~N\nO~~P.", id="break"),
    ],
)
def test_html_strikethrough_variants(html: str, expected: str) -> None:
    assert _convert_html(f"<p>{html}</p>") == expected


def test_preserves_non_utf8_percent_encoded_href_path() -> None:
    href = "https://abc.com/hist/%a5%c8%a5%c3%a5%d7%a5%da%a1%bc%a5%b8"
    html = f'<a href="{href}">example</a>'

    markdown = _convert_html(html)

    assert f"[example]({href})" in markdown
    assert "%EF%BF%BD" not in markdown


def test_html_href_still_quotes_raw_unicode_and_spaces() -> None:
    href = "https://example.com/a path/日本語"
    expected_href = "https://example.com/a%20path/%E6%97%A5%E6%9C%AC%E8%AA%9E"

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


def test_deeply_nested_html_converts() -> None:
    html: Final = (
        "<html><body>"
        + '<div style="margin-left:10px">' * 500
        + "<p>Deep content with <b>bold text</b></p>"
        + "</div>" * 500
        + "</body></html>"
    )
    original_limit: Final = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(200)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = MarkItDown().convert_stream(io.BytesIO(html.encode()), file_extension=".html")
    finally:
        sys.setrecursionlimit(original_limit)

    assert result.markdown == "Deep content with **bold text**"
