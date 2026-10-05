import io

import pytest
import requests

from markitdown import MarkItDown, StreamInfo


def _response(content_type: str | None, body: bytes) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response.url = "https://example.com/document.txt"
    response.raw = io.BytesIO(body)
    if content_type is not None:
        response.headers["Content-Type"] = content_type
    return response


@pytest.fixture(scope="module")
def converter() -> MarkItDown:
    return MarkItDown(enable_plugins=False)


@pytest.mark.parametrize(
    "content_type",
    [
        'text/plain; charset=iso-8859-1; profile="urn:example;charset=utf-8"',
        'text/plain; charset=iso-8859-1; profile="urn:example;charset=ascii;v=1"',
        'text/plain; profile="urn:example;charset=utf-8"; charset=iso-8859-1',
        'text/plain; charset="iso-8859-1"',
        "text/plain; charset=iso-8859-1",
    ],
)
def test_quoted_parameter_cannot_override_charset(converter, content_type):
    response = _response(content_type, b"Caf\xe9")

    assert converter.convert_response(response).markdown == "Caf\u00e9"


@pytest.mark.parametrize("content_type", [None, "text/plain", 'text/plain; charset=""'])
def test_response_without_charset_still_converts(converter, content_type):
    assert (
        converter.convert_response(_response(content_type, b"hello")).markdown
        == "hello"
    )


def test_explicit_stream_info_charset_overrides_header(converter):
    response = _response("text/plain; charset=utf-8", b"Caf\xe9")

    result = converter.convert_response(
        response, stream_info=StreamInfo(charset="iso-8859-1")
    )

    assert result.markdown == "Caf\u00e9"
