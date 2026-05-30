# MarkItDown Web Wrapper

A web interface for [MarkItDown](https://github.com/microsoft/markitdown) — convert PDFs, Word docs, PowerPoints, spreadsheets, images and more into clean Markdown via drag & drop.

## Stack

- **Backend** — FastAPI (Python), runs MarkItDown conversions
- **Frontend** — Next.js 16, Tailwind CSS, React Dropzone
- **Containerised** — Docker Compose for one-command local setup

## Quick start

### Option A — Docker (recommended)

```bash
cd webapp
docker compose up --build
```

Frontend → http://localhost:3000  
Backend API → http://localhost:8000

### Option B — Manual

**Backend:**
```bash
cd webapp/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd webapp/frontend
cp .env.example .env.local
pnpm install
pnpm dev
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/formats` | List supported formats |
| `POST` | `/api/convert` | Convert file → Markdown |

### Convert example

```bash
curl -X POST http://localhost:8000/api/convert \
  -F "file=@document.pdf" \
  | jq '.markdown'
```

## Supported formats

PDF, DOCX, PPTX, XLSX, XLS, CSV, JSON, XML, HTML, TXT, PNG, JPG, EPUB, ZIP

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API URL |