import base64
from urllib.parse import quote

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown._uri_utils import parse_data_uri


@pytest.mark.parametrize(
    "payload", [b"Hello", b"\xfb\xff", b"\xff\xff", "Hello, 世界!".encode("utf-8")]
)
@pytest.mark.parametrize("lowercase", [False, True])
def test_percent_encoded_base64_data(payload: bytes, lowercase: bool) -> None:
    encoded = quote(base64.b64encode(payload).decode("ascii"), safe="")
    if lowercase:
        encoded = (
            encoded.replace("%2B", "%2b").replace("%2F", "%2f").replace("%3D", "%3d")
        )
    assert parse_data_uri("data:application/octet-stream;base64," + encoded) == (
        "application/octet-stream",
        {},
        payload,
    )


@pytest.mark.parametrize(
    "header",
    [
        "data:text/plain;base64",
        "DATA:text/plain;BASE64",
        "data:;base64",
        "data:text/plain;charset=utf-8;base64",
    ],
)
def test_percent_encoded_padding_preserves_metadata(header: str) -> None:
    mime, attributes, payload = parse_data_uri(header + ",SGVsbG8%3D")
    assert payload == b"Hello"
    assert mime == (None if header == "data:;base64" else "text/plain")
    assert attributes == ({"charset": "utf-8"} if "charset" in header else {})


@pytest.mark.parametrize("encoded", ["+/8=", "%2B/8=", "+%2F8=", "%2B%2F8%3D"])
def test_raw_plus_is_not_form_decoded_as_space(encoded: str) -> None:
    assert (
        parse_data_uri("data:application/octet-stream;base64," + encoded)[2]
        == b"\xfb\xff"
    )


def test_non_base64_data_still_decodes_once() -> None:
    assert parse_data_uri("data:text/plain,%252F+%2C")[2] == b"%2F+,"


def test_public_conversion_accepts_percent_encoded_base64() -> None:
    text = "Hello, 世界!"
    encoded = quote(base64.b64encode(text.encode("utf-8")).decode("ascii"), safe="")
    result = MarkItDown().convert_uri(
        "data:text/plain;charset=utf-8;base64," + encoded,
        stream_info=StreamInfo(extension=".txt"),
    )
    assert result.markdown == text
