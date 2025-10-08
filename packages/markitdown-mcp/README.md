# MarkItDown-MCP

[![PyPI](https://img.shields.io/pypi/v/markitdown-mcp.svg)](https://pypi.org/project/markitdown-mcp/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown-mcp)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

The `markitdown-mcp` package provides a lightweight STDIO, Streamable HTTP, and SSE MCP server for calling MarkItDown.

## Available Tools

### `convert_to_markdown(uri)`
Convert a resource described by a URI to markdown.

**Parameters:**
- `uri` (str): An `http:`, `https:`, `file:`, or `data:` URI

**Use cases:**
- Converting web pages or publicly accessible files
- Converting local files (when using volume mounts with `file://` URIs)
- Converting uploaded files (using URLs from `upload_file` tool or `/upload` endpoint)

### `get_upload_instructions()` 🌟 **BEST for Large Files - Zero Tokens!**
Get instructions for uploading files directly via HTTP, completely bypassing the LLM context.

**Returns:**
- Upload endpoint URL and curl command (HTTP mode)
- Fallback instructions (STDIO mode)

**Workflow (HTTP mode):**
```
1. get_upload_instructions() → Returns upload endpoint and curl command
2. User runs: curl -X POST http://localhost:3001/upload -F "file=@large.pdf"
3. User gets URL: http://localhost:3001/temp/uuid
4. User: "Convert <url> to markdown"
5. convert_to_markdown(url) → File never entered LLM context!
```

**Why this is THE BEST approach:**
- ✅ **ZERO tokens** - File content NEVER enters LLM context
- ✅ **Any size** - Up to 10MB (server-limited, not context-limited)
- ✅ **Fastest** - Direct HTTP upload, no base64 encoding overhead
- ✅ **Reusable** - URL valid for 1 hour

**Example usage from Claude Desktop:**
```
You: "I need to convert my-large-report.pdf to markdown"
Claude: [calls get_upload_instructions()]
        "Please upload your file using this command:

        curl -X POST http://localhost:3001/upload -F 'file=@my-large-report.pdf'

        Then share the URL from the response with me."

You: [runs command, gets URL] "Here's the URL: http://localhost:3001/temp/abc123..."
Claude: [calls convert_to_markdown with URL - ZERO file tokens used!]
        "Here's the markdown conversion..."
```

### `upload_file(content, filename)` ⭐ **Good for Large Files**
Upload a file and get a temporary URL for token-efficient conversion.

**Parameters:**
- `content` (str): Base64-encoded file content (max 10MB)
- `filename` (str, optional): Filename for the upload

**Returns:**
- A temporary `file://` URL valid for 1 hour

**Workflow:**
```
1. upload_file() → Returns file:// URL (base64 sent once)
2. convert_to_markdown(url) → Converts file (only URL in context)
3. Any follow-up questions → Only URL referenced (minimal tokens)
```

**Why this is better than `convert_file_to_markdown`:**
- ✅ Base64 content sent only once (during upload)
- ✅ Conversion uses only the URL (~50 tokens vs 500K+)
- ✅ Follow-up questions reference URL, not file content
- ✅ Works in both STDIO and HTTP modes
- ✅ Supports files up to 10MB (vs 5MB limit)

**Note:** In HTTP mode, prefer using `get_upload_instructions()` for true zero-token uploads!

### `convert_file_to_markdown(content, filename, mimetype)`
Convert a file to markdown by providing its base64-encoded content directly.

**⚠️ ONLY USE FOR SMALL FILES (<1MB)**. For larger files, use `upload_file()` instead.

**Parameters:**
- `content` (str): Base64-encoded file content (5MB hard limit, 1MB recommended)
- `filename` (str, optional): Filename for extension-based format detection (e.g., "document.pdf")
- `mimetype` (str, optional): MIME type hint (e.g., "application/pdf", "image/png")

**Use cases:**
- Small files (<1MB) where a single-step conversion is preferred
- Quick one-off conversions

**Usage from Claude Desktop:**

When using this tool from Claude Desktop, you can simply reference files naturally - Claude handles the base64 encoding automatically:

```
You: "Convert my-document.pdf to markdown using the markitdown tool"
Claude: [reads file, encodes it, calls convert_file_to_markdown, returns result]
```

**Programmatic usage example:**

```python
import base64

# Read and encode a file
with open("document.pdf", "rb") as f:
    content = base64.b64encode(f.read()).decode('utf-8')

# Convert using the MCP tool
markdown = await convert_file_to_markdown(
    content=content,
    filename="document.pdf",
    mimetype="application/pdf"
)
```

**Note:** The base64 encoding requirement is due to MCP using JSON-RPC, which doesn't support binary data directly. MCP clients like Claude Desktop handle this encoding automatically for you.

## Upload Endpoint (HTTP/SSE Mode Only)

When running in HTTP or SSE mode (`--http`), the server provides a `/upload` endpoint for token-efficient handling of large files.

### How It Works

1. **Upload file via HTTP POST:**
```bash
curl -X POST http://localhost:3001/upload \
  -F "file=@document.pdf"
```

2. **Receive temporary URL:**
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "http://localhost:3001/temp/550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf",
  "size": 1048576,
  "expires_in": 3600
}
```

3. **Use URL with `convert_to_markdown` tool:**
```
You: "Convert the file at http://localhost:3001/temp/550e8400-... to markdown"
Claude: [calls convert_to_markdown with the URL]
```

### Benefits

- **Token-efficient**: File content doesn't go into LLM context
- **No volume mounts needed**: Works with remote/containerized servers
- **Automatic cleanup**: Files auto-delete after 1 hour or first access
- **Size limit**: 10MB maximum per upload

## Decision Tree: Which Method to Use?

Choose the right approach based on your file size and server mode:

```
┌─ Running in HTTP mode (--http)?
│
├─ YES (HTTP mode)
│  │
│  ├─ File < 1MB
│  │  └─ Use convert_file_to_markdown()
│  │     • Simple one-step conversion
│  │
│  └─ File 1MB - 10MB
│     └─ Use get_upload_instructions() 🌟 BEST!
│        • ZERO tokens - file never enters LLM context!
│        • Claude guides you to upload via curl
│        • You run: curl -X POST .../upload -F "file=@yourfile"
│        • Share returned URL with Claude
│        • Claude calls convert_to_markdown(url)
│
└─ NO (STDIO mode)
   │
   ├─ File < 1MB
   │  └─ Use convert_file_to_markdown()
   │     • Simple one-step conversion
   │
   └─ File 1MB - 10MB
      └─ Use upload_file() → convert_to_markdown() ⭐
         • Base64 sent once (during upload)
         • Conversion uses only file:// URL
         • Follow-ups reference URL, not file content

Special cases:
├─ File > 10MB → Use volume mount + convert_to_markdown(file://...)
└─ Public URL available → Use convert_to_markdown(https://...) directly
```

### Examples by Scenario

**Small file (<1MB):**
```
You: "Convert my-small-doc.pdf to markdown"
Claude: [uses convert_file_to_markdown with base64 content]
```

**Large file (1-10MB) in HTTP mode - ZERO TOKEN APPROACH 🌟:**
```
You: "I need to convert my-large-report.pdf to markdown"

Claude: [calls get_upload_instructions()]
        "To convert this file with maximum efficiency (zero tokens!), please upload
        it directly using this command:

        curl -X POST http://localhost:3001/upload -F 'file=@my-large-report.pdf'

        This will return a URL that I can use for conversion."

You: [runs the command]
     {"url": "http://localhost:3001/temp/550e8400-...", "expires_in": 3600}
     "Here's the URL: http://localhost:3001/temp/550e8400-..."

Claude: [calls convert_to_markdown with URL - ZERO file tokens used!]
        "Here's the markdown conversion... [shows content]"

You: "What are the main recommendations?"

Claude: [References the URL/already-converted content - still zero file tokens!]
        "Based on the document, the main recommendations are..."
```

**Large file (1-10MB) in STDIO mode:**
```
You: "Upload my-large-report.pdf"
Claude: [calls upload_file tool, receives file:///tmp/markitdown_xxx/uuid]
        "File uploaded successfully! Ready to convert."

You: "Convert it to markdown"
Claude: [calls convert_to_markdown with file:// URL - only ~50 tokens!]
        "Here's the markdown conversion..."

You: "What are the main recommendations?"
Claude: [References already-converted markdown - no re-upload needed!]
```

**Public URL:**
```
You: "Convert https://example.com/document.pdf to markdown"
Claude: [uses convert_to_markdown with https:// URI]
```

**Very large file (>10MB) with volume mount:**
```bash
# Run with volume mount
docker run -it --rm -v /local/dir:/workdir markitdown-mcp:latest

# Then in Claude:
You: "Convert file:///workdir/huge-document.pdf to markdown"
Claude: [uses convert_to_markdown with file:// URI]
```

## Running as a Persistent Service (RECOMMENDED)

For production use or persistent access from Claude Code, run markitdown-mcp as a Docker service:

### Quick Start

```bash
# 1. Navigate to the markitdown-mcp directory
cd packages/markitdown-mcp

# 2. Build the Docker image (if not already built)
# Option A: Use the helper script (recommended - handles cache-busting)
./build.sh          # Linux/Mac
# or
build.bat           # Windows

# Option B: Manual build with cache-busting (picks up code changes)
docker build -f Dockerfile --build-arg CACHE_BUST=$(date +%s) -t markitdown-mcp:latest ../..

# Option C: Force complete rebuild (slower, but guarantees fresh build)
docker build --no-cache -f Dockerfile -t markitdown-mcp:latest ../..

# 3. (Optional) Configure environment variables
cp .env.example .env
# Edit .env to set your OPENAI_API_KEY for image descriptions

# 4. Start the service
docker compose up -d

# 5. Verify it's running
curl http://localhost:3001/upload
```

**Why cache-busting matters:**
Docker caches build layers. When you modify Python code in `__main__.py`, Docker might not detect the change and reuse old cached layers. The `--build-arg CACHE_BUST=$(date +%s)` ensures Docker rebuilds the Python package installation layer.

The service will:
- ✅ Run persistently in the background
- ✅ Restart automatically if it crashes
- ✅ Maintain uploaded files for 1 hour
- ✅ Be accessible at `http://localhost:3001/mcp` (Streamable HTTP)

### Connecting from Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "markitdown": {
      "url": "http://localhost:3001/mcp",
      "transport": "streamable-http"
    }
  }
}
```

Then use it naturally:

```
You: "How do I upload a large file?"
Claude: [Calls get_upload_instructions() and provides curl command]

You: [Uploads via curl] "Here's the URL: http://localhost:3001/temp/abc123..."
Claude: [Converts with ZERO file tokens!]
```

### Service Management

```bash
# Start service
docker compose up -d

# View logs
docker compose logs -f

# Stop service
docker compose down

# Restart service
docker compose restart

# Check status
docker compose ps
```

## Installation

To install the package, use pip:

```bash
pip install markitdown-mcp
```

## Usage

To run the MCP server, using STDIO (default) use the following command:


```bash
markitdown-mcp
```

To run the MCP server, using Streamable HTTP and SSE use the following command:

```bash
markitdown-mcp --http --host 127.0.0.1 --port 3001
```

## LLM-Enhanced Image Descriptions

By default, image conversions extract only metadata (dimensions, EXIF data). To enable LLM-powered content descriptions for images, configure OpenAI credentials:

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `OPENAI_MODEL` (optional): Model to use for descriptions (default: `gpt-4o`)

### Example Usage

**STDIO mode:**
```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o"  # optional
markitdown-mcp
```

**HTTP mode:**
```bash
export OPENAI_API_KEY="sk-..."
markitdown-mcp --http --host 127.0.0.1 --port 3001
```

**Docker:**
```bash
docker run --rm -p 3001:3001 \
  -e OPENAI_API_KEY="sk-..." \
  -e OPENAI_MODEL="gpt-4o" \
  markitdown-mcp:latest --http --host 0.0.0.0 --port 3001
```

**Docker Compose:**

Copy `.env.example` to `.env` and configure your API key:
```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

The docker-compose.yml automatically uses the `.env` file:
```yaml
services:
  markitdown-mcp:
    image: markitdown-mcp:latest
    ports:
      - "3001:3001"
    environment:
      - MARKITDOWN_ENABLE_PLUGINS=${MARKITDOWN_ENABLE_PLUGINS:-false}
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4o}
    command: ["--http", "--host", "0.0.0.0", "--port", "3001"]
```

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-p",
        "3001:3001",
        "-e",
        "OPENAI_API_KEY=sk-...",
        "-e",
        "OPENAI_MODEL=gpt-4o",
        "markitdown-mcp:latest",
        "--http",
        "--host",
        "0.0.0.0",
        "--port",
        "3001"
      ]
    }
  }
}
```

### What This Enables

**Without LLM (default):**
```markdown
ImageSize: 1109x1373
```

**With LLM enabled:**
```markdown
ImageSize: 1109x1373

