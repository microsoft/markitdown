# MarkItDown Python API Reference

Complete Python API documentation for MarkItDown.

## Installation

```bash
pip install 'markitdown[all]'
```

## Core Classes

### MarkItDown

Main class for document conversion.

```python
from markitdown import MarkItDown

md = MarkItDown(
    enable_plugins: bool = False,
    llm_client: Any = None,
    llm_model: str = None,
    llm_prompt: str = None,
    docintel_endpoint: str = None
)
```

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_plugins` | `bool` | `False` | Enable third-party plugins |
| `llm_client` | `Any` | `None` | OpenAI-compatible client for images |
| `llm_model` | `str` | `None` | Model name (e.g., "gpt-4o") |
| `llm_prompt` | `str` | `None` | Custom prompt for image descriptions |
| `docintel_endpoint` | `str` | `None` | Azure Document Intelligence endpoint |

#### Methods

##### convert()

Convert a file or URL to Markdown.

```python
result = md.convert(
    source: str | Path,
    **kwargs
) -> DocumentConverterResult
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | `str` or `Path` | File path or URL to convert |

Returns: `DocumentConverterResult`

##### convert_stream()

Convert from a binary file-like object.

```python
result = md.convert_stream(
    stream: BinaryIO,
    **kwargs
) -> DocumentConverterResult
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `stream` | `BinaryIO` | Binary file-like object (e.g., `io.BytesIO`) |

> **Note:** As of v0.1.0, `convert_stream()` requires binary streams only.
> Text streams (`io.StringIO`) are no longer supported.

### DocumentConverterResult

Result object from conversion.

```python
@dataclass
class DocumentConverterResult:
    text_content: str  # The converted Markdown content
    title: str | None  # Document title if available
```

## Basic Usage

### Simple Conversion

```python
from markitdown import MarkItDown

md = MarkItDown()

# Convert file
result = md.convert("document.pdf")
print(result.text_content)

# Access title if available
if result.title:
    print(f"Title: {result.title}")
```

### Convert from Stream

```python
from markitdown import MarkItDown
import io

md = MarkItDown()

# From bytes
with open("document.pdf", "rb") as f:
    content = f.read()

stream = io.BytesIO(content)
result = md.convert_stream(stream)
print(result.text_content)

# From HTTP response
import requests

response = requests.get("https://example.com/document.pdf")
stream = io.BytesIO(response.content)
result = md.convert_stream(stream)
```

### Convert URL

```python
from markitdown import MarkItDown

md = MarkItDown()

# YouTube video
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.text_content)

# Web page
result = md.convert("https://example.com/article.html")
print(result.text_content)
```

## Advanced Usage

### LLM Image Descriptions

Use OpenAI or compatible API for intelligent image descriptions.

```python
from markitdown import MarkItDown
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()  # Uses OPENAI_API_KEY env var

# Create MarkItDown with LLM support
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="Describe this image in detail, including any text visible."
)

# Convert image with AI description
result = md.convert("screenshot.png")
print(result.text_content)

# Convert PowerPoint with AI-described images
result = md.convert("presentation.pptx")
print(result.text_content)
```

### Azure Document Intelligence

For complex PDFs with tables, forms, and scanned content.

```python
from markitdown import MarkItDown

# Using endpoint directly
md = MarkItDown(
    docintel_endpoint="https://your-resource.cognitiveservices.azure.com/"
)

result = md.convert("complex-form.pdf")
print(result.text_content)
```

```python
# With environment variables
import os

os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"] = "https://..."
os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"] = "your-key"

