#!/usr/bin/env python3 -m pytest
import os
import pytest
from typing import List
import dataclasses

if __name__ == "__main__":
    from _test_vectors import FileTestVector
else:
    from ._test_vectors import FileTestVector

from markitdown import (
    MarkItDown,
)

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

IMAGE_TEST_VECTOR = FileTestVector(
    filename="test_llm.jpg",
    mimetype="image/jpeg",
    charset=None,
    url=None,
    must_include=["# Description:", "Test description from LLM"],
    must_not_include=[],
)

def llm_describber_callback(data_uri: str, prompt: str) -> str:
    """A mock LLM describer callback for testing."""
    return "Test description from LLM"

def test_image_converter_with_llm_describber():
    """Test the ImageConverter with a custom llm_describber."""
    markitdown = MarkItDown()

    result = markitdown.convert(
        os.path.join(TEST_FILES_DIR, IMAGE_TEST_VECTOR.filename),
        llm_describber=llm_describber_callback,
    )

    for string in IMAGE_TEST_VECTOR.must_include:
        assert string in result.markdown
    for string in IMAGE_TEST_VECTOR.must_not_include:
        assert string not in result.markdown
