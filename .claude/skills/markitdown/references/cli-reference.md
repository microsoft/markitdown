# MarkItDown CLI Reference

Complete command-line interface documentation for MarkItDown.

## Basic Syntax

```bash
markitdown [OPTIONS] [INPUT_FILE]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `INPUT_FILE` | Path to file or URL to convert. Can also be piped via stdin. |

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output file path (default: stdout) |
| `--use-plugins` | | Enable third-party plugins |
| `--list-plugins` | | List installed plugins and exit |
| `--docintel` | `-d` | Use Azure Document Intelligence |
| `--endpoint` | `-e` | Azure Document Intelligence endpoint URL |
| `--help` | `-h` | Show help message |
| `--version` | | Show version |

## Usage Examples

### Basic Conversion

```bash
# Convert PDF to markdown (stdout)
markitdown document.pdf

# Save to file
markitdown document.pdf -o output.md

# Convert Word document
markitdown report.docx -o report.md

# Convert PowerPoint
markitdown presentation.pptx -o slides.md

# Convert Excel
markitdown data.xlsx -o data.md
```

### Piping Input

```bash
# Pipe file content
cat document.pdf | markitdown > output.md

# Download and convert
curl -s "https://example.com/doc.pdf" | markitdown > output.md

# From clipboard (macOS)
pbpaste | markitdown
```

### Batch Processing

```bash
# Convert all PDFs in directory
for f in *.pdf; do
    markitdown "$f" -o "${f%.pdf}.md"
done

# Using find for recursive conversion
find . -name "*.docx" -exec sh -c 'markitdown "$1" -o "${1%.docx}.md"' _ {} \;

# Parallel processing with xargs
ls *.pdf | xargs -P 4 -I {} sh -c 'markitdown "$1" -o "${1%.pdf}.md"' _ {}
```

### URL Conversion

```bash
# YouTube video transcript
markitdown "https://www.youtube.com/watch?v=VIDEO_ID" -o transcript.md

# Web page
markitdown "https://example.com/article" -o article.md
```

### Azure Document Intelligence

```bash
# Set environment variables
ENDPOINT="https://your-resource.cognitiveservices.azure.com/"
export AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="$ENDPOINT"
export AZURE_DOCUMENT_INTELLIGENCE_KEY="your-key"

# Convert with Document Intelligence
markitdown complex-document.pdf -d \
  -e "$AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT" \
  -o output.md

# For better PDF extraction
markitdown scanned-document.pdf -d \
  -e "$AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
```

### Plugin Usage

```bash
# List available plugins
markitdown --list-plugins

# Convert with plugins enabled
markitdown --use-plugins document.pdf -o output.md

# Check if specific plugin is installed
markitdown --list-plugins | grep "plugin-name"
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` | Azure Document Intelligence endpoint |
| `AZURE_DOCUMENT_INTELLIGENCE_KEY` | Azure Document Intelligence API key |
| `OPENAI_API_KEY` | OpenAI API key for LLM image descriptions |

## File Format Detection

MarkItDown automatically detects file formats based on:

1. File extension
2. MIME type
3. File magic bytes

Supported extensions:

| Extension | Format |
|-----------|--------|
| `.pdf` | PDF documents |
| `.docx` | Word documents |
| `.doc` | Legacy Word |
| `.pptx` | PowerPoint |
| `.ppt` | Legacy PowerPoint |
| `.xlsx` | Excel spreadsheets |
| `.xls` | Legacy Excel |
| `.csv` | CSV data |
| `.json` | JSON data |
| `.xml` | XML data |
| `.html`, `.htm` | HTML pages |
| `.msg` | Outlook messages |
| `.epub` | EPub books |
| `.zip` | ZIP archives |
| `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp` | Images |
| `.mp3`, `.wav` | Audio files |

## Tips and Best Practices

### Performance

```bash
# For large files, redirect to file instead of stdout
markitdown large-file.pdf -o output.md  # Faster than > output.md

# Process multiple files in parallel
parallel markitdown {} -o {.}.md ::: *.pdf
```

### Error Handling

```bash
# Check if conversion succeeded
if markitdown document.pdf -o output.md; then
    echo "Conversion successful"
else
    echo "Conversion failed" >&2
fi

# Capture errors
markitdown document.pdf -o output.md 2>errors.log
```

### Integration with Other Tools

```bash
# Convert and search
markitdown document.pdf | grep -i "keyword"

# Convert and count words
markitdown document.pdf | wc -w

# Convert and extract links
markitdown document.pdf | grep -oE '\[.*?\]\(.*?\)'

# Convert and send to LLM
markitdown document.pdf | llm "Summarize this document"
```
