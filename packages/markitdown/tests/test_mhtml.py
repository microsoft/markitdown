"""MHTML conversion: HTML extraction, transfer encodings, charsets, and errors."""

import base64
import io

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import MhtmlConverter

HEADERS = (
    "From: <Saved by Blink>\n"
    "Subject: Saved Subject\n"
    "MIME-Version: 1.0\n"
    'Content-Type: multipart/related; type="text/html"; boundary="B"\n'
)

PNG_PART = (
    "--B\n"
    "Content-Type: image/png\n"
    "Content-Transfer-Encoding: base64\n"
    "Content-Location: https://example.com/pic.png\n"
    "\n"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==\n"
)


def _mhtml(html_headers: str, html_body: str, extra_parts: str = "") -> bytes:
    text = f"{HEADERS}\n--B\n{html_headers}\n{html_body}\n{extra_parts}--B--\n"
    return text.encode("utf-8")


@pytest.fixture(scope="module")
def converter() -> MarkItDown:
    return MarkItDown(enable_plugins=False)


def test_mhtml_quoted_printable_html_is_converted(converter: MarkItDown) -> None:
    data = _mhtml(
        "Content-Type: text/html; charset=utf-8\n"
        "Content-Transfer-Encoding: quoted-printable\n",
        "<html><head><title>Page</title></head><body><h1>Caf=C3=A9</h1>"
        '<p>See <a href=3D"https://example.com/a">this</a>.</p></body></html>',
        PNG_PART,
    )

    result = converter.convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".mhtml")
    )

    assert result.markdown == "# Café\n\nSee [this](https://example.com/a)."
    assert result.title == "Page"


def test_mhtml_base64_non_utf8_charset_is_decoded(converter: MarkItDown) -> None:
    html = "<html><body><p>Grüße</p></body></html>".encode("iso-8859-1")
    data = _mhtml(
        "Content-Type: text/html; charset=iso-8859-1\n"
        "Content-Transfer-Encoding: base64\n",
        base64.encodebytes(html).decode("ascii"),
    )

    result = converter.convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".mht")
    )

    assert result.markdown == "Grüße"


def test_mhtml_part_without_charset_is_read_as_utf8(converter: MarkItDown) -> None:
    data = _mhtml(
        "Content-Type: text/html\nContent-Transfer-Encoding: quoted-printable\n",
        "<html><body><p>Caf=C3=A9</p></body></html>",
    )

    result = converter.convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".mhtml")
    )

    assert result.markdown == "Café"


def test_mhtml_ignores_embedded_resources_and_scripts(converter: MarkItDown) -> None:
    data = _mhtml(
        "Content-Type: text/html; charset=utf-8\nContent-Transfer-Encoding: 7bit\n",
        "<html><body><script>var x = 1;</script><p>Body</p></body></html>",
        PNG_PART,
    )

    result = converter.convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".mhtml")
    )

    assert result.markdown == "Body"


def test_mhtml_title_falls_back_to_subject(converter: MarkItDown) -> None:
    data = _mhtml(
        "Content-Type: text/html; charset=utf-8\nContent-Transfer-Encoding: 7bit\n",
        "<html><body><p>No title element</p></body></html>",
    )

    result = converter.convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".mhtml")
    )

    assert result.title == "Saved Subject"


def test_mhtml_detected_from_content_without_extension(converter: MarkItDown) -> None:
    data = _mhtml(
        "Content-Type: text/html; charset=utf-8\nContent-Transfer-Encoding: 7bit\n",
        "<html><body><h1>Detected</h1></body></html>",
    )

    result = converter.convert_stream(io.BytesIO(data))

    assert result.markdown == "# Detected"


def test_mhtml_without_html_part_raises() -> None:
    data = _mhtml(
        "Content-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: 7bit\n",
        "just text",
    )

    with pytest.raises(ValueError, match="No text/html part"):
        MhtmlConverter().convert(io.BytesIO(data), StreamInfo(extension=".mhtml"))


def test_mhtml_xhtml_root_part_is_converted(converter: MarkItDown) -> None:
    data = _mhtml(
        "Content-Type: application/xhtml+xml; charset=utf-8\n"
        "Content-Transfer-Encoding: 7bit\n",
        '<html xmlns="http://www.w3.org/1999/xhtml"><body><h1>XHTML</h1></body></html>',
    )

    result = converter.convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".mhtml")
    )

    assert result.markdown == "# XHTML"


def test_mhtml_start_parameter_selects_root_part(converter: MarkItDown) -> None:
    text = (
        "MIME-Version: 1.0\n"
        'Content-Type: multipart/related; type="text/html"; boundary="B";'
        ' start="<root@x>"\n\n'
        "--B\nContent-Type: text/html; charset=utf-8\nContent-ID: <frame@x>\n\n"
        "<html><body><p>IFRAME</p></body></html>\n"
        "--B\nContent-Type: text/html; charset=utf-8\nContent-ID: <root@x>\n\n"
        "<html><body><h1>MAIN</h1></body></html>\n"
        "--B--\n"
    )

    result = converter.convert_stream(
        io.BytesIO(text.encode()), stream_info=StreamInfo(extension=".mhtml")
    )

    assert result.markdown == "# MAIN"
