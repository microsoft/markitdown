> [!IMPORTANT]
> (12/19/24) Hello! MarkItDown team members will be resting and recharging with family and friends over the holiday period. Activity/responses on the project may be delayed during the period of Dec 21-Jan 06. We will be excited to engage with you in the new year!

# MarkItDown

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)


MarkItDown is a utility for converting various files to Markdown (e.g., for indexing, text analysis, etc).
It supports:
- PDF
- PowerPoint
- Word
- Excel
- Images (EXIF metadata and OCR)
- Audio (EXIF metadata and speech transcription)
- HTML
- Text-based formats (CSV, JSON, XML)
- ZIP files (iterates over contents)

To install MarkItDown, use pip: `pip install markitdown`. Alternatively, you can install it from the source: `pip install -e .`

## Usage

### Command-Line

```bash
markitdown path-to-file.pdf > document.md
```

Or use `-o` to specify the output file:

```bash
markitdown path-to-file.pdf -o document.md
```

You can also pipe content:

```bash
cat path-to-file.pdf | markitdown
```

### Python API

Basic usage in Python:

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("test.xlsx")
print(result.text_content)
```

To use Large Language Models for image descriptions, provide `llm_client` and `llm_model`:

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("example.jpg")
print(result.text_content)
```

### Docker

```sh
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```
<details>
    
<summary>Batch Processing Multiple Files</summary>

This example shows how to convert multiple files to markdown format in a single run. The script processes all supported files in a directory and creates corresponding markdown files.


```python convert.py
from markitdown import MarkItDown
from openai import OpenAI
import os
client = OpenAI(api_key="your-api-key-here")
md = MarkItDown(llm_client=client, llm_model="gpt-4o-2024-11-20")
supported_extensions = ('.pptx', '.docx', '.pdf', '.jpg', '.jpeg', '.png')
files_to_convert = [f for f in os.listdir('.') if f.lower().endswith(supported_extensions)]
for file in files_to_convert:
    print(f"\nConverting {file}...")
    try:
        md_file = os.path.splitext(file)[0] + '.md'
        result = md.convert(file)
        with open(md_file, 'w') as f:
            f.write(result.text_content)
        
        print(f"Successfully converted {file} to {md_file}")
    except Exception as e:
        print(f"Error converting {file}: {str(e)}")

print("\nAll conversions completed!")
```
2. Place the script in the same directory as your files
3. Install required packages: like openai
4. Run script ```bash python convert.py ```

Note that original files will remain unchanged and new markdown files are created with the same base name.

</details>
