"""SRT subtitle conversion: cue text, timestamps, markup, and line endings."""

import io

import pytest

from markitdown import MarkItDown, StreamInfo


@pytest.fixture(scope="module")
def converter() -> MarkItDown:
    return MarkItDown(enable_plugins=False)


def _convert(converter: MarkItDown, content: str, **info) -> str:
    return converter.convert_stream(
        io.BytesIO(content.encode("utf-8")),
        stream_info=StreamInfo(extension=".srt", **info),
    ).markdown


@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"], ids=["LF", "CRLF", "CR"])
def test_srt_cues_become_timestamped_lines(converter: MarkItDown, newline: str) -> None:
    content = newline.join(
        [
            "1",
            "00:00:01,000 --> 00:00:03,500",
            "Hello there.",
            "",
            "2",
            "01:02:05,250 --> 01:02:07,000",
            "Goodbye.",
            "",
        ]
    )

    assert _convert(converter, content) == (
        "[00:00:01] Hello there.\n\n[01:02:05] Goodbye."
    )


def test_srt_multiline_cue_is_joined_and_markup_removed(
    converter: MarkItDown,
) -> None:
    content = (
        "1\n00:00:01,000 --> 00:00:02,000\n"
        '<i>Hello</i> <font color="red">there</font>.\n{\\an8}Second  line\n'
    )

    assert _convert(converter, content) == "[00:00:01] Hello there. Second line"


def test_srt_bom_and_non_ascii_are_preserved(converter: MarkItDown) -> None:
    content = "﻿1\n00:00:01,000 --> 00:00:02,000\nCafé 你好\n"

    assert _convert(converter, content, charset="utf-8") == "[00:00:01] Café 你好"


def test_srt_cue_without_number_and_without_text(converter: MarkItDown) -> None:
    content = (
        "00:00:01,000 --> 00:00:02,000\nNo number\n\n"
        "2\n00:00:03,000 --> 00:00:04,000\n\n\n"
        "3\n00:00:05.5 --> 00:00:06.5\nDot milliseconds\n"
    )

    assert _convert(converter, content) == (
        "[00:00:01] No number\n\n[00:00:05] Dot milliseconds"
    )


def test_srt_detected_without_extension(converter: MarkItDown) -> None:
    content = "1\n00:00:01,000 --> 00:00:02,000\nDetected\n"

    result = converter.convert_stream(io.BytesIO(content.encode()))

    assert result.markdown == "[00:00:01] Detected"


def test_srt_late_non_ascii_after_charset_sample(converter: MarkItDown) -> None:
    cue = "1\n00:00:01,000 --> 00:00:02,000\nplain ascii text\n\n"
    content = cue * 3000 + "2\n00:00:03,000 --> 00:00:04,000\nCafé 你好\n"
    assert len(content.encode()) > 65536

    result = _convert(converter, content, charset="ascii")

    assert result.endswith("[00:00:03] Café 你好")


def test_srt_missing_separator_and_blank_line_inside_cue(
    converter: MarkItDown,
) -> None:
    content = (
        "1\n00:00:01,000 --> 00:00:02,000\nHello\n"
        "2\n00:00:03,000 --> 00:00:04,000\nLine one\n\nLine two\n\n"
        "3\n00:00:05,000 --> 00:00:06,000\nEnd\n"
    )

    assert _convert(converter, content) == (
        "[00:00:01] Hello\n\n[00:00:03] Line one Line two\n\n[00:00:05] End"
    )


def test_srt_keeps_angle_brackets_that_are_not_styling(converter: MarkItDown) -> None:
    content = "1\n00:00:01,000 --> 00:00:02,000\n<Bob> if x<y and z>w <B>bold</B>\n"

    assert _convert(converter, content) == "[00:00:01] <Bob> if x<y and z>w bold"


def test_srt_hours_are_zero_padded(converter: MarkItDown) -> None:
    content = "1\n0:00:01,000 --> 0:00:02,000\nHi\n"

    assert _convert(converter, content) == "[00:00:01] Hi"


def test_srt_without_cues_falls_back_to_plain_text(converter: MarkItDown) -> None:
    assert _convert(converter, "just some plain text\n") == "just some plain text\n"
