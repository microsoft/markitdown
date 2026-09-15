import io

import pytest

from markitdown import StreamInfo
from markitdown.converters import HtmlConverter


@pytest.mark.parametrize(
    "head, source_url, expected",
    [
        (
            "",
            "https://example.com/docs/page.html",
            "https://example.com/docs/guide.html",
        ),
        (
            '<base href="../assets/">',
            "https://example.com/docs/page.html",
            "https://example.com/assets/guide.html",
        ),
        (
            '<base href="https://cdn.example.com/docs/">',
            None,
            "https://cdn.example.com/docs/guide.html",
        ),
        (
            '<base href="/first/"><base href="/second/">',
            "https://example.com/page",
            "https://example.com/first/guide.html",
        ),
        ("", None, "guide.html"),
    ],
)
def test_html_link_uses_document_base(head, source_url, expected):
    html = (
        f'<html><head>{head}</head><body><a href="guide.html">Guide</a></body></html>'
    )
    result = HtmlConverter().convert(
        io.BytesIO(html.encode()),
        StreamInfo(extension=".html", url=source_url),
    )
    assert result.markdown == f"[Guide]({expected})"


def test_html_base_resolves_images_and_lazy_images():
    result = HtmlConverter().convert_string(
        '<base href="../images/">'
        '<img src="chart.png" alt="Chart">'
        '<img src="data:image/png;base64,abc" data-src="photo.jpg" alt="Photo">',
        url="https://example.com/docs/page.html",
    )
    assert "![Chart](https://example.com/images/chart.png)" in result.markdown
    assert "![Photo](https://example.com/images/photo.jpg)" in result.markdown


def test_html_base_preserves_absolute_urls_and_encoded_paths():
    result = HtmlConverter().convert_string(
        '<a href="https://other.example/a">Absolute</a>'
        '<a href="guide%20one.html#part">Encoded</a>'
        '<a href="javascript:alert(1)">Script</a>',
        url="https://example.com/docs/page.html",
    )
    assert "[Absolute](https://other.example/a)" in result.markdown
    assert (
        "[Encoded](https://example.com/docs/guide%20one.html#part)" in result.markdown
    )
    assert "javascript:" not in result.markdown


def test_response_conversion_uses_final_response_url():
    from requests import Response
    from markitdown import MarkItDown

    response = Response()
    response.url = "https://example.com/final/page.html"
    response.status_code = 200
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.raw = io.BytesIO(b'<html><body><a href="next.html">Next</a></body></html>')

    result = MarkItDown().convert_response(response)

    assert result.markdown == "[Next](https://example.com/final/next.html)"


def test_malformed_base_does_not_discard_document():
    result = HtmlConverter().convert_string(
        '<base href="https://[broken">' '<p>Text</p><a href="next.html">Next</a>',
        url="https://example.com/docs/page.html",
    )
    assert "Text" in result.markdown
    assert "[Next](https://example.com/docs/next.html)" in result.markdown
