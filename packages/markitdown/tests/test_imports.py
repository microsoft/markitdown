"""Check startup in fresh interpreters so other tests cannot hide eager imports."""

import os
from pathlib import Path
import subprocess
import sys
from textwrap import dedent

import pytest


@pytest.mark.parametrize("entrypoint", ["module", "console"])
@pytest.mark.parametrize(
    "args, returncode, expected",
    [
        (["--help"], 0, "Convert various file formats to markdown."),
        (["--version"], 0, "markitdown "),
        (["--foobar"], 2, "unrecognized arguments"),
        (["--list-plugins"], 0, "Installed MarkItDown 3rd-party Plugins:"),
    ],
)
def test_cli_without_conversion_dependencies(entrypoint, args, returncode, expected):
    # -S excludes site-packages, including all conversion dependencies. Point at
    # the source explicitly because editable installs also live in site-packages.
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    if entrypoint == "module":
        command = ["-m", "markitdown"]
    else:
        command = ["-c", "from markitdown.__main__ import main; main()"]
    result = subprocess.run(
        [sys.executable, "-S", *command, *args],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == returncode, result.stderr
    assert expected in result.stdout + result.stderr


def test_public_exports():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            dedent(
                """
                import sys
                import markitdown

                assert "markitdown._markitdown" not in sys.modules
                assert set(markitdown.__all__) <= set(dir(markitdown))
                assert not hasattr(markitdown, "unknown_export")
                assert "markitdown._markitdown" not in sys.modules

                from markitdown import MarkItDown
                from markitdown import _markitdown

                assert MarkItDown is _markitdown.MarkItDown
                assert vars(markitdown)["MarkItDown"] is MarkItDown

                namespace = {}
                exec("from markitdown import *", namespace)
                for name in markitdown.__all__:
                    assert namespace[name] is getattr(markitdown, name)
                for name in (
                    "PRIORITY_SPECIFIC_FILE_FORMAT",
                    "PRIORITY_GENERIC_FILE_FORMAT",
                ):
                    assert namespace[name] is getattr(_markitdown, name)
                    assert vars(markitdown)[name] is namespace[name]
                """
            ),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
