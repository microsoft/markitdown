#!/usr/bin/env python3 -m pytest
import subprocess
import sys
from pathlib import Path
from markitdown import __version__


TEST_FILES_DIR = Path(__file__).parent / "test_files"

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


def test_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--foobar"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), "Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, "Expected 'SYNTAX' to appear in STDERR"


def test_include_docx_comments() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "markitdown",
            str(TEST_FILES_DIR / "test_with_comment.docx"),
            "--include-comments",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert "This is a test comment. 12df-321a" in result.stdout


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
