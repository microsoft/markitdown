import json
import queue
import subprocess
import sys
import threading
from collections.abc import Iterator
from dataclasses import dataclass, field

import pytest


@dataclass
class StdioServer:
    process: subprocess.Popen[str]
    stdout: queue.Queue[str] = field(default_factory=queue.Queue)
    stderr: list[str] = field(default_factory=list)

    def send(self, message: dict[str, object]) -> None:
        assert self.process.stdin is not None
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def receive(self, timeout: float = 15) -> dict[str, object]:
        try:
            line = self.stdout.get(timeout=timeout)
        except queue.Empty:
            stderr = "".join(self.stderr)
            pytest.fail(
                f"MCP server did not respond within {timeout} seconds.\n"
                f"stderr:\n{stderr}"
            )
        return json.loads(line)

    def receive_response(self, request_id: str) -> dict[str, object]:
        while True:
            message = self.receive()
            if message.get("id") == request_id:
                return message


@pytest.fixture
def stdio_server() -> Iterator[StdioServer]:
    process = subprocess.Popen(
        [sys.executable, "-m", "markitdown_mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        bufsize=1,
    )
    server = StdioServer(process)

    assert process.stdout is not None
    assert process.stderr is not None

    def read_stdout() -> None:
        assert process.stdout is not None
        for line in process.stdout:
            server.stdout.put(line)

    stdout_reader = threading.Thread(
        target=read_stdout,
        daemon=True,
    )
    stderr_reader = threading.Thread(
        target=server.stderr.extend,
        args=(process.stderr,),
        daemon=True,
    )
    stdout_reader.start()
    stderr_reader.start()

    try:
        yield server
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def test_malformed_and_oversized_requests_do_not_break_stdio_session(
    stdio_server: StdioServer,
) -> None:
    stdio_server.send(
        {
            "jsonrpc": "2.0",
            "id": "initialize",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "resilience-test", "version": "1.0"},
            },
        }
    )
    initialization = stdio_server.receive_response("initialize")
    assert initialization["id"] == "initialize"
    assert "result" in initialization

    stdio_server.send(
        {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }
    )

    # This is a valid JSON-RPC envelope but an invalid MCP tools/call request.
    # MCP SDK 1.8.x let the validation error terminate its receive loop.
    stdio_server.send(
        {
            "jsonrpc": "2.0",
            "id": "invalid-request",
            "method": "tools/call",
        }
    )
    invalid_response = stdio_server.receive_response("invalid-request")
    assert invalid_response["id"] == "invalid-request"
    assert invalid_response["error"]["code"] == -32602  # type: ignore[index]

    stdio_server.send(
        {
            "jsonrpc": "2.0",
            "id": {"invalid": True},
            "method": "tools/list",
            "params": {},
        }
    )

    stdio_server.send(
        {
            "jsonrpc": "2.0",
            "id": "oversized-request",
            "method": "tools/call",
            "params": {"arguments": {"value": "x" * 1_000_000}},
        }
    )
    oversized_response = stdio_server.receive_response("oversized-request")
    assert oversized_response["id"] == "oversized-request"
    assert oversized_response["error"]["code"] == -32602  # type: ignore[index]

    stdio_server.send(
        {
            "jsonrpc": "2.0",
            "id": "recovery",
            "method": "tools/list",
            "params": {},
        }
    )
    recovery = stdio_server.receive_response("recovery")
    assert recovery["id"] == "recovery"
    assert recovery["result"]["tools"][0]["name"] == "convert_to_markdown"  # type: ignore[index]
    assert stdio_server.process.poll() is None
