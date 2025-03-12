#!/usr/bin/env python3 -m pytest
import subprocess
import pytest
from markitdown import __version__


def test_version() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--version"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), f"Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, f"Expected 'SYNTAX' to appear in STDERR"


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
