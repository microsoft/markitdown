import os
import shutil
from pathlib import Path

import pytest

from markitdown import MarkItDown

TEST_FILES_DIR = Path(__file__).parent.parent / "test_files"

# Skip exiftool tests if not installed
skip_exiftool = shutil.which("exiftool") is None

JPG_TEST_EXIFTOOL = {
    "Author": "AutoGen Authors",
    "Title": "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
    "Description": "AutoGen enables diverse LLM-based applications",
    "ImageSize": "1615x1967",
    "DateTimeOriginal": "2024:03:14 22:10:00",
}


@pytest.mark.skipif(
    skip_exiftool,
    reason="do not run if exiftool is not installed",
)
def test_markitdown_exiftool() -> None:
    markitdown = MarkItDown()

    # Test JPG metadata processing
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test.jpg"))
    for key in JPG_TEST_EXIFTOOL:
        target = f"{key}: {JPG_TEST_EXIFTOOL[key]}"
        assert target in result.text_content
