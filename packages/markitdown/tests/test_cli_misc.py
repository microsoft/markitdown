#!/usr/bin/env python3 -m pytest
import argparse
import io
import subprocess
import sys
from markitdown import __version__
from markitdown.__main__ import _handle_output
from markitdown._base_converter import DocumentConverterResult

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


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


def test_stdin_dash_filename() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "-", "-x", "txt"],
        input=b"Hello from stdin dash mode",
        capture_output=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr!r}"
    stdout = result.stdout.decode("utf-8", errors="replace")
    assert "Hello from stdin dash mode" in stdout


def test_docintel_rejects_stdin_dash() -> None:
    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            "-",
            "-d",
            "-e",
            "https://example.cognitiveservices.azure.com/",
        ],
        input=b"dummy",
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "stdin is not supported" in result.stdout


def test_handle_output_stdout_encoding_none(monkeypatch) -> None:
    class DummyStdout(io.StringIO):
        @property
        def encoding(self):
            return None

    dummy = DummyStdout()
    monkeypatch.setattr(sys, "stdout", dummy)

    args = argparse.Namespace(output=None)
    result = DocumentConverterResult("Hello ✅")
    _handle_output(args, result)

    assert "Hello ✅" in dummy.getvalue()


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    test_stdin_dash_filename()
    test_docintel_rejects_stdin_dash()
    print("All tests passed!")
