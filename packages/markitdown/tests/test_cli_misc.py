#!/usr/bin/env python3 -m pytest
import subprocess
from markitdown import __version__

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


def test_version() -> None:
    result = subprocess.run(
        ["python3", "-m", "markitdown", "--version"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag() -> None:
    result = subprocess.run(
        ["python3", "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), "Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, "Expected 'SYNTAX' to appear in STDERR"


def test_batch_help() -> None:
    """Test that batch options are available in help"""
    result = subprocess.run(
        ["python3", "-m", "markitdown", "--help"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert "--batch" in result.stdout, "Expected --batch option in help"
    assert "--recursive" in result.stdout, "Expected --recursive option in help"
    assert "--types" in result.stdout, "Expected --types option in help"


def test_batch_missing_directory() -> None:
    """Test that batch mode requires a directory"""
    result = subprocess.run(
        ["python3", "-m", "markitdown", "--batch"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert "Directory path is required" in result.stdout, "Expected directory requirement message"


def test_batch_nonexistent_directory() -> None:
    """Test that batch mode handles nonexistent directory"""
    result = subprocess.run(
        ["python3", "-m", "markitdown", "--batch", "/nonexistent/directory"], 
        capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert "Directory does not exist" in result.stdout, "Expected directory existence check"


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    test_batch_help()
    test_batch_missing_directory()
    test_batch_nonexistent_directory()
    print("All tests passed!")
