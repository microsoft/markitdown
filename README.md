# MarkItDown  

MarkItDown is a lightweight Python utility designed to convert diverse file formats into Markdown, optimized for use with large language models (LLMs) and text analysis pipelines. Unlike traditional converters such as textract [(github.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgithub.com%2Fdeanmalmgren%2Ftextract"), MarkItDown emphasizes preserving document structure—headings, lists, tables, links—while producing output that is both token-efficient and LLM-friendly.  

It currently supports conversion from:  
- PDF, Word, PowerPoint, Excel (including legacy formats)  
- Images (EXIF metadata + OCR)  
- Audio (metadata + transcription)  
- HTML, CSV, JSON, XML  
- ZIP archives  
- YouTube URLs  
- EPubs  
- And more  

---

## Why Markdown?  
Markdown is close to plain text yet expressive enough to capture document hierarchy. Mainstream LLMs, including GPT‑4o, natively handle Markdown, making it an ideal format for efficient, structured text analysis.  

---

## Prerequisites  
- Python 3.10+  
- Recommended: virtual environment (venv, uv, or Anaconda) to isolate dependencies  

---

## Installation  
Install via pip:  
```bash
pip install 'markitdown[all]'
```
  Or from source:  
```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```
  
Optional dependencies can be installed selectively (e.g., `pip install 'markitdown[pdf, docx, pptx]'`).  

---

## Usage  

### Command Line  
```bash
markitdown path-to-file.pdf > document.md
markitdown path-to-file.pdf -o document.md
cat path-to-file.pdf | markitdown
```
  
### Python API  
```python
from markitdown import MarkItDown
md = MarkItDown(enable_plugins=False)
result = md.convert("test.xlsx")
print(result.text_content)
```
  
Supports integration with Azure Document Intelligence and Azure Content Understanding for advanced cloud-based extraction, structured field parsing (YAML front matter), and multimodal analysis.  

---

## Plugins  
MarkItDown supports third‑party plugins (disabled by default). Example:  
- **markitdown‑ocr**: Adds OCR for embedded images in PDFs, DOCX, PPTX, XLSX using LLM Vision.  

Enable plugins via CLI or Python API:  
```bash
markitdown --use-plugins path-to-file.pdf
```
  
---

## Docker  
```bash
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```
  
---

## Contributing  
Contributions are welcome. A Contributor License Agreement (CLA) is required. Issues and PRs are tracked on GitHub, with some flagged as “open for contribution” or “open for review.”  

Run tests with `hatch` or Devcontainer, and ensure pre‑commit checks pass before submitting PRs.  

---

## Security Considerations  
MarkItDown performs I/O with the privileges of the current process.  
- **Sanitize inputs** in untrusted environments.  
- **Use narrow APIs** (`convert_local()`, `convert_stream()`) instead of the permissive `convert()` when possible.  
- Restrict file paths, URI schemes, and network destinations to avoid exposure to sensitive resources.  