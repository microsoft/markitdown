# MarkItDown

> [!IMPORTANT]
> MarkItDown is a Python package and command-line utility for converting various files to Markdown (e.g., for indexing, text analysis, etc). 
>
> For more information, and full documentation, see the project [README.md](https://github.com/microsoft/markitdown) on GitHub.

## Installation

From PyPI:

```bash
pip install markitdown[all]
```

From source:

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e packages/markitdown[all]
```

## Usage

### Command-Line

```bash
markitdown path-to-file.pdf > document.md
```

#### PDF Table Extraction

By default, PDF conversion outputs plain text (table structure is not preserved). You can enable experimental
table detection with the `--pdf-tables` flag:

```bash
markitdown --pdf-tables plumber invoice.pdf
markitdown --pdf-tables auto report.pdf
```

Modes:

* `none` (default): plain text via pdfminer.
* `plumber`: use `pdfplumber` if installed (general-purpose detection).
* `camelot`: use `camelot` if installed (works best on ruled tables; requires a real file path, not stdin).
* `auto`: try plumber first, then camelot; fall back to plain text.

Install optional dependencies:

```bash
pip install "markitdown[pdf-tables]"
```

Notes:
* Camelot may need Ghostscript for lattice mode (`apt-get install ghostscript` on Debian/Ubuntu).
* If dependencies are missing, MarkItDown silently falls back to plain text.
* Output is best-effort; complex/merged cells may degrade gracefully.

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("test.xlsx")
print(result.text_content)
```

Enable PDF tables in code:

```python
result = md.convert("sample.pdf", pdf_tables="auto")
print(result.markdown)
```

### More Information

For more information, and full documentation, see the project [README.md](https://github.com/microsoft/markitdown) on GitHub.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
