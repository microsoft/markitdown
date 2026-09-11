# MarkItDown Examples

Practical examples for common use cases.

## Document Processing

### Extract Text from PDF

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("report.pdf")

# Get plain text
text = result.text_content
print(f"Extracted {len(text)} characters")
```

### Convert Word Document

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.docx")

# Save as markdown file
with open("document.md", "w") as f:
    f.write(result.text_content)
```

### Process PowerPoint Presentation

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("slides.pptx")

# Each slide becomes a section
print(result.text_content)
```

### Extract Data from Excel

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.xlsx")

# Tables are converted to Markdown tables
print(result.text_content)
```

## Image Processing

### Basic OCR

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("screenshot.png")

# Extracts EXIF metadata and OCR text
print(result.text_content)
```

### AI-Powered Image Description

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="Describe this image in detail."
)

result = md.convert("diagram.png")
print(result.text_content)
```

### Process Multiple Images

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()
image_dir = Path("./images")

for image in image_dir.glob("*.png"):
    result = md.convert(str(image))
    output = image_dir / f"{image.stem}.md"
    output.write_text(f"# {image.name}\n\n{result.text_content}")
    print(f"Processed: {image.name}")
```

## Audio Processing

### Transcribe Audio File

```python
from markitdown import MarkItDown

# Requires [audio-transcription] extra
md = MarkItDown()
result = md.convert("interview.mp3")

print(result.text_content)
```

### Process Meeting Recording

```python
from markitdown import MarkItDown
from datetime import datetime

md = MarkItDown()
result = md.convert("meeting.wav")

# Add metadata
output = f"""# Meeting Transcript
Date: {datetime.now().strftime("%Y-%m-%d")}

## Transcript

{result.text_content}
"""

with open("meeting-notes.md", "w") as f:
    f.write(output)
```

## Web Content

### YouTube Video Transcript

```python
from markitdown import MarkItDown

# Requires [youtube-transcription] extra
md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

print(result.text_content)
```

### Extract YouTube Video for Notes

```python
from markitdown import MarkItDown

def youtube_to_notes(video_url: str, output_path: str):
    """Convert YouTube video to study notes."""
    md = MarkItDown()
    result = md.convert(video_url)

    # Structure the output
    content = f"""# Video Notes

Source: {video_url}

## Transcript

{result.text_content}

## Key Points

[Add your notes here]

## Questions

[Add questions for review]
"""

    with open(output_path, "w") as f:
        f.write(content)

# Usage
youtube_to_notes(
    "https://www.youtube.com/watch?v=VIDEO_ID",
    "lecture-notes.md"
)
```

### Convert HTML Page

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("page.html")

# Preserves structure: headings, lists, links
print(result.text_content)
```

## Data Files

### CSV to Markdown Table

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.csv")

# Data becomes a Markdown table
print(result.text_content)
```

### JSON to Markdown

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("config.json")

print(result.text_content)
```

### XML to Markdown

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.xml")

print(result.text_content)
```

## Archive Processing

### Process ZIP Contents

```python
from markitdown import MarkItDown

md = MarkItDown()

# Iterates through ZIP contents
result = md.convert("documents.zip")
print(result.text_content)
```

### Extract Documentation from ZIP

```python
from markitdown import MarkItDown
from pathlib import Path
import zipfile
import tempfile

def extract_docs_from_zip(zip_path: str) -> str:
    """Extract and convert all documents from ZIP."""
    md = MarkItDown()
    all_content = []

    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(temp_dir)

        for file in Path(temp_dir).rglob("*"):
            if file.is_file() and file.suffix in ['.pdf', '.docx', '.txt']:
                try:
                    result = md.convert(str(file))
                    all_content.append(f"## {file.name}\n\n{result.text_content}")
                except Exception as e:
                    all_content.append(f"## {file.name}\n\nError: {e}")

    return "\n\n---\n\n".join(all_content)

# Usage
content = extract_docs_from_zip("project-docs.zip")
with open("all-docs.md", "w") as f:
    f.write(content)
```

## LLM Integration

### Prepare Documents for RAG

```python
from markitdown import MarkItDown
from pathlib import Path

def prepare_for_rag(docs_dir: str) -> list[dict]:
    """Prepare documents for RAG indexing."""
    md = MarkItDown()
    documents = []

    for file in Path(docs_dir).glob("*"):
        if file.is_file():
            try:
                result = md.convert(str(file))
                documents.append({
                    "source": str(file),
                    "title": result.title or file.stem,
                    "content": result.text_content
                })
            except Exception as e:
                print(f"Skipped {file}: {e}")

    return documents

# Usage
docs = prepare_for_rag("./knowledge-base")
print(f"Prepared {len(docs)} documents")
```

### Summarize Document with LLM

```python
from markitdown import MarkItDown
from openai import OpenAI

def summarize_document(file_path: str) -> str:
    """Convert document and generate summary."""
    # Convert to markdown
    md = MarkItDown()
    result = md.convert(file_path)

    # Summarize with LLM
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Summarize the following document concisely."},
            {"role": "user", "content": result.text_content[:10000]}
        ]
    )

    return response.choices[0].message.content

# Usage
summary = summarize_document("long-report.pdf")
print(summary)
```

### Q&A Over Documents

```python
from markitdown import MarkItDown
from openai import OpenAI

class DocumentQA:
    def __init__(self):
        self.md = MarkItDown()
        self.client = OpenAI()
        self.documents = {}

    def load_document(self, file_path: str, doc_id: str):
        """Load and convert document."""
        result = self.md.convert(file_path)
        self.documents[doc_id] = result.text_content

    def ask(self, doc_id: str, question: str) -> str:
        """Ask question about loaded document."""
        if doc_id not in self.documents:
            raise ValueError(f"Document {doc_id} not loaded")

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"Answer questions based on this document:\n\n{self.documents[doc_id][:15000]}"
                },
                {"role": "user", "content": question}
            ]
        )

        return response.choices[0].message.content

