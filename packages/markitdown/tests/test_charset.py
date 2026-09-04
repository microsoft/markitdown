#!/usr/bin/env python3 -m pytest
import io
import json

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown._charset_utils import decode_bytes, normalize_charset

# Longer than the 4k prefix that _get_stream_info_guesses sniffs for a charset,
# so the non-ASCII character below lands outside the sniffed window.
_PREFIX_PADDING = "word " * 1200

# Sits beyond _PREFIX_PADDING, and is not representable in ASCII or cp1252-as-ASCII.
_LATE_CHARACTER = "—"  # em dash


def _convert_bytes(data: bytes, extension: str) -> str:
    markitdown = MarkItDown()
    return markitdown.convert(
        io.BytesIO(data), stream_info=StreamInfo(extension=extension)
    ).markdown


def _convert_declared(data: bytes, extension: str, charset: str) -> str:
    """Convert with a charset declared up front, as a Content-Type header would."""
    markitdown = MarkItDown()
    return markitdown.convert(
        io.BytesIO(data), stream_info=StreamInfo(extension=extension, charset=charset)
    ).markdown


def test_decode_bytes_honors_correct_charset():
    assert decode_bytes("café".encode("utf-8"), "utf-8") == "café"
    assert decode_bytes("café".encode("cp1252"), "cp1252") == "café"


def test_decode_bytes_recovers_from_wrong_charset():
    """A charset that cannot decode the data must not raise."""
    assert decode_bytes("café".encode("utf-8"), "ascii") == "café"


def test_decode_bytes_recovers_from_unknown_charset():
    assert decode_bytes(b"plain text", "not-a-real-codec") == "plain text"


def test_decode_bytes_without_charset_detects():
    assert decode_bytes("café".encode("utf-8")) == "café"


@pytest.mark.parametrize(
    "data",
    [
        b"valid ascii tail \xc3\x28",  # truncated utf-8 sequence
        b"valid ascii tail \xff\xff\xff",
        b"\xff\xfe\x00 utf-16 byte order mark",
        b"",
    ],
)
def test_decode_bytes_never_raises(data):
    """Undecodable bytes degrade to a lossy decode rather than failing the conversion."""
    assert isinstance(decode_bytes(data, "utf-8"), str)
    assert isinstance(decode_bytes(data), str)


def test_decode_bytes_preserves_decodable_text_around_bad_bytes():
    assert "valid ascii tail" in decode_bytes(b"valid ascii tail \xc3\x28", "utf-8")


def test_normalize_charset():
    assert normalize_charset(None) is None
    assert normalize_charset("UTF8") == normalize_charset("utf-8")
    assert normalize_charset("not-a-real-codec") == "not-a-real-codec"


def test_non_ascii_beyond_sniffed_prefix():
    """
    Regression: the charset is sniffed from the first 4k of the stream but used
    to decode all of it, so a mostly-ASCII document whose first non-ASCII
    character appears past that window used to fail with a UnicodeDecodeError.
    """
    content = _PREFIX_PADDING + _LATE_CHARACTER + " tail"
    result = _convert_bytes(content.encode("utf-8"), ".txt")
    assert _LATE_CHARACTER in result
    assert "tail" in result


# A charset can also arrive already declared -- from a Content-Type header, or
# from the caller -- in which case it is trusted without being sniffed at all.
# These cover each converter that decodes a whole stream with such a charset.


def test_declared_charset_too_narrow_plain_text():
    content = _PREFIX_PADDING + _LATE_CHARACTER
    result = _convert_declared(content.encode("utf-8"), ".txt", "ascii")
    assert _LATE_CHARACTER in result


def test_declared_charset_too_narrow_csv():
    content = "header\n" + _PREFIX_PADDING + "\n" + _LATE_CHARACTER + "\n"
    result = _convert_declared(content.encode("utf-8"), ".csv", "ascii")
    assert _LATE_CHARACTER in result


def test_declared_charset_too_narrow_ipynb():
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": [
            # Padded so the non-ASCII cell below falls outside the sniffed prefix,
            # leaving the declared charset the only one in play.
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [_PREFIX_PADDING],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"late {_LATE_CHARACTER} character"],
            },
        ],
    }
    data = json.dumps(notebook, ensure_ascii=False).encode("utf-8")
    result = _convert_declared(data, ".ipynb", "ascii")
    assert _LATE_CHARACTER in result


def test_pure_ascii_still_round_trips():
    content = _PREFIX_PADDING + "plain ascii tail"
    result = _convert_bytes(content.encode("ascii"), ".txt")
    assert "plain ascii tail" in result


def test_non_utf8_charset_is_not_clobbered():
    """Widening applies only to an ASCII guess -- other charsets are preserved."""
    markitdown = MarkItDown()
    content = "テスト " + _PREFIX_PADDING
    stream = io.BytesIO(content.encode("cp932"))
    guesses = markitdown._get_stream_info_guesses(
        stream, base_guess=StreamInfo(extension=".txt")
    )
    assert normalize_charset(guesses[0].charset) == normalize_charset("cp932")
    assert "テスト" in markitdown.convert(stream, file_extension=".txt").markdown
