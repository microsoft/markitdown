from __future__ import annotations

import sys
from io import BytesIO
from typing import Final

import pytest

from markitdown import StreamInfo
from markitdown.converters import (
    BingSerpConverter,
    HtmlConverter,
    RssConverter,
    WikipediaConverter,
)


@pytest.mark.parametrize(
    ("converter", "url"),
    [
        pytest.param(
            BingSerpConverter, "https://www.bing.com/search?q=garden", id="bing"
        ),
        pytest.param(
            WikipediaConverter, "https://en.wikipedia.org/wiki/Garden", id="wikipedia"
        ),
    ],
)
@pytest.mark.parametrize(
    ("mimetype", "expected"),
    [
        pytest.param("text/html; charset=utf-8", True, id="html"),
        pytest.param("application/xhtml+xml", True, id="xhtml"),
        pytest.param("text/plain", False, id="plain-text"),
    ],
)
def test_html_specialized_converter_mime_types(
    converter: type[BingSerpConverter | WikipediaConverter],
    url: str,
    mimetype: str,
    *,
    expected: bool,
) -> None:
    assert (
        converter().accepts(
            BytesIO(b"<p>Garden</p>"), StreamInfo(url=url, mimetype=mimetype)
        )
        is expected
    )


@pytest.mark.parametrize(
    "destination",
    [pytest.param("a1_w", id="invalid-utf8"), pytest.param("a1A", id="invalid-base64")],
)
def test_bing_invalid_redirect_keeps_original_link(destination: str) -> None:
    result: Final = BingSerpConverter().convert(
        BytesIO(
            f'<li class="b_algo"><a href="https://www.bing.com/ck?a&amp;u={destination}">Garden</a></li>'.encode()
        ),
        StreamInfo(url="https://www.bing.com/search?q=garden"),
    )
    assert result.markdown == (
        "## A Bing search for 'garden' found the following results:\n\n"
        f"{'*' if sys.version_info >= (3, 11) else '-'} [Garden](https://www.bing.com/ck?a&u={destination})"
    )


def test_wikipedia_without_content_container_converts_document() -> None:
    result: Final = WikipediaConverter().convert(
        BytesIO(
            b"<html><head><title>Garden notes</title></head><body><p>Garden</p></body></html>"
        ),
        StreamInfo(url="https://en.wikipedia.org/wiki/Garden"),
    )
    assert (result.title, result.markdown) == (
        "Garden notes",
        "Garden" if sys.version_info >= (3, 11) else "Garden notes\n\nGarden",
    )


def test_html_default_link_title_uses_destination() -> None:
    assert HtmlConverter().convert_string(
        '<a href="https://example.org/">Garden</a>', default_title=True
    ).markdown == ('[Garden](https://example.org/ "https://example.org/")')


@pytest.mark.parametrize(
    "source",
    [
        pytest.param(b"<feed invalid", id="malformed-xml"),
        pytest.param(
            b'<!DOCTYPE feed [<!ENTITY garden "Garden">]><feed>&garden;</feed>',
            id="entity-declaration",
        ),
    ],
)
def test_feed_rejection_restores_stream_position(source: bytes) -> None:
    stream: Final = BytesIO(b"skip" + source)
    stream.seek(4)
    assert (
        RssConverter().accepts(stream, StreamInfo(extension=".xml")),
        stream.tell(),
    ) == (False, 4)


def test_html_empty_link_keeps_adjacent_words() -> None:
    assert (
        HtmlConverter()
        .convert_string('<p>one<a href="https://example.org/"></a>two</p>')
        .markdown
        == "onetwo"
    )
