"""Resource-usage guarantees for the MCP server.

One server process is started per MCP client session (e.g. every Claude Code
window), so idle footprint and per-call overhead multiply quickly.
"""

import asyncio
import json
import os
import subprocess
import sys
import threading
import time
from unittest.mock import Mock

from markitdown_mcp import __main__ as server


def call_convert(uri: str = "https://example.com/sample.pdf"):
    return server.mcp.call_tool("convert_to_markdown", {"uri": uri})


def test_import_defers_heavy_dependencies_and_caps_blas_threads():
    """Startup must not pay for markitdown's converter stack (numpy, onnxruntime,
    pandas, ...) until a conversion is requested, and numpy's OpenBLAS must not
    reserve a buffer per CPU core (~360MB on a 12-core machine)."""
    probe = (
        "import json, os, sys\n"
        "import markitdown_mcp.__main__\n"
        "print(json.dumps({\n"
        "  'heavy': sorted(m for m in ('markitdown', 'numpy', 'onnxruntime',"
        " 'magika', 'pandas') if m in sys.modules),\n"
        "  'openblas': os.environ.get('OPENBLAS_NUM_THREADS'),\n"
        "}))\n"
    )
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")
    }
    result = subprocess.run(
        [sys.executable, "-c", probe],
        capture_output=True,
        text=True,
        env=env,
        timeout=300,
        check=True,
    )
    report = json.loads(result.stdout.strip().splitlines()[-1])
    assert report["heavy"] == []
    assert report["openblas"] == "1"


def test_converter_is_built_once_and_reused(monkeypatch):
    converter = Mock()
    converter.convert_uri.return_value.markdown = "# ok"
    factory = Mock(return_value=converter)
    monkeypatch.setattr(server, "MarkItDown", factory)

    async def run():
        for _ in range(3):
            await call_convert()

    asyncio.run(run())

    assert factory.call_count == 1
    assert converter.convert_uri.call_count == 3


def test_conversion_does_not_block_the_event_loop(monkeypatch):
    """A slow conversion must run off the event loop so the server keeps
    answering pings, cancellations and other requests meanwhile."""
    converting = threading.Event()
    loop_ran_meanwhile = threading.Event()

    def slow_convert(uri):
        converting.set()
        # Stay busy until the event loop proves it is still running. A blocked
        # loop never can, so this times out; a free one answers in milliseconds.
        loop_ran_meanwhile.wait(timeout=5)
        return Mock(markdown="# slow")

    converter = Mock()
    converter.convert_uri.side_effect = slow_convert
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    async def run():
        async def watcher():
            while True:
                await asyncio.sleep(0.01)
                if converting.is_set():
                    loop_ran_meanwhile.set()

        watch_task = asyncio.create_task(watcher())
        try:
            await call_convert()
        finally:
            watch_task.cancel()

    asyncio.run(run())
    assert converting.is_set()
    assert loop_ran_meanwhile.is_set()


def test_conversions_on_the_shared_converter_are_serialized(monkeypatch):
    """Converters keep per-call state on the instance (e.g. RssConverter sets
    self._kwargs), so the shared instance must never convert concurrently."""
    active = 0
    peak = 0
    guard = threading.Lock()

    def convert(uri):
        nonlocal active, peak
        with guard:
            active += 1
            peak = max(peak, active)
        time.sleep(0.1)
        with guard:
            active -= 1
        return Mock(markdown="# ok")

    converter = Mock()
    converter.convert_uri.side_effect = convert
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    async def run():
        await asyncio.gather(*(call_convert() for _ in range(4)))

    asyncio.run(run())

    assert converter.convert_uri.call_count == 4
    assert peak == 1


def test_fetches_have_a_default_timeout(monkeypatch):
    """A hung remote server must not hold the (serialized) converter forever."""
    converter = Mock()
    converter.convert_uri.return_value.markdown = "# ok"
    factory = Mock(return_value=converter)
    monkeypatch.setattr(server, "MarkItDown", factory)
    asyncio.run(call_convert())

    session = factory.call_args.kwargs["requests_session"]
    assert "text/markdown" in session.headers["Accept"]

    sent = Mock()
    monkeypatch.setattr(server.requests.Session, "request", sent)
    session.get("https://example.com/sample.pdf")
    assert sent.call_args.kwargs["timeout"] is not None

    session.get("https://example.com/sample.pdf", timeout=5)
    assert sent.call_args.kwargs["timeout"] == 5
