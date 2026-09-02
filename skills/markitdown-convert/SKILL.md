---
name: markitdown-convert
description: Converts documents (PDF/PPTX/DOCX/XLSX) and images to structured Markdown using markitdown-mcp MCP server + AI vision OCR. Use when the user asks to convert any document or image file to markdown, or mentions markitdown.
version: 1.0.0
---

# MarkItDown Document-to-Markdown Workflow

## Prerequisites

- markitdown-mcp MCP Server is configured and running (STDIO mode)
- Three MCP tools available: `convert_to_markdown`, `analyze_document`, `ocr_image`
- Path 1 (LLM): Optional — requires `MARKITDOWN_LLM_API_KEY` / `MARKITDOWN_LLM_BASE_URL` / `MARKITDOWN_LLM_MODEL` environment variables
- Path 2 (AI assistant-driven): No extra configuration needed — uses the AI assistant's own Read visual capability for OCR

## Step 1: Format Routing

After receiving a file, determine its type and select the appropriate path:

| File Type | Extensions | Handling |
|---|---|---|
| Document files | .pdf .pptx .docx .xlsx .html .csv | Use MCP tools |
| Raw images | .png .jpg .jpeg .gif .bmp .webp | **Bypass MCP** — use the Read tool's visual OCR directly |
| Other | Unknown format | Try `convert_to_markdown` first; if it fails, notify the user |

**Key limitation**: The three MCP tools only accept document formats and do not support raw image input.

## Step 2: Determine Document Type (for document files)

Call the `analyze_document` tool and inspect the returned `text_skeleton`:

- **text_skeleton contains rich text** → Pure text / semi-structured document (e.g., text-based PDF, DOCX)
  - Use `convert_to_markdown` directly for a one-step conversion
  - If the document contains images and their content needs to be OCR'd, proceed to Step 3

- **text_skeleton contains only image references or is nearly empty** → Scanned document (e.g., scanned PDF, image-based PPT)
  - Must proceed to Step 3 for the OCR workflow

## Step 3: Image OCR Workflow

### 3.1 Collect Images

The `analyze_document` result includes a list of images, each with path and dimension information. Images are typically saved in a temporary directory.

### 3.2 Filter Out Decorative Images

**Not all images need OCR**. Skip the following types:

| Filter Condition | Description |
|---|---|
| Any dimension >= 2000px | Usually full-page backgrounds or decorative base images |
| Any dimension <= 15px | Divider lines, thin decorative elements |
| Width <= 72px **and** Height <= 72px **and** File size < 2KB | Small icons, decorative elements |

**Note**: Do not use <= 120px as the threshold — it will incorrectly remove meaningful small images (e.g., a 220x64 "PRACTICE" badge, 112x112 step icons). The 72px + 2KB dual condition is a verified safe threshold.

### 3.3 OCR Each Image

For each remaining image after filtering, use the **Read tool** to read it:

```
Read(file_path="<absolute path to image>")
```

The AI assistant uses its visual capability to directly "see" the image content and extract text.

**Batch processing tip**: Read 5 images in parallel each time to avoid context overload from too many simultaneous requests.

### 3.4 OCR Extraction Guidelines

When reading each image, ensure the following content is extracted:

- **Body paragraphs**: Fully reconstruct the text without omissions
- **Headings/Subheadings**: Recognize the hierarchy and map them to `#`/`##`/`###`
- **Data tables**: Reconstruct in Markdown table format (`| col1 | col2 |`)
- **Footnotes/Annotations**: Mark with `*` and place after the relevant paragraph
- **Signatures and dates**: Preserve the original text
- **Lists**: Reconstruct as ordered/unordered lists

## Step 4: Assemble Final Markdown

Merge all OCR results with the structural information from text_skeleton:

1. Use the section headings from text_skeleton as the skeleton
2. Embed the OCR-extracted body text into the corresponding sections
3. Use standard Markdown table syntax for tables
4. Mark footnotes with `*` and place them immediately after the relevant content
5. Preserve the original document's heading hierarchy (`#` for level 1, `##` for level 2, etc.)
6. Place signatures and dates at the end of the document

**Output location**: Save to the same directory as the source file (e.g., `D:\`), with the filename being the source filename plus the `.md` extension.

## Step 5: Verification

- Confirm all sections have content (not just empty image references)
- Confirm table formatting is correct (renders properly)
- Confirm no pages are missing
- Use `present_files` to show the result to the user

## Common Pitfalls

1. **Windows short paths**: Image paths extracted by MCP may use 8.3 short names (e.g., `ADMINI~1`), which the Read tool cannot resolve. markitdown-mcp has fixed this with `os.path.realpath()`, but check for path issues if encountered.

2. **Scanned PDFs having an empty text_skeleton is normal**: This is not an error — it means every page of the PDF is an image. Proceed directly to the OCR workflow.

3. **Image filter thresholds must not be too aggressive**: A previous threshold of < 120px & < 3KB incorrectly removed meaningful content images. Strictly use the 72px + 2KB dual condition.

4. **MCP Server must be restarted after dependency changes**: The old process will not load newly installed Python packages.

5. **Do not use MCP for raw images**: The MCP tools do not support raw image input (PNG/JPG, etc.) — use the Read visual capability directly instead.

## Path 1 vs Path 2 Selection Guide

| Scenario | Recommended Path |
|---|---|
| User has configured LLM environment variables | Path 1: Fully automatic — MCP internally calls LLM to describe images |
| User has not configured LLM (default) | Path 2: AI assistant Read visual OCR |
| Pure text document (no images) | Use `convert_to_markdown` directly — neither path is needed |
| Batch document processing | Path 1 is more efficient (no per-page Read calls) |
| High quality requirements (tables, footnotes, signatures) | Path 2 is more flexible — the AI assistant can understand document structure |
