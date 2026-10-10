from __future__ import annotations

import io
import sys
import warnings
from collections.abc import Callable
from pathlib import Path
from typing import Final

import pytest
from markitdown import MarkItDown, StreamInfo
from markitdown.converters import HtmlConverter, WikipediaConverter


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        pytest.param("", "FirstLast", id="empty"),
        pytest.param(" ", "First Last", id="space"),
        pytest.param("\t", "First Last", id="tab"),
        pytest.param("&#160;", "First\u00a0Last", id="nonbreaking-space"),
        pytest.param("<br>", "First\nLast", id="break"),
        pytest.param("word", "First<u>word</u>Last", id="word"),
        pytest.param(" word ", "First <u>word</u> Last", id="padded-word"),
    ],
)
def test_html_underlined_content_is_preserved(
    convert_html: Callable[[str], str], content: str, expected: str
) -> None:
    assert convert_html(f"<p>First<u>{content}</u>Last</p>") == expected


@pytest.mark.parametrize(
    ("href", "expected"),
    [
        pytest.param(
            "https://abc.com/hist/%a5%c8%a5%c3%a5%d7%a5%da%a1%bc%a5%b8",
            "https://abc.com/hist/%a5%c8%a5%c3%a5%d7%a5%da%a1%bc%a5%b8",
            id="non-utf8-octets",
        ),
        pytest.param(
            "https://example.com/a path/日本語",
            "https://example.com/a%20path/%E6%97%A5%E6%9C%AC%E8%AA%9E",
            id="unicode-spaces",
        ),
        pytest.param(
            "https://example.com/100% complete",
            "https://example.com/100%25%20complete",
            id="literal-percent",
        ),
        pytest.param(
            "https://example.com/items/%ZZ/%2F",
            "https://example.com/items/%25ZZ/%2F",
            id="malformed-escape",
        ),
        pytest.param(
            "https://example.com/items/a%2Fb",
            "https://example.com/items/a%2Fb",
            id="encoded-slash",
        ),
        pytest.param(
            "https://example.com/a path?query=a b%20c#fragment with spaces",
            "https://example.com/a%20path?query=a b%20c#fragment with spaces",
            id="query-fragment",
        ),
    ],
)
def test_html_href_escaping(
    convert_html: Callable[[str], str], href: str, expected: str
) -> None:
    assert convert_html(f'<a href="{href}">example</a>') == f"[example]({expected})"


@pytest.mark.parametrize(
    ("source", "lazy_source", "keep_data_uris", "expected"),
    [
        pytest.param(
            "data:image/gif;base64,AAAA",
            "https://example.com/photo.jpg",
            False,
            "https://example.com/photo.jpg",
            id="lazy-placeholder",
        ),
        pytest.param(
            "https://example.com/photo.jpg",
            "https://example.com/other.jpg",
            False,
            "https://example.com/photo.jpg",
            id="real-source",
        ),
        pytest.param(
            "",
            "https://example.com/photo.jpg",
            False,
            "https://example.com/photo.jpg",
            id="missing-source",
        ),
        pytest.param(
            "data:image/gif;base64,AAAA",
            "",
            False,
            "data:image/gif;base64...",
            id="truncated-data-uri",
        ),
        pytest.param(
            "data:image/gif;base64,AAAA",
            "https://example.com/photo.jpg",
            True,
            "data:image/gif;base64,AAAA",
            id="keep-data-uri",
        ),
        pytest.param(
            "DATA:image/png;base64,AAAA",
            "",
            False,
            "DATA:image/png;base64...",
            id="uppercase-truncated",
        ),
        pytest.param(
            "DATA:image/png;base64,AAAA",
            "",
            True,
            "DATA:image/png;base64,AAAA",
            id="uppercase-kept",
        ),
    ],
)
def test_html_image_source(
    source: str, lazy_source: str, *, keep_data_uris: bool, expected: str
) -> None:
    assert (
        HtmlConverter()
        .convert_string(
            f'<img src="{source}" data-src="{lazy_source}" alt="A photo">',
            keep_data_uris=keep_data_uris,
        )
        .markdown
        == f"![A photo]({expected})"
    )


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        pytest.param(
            '<span lang="en" dir="ltr"><span class="mw-page-title-main">Paris</span></span>',
            "Paris",
            id="title-span",
        ),
        pytest.param("<i>Escherichia coli</i>", "Escherichia coli", id="italic"),
        pytest.param(
            "<i>Titanic</i> (1997 film)", "Titanic (1997 film)", id="mixed-content"
        ),
    ],
)
def test_wikipedia_title(heading: str, expected: str) -> None:
    result: Final = WikipediaConverter().convert(
        io.BytesIO(
            f"<html><head><title>{expected} - Wikipedia</title></head><body>"
            f'<h1 id="firstHeading">{heading}</h1>'
            '<div id="mw-content-text"><p>Body text.</p></div></body></html>'.encode()
        ),
        StreamInfo(
            url="https://en.wikipedia.org/wiki/Example",
            mimetype="text/html",
            extension=".html",
        ),
    )
    assert (result.title, result.markdown) == (expected, f"# {expected}\n\nBody text.")


