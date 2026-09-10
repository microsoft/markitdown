#!/usr/bin/env python3 -m pytest
import io
import subprocess
import sys
from types import SimpleNamespace

from markitdown import __version__
from markitdown.__main__ import main

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


def test_windows_pipe_input_is_buffered_before_conversion(monkeypatch, capsys) -> None:
    class WindowsPipe(io.BytesIO):
        def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
            if whence == io.SEEK_END:
                return super().seek(offset, whence)
            return 0

    stdin = SimpleNamespace(
        buffer=WindowsPipe(b"<html><body><h1>Test HTML</h1></body></html>")
    )
    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "argv", ["markitdown", "-x", "html"])

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "# Test HTML"


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
