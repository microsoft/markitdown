# Security Best Practices for MarkItDown

## Table of Contents
- [Overview](#overview)
- [Core Library Security](#core-library-security)
- [MCP Server Security](#mcp-server-security)
- [Plugin Security](#plugin-security)
- [Network Security](#network-security)
- [Deployment Checklist](#deployment-checklist)

---

## Overview

MarkItDown performs I/O operations with the privileges of the current user process.
This includes:
- Reading local files
- Making HTTP/HTTPS network requests
- Loading 3rd-party plugins

**Always sanitize inputs and restrict capabilities in untrusted environments.**

---

## Core Library Security

### Path Validation

MarkItDown includes built-in path traversal detection:

```python
from markitdown import MarkItDown

md = MarkItDown()

# ✅ Safe: normal paths
result = md.convert("/home/user/documents/report.pdf")

# ❌ Blocked: path traversal attempt
try:
    md.convert("../../../etc/passwd")  # Raises ValueError
except ValueError as e:
    print(f"Security check blocked: {e}")
```

The `security_check` parameter (enabled by default):
- Detects `..` path traversal attempts
- Warns about symbolic links
- Resolves paths to absolute form

To explicitly disable (**not recommended**):
```python
md.convert("file.pdf", security_check=False)  # ⚠️ Only if you have already validated
```

### File Size Limits

**Local files**: No built-in limit - validate before passing to MarkItDown.
**HTTP downloads**: 100MB default limit, configurable:

```python
# Increase download limit to 500MB
md.convert("https://example.com/large.pdf", max_download_size=500*1024*1024)

# Disable limit entirely (not recommended)
md.convert("https://example.com/large.pdf", max_download_size=float('inf'))
```

### Input Sanitization

Before calling MarkItDown in server-side code:

```python
def safe_convert(user_provided_path: str, base_dir: str) -> str:
    """Example: Restrict conversions to a specific directory."""
    import os

    # 1. Resolve to absolute path
    absolute_path = os.path.abspath(user_provided_path)

    # 2. Verify it's within the allowed directory
    base_absolute = os.path.abspath(base_dir)
    if not absolute_path.startswith(base_absolute + os.sep):
        raise ValueError(f"Path outside allowed directory: {user_provided_path}")

    # 3. Check file size
    file_size = os.path.getsize(absolute_path)
    if file_size > 50 * 1024 * 1024:  # 50MB
        raise ValueError(f"File too large: {file_size} bytes")

    # 4. Now safe to convert
    md = MarkItDown()
    return md.convert(absolute_path).markdown
```

---

## MCP Server Security

### Critical: Default Configuration

By default, the MCP server **has NO security restrictions**. It can:
- Read ANY file accessible to the user
- Download ANY HTTP/HTTPS resource
- Run with FULL user privileges

**Never expose the default configuration to untrusted networks.**

### Secure Configuration

Set these environment variables before starting the server:

```bash
# Linux/macOS
export MARKITDOWN_MCP_API_KEY="your-secret-key-here"
export MARKITDOWN_MCP_ALLOWED_PATHS="/home/user/documents:/home/user/reports"
export MARKITDOWN_MCP_MAX_FILE_SIZE="52428800"  # 50MB

# Windows (PowerShell)
$env:MARKITDOWN_MCP_API_KEY = "your-secret-key-here"
$env:MARKITDOWN_MCP_ALLOWED_PATHS = "C:\Users\user\Documents;C:\Users\user\Reports"
$env:MARKITDOWN_MCP_MAX_FILE_SIZE = "52428800"
```

### Verify Configuration

Check your security settings before deployment:

```bash
markitdown-mcp --show-security-config
```

This will display:
- API key status (required / not required)
- Allowed URI schemes
- Maximum file size
- Symbolic link handling
- Allowed path whitelist

### Authentication

When an API key is configured, clients must provide it:

```python
# Example MCP client call with API key
result = await mcp_client.call_tool(
    "convert_to_markdown",
    {
        "uri": "file:///home/user/documents/report.pdf",
        "api_key": "your-secret-key-here"  # Required if configured
    }
)
```

### Path Whitelist

The path whitelist restricts which directories can be accessed:

```bash
# Allow multiple directories (Unix uses colon, Windows uses semicolon)
MARKITDOWN_MCP_ALLOWED_PATHS="/data/reports:/data/documents"  # Linux/macOS
MARKITDOWN_MCP_ALLOWED_PATHS="C:\Data\Reports;C:\Data\Documents"  # Windows
```

**Important**: Child directories are also allowed.
Example: If `/data/reports` is allowed, `/data/reports/2024/` is also accessible.

### Scheme Restriction

Restrict to only the URI schemes you need:

```bash
# Only allow local files (no network downloads)
MARKITDOWN_MCP_ALLOWED_SCHEMES="file"

# Allow local files + HTTPS only (no plain HTTP)
MARKITDOWN_MCP_ALLOWED_SCHEMES="file,https"
```

### HTTP/SSE Deployment Security

**Never bind to `0.0.0.0` or any public interface without:**
1. ✅ Configuring an API key
2. ✅ Setting up a path whitelist
3. ✅ Placing behind a reverse proxy with TLS
4. ✅ Adding network-level firewall restrictions

**Recommended secure deployment:**
```bash
# Keep default localhost binding (127.0.0.1 only)
markitdown-mcp --http

# Use a reverse proxy (nginx, Caddy, etc.) for external access
# with TLS authentication and IP whitelisting
```

---

## Plugin Security

Plugins are disabled by default for security reasons.

### Enable Plugins Safely

```python
# Only enable plugins if you trust all installed plugins
md = MarkItDown(enable_plugins=True)
```

### Plugin Installation Risks

Plugins:
- Run with full user privileges
- Can execute arbitrary Python code
- Can register converters that modify behavior

**Only install plugins from trusted sources.**

### Verify Installed Plugins

```bash
# List discovered plugins before enabling
markitdown --list-plugins
```

Audit plugin source code before enabling in production.

---

## Network Security

### HTTP Request Security

MarkItDown uses `requests` library for HTTP downloads. Consider:

1. **Don't allow SSRF**: Block requests to private IP ranges in server-side code
2. **Use timeouts**: Set reasonable timeouts to prevent hanging connections
3. **Verify SSL**: Don't disable SSL verification (default is enabled)

```python
# Example: Add network layer protection in server-side code
def safe_convert_url(url: str):
    from urllib.parse import urlparse
    import ipaddress

    # 1. Check for private IP addresses (SSRF protection)
    hostname = urlparse(url).hostname
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError(f"Access to private IP blocked: {hostname}")
    except ValueError:
        # Not an IP address - DNS resolution happens at request time
        # Consider DNS-level SSRF protection for critical deployments
        pass

    # 2. Now convert
    return MarkItDown().convert(url)
```

### Proxy Configuration

If you need to route traffic through a proxy:

```python
import requests
from markitdown import MarkItDown

# Create a custom session with proxy settings
session = requests.Session()
session.proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "https://proxy.example.com:8080",
}

md = MarkItDown()
md._requests_session = session  # Override internal session
```

---

## Deployment Checklist

### Development / Local Use
- [ ] Keep default localhost binding for MCP server
- [ ] No API key required (but still recommended)
- [ ] Plugins disabled unless actively testing

### Staging / Internal Network
- [ ] Configure API key authentication
- [ ] Set up path whitelist to only required directories
- [ ] Restrict URI schemes to minimum necessary
- [ ] Enable logging to monitor usage

### Production / Internet-Facing
- [ ] **MANDATORY**: API key with strong random secret
- [ ] **MANDATORY**: Path whitelist restricted to application data only
- [ ] **MANDATORY**: TLS encryption (HTTPS)
- [ ] Reverse proxy with authentication layer
- [ ] Network-level firewall / IP whitelisting
- [ ] Rate limiting to prevent abuse
- [ ] Request logging with audit trail
- [ ] Regular security updates
- [ ] File type validation (only allow expected formats)
- [ ] Sandboxed process / container with reduced privileges

### Docker Deployment Security

When running the MCP server in Docker:

```dockerfile
# ✅ Good: Run as non-root user
RUN useradd -m markitdown
USER markitdown

# ✅ Good: Mount only required directories as read-only
docker run -v /host/path:/container/path:ro markitdown-mcp

# ❌ Bad: Mounting entire home directory or root
# docker run -v /home:/home markitdown-mcp  # ⚠️ Avoid!
```

---

## Reporting Security Issues

If you discover a security vulnerability in MarkItDown:

1. **Do NOT open a public issue** - this discloses the vulnerability before a fix is available
2. Contact the maintainers privately with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested mitigation

---

## Security Updates

Subscribe to release notifications to receive security patch announcements:
- GitHub Releases: Watch the repository
- PyPI: Enable release notifications for `markitdown`

---

## Disclaimer

This document provides guidance, but every deployment is different.
**Always conduct a security review before exposing MarkItDown to untrusted inputs or networks.**

Security is a continuous process, not a one-time configuration.
