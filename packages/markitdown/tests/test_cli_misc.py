#!/usr/bin/env python3 -m pytest
import io
import subprocess
import sys
from types import SimpleNamespace

import pytest

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


@pytest.mark.parametrize("from_stdin", [False, True], ids=["file", "stdin"])
@pytest.mark.parametrize(
    "options, expected",
    [
        ([], "H2O and x2"),
        (
            ["--sub-symbol", "<sub>", "--sup-symbol", "<sup>"],
            "H<sub>2</sub>O and x<sup>2</sup>",
        ),
        (["--sub-symbol", "~", "--sup-symbol", "^"], "H~2~O and x^2^"),
        (["--sub-symbol", "", "--sup-symbol", "^"], "H2O and x^2^"),
    ],
)
def test_subscript_superscript_options(tmp_path, from_stdin, options, expected):
    from .test_module_misc import _write_underlined_docx

    path = tmp_path / "scripts.docx"
    _write_underlined_docx(
        path,
        paragraph_xml=(
            "<w:r><w:t>H</w:t></w:r>"
            '<w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t>2</w:t></w:r>'
            '<w:r><w:t xml:space="preserve">O and x</w:t></w:r>'
            '<w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:t>2</w:t></w:r>'
        ),
    )
    command = [sys.executable, "-m", "markitdown", *options]
    command += ["--extension", "docx"] if from_stdin else [str(path)]
    result = subprocess.run(
        command, input=path.read_bytes() if from_stdin else None, capture_output=True
    )
    assert result.returncode == 0, result.stderr.decode()
    assert result.stdout.decode().strip() == expected


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