md = MarkItDown(docintel_endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"])
result = md.convert("scanned-document.pdf")
```

### Plugin System

```python
from markitdown import MarkItDown

# Enable all installed plugins
md = MarkItDown(enable_plugins=True)

result = md.convert("document.pdf")
print(result.text_content)
```

## Batch Processing

### Process Directory

```python
from markitdown import MarkItDown
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_file(
    md: MarkItDown, file_path: Path, output_dir: Path
) -> tuple[Path, bool, str]:
    """Convert a single file and return status."""
    try:
        result = md.convert(str(file_path))
        output_file = output_dir / f"{file_path.stem}.md"
        output_file.write_text(result.text_content)
        return file_path, True, ""
    except Exception as e:
        return file_path, False, str(e)

def batch_convert(
    input_dir: str,
    output_dir: str,
    extensions: list[str] = None,
    max_workers: int = 4
) -> dict:
    """Convert all files in directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    md = MarkItDown()
    results = {"success": [], "failed": []}

    # Collect files
    if extensions:
        files = []
        for ext in extensions:
            files.extend(input_path.glob(f"*.{ext}"))
    else:
        files = [f for f in input_path.iterdir() if f.is_file()]

    # Process in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(convert_file, md, f, output_path): f
            for f in files
        }

        for future in as_completed(futures):
            file_path, success, error = future.result()
            if success:
                results["success"].append(str(file_path))
            else:
                results["failed"].append({"file": str(file_path), "error": error})

    return results

# Usage
results = batch_convert(
    input_dir="./documents",
    output_dir="./markdown",
    extensions=["pdf", "docx", "pptx"],
    max_workers=4
)
print(f"Converted: {len(results['success'])}")
print(f"Failed: {len(results['failed'])}")
```

### Process with Progress

```python
from markitdown import MarkItDown
from pathlib import Path
from tqdm import tqdm

def convert_with_progress(input_dir: str, output_dir: str):
    """Convert files with progress bar."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    md = MarkItDown()
    files = list(input_path.glob("*"))

    for file in tqdm(files, desc="Converting"):
        if file.is_file():
            try:
                result = md.convert(str(file))
                output_file = output_path / f"{file.stem}.md"
                output_file.write_text(result.text_content)
            except Exception as e:
                tqdm.write(f"Error: {file.name} - {e}")

# Usage
convert_with_progress("./documents", "./markdown")
```

## Error Handling

```python
from markitdown import MarkItDown

md = MarkItDown()

try:
    result = md.convert("document.pdf")
    print(result.text_content)
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Conversion error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Safe Conversion Function

```python
from markitdown import MarkItDown
from typing import Optional

def safe_convert(file_path: str) -> Optional[str]:
    """Safely convert file, returning None on error."""
    md = MarkItDown()
    try:
        result = md.convert(file_path)
        return result.text_content
    except Exception:
        return None

# Usage
content = safe_convert("document.pdf")
if content:
    print(content)
else:
    print("Conversion failed")
```

## Integration Examples

### FastAPI Endpoint

```python
from fastapi import FastAPI, UploadFile, HTTPException
from markitdown import MarkItDown
import io

app = FastAPI()
md = MarkItDown()

@app.post("/convert")
async def convert_document(file: UploadFile):
    """Convert uploaded document to Markdown."""
    try:
        content = await file.read()
        stream = io.BytesIO(content)
        result = md.convert_stream(stream)
        return {"markdown": result.text_content, "title": result.title}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### LangChain Document Loader

```python
from markitdown import MarkItDown
from langchain.schema import Document

def load_document(file_path: str) -> Document:
    """Load document as LangChain Document."""
    md = MarkItDown()
    result = md.convert(file_path)

    return Document(
        page_content=result.text_content,
        metadata={
            "source": file_path,
            "title": result.title or ""
        }
    )

# Usage
doc = load_document("report.pdf")
print(doc.page_content[:500])
```

## Type Hints

```python
from markitdown import MarkItDown, DocumentConverterResult
from pathlib import Path
from typing import BinaryIO

def convert_file(path: str | Path) -> DocumentConverterResult:
    md = MarkItDown()
    return md.convert(str(path))

def convert_stream(stream: BinaryIO) -> str:
    md = MarkItDown()
    result = md.convert_stream(stream)
    return result.text_content
```
