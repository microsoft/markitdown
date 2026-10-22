"""Tests for PlainTextConverter (src/markitdown/converters/_plain_text_converter.py)."""

import io

import pytest

from markitdown import MarkItDown, StreamInfo


@pytest.fixture(scope="module")
def converter() -> MarkItDown:
    return MarkItDown(enable_plugins=False)


@pytest.mark.parametrize(
    "extension", [".txt", ".text", ".md", ".markdown", ".json", ".jsonl"]
)
def test_accepted_extensions_pass_content_through(
    converter: MarkItDown, extension: str
) -> None:
    result = converter.convert_stream(
        io.BytesIO(b"hello, world"),
        stream_info=StreamInfo(extension=extension, charset="utf-8"),
    )
    assert result.markdown == "hello, world"


@pytest.mark.parametrize(
    "mimetype", ["text/plain", "text/x-log", "application/json", "application/markdown"]
)
def test_accepted_mimetype_prefixes_pass_content_through(
    converter: MarkItDown, mimetype: str
) -> None:
    result = converter.convert_stream(
        io.BytesIO(b"hello, world"),
        stream_info=StreamInfo(mimetype=mimetype, charset="utf-8"),
    )
    assert result.markdown == "hello, world"


def test_declared_charset_is_honored_even_with_an_unrecognized_extension(
    converter: MarkItDown,
) -> None:
    # accepts() short-circuits to True whenever stream_info.charset is set,
    # regardless of extension/mimetype -- exercise that branch directly.
    body = "grüße".encode("utf-8")
    result = converter.convert_stream(
        io.BytesIO(body),
        stream_info=StreamInfo(extension=".some-unknown-ext", charset="utf-8"),
    )
    assert result.markdown == "grüße"


def test_charset_is_auto_detected_when_not_declared(converter: MarkItDown) -> None:
    # UTF-8 encodes non-ASCII text distinctively enough for charset_normalizer
    # to detect reliably without a declared charset.
    body = "grüße".encode("utf-8")
    result = converter.convert_stream(
        io.BytesIO(body),
        stream_info=StreamInfo(extension=".txt"),
    )
    assert result.markdown == "grüße"
