# MarkItDown Sample Plugin

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)


This project shows how to create a sample plugin for MarkItDown. The two most important parts are as follows:

First, implement you custom DocumentConverter:

```python
from typing import Union
from markitdown import DocumentConverter, DocumentConverterResult


class RtfConverter(DocumentConverter):
    def convert(self, local_path, **kwargs) -> Union[None, DocumentConverterResult]:
        # Bail if not an RTF file 
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".rtf":
            return None

	# Implement the conversion logic here ...

        # Return the result
        return DocumentConverterResult(
            title=title,
            text_content=text_content,
        )
```

Second, you create an entrypoint in the `pyproject.toml` file:

```toml
[project.entry-points."markitdown.plugin.converters"]
rtf = "markitdown_sample_plugin:RtfConverter"
```

Here, the value of `rtf` can be any key, but should ideally be the name of the plugin, or the extension it supports. The value is the fully qualified name of the class that implements the `DocumentConverter` interface.


Once the plugin package is installed (e.g., `pip install -e .`), MarkItDown will automatically discover the plugin and register it for use.


## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
