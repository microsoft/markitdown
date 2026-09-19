"""Charset sampling must not mistake a split UTF-8 character for another encoding."""

import io

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown._markitdown import _read_charset_sample


_SAMPLE_SIZE = 65536
_SPLIT_CHARACTERS = [
    (character, split)
    for character in ("\u00e9", "\u65e5", "\U0001f600")
    for split in range(1, len(character.encode("utf-8")))
]


def _split_utf8_json(character: str, split: int) -> bytes:
    prefix = '{"name":"r\u00e9sum\u00e9","notes":"'.encode("utf-8")
    return (
        prefix
        + b"a" * (_SAMPLE_SIZE - split - len(prefix))
        + (character + '"}').encode("utf-8")
    )


@pytest.fixture(scope="module")
def markitdown() -> MarkItDown:
    return MarkItDown()


@pytest.mark.parametrize("character,split", _SPLIT_CHARACTERS)
def test_charset_sample_completes_only_the_split_character(
    character: str, split: int
) -> None:
    data = _split_utf8_json(character, split)
    stream = io.BytesIO(data)
    expected_size = _SAMPLE_SIZE + len(character.encode("utf-8")) - split

    sample = _read_charset_sample(stream)

    assert sample == data[:expected_size]
    assert stream.tell() == expected_size
    assert expected_size <= _SAMPLE_SIZE + 3
    sample.decode("utf-8")


@pytest.mark.parametrize("character,split", _SPLIT_CHARACTERS)
def test_split_utf8_json_preserves_content(
    markitdown: MarkItDown, character: str, split: int
) -> None:
    data = _split_utf8_json(character, split)
    stream = io.BytesIO(data)

    guesses = markitdown._get_stream_info_guesses(stream, StreamInfo())
    assert guesses[0].charset == "utf-8"
    assert stream.tell() == 0

    result = markitdown.convert_stream(stream)

    assert result.markdown == data.decode("utf-8")


@pytest.mark.parametrize(
    "sample,tail",
    [
        (b"", b""),
        (b"ordinary text", b""),
        (b"short incomplete \xc3", b""),
        (b"a" * _SAMPLE_SIZE, b"\xc3\xa9"),
        (b"a" * (_SAMPLE_SIZE - 2) + b"\xc3\xa9", b"\xf0\x9f\x98\x80"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xc3", b""),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xf0", b"\x9f"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xc3", b"x"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xe0", b"\x80\x80"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xed", b"\xa0\x80"),
        (b"\xff" + b"a" * (_SAMPLE_SIZE - 2) + b"\xc3", b"\xa9"),
    ],
    ids=[
        "empty",
        "short",
        "short-incomplete",
        "ascii",
        "complete-utf8",
        "incomplete-at-eof",
        "incomplete-after-lookahead",
        "invalid-continuation",
        "overlong",
        "surrogate",
        "non-utf8-prefix",
    ],
)
def test_other_charset_samples_are_unchanged(sample: bytes, tail: bytes) -> None:
    stream = io.BytesIO(sample + tail)

    assert _read_charset_sample(stream) == sample
    assert stream.tell() <= _SAMPLE_SIZE + 3


def test_charset_guesses_restore_nonzero_stream_position(
    markitdown: MarkItDown,
) -> None:
    stream = io.BytesIO(b"prefix" + _split_utf8_json("\U0001f600", 1))
    stream.seek(len(b"prefix"))

    markitdown._get_stream_info_guesses(stream, StreamInfo())

    assert stream.tell() == len(b"prefix")


def test_explicit_charset_still_takes_precedence(markitdown: MarkItDown) -> None:
    data = _split_utf8_json("\u00e9", 1)

    result = markitdown.convert_stream(
        io.BytesIO(data),
        stream_info=StreamInfo(extension=".json", charset="cp1252"),
    )

    assert result.markdown == data.decode("cp1252")
