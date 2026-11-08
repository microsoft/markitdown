"""Exercise CLI transport options without starting a listening server."""

import sys
from unittest.mock import Mock

import pytest

from markitdown_mcp import __main__ as server


def test_default_transport_uses_stdio(monkeypatch):
    run = Mock()
    monkeypatch.setattr(server.mcp, "run", run)
    monkeypatch.setattr(sys, "argv", ["markitdown-mcp"])

    server.main()

    run.assert_called_once_with()


@pytest.mark.parametrize("transport", ["--http", "--sse"])
@pytest.mark.parametrize(
    "port_args, expected_port",
    [([], 3001), (["--port", "0"], 0), (["--port", "4321"], 4321)],
)
def test_http_port_reaches_uvicorn(monkeypatch, transport, port_args, expected_port):
    run = Mock()
    monkeypatch.setattr(server.uvicorn, "run", run)
    monkeypatch.setattr(sys, "argv", ["markitdown-mcp", transport, *port_args])

    server.main()

    run.assert_called_once()
    assert run.call_args.kwargs["host"] == "127.0.0.1"
    assert run.call_args.kwargs["port"] == expected_port


@pytest.mark.parametrize("port", ["0", "4321"])
def test_explicit_port_requires_http_transport(monkeypatch, capsys, port):
    run = Mock()
    monkeypatch.setattr(server.mcp, "run", run)
    monkeypatch.setattr(sys, "argv", ["markitdown-mcp", "--port", port])

    with pytest.raises(SystemExit) as exc:
        server.main()

    assert exc.value.code == 2
    assert "Host and port arguments are only valid" in capsys.readouterr().err
    run.assert_not_called()