# Usage
qa = DocumentQA()
qa.load_document("contract.pdf", "contract")
answer = qa.ask("contract", "What are the payment terms?")
print(answer)
```

## Jupyter Notebooks

### Convert Notebook to Markdown

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("analysis.ipynb")

# Output includes code cells, outputs, and markdown cells
print(result.text_content)
```

### Extract Code from Notebook

```python
from markitdown import MarkItDown
import re

def extract_code_cells(notebook_path: str) -> list[str]:
    """Extract only code from notebook."""
    md = MarkItDown()
    result = md.convert(notebook_path)

    # Find code blocks
    code_blocks = re.findall(
        r"```python\n(.*?)```",
        result.text_content,
        re.DOTALL
    )
    return code_blocks

# Usage
code = extract_code_cells("data_analysis.ipynb")
for i, block in enumerate(code, 1):
    print(f"--- Cell {i} ---")
    print(block)
```

### Batch Convert Notebooks

```python
from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()

for notebook in Path("./notebooks").glob("*.ipynb"):
    result = md.convert(str(notebook))
    output = notebook.with_suffix(".md")
    output.write_text(result.text_content)
    print(f"Converted: {notebook.name}")
```

## RSS and Atom Feeds

### Parse RSS Feed

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("https://example.com/feed.rss")

# Feed entries converted to markdown
print(result.text_content)
```

### Monitor Multiple Feeds

```python
from markitdown import MarkItDown
from datetime import datetime

def aggregate_feeds(feed_urls: list[str]) -> str:
    """Combine multiple RSS feeds into one document."""
    md = MarkItDown()
    sections = []

    for url in feed_urls:
        try:
            result = md.convert(url)
            sections.append(f"## Feed: {url}\n\n{result.text_content}")
        except Exception as e:
            sections.append(f"## Feed: {url}\n\nError: {e}")

    header = f"# Feed Aggregation\nGenerated: {datetime.now()}\n\n"
    return header + "\n\n---\n\n".join(sections)

# Usage
feeds = [
    "https://news.ycombinator.com/rss",
    "https://example.com/blog/feed.xml"
]
content = aggregate_feeds(feeds)
print(content)
```

## Wikipedia

### Extract Article Content

```python
from markitdown import MarkItDown

md = MarkItDown()

# Extracts main article content, excludes navigation/sidebars
result = md.convert("https://en.wikipedia.org/wiki/Python")
print(result.text_content)
```

### Research Multiple Topics

```python
from markitdown import MarkItDown
from pathlib import Path

def research_topics(topics: list[str], output_dir: str):
    """Download Wikipedia articles for research."""
    md = MarkItDown()
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for topic in topics:
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        try:
            result = md.convert(url)
            filename = f"{topic.lower().replace(' ', '-')}.md"
            (output_path / filename).write_text(result.text_content)
            print(f"Downloaded: {topic}")
        except Exception as e:
            print(f"Failed: {topic} - {e}")

# Usage
research_topics(
    ["Machine learning", "Neural network", "Deep learning"],
    "./research"
)
```

### Build Knowledge Base from Wikipedia

```python
from markitdown import MarkItDown

def build_wiki_context(topics: list[str]) -> str:
    """Build LLM context from Wikipedia articles."""
    md = MarkItDown()
    sections = []

    for topic in topics:
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        try:
            result = md.convert(url)
            # Truncate long articles
            content = result.text_content[:5000]
            sections.append(f"## {topic}\n\n{content}")
        except Exception:
            continue

    return "\n\n---\n\n".join(sections)

# Usage
context = build_wiki_context(["Python", "JavaScript", "Rust"])
```

## Azure Document Intelligence

### Complex PDF with Tables

```python
from markitdown import MarkItDown
import os

# Set up credentials
os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"] = "your-key"

md = MarkItDown(
    docintel_endpoint="https://your-resource.cognitiveservices.azure.com/"
)

# Better extraction for complex layouts
result = md.convert("financial-report.pdf")
print(result.text_content)
```

### Scanned Document Processing

```python
from markitdown import MarkItDown

md = MarkItDown(
    docintel_endpoint="https://your-resource.cognitiveservices.azure.com/"
)

# OCR and layout analysis for scanned docs
result = md.convert("scanned-contract.pdf")
print(result.text_content)
```

## CLI Examples

### Basic Conversion

```bash
# PDF to stdout
markitdown report.pdf

# Save to file
markitdown report.pdf -o report.md

# Word document
markitdown document.docx -o document.md

# PowerPoint
markitdown slides.pptx -o slides.md
```

### Batch Processing

```bash
# Convert all PDFs
for f in *.pdf; do markitdown "$f" -o "${f%.pdf}.md"; done

# With parallel processing
ls *.pdf | xargs -P 4 -I {} sh -c 'markitdown "$1" -o "${1%.pdf}.md"' _ {}

# Recursive conversion
find . -name "*.docx" -exec sh -c 'markitdown "$1" -o "${1%.docx}.md"' _ {} \;
```

### Piping and Integration

```bash
# Pipe to grep
markitdown document.pdf | grep -i "important"

# Count words
markitdown document.pdf | wc -w

# Send to LLM CLI
markitdown document.pdf | llm "Summarize this document"

# Download and convert
curl -sL "https://example.com/doc.pdf" | markitdown > doc.md
```

### Document Intelligence CLI

```bash
# Set credentials
export AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="https://..."
export AZURE_DOCUMENT_INTELLIGENCE_KEY="..."

# Convert with Document Intelligence
markitdown complex.pdf -d -e "$AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT" -o output.md
```
