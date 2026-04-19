# MarkItDown HTTPS Server

An **HTTPS** server that accepts a file upload and returns a **MarkItDown** conversion as the response body.

## Install (from this repo)

```bash
pip install -e packages/markitdown-https-server
```

## Generate a local TLS cert (self-signed)

```bash
mkdir -p .certs
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout .certs/localhost.key \
  -out .certs/localhost.crt \
  -days 365 \
  -subj "/CN=localhost"
```

## Run

```bash
markitdown-https-server \
  --host 127.0.0.1 --port 3443 \
  --certfile .certs/localhost.crt \
  --keyfile .certs/localhost.key
```

## Convert an uploaded file

```bash
curl -k https://127.0.0.1:3443/convert \
  -F "file=@./some-document.pdf" \
  -o output.md
```

Notes:
- `-k` skips TLS verification for self-signed certs.
- Response `Content-Type` is `text/markdown; charset=utf-8`.