# Description:
The image shows a detailed technical diagram of a distributed system architecture...
[Full AI-generated description of image content]
```

### Notes

- LLM descriptions work for: `.jpg`, `.jpeg`, `.png` images
- The `openai` Python package must be installed (included by default)
- Only affects image conversions; other formats work without OpenAI
- If `OPENAI_API_KEY` is not set, images fall back to metadata-only conversion

## Running in Docker

To run `markitdown-mcp` in Docker, build the Docker image from the **repository root** to ensure both packages use the latest local source:

```bash
# Build from repository root (not from packages/markitdown-mcp)
cd ../..  # Navigate to repository root if you're in packages/markitdown-mcp
docker build -f packages/markitdown-mcp/Dockerfile -t markitdown-mcp:latest .
```

This ensures both `markitdown` and `markitdown-mcp` are installed from your latest local source code, not from PyPI.

### Option 1: STDIO Mode (for Claude Desktop)
```bash
docker run -it --rm markitdown-mcp:latest
```
This will be sufficient for remote URIs and small files (<1MB) via `convert_file_to_markdown`.

### Option 2: HTTP Mode with Upload Endpoint (for large files, token-efficient)
```bash
docker run --rm -p 3001:3001 markitdown-mcp:latest --http --host 0.0.0.0 --port 3001
```

**Important:** When running in Docker HTTP mode, bind to `0.0.0.0` (not `127.0.0.1`) so the server is accessible from outside the container.

**Workflow for large files:**
```bash
# 1. Start container in HTTP mode
docker run --rm -p 3001:3001 markitdown-mcp:latest --http --host 0.0.0.0 --port 3001

