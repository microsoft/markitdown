#!/usr/bin/env python3 -m pytest
import os

from markitdown import MarkItDown, StreamInfo
from markitdown_sample_plugin import RtfConverter

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

RTF_TEST_STRINGS = {
    "This is a Sample RTF File",
    "It is included to test if the MarkItDown sample plugin can correctly convert RTF files.",
}


def test_converter() -> None:
    """Tests the RTF converter dirctly."""
    with open(os.path.join(TEST_FILES_DIR, "test.rtf"), "rb") as file_stream:
        converter = RtfConverter()
        result = converter.convert(
            file_stream=file_stream,
            stream_info=StreamInfo(
                mimetype="text/rtf", extension=".rtf", filename="test.rtf"
            ),
        )

        for test_string in RTF_TEST_STRINGS:
            assert test_string in result.text_content


def test_markitdown() -> None:
    """Tests that MarkItDown correctly loads the plugin."""
    md = MarkItDown(enable_plugins=True)
    result = md.convert(os.path.join(TEST_FILES_DIR, "test.rtf"))

    for test_string in RTF_TEST_STRINGS:
        assert test_string in result.text_content


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_converter()
    test_markitdown()
    print("All tests passed.")
