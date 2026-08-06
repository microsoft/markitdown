#!/usr/bin/env python3 -m pytest
import io

from markitdown import MarkItDown, StreamInfo
from markitdown.converter_utils.charset import decode_text

# Charset detection only inspects the first 4k of a stream, so the non-ASCII bytes in
# these fixtures are placed well past that boundary to exercise the misdetection path.
PADDING = "a" * 5000
ACCENTED_TEXT = "Considerações de segurança: acentuação e cedilha."


def test_utf8_bytes_after_detection_window() -> None:
    """A UTF-8 file that looks like ASCII in its first 4k must still convert."""
    content = (PADDING + "\n" + ACCENTED_TEXT + "\n").encode("utf-8")

    markitdown = MarkItDown()
    result = markitdown.convert_stream(
        io.BytesIO(content), stream_info=StreamInfo(extension=".md")
    )

    assert ACCENTED_TEXT in result.markdown


def test_csv_utf8_bytes_after_detection_window() -> None:
    """The same misdetection must not break the CSV converter."""
    content = ("header\n" + PADDING + "\n" + ACCENTED_TEXT + "\n").encode("utf-8")

    markitdown = MarkItDown()
    result = markitdown.convert_stream(
        io.BytesIO(content), stream_info=StreamInfo(extension=".csv")
    )

    assert ACCENTED_TEXT in result.markdown


def test_decode_text_recovers_from_wrong_charset() -> None:
    """A charset that fails on the full content must not raise.

    'ascii' fits the first 4k but not the accented tail. Re-detection then picks the
    encoding it judges best. Which one that is depends on charset_normalizer's
    heuristics, so the guarantee under test is that decoding yields usable text
    instead of raising UnicodeDecodeError.
    """
    content = (PADDING + "\n" + ACCENTED_TEXT + "\n").encode("cp1252")

    decoded = decode_text(content, "ascii")

    assert isinstance(decoded, str)
    assert PADDING in decoded


def test_decode_text_honors_a_valid_charset() -> None:
    """An explicit charset that does decode the content is used as given."""
    content = ACCENTED_TEXT.encode("cp1252")

    assert decode_text(content, "cp1252") == ACCENTED_TEXT


def test_decode_text_without_charset() -> None:
    """With no charset supplied, detection runs over the whole content."""
    content = (PADDING + "\n" + ACCENTED_TEXT + "\n").encode("utf-8")

    assert ACCENTED_TEXT in decode_text(content, None)


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    for test in [
        test_utf8_bytes_after_detection_window,
        test_csv_utf8_bytes_after_detection_window,
        test_decode_text_recovers_from_wrong_charset,
        test_decode_text_honors_a_valid_charset,
        test_decode_text_without_charset,
    ]:
        print(f"Running {test.__name__}...", end="")
        test()
        print("OK")
    print("All tests passed!")
