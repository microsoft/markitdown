#!/usr/bin/env python3 -m pytest
import subprocess
import sys
from markitdown import __version__

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


def test_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--version"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), "Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, "Expected 'SYNTAX' to appear in STDERR"


def test_info_flag() -> None:
    import json
    import os
    tests_dir = os.path.dirname(__file__)
    docx_file = os.path.join(tests_dir, "test_files", "test.docx")
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--info", docx_file], capture_output=True, text=True
    )
    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["detected_converter"] == "DocxConverter"
    assert "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in data["mime_type"]
    assert data["size_bytes"] > 0
    assert data["path"] == docx_file


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    test_info_flag()
    print("All tests passed!")
