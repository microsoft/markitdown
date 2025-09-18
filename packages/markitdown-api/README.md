# MarkItDown API

[![PyPI](https://img.shields.io/pypi/v/markitdown-api.svg)](https://pypi.org/project/markitdown-api/)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

The `markitdown-api` package provides a REST API server for MarkItDown, allowing you to convert various file formats to markdown over HTTP.

## Features

- Convert files to markdown via file upload
- Convert URLs to markdown
- Support for various input formats (documents, images, audio, etc.)
- Swagger/OpenAPI documentation
- Rate limiting and authentication options
- Health monitoring endpoints

## Installation

```bash
pip install markitdown-api
```

## Usage

To start the API server:

```bash
markitdown-api
```

Or with custom host/port:

```bash
markitdown-api --host 0.0.0.0 --port 8000
```

### API Documentation

Once the server is running, you can access:

- Swagger UI: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

### API Endpoints

- `POST /convert/file` - Convert uploaded file to markdown
- `POST /convert/url` - Convert URL to markdown
- `GET /health` - Server health check

See the Swagger documentation for detailed API specifications.

## Security Considerations

- Set appropriate rate limits for your deployment
- Consider implementing authentication for production use
- Monitor server resources and implement appropriate limits

## Configuration

The server can be configured via environment variables:

- `MARKITDOWN_API_HOST` - Host to bind to (default: 127.0.0.1)
- `MARKITDOWN_API_PORT` - Port to listen on (default: 8000)
- `MARKITDOWN_API_WORKERS` - Number of worker processes (default: 1)
- `MARKITDOWN_API_ENABLE_PLUGINS` - Enable MarkItDown plugins (default: false)
- `MARKITDOWN_API_RATE_LIMIT` - Requests per minute per IP (default: 60)

## Development

To run the server in development mode with hot reloading:

```bash
uvicorn markitdown_api:app --reload
```

## License

MIT