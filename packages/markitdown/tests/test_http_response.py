import io

import pytest
import requests
from requests.adapters import BaseAdapter
from urllib3.exceptions import ProtocolError

from markitdown import MarkItDown


class _TrackingBody(io.BytesIO):
    def __init__(self, *, fail_during_read=False):
        super().__init__(b"# Downloaded document\n")
        self.fail_during_read = fail_during_read
        self.released = False

    def stream(self, amount, decode_content=True):
        yield self.read(amount)
        if self.fail_during_read:
            raise ProtocolError("Connection interrupted during download")

    def release_conn(self):
        self.released = True


class _ResponseAdapter(BaseAdapter):
    def __init__(self, response):
        self.response = response

    def send(self, request, **kwargs):
        self.response.request = request
        self.response.url = request.url
        return self.response

    def close(self):
        pass


def _converter_with_response(*, status_code=200, fail_during_read=False):
    body = _TrackingBody(fail_during_read=fail_during_read)
    response = requests.Response()
    response.status_code = status_code
    response.headers["content-type"] = "text/plain; charset=utf-8"
    response.raw = body
    session = requests.Session()
    session.mount("https://example.test/", _ResponseAdapter(response))
    return MarkItDown(requests_session=session), body, response


def test_convert_uri_returns_downloaded_content():
    converter, _, _ = _converter_with_response()

    result = converter.convert_uri("https://example.test/document.txt")

    assert result.markdown == "# Downloaded document\n"


@pytest.mark.parametrize("status_code", [404, 500])
def test_convert_uri_closes_response_on_http_error(status_code):
    converter, body, response = _converter_with_response(status_code=status_code)

    with pytest.raises(requests.HTTPError) as exc_info:
        converter.convert_uri("https://example.test/document.txt")

    assert exc_info.value.response is response
    assert body.closed
    assert body.released


def test_convert_uri_closes_response_on_download_error():
    converter, body, _ = _converter_with_response(fail_during_read=True)

    with pytest.raises(requests.exceptions.ChunkedEncodingError):
        converter.convert_uri("https://example.test/document.txt")

    assert body.closed
    assert body.released
