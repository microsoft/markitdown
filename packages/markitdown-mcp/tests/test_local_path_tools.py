import asyncio
from pathlib import Path
from unittest.mock import Mock

import pytest
from mcp.server.mcpserver.exceptions import ToolError, UnexpectedToolError

from markitdown_mcp import __main__ as server

EXPECTED_MARKDOWN = "# Hello\n\nA **markitdown** fixture."

UNC_AND_DEVICE_PATHS = [
    r"\\attacker.example\share\sample.docx",
    "//attacker.example/share/sample.docx",
    r"\\?\UNC\attacker.example\share\sample.docx",
    r"\\.\pipe\sample",
]


def call_tool(name: str, arguments: dict):
    return asyncio.run(server.mcp.call_tool(name, arguments))


def tool_text(result) -> str:
    return "".join(block.text for block in result.content)


@pytest.fixture
def sample_dir(tmp_path: Path) -> Path:
    (tmp_path / "sample.md").write_text(EXPECTED_MARKDOWN + "\n")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "nested.md").write_text("nested\n")
    return tmp_path


def test_convert_file_converts_a_local_file(sample_dir):
    result = call_tool("convert_file", {"file_path": str(sample_dir / "sample.md")})

    assert EXPECTED_MARKDOWN in tool_text(result)


def test_convert_directory_converts_recursively(sample_dir):
    result = call_tool("convert_directory", {"dir_path": str(sample_dir)})

    text = tool_text(result)
    assert EXPECTED_MARKDOWN.splitlines()[0] in text
    assert "nested" in text


def test_convert_directory_can_stay_flat(sample_dir):
    result = call_tool(
        "convert_directory", {"dir_path": str(sample_dir), "recursive": False}
    )

    assert "nested" not in tool_text(result)


@pytest.mark.parametrize(
    "tool, argument",
    [
        ("convert_file", "file_path"),
        ("convert_directory", "dir_path"),
    ],
)
@pytest.mark.parametrize("path", UNC_AND_DEVICE_PATHS)
def test_unc_and_device_paths_are_rejected_before_resolution(
    monkeypatch, tool, argument, path
):
    """Resolving a UNC path already contacts the remote host, so the path must
    be rejected before Path.resolve() ever sees it."""
    resolve = Mock(side_effect=AssertionError("resolve() must not be reached"))
    monkeypatch.setattr(server.Path, "resolve", resolve)

    with pytest.raises(ToolError) as raised:
        call_tool(tool, {argument: path})

    assert not isinstance(raised.value, UnexpectedToolError)
    assert "UNC and Windows device paths are not supported" in str(raised.value)
    resolve.assert_not_called()


@pytest.mark.parametrize(
    "tool, argument",
    [
        ("convert_file", "file_path"),
        ("convert_directory", "dir_path"),
    ],
)
def test_missing_path_reports_errno_without_the_path(tmp_path, tool, argument):
    missing = tmp_path / "private" / "missing"

    with pytest.raises(ToolError) as raised:
        call_tool(tool, {argument: str(missing)})

    message = str(raised.value)
    assert not isinstance(raised.value, UnexpectedToolError)
    assert "Could not read the resource" in message
    assert str(missing) not in message


def test_convert_directory_rejects_a_file(sample_dir):
    with pytest.raises(ToolError) as raised:
        call_tool("convert_directory", {"dir_path": str(sample_dir / "sample.md")})

    assert not isinstance(raised.value, UnexpectedToolError)
    assert "Not a directory" in str(raised.value)