# 2. In another terminal, upload your file
curl -X POST http://localhost:3001/upload -F "file=@large-document.pdf"

# 3. You'll get a response like:
# {
#   "file_id": "abc123...",
#   "url": "http://localhost:3001/temp/abc123...",
#   "expires_in": 3600
# }

# 4. Use the URL with Claude Code
# In Claude Code, tell it: "Convert http://localhost:3001/temp/abc123... to markdown"
```

### Option 3: Volume Mounts (for file:// URIs)
To access local files via `file://` URIs, mount a directory:

```bash
docker run -it --rm -v /home/user/data:/workdir markitdown-mcp:latest
```

Once mounted, files are accessible under `/workdir`. For example, `example.txt` in `/home/user/data` becomes `file:///workdir/example.txt`.

## Accessing from Claude Desktop

### Quick Start Configurations

Follow [these instructions](https://modelcontextprotocol.io/quickstart/user#for-claude-desktop-users) to access Claude's `claude_desktop_config.json` file, then choose one of the configurations below:

### Option 1: HTTP Mode - Zero Token Uploads (RECOMMENDED for Large Files)

**Best for:** Files 1-10MB that you want to convert with ZERO token usage

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-p",
        "3001:3001",
        "markitdown-mcp:latest",
        "--http",
        "--host",
        "0.0.0.0",
        "--port",
        "3001"
      ]
    }
  }
}
```

**Usage:**
```
You: "I need to convert my-large-report.pdf to markdown"

