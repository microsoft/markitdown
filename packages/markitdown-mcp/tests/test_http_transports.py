"""Exercise the combined HTTP app without a listening socket or subprocess."""

import asyncio
import json
from contextlib import aclosing, asynccontextmanager
from urllib.parse import parse_qs, urlsplit

import httpx2 as httpx

from markitdown_mcp.__main__ import create_starlette_app, mcp


BASE_URL = "http://127.0.0.1:3001"
INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "0"},
    },
}
INITIALIZED = {"jsonrpc": "2.0", "method": "notifications/initialized"}
CONVERT = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "convert_to_markdown",
        "arguments": {"uri": "data:text/plain,Hello%20from%20HTTP"},
    },
}


class _SSEBody(httpx.AsyncByteStream):
    def __init__(self, messages):
        self.messages = messages

    async def __aiter__(self):
        while True:
            message = await self.messages.get()
            assert message["type"] == "http.response.body"
            yield message.get("body", b"")
            if not message.get("more_body", False):
                return


@asynccontextmanager
async def sse_connection(app):
    # ASGITransport buffers responses until completion, so drive the open SSE
    # request directly and let httpx parse its streamed response body.
    incoming = asyncio.Queue()
    outgoing = asyncio.Queue()
    await incoming.put({"type": "http.request", "body": b"", "more_body": False})
    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.4"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/sse",
        "raw_path": b"/sse",
        "root_path": "",
        "query_string": b"",
        "headers": [
            (b"host", b"127.0.0.1:3001"),
            (b"accept", b"text/event-stream"),
        ],
        "client": ("127.0.0.1", 1234),
        "server": ("127.0.0.1", 3001),
    }
    task = asyncio.create_task(app(scope, incoming.get, outgoing.put))
    try:
        start = await outgoing.get()
        assert start["type"] == "http.response.start"
        assert start["status"] == 200
        response = httpx.Response(
            start["status"],
            headers=start["headers"],
            stream=_SSEBody(outgoing),
            request=httpx.Request("GET", BASE_URL + "/sse"),
        )
        assert response.headers["content-type"].startswith("text/event-stream")
        async with aclosing(httpx.EventSource(response).__aiter__()) as events:
            yield events
    finally:
        await incoming.put({"type": "http.disconnect"})
        await asyncio.wait_for(task, timeout=5)


def assert_conversion(response):
    assert response["id"] == CONVERT["id"]
    result = response["result"]
    assert result["isError"] is False
    assert result["content"][0]["text"] == "Hello from HTTP"


def test_streamable_http_initializes_with_app_lifespan():
    async def exercise():
        app = create_starlette_app(mcp)
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url=BASE_URL,
                headers={"accept": "application/json, text/event-stream"},
            ) as client:
                response = await client.post("/mcp", json=INITIALIZE)
                assert response.status_code == 200
                assert response.headers["content-type"].startswith("application/json")
                initialized = response.json()
                assert initialized["id"] == INITIALIZE["id"]
                assert initialized["result"]["serverInfo"]["name"] == "markitdown"
                assert "mcp-session-id" not in response.headers

                client.headers["mcp-protocol-version"] = initialized["result"][
                    "protocolVersion"
                ]
                response = await client.post("/mcp", json=INITIALIZED)
                assert response.status_code == 202
                response = await client.post("/mcp", json=CONVERT)
                assert response.status_code == 200
                assert_conversion(response.json())

    asyncio.run(asyncio.wait_for(exercise(), timeout=15))


def test_sse_session_uses_preserved_message_route():
    async def exercise():
        app = create_starlette_app(mcp)
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url=BASE_URL
            ) as client:
                async with sse_connection(app) as events:
                    endpoint = await anext(events)
                    assert endpoint.event == "endpoint"
                    url = urlsplit(endpoint.data)
                    assert url.path == "/messages/"
                    assert parse_qs(url.query)["session_id"]

                    response = await client.post(endpoint.data, json=INITIALIZE)
                    assert response.status_code == 202
                    event = await anext(events)
                    assert event.event == "message"
                    initialized = json.loads(event.data)
                    assert initialized["id"] == INITIALIZE["id"]
                    assert initialized["result"]["serverInfo"]["name"] == "markitdown"

                    response = await client.post(endpoint.data, json=INITIALIZED)
                    assert response.status_code == 202
                    response = await client.post(endpoint.data, json=CONVERT)
                    assert response.status_code == 202
                    event = await anext(events)
                    assert event.event == "message"
                    assert_conversion(json.loads(event.data))

    asyncio.run(asyncio.wait_for(exercise(), timeout=15))
