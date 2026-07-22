#!/usr/bin/env python3 -m pytest
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


def test_extract_images_to(tmp_path) -> None:
    """End-to-end CLI: --extract-images-to should write images to disk and
    reference them in the markdown printed on stdout."""
    out_dir = tmp_path / "imgs"
    pptx_path = os.path.join(TEST_FILES_DIR, "test.pptx")
    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            "--extract-images-to",
            str(out_dir),
            pptx_path,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert out_dir.is_dir(), "extraction directory should be created"
    written = [p for p in out_dir.iterdir() if p.is_file()]
    assert written, "at least one image should have been extracted"
    # Markdown links use the user-supplied path joined with the filename
    # (forward-slash form), matching whatever was passed on the CLI.
    expected_prefix = str(out_dir).replace("\\", "/")
    for path in written:
        assert path.stat().st_size > 0, f"{path} is empty"
        assert f"]({expected_prefix}/{path.name})" in result.stdout


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