Claude: [Calls get_upload_instructions()]
        "Please upload using: curl -X POST http://localhost:3001/upload -F 'file=@your-file.pdf'"

You: [Runs command] "Here's the URL: http://localhost:3001/temp/abc123..."

Claude: [Converts using URL - ZERO file tokens!]
```

**Benefits:**
- ✅ **ZERO tokens** - File never enters LLM context
- ✅ Fastest method for large files
- ✅ Up to 10MB file size
- ✅ Files accessible for 1 hour

### Option 2: STDIO Mode - Simple Setup

**Best for:** Quick setup, files up to 10MB with one-time token cost

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "markitdown-mcp:latest"
      ]
    }
  }
}
```

**Usage:**
```
You: "Upload my-presentation.pptx"
Claude: [Uses upload_file MCP tool - file saved, URL returned]

You: "Convert it to markdown and summarize"
Claude: [Uses convert_to_markdown with URL - token efficient!]
```

**Benefits:**
- ✅ No port mapping needed
- ✅ Simple configuration
- ✅ Token-efficient (content sent once)
- ✅ Works for files up to 10MB

### Option 3: Docker with Volume Mounts (For file:// URIs)

**Best for:** Very large files (>10MB) or when you need persistent file access

If you need to use `file://` URIs to access local files, you can mount a directory:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
	"run",
	"--rm",
	"-i",
	"-v",
	"/home/user/data:/workdir",
	"markitdown-mcp:latest"
      ]
    }
  }
}
```

**Note:** With the `convert_file_to_markdown` tool, volume mounts are no longer necessary. This option is provided for compatibility with the `convert_to_markdown(uri)` tool when using `file://` URIs.

