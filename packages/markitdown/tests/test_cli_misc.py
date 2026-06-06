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


def test_help_includes_agent_help_breadcrumb() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert "LLM agent? Use --agent-help for token-optimized usage." in result.stdout


def test_agent_help_outputs_ahf_without_running_conversion() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--agent-help"],
        input="plain text that must not be converted",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert result.stdout.startswith(
        "ah1 markitdown :: convert files and streams to markdown\n"
    )
    assert (
        "cmd markitdown [filename] [--output path] [--extension str] [--mime-type str] [--charset str] :: convert input to markdown"
        in result.stdout
    )
    assert "more? markitdown --agent-help" in result.stdout
    assert "ah2 markitdown" in result.stdout
    assert (
        "use markitdown [filename] [--output path] [--extension str] [--mime-type str] [--charset str]"
        in result.stdout
    )
    assert (
        "arg filename:path opt :: input file path; omit to read from stdin"
        in result.stdout
    )
    assert (
        "flag --use-docintel:bool opt :: use Azure Document Intelligence; requires --endpoint and filename"
        in result.stdout
    )
    assert (
        "flag --use-cu:bool opt :: use Azure Content Understanding; requires --cu-endpoint and filename"
        in result.stdout
    )
    assert "ex markitdown example.pdf -o example.md" in result.stdout
    assert "plain text that must not be converted" not in result.stdout


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
    assert not result.stderr.startswith("err ")


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
