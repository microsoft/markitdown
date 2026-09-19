#!/usr/bin/env python3 -m pytest
"""A result URL that uses `u=` for its own purpose must survive conversion.

Bing puts each search result behind a `/ck/a` redirect link. The real
destination sits in a base64 `u` query parameter. The converter decodes that
parameter, but it did so for every link that has `u=`. A normal result that
uses `u=` for its own purpose was therefore rewritten into garbage.
"""

import io

from markitdown import MarkItDown, StreamInfo

SERP_URL = "https://www.bing.com/search?q=python"

REDIRECT_TARGET = "https://docs.python.org/3/"
REDIRECT_HREF = (
    "https://www.bing.com/ck/a?!&amp;&amp;p=xyz"
    "&amp;u=a1aHR0cHM6Ly9kb2NzLnB5dGhvbi5vcmcvMy8="
)

NORMAL_HREF = "https://example.com/profile?u=abcdef"

LOOKALIKE_HREF = "https://not-bing.com/ck/a?u=a1aHR0cHM6Ly9kb2NzLnB5dGhvbi5vcmcvMy8="

LOOKALIKE_PATH_HREF = (
    "https://www.bing.com/ck/abc?u=a1aHR0cHM6Ly9kb2NzLnB5dGhvbi5vcmcvMy8="
)


def _serp(*hrefs: str) -> io.BytesIO:
    items = "".join(
        '<li class="b_algo"><h2><a href="%s">Result %d</a></h2><p>Snippet %d.</p></li>'
        % (href, i, i)
        for i, href in enumerate(hrefs, start=1)
    )
    html = (
        "<html><head><title>python - Search</title></head><body>"
        '<ol id="b_results">%s</ol></body></html>' % items
    )
    return io.BytesIO(html.encode("utf-8"))


def _convert(*hrefs: str) -> str:
    return (
        MarkItDown()
        .convert_stream(
            _serp(*hrefs),
            stream_info=StreamInfo(
                url=SERP_URL,
                mimetype="text/html",
                extension=".html",
                charset="utf-8",
            ),
        )
        .markdown
    )


def test_bing_redirect_is_decoded_to_its_destination() -> None:
    markdown = _convert(REDIRECT_HREF)

    assert "](%s)" % REDIRECT_TARGET in markdown
    assert "ck/a" not in markdown


def test_normal_url_keeps_its_own_u_parameter() -> None:
    markdown = _convert(NORMAL_HREF)

    assert "](%s)" % NORMAL_HREF in markdown


def test_normal_url_survives_next_to_a_redirect() -> None:
    markdown = _convert(REDIRECT_HREF, NORMAL_HREF)

    assert "](%s)" % REDIRECT_TARGET in markdown
    assert "](%s)" % NORMAL_HREF in markdown


def test_lookalike_host_is_not_treated_as_a_bing_redirect() -> None:
    markdown = _convert(LOOKALIKE_HREF)

    assert "](%s)" % LOOKALIKE_HREF in markdown


def test_lookalike_path_is_not_treated_as_a_bing_redirect() -> None:
    markdown = _convert(LOOKALIKE_PATH_HREF)

    assert "](%s)" % LOOKALIKE_PATH_HREF in markdown
