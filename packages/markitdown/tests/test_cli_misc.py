#!/usr/bin/env python3 -m pytest
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from markitdown import __version__

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


def test_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--version"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), "Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, "Expected 'SYNTAX' to appear in STDERR"


def test_llm_cli_options_are_passed_to_markitdown(monkeypatch, capsys) -> None:
    import markitdown.__main__ as markitdown_cli

    llm_client = object()
    markitdown_instance = Mock()
    markitdown_instance.convert.return_value = SimpleNamespace(markdown="converted")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "markitdown",
            "document.pdf",
            "--use-plugins",
            "--llm-client",
            "openai",
            "--llm-model",
            "gpt-4o",
            "--llm-prompt",
            "Extract the text.",
        ],
    )

    with (
        patch.object(markitdown_cli, "_create_llm_client", return_value=llm_client) as create_llm_client,
        patch.object(markitdown_cli, "MarkItDown", return_value=markitdown_instance) as markitdown_cls,
    ):
        markitdown_cli.main()

    create_llm_client.assert_called_once_with("openai")
    markitdown_cls.assert_called_once_with(
        enable_plugins=True,
        llm_client=llm_client,
        llm_model="gpt-4o",
        llm_prompt="Extract the text.",
    )
    markitdown_instance.convert.assert_called_once_with(
        "document.pdf", stream_info=None, keep_data_uris=False
    )
    assert capsys.readouterr().out.strip() == "converted"


def test_llm_model_requires_llm_client(monkeypatch, capsys) -> None:
    import markitdown.__main__ as markitdown_cli

    monkeypatch.setattr(sys, "argv", ["markitdown", "document.pdf", "--llm-model", "gpt-4o"])

    with pytest.raises(SystemExit):
        markitdown_cli.main()

    assert "--llm-model and --llm-prompt require --llm-client" in capsys.readouterr().out


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
