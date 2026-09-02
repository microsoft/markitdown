---
component_id: 6
component_name: MCP Server Interface
---

# MCP Server Interface

## Component Description

Implements the Model Context Protocol (MCP), exposing the library's conversion capabilities as a tool for AI agents via a Starlette-based web server.

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

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-mcp/src/markitdown_mcp/__main__.py (lines 21-23)
```
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    return MarkItDown(enable_plugins=check_plugins_enabled()).convert_uri(uri).markdown
```


## Source Files:

- `packages/markitdown-mcp/src/markitdown_mcp/__main__.py`

