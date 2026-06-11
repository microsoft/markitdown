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

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("test.xlsx")
print(result.text_content)
```

### gRPC API

Install the gRPC extra first: `pip install 'markitdown[grpc]'`

- Protobuf definition: `proto/markitdown/v1/markitdown.proto`
- Server entrypoint: `markitdown-grpc --bind-address 127.0.0.1:50051`
- Stub regeneration: `./scripts/regenerate-grpc.sh`

Three RPCs are available:

- `Convert` returns the full Markdown in a single response.
- `ConvertStream` returns the Markdown as an ordered stream of chunks.
- `ConvertDocumentStream` returns the document as an ordered stream of structured elements (headings, paragraphs, tables, lists, code blocks, images, ...).

Both streaming RPCs support EXPERIMENTAL incremental conversion (`streaming_options.experimental_incremental`): PDF and PPTX results stream as each page or slide is processed, backed by the `markitdown.streaming` package.

The server is unauthenticated and performs I/O with the privileges of the server process; bind to localhost unless the network path is otherwise secured. See [Security Considerations](https://github.com/microsoft/markitdown#security-considerations).

### More Information

For more information, and full documentation, see the project [README.md](https://github.com/microsoft/markitdown) on GitHub.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
