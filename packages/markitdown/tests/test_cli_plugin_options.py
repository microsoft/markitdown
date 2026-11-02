"""Custom converter options passed through the CLI."""

import io
import sys
from types import SimpleNamespace

import pytest

from markitdown import DocumentConverter, DocumentConverterResult
from markitdown.__main__ import main


@pytest.mark.parametrize("stdin", [False, True])
def test_plugin_options_reach_converter(monkeypatch, tmp_path, capsys, stdin):
    seen = []

    class PluginConverter(DocumentConverter):
        def accepts(self, file_stream, stream_info, **kwargs):
            return stream_info.extension == ".plugin"

        def convert(self, file_stream, stream_info, **kwargs):
            seen.append(kwargs)
            return DocumentConverterResult(markdown="plugin output")

    def register_converters(markitdown, **kwargs):
        markitdown.register_converter(PluginConverter())

    monkeypatch.setattr(
        "markitdown._markitdown._plugins",
        [SimpleNamespace(register_converters=register_converters)],
    )
    args = [
        "markitdown",
        "--use-plugins",
        "--plugin-option",
        "image_dir=./assets=original",
        "--plugin-option",
        "caption=",
    ]
    if stdin:
        monkeypatch.setattr(sys, "stdin", SimpleNamespace(buffer=io.BytesIO(b"data")))
        args += ["--extension", "plugin"]
    else:
        source = tmp_path / "document.plugin"
        source.write_bytes(b"data")
        args.append(str(source))
    monkeypatch.setattr(sys, "argv", args)

    main()

    assert capsys.readouterr().out.strip() == "plugin output"
    assert len(seen) == 1
    assert seen[0]["image_dir"] == "./assets=original"
    assert seen[0]["caption"] == ""
    assert seen[0]["keep_data_uris"] is False


@pytest.mark.parametrize(
    "options, message",
    [
        (["--plugin-option", "image_dir=assets"], "requires --use-plugins"),
        (["--use-plugins", "--plugin-option", "image_dir"], "NAME=VALUE"),
        (["--use-plugins", "--plugin-option", "=assets"], "option name"),
        (["--use-plugins", "--plugin-option", "bad-name=assets"], "option name"),
        (["--use-plugins", "--plugin-option", "_parent_converters=x"], "reserved"),
        (["--use-plugins", "--plugin-option", "keep_data_uris=True"], "reserved"),
        (["--use-plugins", "--plugin-option", "source=other"], "reserved"),
        (["--use-plugins", "--plugin-option", "self=other"], "reserved"),
        (["--use-plugins", "--plugin-option", "path=other"], "reserved"),
        (["--use-plugins", "--plugin-option", "stream=other"], "reserved"),
        (["--use-plugins", "--plugin-option", "uri=other"], "reserved"),
        (["--use-plugins", "--plugin-option", "llm_client=x"], "reserved"),
        (
            ["--use-plugins", "--plugin-option", "x=1", "--plugin-option", "x=2"],
            "Duplicate",
        ),
    ],
)
def test_invalid_plugin_options_fail_before_conversion(
    monkeypatch, capsys, options, message
):
    monkeypatch.setattr(sys, "argv", ["markitdown", *options, "missing.plugin"])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 2
    assert message in capsys.readouterr().err


def test_plugins_remain_disabled_without_flag(monkeypatch, tmp_path, capsys):
    def register_converters(*args, **kwargs):
        pytest.fail("plugins must remain disabled without --use-plugins")

    monkeypatch.setattr(
        "markitdown._markitdown._plugins",
        [SimpleNamespace(register_converters=register_converters)],
    )
    source = tmp_path / "plain.txt"
    source.write_text("ordinary text", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["markitdown", str(source)])

    main()

    assert capsys.readouterr().out.strip() == "ordinary text"
