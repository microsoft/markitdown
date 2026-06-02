#!/usr/bin/env python3 -m pytest
import subprocess
import sys

from markitdown import __version__

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


def test_extract_images_requires_output_dir() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--extract-images", "fake.pdf"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "--output-dir is required" in result.stdout


def test_help_lists_extract_images_options() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--extract-images" in result.stdout
    assert "--output-dir" in result.stdout


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    test_extract_images_requires_output_dir()
    test_help_lists_extract_images_options()
    print("All tests passed!")
