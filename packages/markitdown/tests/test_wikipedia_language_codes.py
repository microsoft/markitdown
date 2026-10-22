#!/usr/bin/env python3 -m pytest
"""Wikipedia language subdomains of any shape must reach the dedicated converter.

The acceptance regex previously only matched two- or three-letter codes, so
simple.wikipedia.org (six letters) and hyphenated codes such as
zh-min-nan.wikipedia.org silently fell through to the generic HTML converter,
losing the title extraction and mw-content-text focusing.
"""

import io

import pytest
from markitdown import StreamInfo
from markitdown.converters import WikipediaConverter

PAGE = io.BytesIO(
    b"""<html><head><title>Example - Wikipedia</title></head><body>
<h1 id="firstHeading">Example</h1>
<div id="mw-content-text"><p>Body text.</p></div>
</body></html>"""
)


def _stream_info(url: str) -> StreamInfo:
    return StreamInfo(url=url, mimetype="text/html", extension=".html")


@pytest.mark.parametrize(
    "url",
    [
        "https://en.wikipedia.org/wiki/Python",
        "https://de.wikipedia.org/wiki/Python",
        "https://en.m.wikipedia.org/wiki/Python",
        "https://gcr.wikipedia.org/wiki/Port",
        "https://simple.wikipedia.org/wiki/Python",
        "https://zh-min-nan.wikipedia.org/wiki/Main",
        "https://be-x-old.wikipedia.org/wiki/Main",
    ],
)
def test_accepts_wikipedia_language_subdomains(url: str) -> None:
    assert WikipediaConverter().accepts(PAGE, _stream_info(url))


@pytest.mark.parametrize(
    "url",
    [
        "https://example.org/wiki/Python",
        "https://en.wikipedia.org.evil.test/wiki/Python",
        "https://wikipedia.org/wiki/Python",
    ],
)
def test_rejects_non_wikipedia_urls(url: str) -> None:
    assert not WikipediaConverter().accepts(PAGE, _stream_info(url))


def test_simple_wikipedia_conversion_uses_the_converter() -> None:
    """End-to-end: a simple.wikipedia.org page keeps Wikipedia-specific parsing."""
    result = WikipediaConverter().convert(
        PAGE, _stream_info("https://simple.wikipedia.org/wiki/Example")
    )
    assert result.title == "Example"
    assert result.markdown.lstrip().startswith("# Example")
