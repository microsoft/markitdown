#!/usr/bin/env python3 -m pytest
import json
import os
import subprocess
from markitdown import __version__

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


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
    ), "Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, "Expected 'SYNTAX' to appear in STDERR"


def test_info_outputs_xlsx_metadata_without_conversion() -> None:
    test_file = os.path.join(TEST_FILES_DIR, "test.xlsx")

    result = subprocess.run(
        ["python", "-m", "markitdown", "--info", test_file],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    info = json.loads(result.stdout)

    assert set(info.keys()) == {
        "path",
        "size_bytes",
        "mime_type",
        "extension",
        "charset",
        "detected_converter",
        "page_count",
        "image_count",
        "table_count",
        "estimated_tokens",
        "warning",
    }
    assert info["path"] == test_file
    assert info["size_bytes"] == os.path.getsize(test_file)
    assert info["mime_type"] is not None
    assert info["extension"] == ".xlsx"
    assert info["detected_converter"] == "XlsxConverter"
    assert info["page_count"] is None
    assert info["image_count"] is None
    assert info["table_count"] is None
    assert info["estimated_tokens"] is None
    assert info["warning"] is None
    assert "## Sheet1" not in result.stdout
    assert "Alpha" not in result.stdout


def test_info_outputs_warning_for_unsupported_file() -> None:
    test_file = os.path.join(TEST_FILES_DIR, "random.bin")

    result = subprocess.run(
        ["python", "-m", "markitdown", "--info", test_file],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    info = json.loads(result.stdout)

    assert info["path"] == test_file
    assert info["size_bytes"] == os.path.getsize(test_file)
    assert info["extension"] == ".bin"
    assert info["detected_converter"] is None
    assert info["warning"] == "No converter detected for this file."


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    test_info_outputs_xlsx_metadata_without_conversion()
    test_info_outputs_warning_for_unsupported_file()
    print("All tests passed!")
