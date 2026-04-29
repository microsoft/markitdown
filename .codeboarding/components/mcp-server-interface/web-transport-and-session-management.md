---
component_id: 6.2
component_name: Web Transport & Session Management
---

# Web Transport & Session Management

## Component Description

Implements the network-facing transport layer using the Starlette framework. It manages the complexities of Server-Sent Events (SSE) and Streamable HTTP sessions, providing a robust web interface for the MCP server that includes connection lifecycle management and request routing.

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-mcp/src/markitdown_mcp/__main__.py (lines 34-78)
```
def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    sse = SseServerTransport("/messages/")
    session_manager = StreamableHTTPSessionManager(
        app=mcp_server,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Context manager for session manager."""
        async with session_manager.run():
            print("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                print("Application shutting down...")

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/mcp", app=handle_streamable_http),
            Mount("/messages/", app=sse.handle_post_message),
        ],
        lifespan=lifespan,
    )
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-mcp/src/markitdown_mcp/__main__.py (lines 43-53)
```
    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-mcp/src/markitdown_mcp/__main__.py (lines 55-58)
```
    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await session_manager.handle_request(scope, receive, send)
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-mcp/src/markitdown_mcp/__main__.py (lines 61-68)
```
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Context manager for session manager."""
        async with session_manager.run():
            print("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                print("Application shutting down...")
```


## Source Files:

- `packages/markitdown-mcp/src/markitdown_mcp/__main__.py`

