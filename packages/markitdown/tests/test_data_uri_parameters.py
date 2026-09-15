import base64

import pytest

from markitdown import MarkItDown
from markitdown._uri_utils import parse_data_uri


@pytest.mark.parametrize("use_base64", [False, True])
@pytest.mark.parametrize(
    "parameters, expected",
    [
        ("charset=UTF%2D8", {"charset": "UTF-8"}),
        ("CHAR%53ET=utf-8", {"charset": "utf-8"}),
        (
            "name=report%3bfinal%3d1%2c2.txt;empty=",
            {"name": "report;final=1,2.txt", "empty": ""},
        ),
        ("name=a+b%2Bc.txt", {"name": "a+b+c.txt"}),
        (
            "name=%252F;char%2573et=utf-8",
            {"name": "%2F", "char%73et": "utf-8"},
        ),
    ],
)
def test_percent_encoded_parameters(parameters, expected, use_base64) -> None:
    content = b"Hello; a=b, %20+"
    payload = (
        base64.b64encode(content).decode("ascii")
        if use_base64
        else "Hello%3B%20a%3Db%2C%20%2520%2B"
    )
    marker = ";base64" if use_base64 else ""

    assert parse_data_uri(f"data:text/plain;{parameters}{marker},{payload}") == (
        "text/plain",
        expected,
        content,
    )


def test_percent_encoded_charset_without_media_type() -> None:
    assert parse_data_uri("data:;char%73et=utf%2D8,hello") == (
        None,
        {"charset": "utf-8"},
        b"hello",
    )


@pytest.mark.parametrize("use_base64", [False, True])
@pytest.mark.parametrize(
    "parameter",
    [
        "charset=iso-8859-1",
        "charset=iso%2D8859%2D1",
        "%63harset=iso-8859-1",
        "char%73et=iso%2d8859%2d1",
    ],
)
def test_conversion_honors_charset_parameter(parameter, use_base64) -> None:
    payload = "Q2Fm6Q==" if use_base64 else "Caf%E9"
    marker = ";base64" if use_base64 else ""

    result = MarkItDown(enable_plugins=False).convert_uri(
        f"data:text/plain;{parameter}{marker},{payload}"
    )

    assert result.markdown == "Café"
