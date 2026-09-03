#!/usr/bin/env python3 -m pytest
"""Drive the stdio server through both MCP handshake eras.

The server must answer clients that open with the legacy `initialize`
handshake as well as clients that open with the 2026-07-28 `server/discover`
request, since both are in use across MCP hosts.
"""

import json
import os
import subprocess
import sys
import tempfile
import threading
import time

import pytest

MODERN_ENVELOPE = {
    "io.modelcontextprotocol/clientCapabilities": {},
    "io.modelcontextprotocol/clientInfo": {"name": "test", "version": "0"},
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
}

EXPECTED_MARKDOWN = "# Hello\n\nA **markitdown** fixture."


@pytest.fixture
def fixture_uri():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "sample.md")
        with open(path, "w") as fh:
            fh.write(EXPECTED_MARKDOWN + "\n")
        yield "file://" + path


def run_server(requests, expected_responses):
    """Feed newline-delimited requests to the stdio server, return the responses.

    Stdin is held open until the expected responses arrive: closing it early
    tears the server down before an in-flight request can be answered.
    """
    process = subprocess.Popen(
        [sys.executable, "-m", "markitdown_mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    responses = []
    try:
        for request in requests:
            process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()

        reader = threading.Thread(
            target=lambda: [
                responses.append(json.loads(line))
                for line in process.stdout
                if line.strip()
            ],
            daemon=True,
        )
        reader.start()

        deadline = time.monotonic() + 60
        while len(responses) < expected_responses and time.monotonic() < deadline:
            time.sleep(0.05)
    finally:
        process.stdin.close()
        process.terminate()
        process.wait(timeout=10)
    return sorted(responses, key=lambda response: response["id"])


def test_legacy_initialize_handshake(fixture_uri):
    """A client opening with `initialize` gets the pre-2026 protocol."""
    responses = run_server(
        [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "0"},
                },
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "convert_to_markdown",
                    "arguments": {"uri": fixture_uri},
                },
            },
        ],
        expected_responses=2,
    )

    assert responses[0]["result"]["serverInfo"]["name"] == "markitdown"
    call = responses[1]["result"]
    assert call["isError"] is False
    assert EXPECTED_MARKDOWN in call["content"][0]["text"]


def test_modern_discover_handshake(fixture_uri):
    """A client opening with `server/discover` gets the 2026-07-28 protocol."""
    responses = run_server(
        [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "server/discover",
                "params": {"_meta": MODERN_ENVELOPE},
            },
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "convert_to_markdown",
                    "arguments": {"uri": fixture_uri},
                    "_meta": MODERN_ENVELOPE,
                },
            },
        ],
        expected_responses=2,
    )

    discover = responses[0]["result"]
    assert "2026-07-28" in discover["supportedVersions"]
    call = responses[1]["result"]
    assert call["isError"] is False
    assert EXPECTED_MARKDOWN in call["content"][0]["text"]


def test_unknown_method_does_not_kill_the_server(fixture_uri):
    """An unrecognized method is answered, and the session stays usable."""
    responses = run_server(
        [
            {"jsonrpc": "2.0", "id": 1, "method": "totally/bogus", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "0"},
                },
            },
        ],
        expected_responses=2,
    )

    assert "error" in responses[0]
    assert responses[1]["result"]["serverInfo"]["name"] == "markitdown"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
