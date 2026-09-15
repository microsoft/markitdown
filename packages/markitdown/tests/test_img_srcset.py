"""Responsive images (srcset / data-srcset) must not lose their source.

`<img srcset="a-1x.jpg 1x, a-2x.jpg 2x">` carries the image URL in the
`srcset` attribute rather than `src`. markitdown's `convert_img` only reads
`src` / `data-src`, so such images were rendered as an empty destination
`![alt]()` -- a silent loss of content. The same held for `data-srcset`
(lazy-loaded responsive images).
"""
import io

import pytest

from markitdown import MarkItDown


def _convert_html(html: str, **kwargs) -> str:
    result = MarkItDown().convert_stream(
        io.BytesIO(html.encode("utf-8")),
        file_extension=".html",
        **kwargs,
    )
    return result.markdown


def test_img_uses_srcset_when_src_absent() -> None:
    html = '<img srcset="photo-1x.jpg 1x, photo-2x.jpg 2x" alt="A photo">'

    markdown = _convert_html(html)

    assert "![A photo]()" not in markdown
    assert "photo-1x.jpg" in markdown


def test_img_prefers_src_over_srcset() -> None:
    html = '<img src="real.jpg" srcset="other-1x.jpg 1x, other-2x.jpg 2x" alt="A">'

    markdown = _convert_html(html)

    assert "![A](real.jpg)" in markdown


def test_img_prefers_srcset_over_lazy_placeholder_data_uri() -> None:
    placeholder = (
        "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
    )
    html = f'<img src="{placeholder}" srcset="photo-1x.jpg 1x" alt="A">'

    markdown = _convert_html(html)

    assert "photo-1x.jpg" in markdown
    assert placeholder not in markdown


def test_img_uses_data_srcset_when_src_and_data_src_absent() -> None:
    html = '<img data-srcset="lazy-1x.jpg 1x, lazy-2x.jpg 2x" alt="Lazy">'

    markdown = _convert_html(html)

    assert "![Lazy]()" not in markdown
    assert "lazy-1x.jpg" in markdown


def test_img_prefers_data_src_over_srcset() -> None:
    html = '<img data-src="real.jpg" srcset="other-1x.jpg 1x" alt="A">'

    markdown = _convert_html(html)

    assert "![A](real.jpg)" in markdown


@pytest.mark.parametrize(
    ("srcset", "expected"),
    [
        ("photo.jpg", "photo.jpg"),  # single URL, no descriptor
        ("photo.jpg 1x", "photo.jpg"),  # density descriptor
        ("photo.jpg 800w", "photo.jpg"),  # width descriptor
        ("photo.jpg 1x, hi.jpg 2x", "photo.jpg"),  # multiple candidates
        ("  spaced.jpg   2x  ", "spaced.jpg"),  # messy whitespace
    ],
)
def test_srcset_first_candidate_is_extracted(srcset: str, expected: str) -> None:
    markdown = _convert_html(f'<img srcset="{srcset}" alt="A">')

    assert f"![A]({expected})" in markdown


def test_srcset_url_with_commas_in_query_is_not_split() -> None:
    # A comma inside a URL must not be mistaken for a candidate separator.
    url = "https://example.com/img?crop=1,2&w=800"
    html = f'<img srcset="{url} 1x" alt="A">'

    markdown = _convert_html(html)

    assert url in markdown
