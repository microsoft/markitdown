---
name: markitdown-convert
description: >-
  Convert PDF, Word, PowerPoint, Excel, HTML, images, audio, EPub, ZIP and
  other files to Markdown with the markitdown CLI or Python API. Use when an
  agent needs document text as Markdown for an LLM pipeline, needs to pick the
  right optional extras, or must convert untrusted input safely.
---

# Converting files with MarkItDown

MarkItDown turns documents into structure-preserving Markdown (headings,
lists, tables, links) for LLM and text-analysis pipelines. Sources of truth in
this repo: `README.md`, `packages/markitdown/src/markitdown/__main__.py` (CLI)
and `packages/markitdown/src/markitdown/_markitdown.py` (Python API).

## Install

Python 3.10–3.14. Install only the extras you need:

```bash
pip install 'markitdown[all]'            # everything
pip install 'markitdown[pdf,docx,pptx]'  # just these formats
```

Extras: `pptx`, `docx`, `xlsx`, `xls`, `pdf`, `outlook`, `az-doc-intel`,
`az-content-understanding`, `audio-transcription`, `youtube-transcription`.
A missing extra is the most common cause of "no converter" failures.

## CLI

```bash
markitdown report.pdf > report.md
markitdown report.pdf -o report.md
cat report.pdf | markitdown -x pdf      # stdin: give an extension hint
markitdown data.csv -c UTF-8            # charset hint
markitdown page.html --keep-data-uris   # keep base64 images (truncated by default)
```

Useful flags: `-x/--extension`, `-m/--mime-type`, `-c/--charset` (hints for
stdin or ambiguous input), `-p/--use-plugins`, `--list-plugins`.

## Python API

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert_local("test.xlsx")
print(result.markdown)
```

Pick the narrowest method:

| Input | Method |
|-------|--------|
| Local path | `convert_local(path)` |
| Open binary stream | `convert_stream(stream, stream_info=...)` |
| A `requests.Response` you fetched yourself | `convert_response(resp)` |
| Any of the above / URIs (permissive) | `convert(source)` |

`convert()` accepts local paths, `http(s):`, `file:` and `data:` URIs and
streams. Only use it for trusted input.

## Image descriptions with an LLM

For images and PPTX, pass an OpenAI-compatible client:

```python
from openai import OpenAI
md = MarkItDown(llm_client=OpenAI(max_retries=5), llm_model="gpt-4o")
```

If the client fails after retries, MarkItDown falls back to other converters.

## Azure services (optional, billable)

- Document Intelligence: `markitdown f.pdf -d -e "$ENDPOINT"` or set
  `MARKITDOWN_DOCINTEL_ENDPOINT`. Uses `AZURE_API_KEY` or
  `DefaultAzureCredential`. `--docintel-model-id`, `--docintel-features`,
  `--docintel-query-fields` tune it.
- Content Understanding: `markitdown f.mp4 --use-cu --cu-endpoint "$ENDPOINT"`
  (or `MARKITDOWN_CU_ENDPOINT`). Restrict routing with `--cu-file-types`.

Each routed conversion is a paid API call. Say so before enabling it.

## Security checklist

MarkItDown does I/O with the current process's privileges.

- Never pass untrusted paths or URIs straight to `convert()`.
- Server-side: validate paths, restrict URI schemes, block private,
  loopback, link-local and metadata addresses.
- Prefer `convert_local()` / `convert_stream()` in services.
- For offline-only use, do not install the cloud extras.
