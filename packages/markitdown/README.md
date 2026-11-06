# MarkItDown

> [!TIP]
> MarkItDown is a Python package and command-line utility for converting various files to Markdown (e.g., for indexing, text analysis, etc).
>
> For more information, and full documentation, see the project [README.md](https://github.com/microsoft/markitdown) on GitHub.

> [!IMPORTANT]
> MarkItDown performs I/O with the privileges of the current process. Like open() or requests.get(), it will access resources that the process itself can access. Sanitize your inputs in untrusted environments, and call the narrowest `convert_*` function needed for your use case (e.g., `convert_stream()`, or `convert_local()`). See the [Security Considerations](https://github.com/microsoft/markitdown#security-considerations) section of the documentation for more information.

## Installation

From PyPI:

```bash
pip install 'markitdown[all]'
```

From source:

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

## Usage

### Command-Line

```bash
markitdown path-to-file.pdf > document.md
```

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("test.xlsx")
print(result.markdown)
```

### Optional conversion diagnostics

```python
from markitdown import MarkItDown

result = MarkItDown().convert("document.html", include_diagnostics=True)
print(result.diagnostics.converter)
print(result.diagnostics.warnings)
```

Diagnostics are `None` by default. When requested, an immutable
`ConversionDiagnostics` reports the successful outer converter's class name and
a tuple of stable warning codes. The initial code,
`html_recursion_plain_text_fallback`, reports when the HTML converter falls back
to plain text after a recursion error. Existing Python warnings and strict-mode
exceptions are preserved. An empty tuple does not guarantee lossless conversion.

Converter-provided diagnostics are preserved. Nested diagnostics are not
aggregated. Charset confidence, failed attempts, cloud involvement, CLI JSON,
and configurable thresholds are outside this initial API. Diagnostic values do
not include input content, filenames, URLs, or exception text. Custom converters
are responsible for following the same convention for their warning codes.

### More Information

For more information, and full documentation, see the project [README.md](https://github.com/microsoft/markitdown) on GitHub.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
