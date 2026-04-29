---
component_id: 6.1
component_name: MCP Tool Implementation
---

# MCP Tool Implementation

## Component Description

Defines the core tools and logic exposed via the MCP protocol. It wraps the MarkItDown library, configuring it based on environment settings and providing the convert_to_markdown tool which handles various URI schemes (file, http, data).

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-mcp/src/markitdown_mcp/__main__.py (lines 21-23)
```
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    return MarkItDown(enable_plugins=check_plugins_enabled()).convert_uri(uri).markdown
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-mcp/src/markitdown_mcp/__main__.py (lines 26-31)
```
def check_plugins_enabled() -> bool:
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false").strip().lower() in (
        "true",
        "1",
        "yes",
    )
```


## Source Files:

- `packages/markitdown-mcp/src/markitdown_mcp/__main__.py`

