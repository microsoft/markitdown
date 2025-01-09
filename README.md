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

### How to Contribute

You can help by looking at issues or helping review PRs. Any issue or PR is welcome, but we have also marked some as 'open for contribution' and 'open for reviewing' to help facilitate community contributions. These are ofcourse just suggestions and you are welcome to contribute in any way you like.


<div align="center">

|                       | All                                      | Especially Needs Help from Community                                                                 |
|-----------------------|------------------------------------------|------------------------------------------------------------------------------------------|
| **Issues**            | [All Issues](https://github.com/microsoft/markitdown/issues) | [Issues open for contribution](https://github.com/microsoft/markitdown/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22) |
| **PRs**               | [All PRs](https://github.com/microsoft/markitdown/pulls)     | [PRs open for reviewing](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+is%3Aopen+label%3A%22open+for+reviewing%22)               |

</div>

### Running Tests and Checks

- Install `hatch` in your environment and run tests:
    ```sh
    pip install hatch  # Other ways of installing hatch: https://hatch.pypa.io/dev/install/
    hatch shell
    hatch test
    ```

  (Alternative) Use the Devcontainer which has all the dependencies installed:
    ```sh
    # Reopen the project in Devcontainer and run:
    hatch test
    ```

- Run pre-commit checks before submitting a PR: `pre-commit run --all-files`

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
