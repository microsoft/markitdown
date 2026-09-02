from __future__ import annotations

import threading
from types import SimpleNamespace

import pytest

from markitdown_mcp import __main__ as main


@pytest.mark.anyio
async def test_convert_to_markdown_runs_conversion_off_event_loop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_loop_thread = threading.get_ident()
    conversion_thread: list[int] = []

    class FakeMarkItDown:
        def __init__(self, *, enable_plugins: bool) -> None:
            self.enable_plugins = enable_plugins

        def convert_uri(self, uri: str) -> SimpleNamespace:
            conversion_thread.append(threading.get_ident())
            return SimpleNamespace(markdown=f"converted:{uri}")

    monkeypatch.setattr(main, "MarkItDown", FakeMarkItDown)

    result = await main.convert_to_markdown("https://example.com/test.txt")

    assert result == "converted:https://example.com/test.txt"
    assert conversion_thread == [conversion_thread[0]]
    assert conversion_thread[0] != event_loop_thread
