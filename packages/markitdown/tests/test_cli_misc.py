"""CLI behavior outside the shared file-vector matrix."""

import io
import os
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from markitdown import __version__
from markitdown.__main__ import main
from markitdown.converters._cu_converter import ContentUnderstandingFileType


# CLI behavior

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


# Service flags and endpoints

# ---------------------------------------------------------------------------
# CLI argument tests
# ---------------------------------------------------------------------------


class TestCLIArgs:
    """Test CLI argument parsing for CU flags."""

    def test_use_cu_without_endpoint_exits(self):
        """--use-cu without --cu-endpoint should exit with error."""
        import subprocess

        result = subprocess.run(
            [sys.executable, "-m", "markitdown", "--use-cu", "fake.pdf"],
            capture_output=True,
            text=True,
            env={**os.environ, "MARKITDOWN_CU_ENDPOINT": ""},
        )
        assert result.returncode != 0
        assert (
            "cu-endpoint" in result.stderr.lower()
            or "cu-endpoint" in (result.stdout or "").lower()
        )

    def test_use_cu_and_use_docintel_mutually_exclusive(self):
        """--use-cu and --use-docintel cannot be used together."""
        import subprocess

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake",
                "--use-docintel",
                "-e",
                "https://fake-di",
                "fake.pdf",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2, result.stderr
        assert (
            "argument -d/--use-docintel: not allowed with argument "
            "--use-cu/--use-content-understanding"
        ) in result.stderr, result.stderr

    def test_cu_file_types_parsing(self):
        """--cu-file-types should parse comma-separated values into enum list."""
        from markitdown.converters import ContentUnderstandingFileType

        raw = "pdf,jpeg,mp4"
        type_names = [t.strip().lower() for t in raw.split(",") if t.strip()]
        cu_types = [ContentUnderstandingFileType(name) for name in type_names]

        assert cu_types == [
            ContentUnderstandingFileType.PDF,
            ContentUnderstandingFileType.JPEG,
            ContentUnderstandingFileType.MP4,
        ]

    def test_cu_file_types_invalid_value(self):
        """Unknown file type name should raise ValueError."""
        from markitdown.converters import ContentUnderstandingFileType

        with pytest.raises(ValueError):
            ContentUnderstandingFileType("nonsense")

    def test_cu_file_types_single_value(self):
        """Single file type (no comma) should parse correctly."""
        from markitdown.converters import ContentUnderstandingFileType

        cu_types = [
            ContentUnderstandingFileType(t.strip().lower())
            for t in "wav".split(",")
            if t.strip()
        ]
        assert cu_types == [ContentUnderstandingFileType.WAV]

    def test_use_cu_wires_kwargs_to_markitdown(self, capsys):
        """--use-cu should pass CU options through to MarkItDown."""
        import markitdown.__main__ as markitdown_cli

        markitdown_instance = MagicMock()
        markitdown_instance.convert.return_value.markdown = "converted"
        markitdown_cls = MagicMock(return_value=markitdown_instance)

        with patch.object(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake-cu",
                "--cu-analyzer",
                "custom-analyzer",
                "--cu-file-types",
                "pdf,jpeg,mp4",
                "fake.pdf",
            ],
        ), patch.object(markitdown_cli, "MarkItDown", markitdown_cls):
            markitdown_cli.main()

        markitdown_cls.assert_called_once_with(
            enable_plugins=False,
            cu_endpoint="https://fake-cu",
            cu_analyzer_id="custom-analyzer",
            cu_file_types=[
                ContentUnderstandingFileType.PDF,
                ContentUnderstandingFileType.JPEG,
                ContentUnderstandingFileType.MP4,
            ],
        )
        markitdown_instance.convert.assert_called_once_with(
            "fake.pdf", stream_info=None, keep_data_uris=False
        )
        assert capsys.readouterr().out == "converted\n"

    def test_use_cu_reads_from_stdin(self, capsys):
        """--use-cu should preserve the CLI's filename-optional stdin mode."""
        import markitdown.__main__ as markitdown_cli

        input_buffer = io.BytesIO(b"fake pdf")
        stdin = MagicMock(buffer=input_buffer)
        markitdown_instance = MagicMock()
        markitdown_instance.convert_stream.return_value.markdown = "converted"
        markitdown_cls = MagicMock(return_value=markitdown_instance)

        with patch.object(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake-cu",
            ],
        ), patch.object(sys, "stdin", stdin), patch.object(
            markitdown_cli, "MarkItDown", markitdown_cls
        ):
            markitdown_cli.main()

        markitdown_cls.assert_called_once_with(
            enable_plugins=False,
            cu_endpoint="https://fake-cu",
        )

        assert markitdown_instance.convert_stream.call_count == 1
        call_args, call_kwargs = markitdown_instance.convert_stream.call_args
        assert call_args[0].read() == b"fake pdf"
        assert call_kwargs == {"stream_info": None, "keep_data_uris": False}
        assert capsys.readouterr().out == "converted\n"


# ---------------------------------------------------------------------------
# Endpoint environment variables (issue #2326)
# ---------------------------------------------------------------------------


class TestEndpointEnvVars:
    """Endpoint flags fall back to operator-configured environment variables."""

    @pytest.mark.parametrize(
        "env_var, argv, kwarg",
        [
            (
                "MARKITDOWN_CU_ENDPOINT",
                ["markitdown", "--use-cu", "fake.pdf"],
                "cu_endpoint",
            ),
            (
                "MARKITDOWN_DOCINTEL_ENDPOINT",
                ["markitdown", "-d", "fake.pdf"],
                "docintel_endpoint",
            ),
        ],
    )
    def test_endpoint_read_from_environment(self, monkeypatch, env_var, argv, kwarg):
        """With the env var set, the endpoint flag can be omitted entirely."""
        from markitdown.__main__ import main

        monkeypatch.setenv(env_var, "https://from-env")
        monkeypatch.setattr(sys, "argv", argv)

        with patch("markitdown.__main__.MarkItDown") as mock_markitdown:
            main()

        assert mock_markitdown.call_args.kwargs[kwarg] == "https://from-env"

    def test_flag_overrides_environment(self, monkeypatch):
        """Fails if the env var is ever read after parsing instead of as an argparse default."""
        from markitdown.__main__ import main

        monkeypatch.setenv("MARKITDOWN_CU_ENDPOINT", "https://from-env")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://from-flag",
                "fake.pdf",
            ],
        )

        with patch("markitdown.__main__.MarkItDown") as mock_markitdown:
            main()

        assert mock_markitdown.call_args.kwargs["cu_endpoint"] == "https://from-flag"

    def test_empty_environment_variable_is_treated_as_unset(self, monkeypatch, capsys):
        """An empty env var must not pass as a valid endpoint."""
        from markitdown.__main__ import main

        monkeypatch.setenv("MARKITDOWN_CU_ENDPOINT", "")
        monkeypatch.setattr(sys, "argv", ["markitdown", "--use-cu", "fake.pdf"])

        with pytest.raises(SystemExit):
            main()

        assert "MARKITDOWN_CU_ENDPOINT" in capsys.readouterr().out


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
