#!/usr/bin/env python3 -m pytest
import os
import subprocess
import tempfile
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


def test_cli_multi_file_stdout():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "test.docx"),
            os.path.join(TEST_FILES_DIR, "test.pdf"),
        ],
        capture_output=True, text=True,
        cwd=os.path.join(os.path.dirname(__file__), ".."),
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert "--- " in result.stdout


def test_cli_multi_file_output_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        result = subprocess.run(
            [
                "python", "-m", "markitdown",
                os.path.join(TEST_FILES_DIR, "test.docx"),
                os.path.join(TEST_FILES_DIR, "test.pdf"),
                "--output-dir", tmp_dir,
            ],
            capture_output=True, text=True,
            cwd=os.path.join(os.path.dirname(__file__), ".."),
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        assert os.path.exists(os.path.join(tmp_dir, "test.docx.md"))
        assert os.path.exists(os.path.join(tmp_dir, "test.pdf.md"))


def test_cli_multi_file_fail_fast():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "nonexistent_xyz.pdf"),
            "--fail-fast",
        ],
        capture_output=True, text=True,
        cwd=os.path.join(os.path.dirname(__file__), ".."),
    )
    assert result.returncode == 1


def test_cli_multi_file_collect_errors():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "test.docx"),
            os.path.join(TEST_FILES_DIR, "nonexistent_xyz.pdf"),
        ],
        capture_output=True, text=True,
        cwd=os.path.join(os.path.dirname(__file__), ".."),
    )
    assert result.returncode == 1
    assert "Error" in result.stderr


def test_cli_workers_flag():
    result = subprocess.run(
        [
            "python", "-m", "markitdown",
            os.path.join(TEST_FILES_DIR, "test.docx"),
            os.path.join(TEST_FILES_DIR, "test.pdf"),
            "--workers", "2",
        ],
        capture_output=True, text=True,
        cwd=os.path.join(os.path.dirname(__file__), ".."),
    )
    assert result.returncode == 0


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