## Using with Claude Code

### Setup for Token-Efficient Large File Conversion

**1. Configure Claude Desktop to use HTTP mode:**

Edit your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-p",
        "3001:3001",
        "markitdown-mcp:latest",
        "--http",
        "--host",
        "0.0.0.0",
        "--port",
        "3001"
      ]
    }
  }
}
```

**2. Upload large files via command line or script:**

Create a helper script `upload-to-markitdown.sh`:
```bash
#!/bin/bash
FILE="$1"
if [ -z "$FILE" ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

# Upload and extract URL
RESPONSE=$(curl -s -X POST http://localhost:3001/upload -F "file=@$FILE")
URL=$(echo $RESPONSE | grep -o '"url":"[^"]*"' | cut -d'"' -f4)

echo "File uploaded successfully!"
echo "URL: $URL"
echo ""
echo "Now tell Claude Code:"
echo "  Convert $URL to markdown"
```

**3. Use with Claude Code:**

```bash
# Upload your large file
./upload-to-markitdown.sh /path/to/large-presentation.pptx

# Output:
# File uploaded successfully!
# URL: http://localhost:3001/temp/550e8400-e29b-41d4-a716-446655440000
#
# Now tell Claude Code:
#   Convert http://localhost:3001/temp/550e8400-... to markdown

# Then in Claude Code:
You: "Convert http://localhost:3001/temp/550e8400-... to markdown"
Claude Code: [Uses convert_to_markdown with the URL - only ~50 tokens used!]
```

### Alternative: Python Upload Script

```python
#!/usr/bin/env python3
import sys
import requests

if len(sys.argv) < 2:
    print("Usage: python upload.py <file>")
    sys.exit(1)

file_path = sys.argv[1]

with open(file_path, 'rb') as f:
    response = requests.post(
        'http://localhost:3001/upload',
        files={'file': f}
    )

result = response.json()
print(f"File uploaded successfully!")
print(f"URL: {result['url']}")
print(f"Expires in: {result['expires_in']} seconds")
print()
print(f"Tell Claude Code:")
print(f"  Convert {result['url']} to markdown")
```

**Usage:**
```bash
python upload.py large-document.pdf
# Then copy the URL and use it with Claude Code
```

## Debugging

To debug the MCP server you can use the `mcpinspector` tool.

```bash
npx @modelcontextprotocol/inspector
```

You can then connect to the inspector through the specified host and port (e.g., `http://localhost:5173/`).

If using STDIO:
* select `STDIO` as the transport type,
* input `markitdown-mcp` as the command, and
* click `Connect`

If using Streamable HTTP:
* select `Streamable HTTP` as the transport type,
* input `http://127.0.0.1:3001/mcp` as the URL, and
* click `Connect`

If using SSE:
* select `SSE` as the transport type,
* input `http://127.0.0.1:3001/sse` as the URL, and
* click `Connect`

Finally:
* click the `Tools` tab,
* click `List Tools`,
* select either `convert_to_markdown` or `convert_file_to_markdown`, and
* run the tool with appropriate parameters.

## Security Considerations

### Development (localhost)

When running locally for development:
- ✅ Server binds to `localhost` by default (secure for single-user)
- ✅ No authentication required for local use
- ✅ Temporary files auto-delete after 1 hour
- ⚠️  HTTP (not HTTPS) - acceptable for localhost

### Production Deployment

For production or multi-user environments, implement these security best practices:

#### 1. TLS/HTTPS Transport
```yaml
# Use reverse proxy (nginx, Caddy, etc.) for HTTPS
# Example nginx config:
server {
    listen 443 ssl http2;
    server_name markitdown.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### 2. Authentication & Authorization
The server runs without authentication by default. For production:

- **Option A: Reverse Proxy Auth**
  - Use nginx/Apache with OAuth 2.1, API keys, or basic auth
  - Recommended for most deployments

- **Option B: Network Isolation**
  - Run in private network/VPN
  - Firewall rules to restrict access

#### 3. Session Management
When using Streamable HTTP, consider implementing:
- `Mcp-Session-Id` header for session tracking
- Prevents cross-client confusion in multi-user scenarios
- Helps with request/response correlation

#### 4. Input Validation
The server implements basic protections:
- ✅ File size limits (10MB uploads, 5MB base64)
- ✅ Base64 validation
- ✅ Path traversal prevention
- ✅ Temporary file cleanup

Additional recommendations:
- Validate file types/MIME types
- Scan uploads for malware (in production)
- Rate limiting on `/upload` endpoint

#### 5. DDoS Mitigation
For production deployments:
- Use Cloudflare, AWS Shield, or similar DDoS protection
- Implement rate limiting at reverse proxy level
- Monitor for abuse patterns
- Consider HTTP/2-specific vulnerabilities

#### 6. Minimal Privileges
```yaml
# docker-compose.yml with user restrictions
services:
  markitdown-mcp:
    user: "nobody:nogroup"  # Run as non-root
    read_only: true         # Read-only filesystem
    tmpfs:
      - /tmp:noexec,nosuid  # Temp files without exec
```

#### 7. Logging & Monitoring
```bash
# Enable detailed logging
docker compose logs -f markitdown-mcp

# Monitor for suspicious activity:
# - Unusual file sizes
# - High request rates
# - Failed authentication attempts (if auth enabled)
```

### Security Checklist for Production

- [ ] HTTPS/TLS enabled via reverse proxy
- [ ] Authentication implemented (OAuth 2.1 recommended)
- [ ] Rate limiting configured
- [ ] DDoS protection in place
- [ ] Input validation enhanced
- [ ] Logging and monitoring active
- [ ] Regular security updates
- [ ] Network isolation (firewall/VPN)
- [ ] File scanning for malware
- [ ] Mcp-Session-Id header implemented

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
