#!/usr/bin/env python3 -m pytest
import builtins
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import markitdown.__main__ as cli
from markitdown import __version__

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


@pytest.mark.parametrize(
    ("arguments", "expected_kwargs"),
    [
        (["input.pdf", "--use-plugins"], {"enable_plugins": True}),
        (
            [
                "input.pdf",
                "--use-plugins",
                "--use-docintel",
                "--endpoint",
                "https://example.cognitiveservices.azure.com",
            ],
            {
                "enable_plugins": True,
                "docintel_endpoint": "https://example.cognitiveservices.azure.com",
            },
        ),
        (
            [
                "input.pdf",
                "--use-plugins",
                "--use-cu",
                "--cu-endpoint",
                "https://example.cognitiveservices.azure.com",
            ],
            {
                "enable_plugins": True,
                "cu_endpoint": "https://example.cognitiveservices.azure.com",
            },
        ),
    ],
)
def test_llm_options_are_forwarded_to_all_constructor_paths(
    monkeypatch, arguments, expected_kwargs
) -> None:
    class FakeOpenAIError(Exception):
        pass

    openai_client = Mock()
    openai_constructor = Mock(return_value=openai_client)
    markitdown_constructor = Mock(
        return_value=SimpleNamespace(
            convert=Mock(return_value=SimpleNamespace(markdown=""))
        )
    )
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(
            OpenAI=openai_constructor,
            OpenAIError=FakeOpenAIError,
        ),
    )
    monkeypatch.setattr(cli, "MarkItDown", markitdown_constructor)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "markitdown",
            *arguments,
            "--llm-client",
            "openai",
            "--llm-model",
            "gpt-4o",
        ],
    )

    cli.main()

    openai_constructor.assert_called_once_with()
    markitdown_constructor.assert_called_once_with(
        **expected_kwargs,
        llm_client=openai_client,
        llm_model="gpt-4o",
    )


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (["input.pdf", "--llm-model", "gpt-4o"], "--llm-model requires --llm-client."),
        (
            ["input.pdf", "--llm-client", "openai"],
            "--llm-client requires a non-empty --llm-model.",
        ),
        (
            ["input.pdf", "--llm-client", "openai", "--llm-model", ""],
            "--llm-client requires a non-empty --llm-model.",
        ),
    ],
)
def test_llm_options_require_client_and_model(
    monkeypatch, capsys, arguments, message
) -> None:
    monkeypatch.setattr(sys, "argv", ["markitdown", *arguments])

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2
    assert message in capsys.readouterr().err


def test_llm_client_rejects_unsupported_values(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        sys, "argv", ["markitdown", "input.pdf", "--llm-client", "azure-openai"]
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_openai_is_imported_only_when_requested(monkeypatch) -> None:
    import_module = builtins.__import__

    def fail_if_openai_imported(name, *args, **kwargs):
        if name == "openai":
            raise AssertionError("openai should not be imported without --llm-client")
        return import_module(name, *args, **kwargs)

    markitdown_constructor = Mock(
        return_value=SimpleNamespace(
            convert=Mock(return_value=SimpleNamespace(markdown=""))
        )
    )
    monkeypatch.setattr(builtins, "__import__", fail_if_openai_imported)
    monkeypatch.setattr(cli, "MarkItDown", markitdown_constructor)
    monkeypatch.setattr(sys, "argv", ["markitdown", "input.pdf"])

    cli.main()

    markitdown_constructor.assert_called_once_with(enable_plugins=False)


def test_openai_missing_package_error_is_actionable(monkeypatch, capsys) -> None:
    import_module = builtins.__import__

    def raise_missing_openai(name, *args, **kwargs):
        if name == "openai":
            raise ModuleNotFoundError("No module named 'openai'", name="openai")
        return import_module(name, *args, **kwargs)

    monkeypatch.delitem(sys.modules, "openai", raising=False)
    monkeypatch.setattr(builtins, "__import__", raise_missing_openai)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "markitdown",
            "input.pdf",
            "--llm-client",
            "openai",
            "--llm-model",
            "gpt-4o",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2
    assert "pip install openai" in capsys.readouterr().err


def test_openai_missing_api_key_error_is_actionable(monkeypatch, capsys) -> None:
    class FakeOpenAIError(Exception):
        pass

    openai_constructor = Mock(
        side_effect=FakeOpenAIError("The api_key client option must be set")
    )
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(
            OpenAI=openai_constructor,
            OpenAIError=FakeOpenAIError,
        ),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "markitdown",
            "input.pdf",
            "--llm-client",
            "openai",
            "--llm-model",
            "gpt-4o",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2
    assert "Set OPENAI_API_KEY" in capsys.readouterr().err


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    print("All tests passed!")
