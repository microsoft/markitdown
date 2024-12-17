# MarkItDown

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)

The MarkItDown library is a utility tool for converting various files to Markdown (e.g., for indexing, text analysis, etc.)

It presently supports:

- PDF (.pdf)
- PowerPoint (.pptx)
- Word (.docx)
- Excel (.xlsx)
- Images (EXIF metadata, and OCR)
- Audio (EXIF metadata, and speech transcription)
- HTML (special handling of Wikipedia, etc.)
- Various other text-based formats (csv, json, xml, etc.)
- ZIP (Iterates over contents and converts each file)

# Installation

You can install `markitdown` using pip:

```python
pip install markitdown
```

or from the source

```sh
pip install -e .
```

# Usage
The API is simple:

```python
from markitdown import MarkItDown

markitdown = MarkItDown()
result = markitdown.convert("test.xlsx")
print(result.text_content)
```

To use this as a command-line utility, install it and then run it like this:

```bash
markitdown path-to-file.pdf
```

This will output Markdown to standard output. You can save it like this:

```bash
markitdown path-to-file.pdf > document.md
```

You can pipe content to standard input by omitting the argument:

```bash
cat path-to-file.pdf | markitdown
```

You can also configure markitdown to use Large Language Models to describe images. To do so you must provide `llm_client` and `llm_model` parameters to MarkItDown object, according to your specific client.


```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("example.jpg")
print(result.text_content)
```

You can also use the project as Docker Image:

```sh
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

### Running Tests

To run tests, install `hatch` using `pip` or other methods as described [here](https://hatch.pypa.io/dev/install).

```sh
pip install hatch
hatch shell
hatch test
```

### Running Pre-commit Checks

Please run the pre-commit checks before submitting a PR.

```sh
pre-commit run --all-files
```

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
