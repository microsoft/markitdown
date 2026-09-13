#!/usr/bin/env python3 -m pytest
"""The site-specific HTML converters need the fallback the generic one has.

``HtmlConverter`` (#1644) and ``RssConverter`` (#2333) recover from the
``RecursionError`` that markdownify's recursive DOM traversal raises on deeply
nested markup. ``WikipediaConverter`` and ``BingSerpConverter`` read the same
kind of page and did not, so a deeply nested page silently lost the
site-specific extraction and came back as the whole document instead.

A lowered recursion limit keeps the test independent of the host's default.
"""

import io
import sys
import warnings
from contextlib import contextmanager

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import BingSerpConverter, WikipediaConverter

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Nested"
BING_URL = "https://www.bing.com/search?q=nested"

ARTICLE_TEXT = "Deep article content"
SITE_NOTICE = "Site notice chrome"
FOOTER = "Footer chrome"
RESULT_TEXT = "Deep result content"

DEPTH = 500
LOW_LIMIT = 200  # well below markdownify's traversal depth for DEPTH nesting


def _nest(text: str) -> str:
    return "<div>" * DEPTH + f"<p>{text}</p>" + "</div>" * DEPTH


WIKIPEDIA_HTML = (
    "<html><head><title>Nested - Wikipedia</title></head><body>"
    f'<div id="siteNotice">{SITE_NOTICE}</div>'
    '<span class="mw-page-title-main">Nested</span>'
    f'<div id="mw-content-text">{_nest(ARTICLE_TEXT)}</div>'
    f'<div id="footer">{FOOTER}</div>'
    "</body></html>"
).encode("utf-8")

BING_HTML = (
    "<html><head><title>nested - Bing</title></head><body>"
    f'<li class="b_algo">{_nest(RESULT_TEXT)}</li>'
    "</body></html>"
).encode("utf-8")


@contextmanager
def _low_recursion_limit():
    original = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(LOW_LIMIT)
        yield
    finally:
        sys.setrecursionlimit(original)


def _convert(html: bytes, url: str) -> tuple[str, list[warnings.WarningMessage]]:
    with _low_recursion_limit():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = MarkItDown().convert_stream(
                io.BytesIO(html),
                stream_info=StreamInfo(
                    extension=".html",
                    mimetype="text/html",
                    charset="utf-8",
                    url=url,
                ),
            )
    return result.markdown, [w for w in caught if "deeply nested" in str(w.message)]


def test_deeply_nested_wikipedia_page_keeps_the_article_extraction() -> None:
    markdown, recursion_warnings = _convert(WIKIPEDIA_HTML, WIKIPEDIA_URL)

    assert len(recursion_warnings) > 0
    assert ARTICLE_TEXT in markdown
    # The page is still read as a Wikipedia page: its heading is emitted, and
    # the chrome outside #mw-content-text stays out of the output.
    assert markdown.startswith("# Nested")
    assert SITE_NOTICE not in markdown
    assert FOOTER not in markdown
    assert "<div" not in markdown


def test_deeply_nested_bing_serp_keeps_the_results_extraction() -> None:
    markdown, recursion_warnings = _convert(BING_HTML, BING_URL)

    assert len(recursion_warnings) > 0
    assert RESULT_TEXT in markdown
    # The page is still read as a Bing results page.
    assert markdown.startswith("## A Bing search for 'nested' found")
    assert "<div" not in markdown


def test_strict_still_surfaces_the_recursion_error() -> None:
    """strict=True is the documented escape hatch on the other converters."""
    with _low_recursion_limit():
        with pytest.raises(RecursionError):
            WikipediaConverter().convert(
                io.BytesIO(WIKIPEDIA_HTML),
                StreamInfo(extension=".html", charset="utf-8", url=WIKIPEDIA_URL),
                strict=True,
            )
        with pytest.raises(RecursionError):
            BingSerpConverter().convert(
                io.BytesIO(BING_HTML),
                StreamInfo(extension=".html", charset="utf-8", url=BING_URL),
                strict=True,
            )


def test_shallow_pages_are_unaffected() -> None:
    shallow = (
        "<html><head><title>Shallow - Wikipedia</title></head><body>"
        '<span class="mw-page-title-main">Shallow</span>'
        '<div id="mw-content-text"><p>Plain <b>article</b> text.</p></div>'
        "</body></html>"
    ).encode("utf-8")

    result = MarkItDown().convert_stream(
        io.BytesIO(shallow),
        stream_info=StreamInfo(
            extension=".html", mimetype="text/html", charset="utf-8", url=WIKIPEDIA_URL
        ),
    )

    assert result.markdown.startswith("# Shallow")
    assert "Plain **article** text." in result.markdown