@pytest.mark.parametrize(
    "title",
    [pytest.param("", id="missing"), pytest.param("<title>   </title>", id="blank")],
)
def test_wikipedia_empty_title(title: str) -> None:
    result: Final = WikipediaConverter().convert(
        io.BytesIO(
            f"<html><head>{title}</head><body><div id='mw-content-text'><p>Hello</p></div></body></html>".encode()
        ),
        StreamInfo(mimetype="text/html", url="https://en.wikipedia.org/wiki/Test"),
    )
    assert (result.title, result.markdown) == (None, "Hello")


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        pytest.param(
            "<p>Plain <s>s element</s> after.</p>", "Plain ~~s element~~ after.", id="s"
        ),
        pytest.param(
            "<p>Plain <del>del element</del> after.</p>",
            "Plain ~~del element~~ after.",
            id="del",
        ),
        pytest.param(
            "<p>Plain <strike>strike element</strike> after.</p>",
            "Plain ~~strike element~~ after.",
            id="strike",
        ),
        pytest.param(
            "<p>Spaces A<strike> B </strike>C.</p>", "Spaces A ~~B~~ C.", id="padded"
        ),
        pytest.param(
            "<p>Runs D<strike>  E  </strike>F.</p>",
            "Runs D ~~E~~ F.",
            id="repeated-spaces",
        ),
        pytest.param("<p>Empty G<strike></strike>H.</p>", "Empty GH.", id="empty"),
        pytest.param(
            "<p>Newline I<strike>J\nK</strike>L.</p>",
            "Newline I~~J K~~L.",
            id="newline",
        ),
        pytest.param(
            "<p>Break M<strike>N<br>O</strike>P.</p>", "Break M~~N\nO~~P.", id="break"
        ),
    ],
)
def test_html_strikethrough(tmp_path: Path, source: str, expected: str) -> None:
    path: Final = tmp_path / "strike.html"
    path.write_text(source, encoding="utf-8")
    assert MarkItDown().convert(str(path)).markdown == expected


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
    result: Final = MarkItDown().convert_stream(
        io.BytesIO(html.encode()), file_extension=".html"
    )
    assert (result.markdown, result.title) == (expected, title)


def test_html_fragment_sniffs_unknown_charset() -> None:
    result: Final = MarkItDown().convert_stream(
        io.BytesIO("<title>Café</title><p>Résumé</p>".encode("cp1252")),
        stream_info=StreamInfo(extension=".html", charset="utf-8"),
    )
    assert (result.markdown, result.title) == ("Café\n\nRésumé", "Café")


def test_html_table_cell_list_keeps_item_boundaries(
    convert_html: Callable[[str], str],
) -> None:
    html: Final = (
        "<table><tr><th>Traded as</th><td><ul>"
        '<li><a href="/nasdaq">Nasdaq</a></li><li>DJIA</li>'
        "</ul></td></tr></table>"
    )
    assert "| Traded as | * [Nasdaq](/nasdaq) * DJIA |" in convert_html(html)


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        pytest.param(
            "<code><ul><li>one</li><li>two</li></ul></code>", "`one two`", id="list"
        ),
        pytest.param("<code><p>one</p><p>two</p></code>", "`one two`", id="paragraphs"),
        pytest.param(
            "<pre><code><ul><li>one</li><li>two</li></ul></code></pre>",
            "```\none\ntwo\n```",
            id="pre",
        ),
        pytest.param(
            "<table><tr><td><code><p>one</p><p>two</p></code></td></tr></table>",
            "|  |\n| --- |\n| `one two` |",
            id="table-cell",
        ),
    ],
)
def test_html_code_block_descendants_keep_boundaries(
    convert_html: Callable[[str], str], html: str, expected: str
) -> None:
    assert convert_html(html) == expected


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
            result: Final = MarkItDown().convert_stream(
                io.BytesIO(html.encode()), file_extension=".html"
            )
    finally:
        sys.setrecursionlimit(original_limit)

    assert result.markdown == "Deep content with **bold text**"


@pytest.fixture
def convert_html() -> Callable[[str], str]:
    converter: Final = MarkItDown()
    return lambda html: (
        converter.convert_stream(
            io.BytesIO(html.encode()), file_extension=".html"
        ).markdown
    )
