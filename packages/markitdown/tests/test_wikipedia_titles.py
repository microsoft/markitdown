#!/usr/bin/env python3 -m pytest
"""Article titles that carry markup must survive conversion."""

import io

from markitdown import StreamInfo
from markitdown.converters import WikipediaConverter

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
