#!/usr/bin/env python3 -m pytest
import os
import pytest

from markitdown import AsyncMarkItDown

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

DOCX_TEST_STRINGS = [
    "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
    "49e168b7-d2ae-407f-a055-2167576f39a1",
    "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
    "# Abstract",
    "# Introduction",
]

@pytest.mark.asyncio
async def test_async_markitdown_basic():
    """Test basic async functionality with a local file."""
    async with AsyncMarkItDown() as markitdown:
        result = await markitdown.convert(os.path.join(TEST_FILES_DIR, "test.docx"))
        
        # Verify the conversion worked as expected
        for test_string in DOCX_TEST_STRINGS:
            text_content = result.text_content.replace("\\", "")
            assert test_string in text_content

if __name__ == "__main__":
    pytest.main([__file__])