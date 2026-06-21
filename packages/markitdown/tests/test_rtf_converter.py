#!/usr/bin/env python3 -m pytest
import os

from markitdown import MarkItDown, StreamInfo

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

RTF_TEST_STRINGS = [
    "RTF Test Document 8f14e45f",
    "This is a plain paragraph c4ca4238 with some bold a87ff679 text.",
    "Italic line e4da3b7f appears here.",
    "A second paragraph 1679091c with more content.",
]


def test_rtf_converter_local() -> None:
    """RTF files convert to Markdown with control words stripped."""
    markitdown = MarkItDown()
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test.rtf"))
    for s in RTF_TEST_STRINGS:
        assert s in result.markdown
    # Control words must not leak into the output.
    assert "\\rtf1" not in result.markdown
    assert "\\par" not in result.markdown


def test_rtf_converter_stream() -> None:
    """RTF conversion works from a binary stream with explicit StreamInfo."""
    markitdown = MarkItDown()
    with open(os.path.join(TEST_FILES_DIR, "test.rtf"), "rb") as stream:
        result = markitdown.convert(
            stream, stream_info=StreamInfo(extension=".rtf", mimetype="application/rtf")
        )
    for s in RTF_TEST_STRINGS:
        assert s in result.markdown


if __name__ == "__main__":
    test_rtf_converter_local()
    test_rtf_converter_stream()
    print("All RTF converter tests passed.")
