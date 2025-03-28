# MarkItDown Sample Plugin

[![PyPI](https://img.shields.io/pypi/v/markitdown-sample-plugin.svg)](https://pypi.org/project/markitdown-sample-plugin/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown-sample-plugin)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)


This project shows how to create a sample plugin for MarkItDown. The most important parts are as follows:

Next, implement your custom DocumentConverter:

```python
from typing import BinaryIO, Any
from markitdown import MarkItDown, DocumentConverter, DocumentConverterResult, StreamInfo

class RtfConverter(DocumentConverter):

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
	
	# Implement logic to check if the file stream is an RTF file
	# ...
	raise NotImplementedError()


    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:

	# Implement logic to convert the file stream to Markdown
	# ...
	raise NotImplementedError()
```

Next, make sure your package implements and exports the following:

```python
# The version of the plugin interface that this plugin uses. 
# The only supported version is 1 for now.
__plugin_interface_version__ = 1 

# The main entrypoint for the plugin. This is called each time MarkItDown instances are created.
def register_converters(markitdown: MarkItDown, **kwargs):
    """
    Called during construction of MarkItDown instances to register converters provided by plugins.
    """

    # Simply create and attach an RtfConverter instance
    markitdown.register_converter(RtfConverter())
```


Finally, create an entrypoint in the `pyproject.toml` file:

```toml
[project.entry-points."markitdown.plugin"]
sample_plugin = "markitdown_sample_plugin"
```

Here, the value of `sample_plugin` can be any key, but should ideally be the name of the plugin. The value is the fully qualified name of the package implementing the plugin.


## Installation

To use the plugin with MarkItDown, it must be installed. To install the plugin from the current directory use:

```bash
pip install -e .
```

Once the plugin package is installed, verify that it is available to MarkItDown by running:

```bash
markitdown --list-plugins
```

To use the plugin for a conversion use the `--use-plugins` flag. For example, to convert an RTF file:

```bash
markitdown --use-plugins path-to-file.rtf
```

In Python, plugins can be enabled as follows:

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True) 
result = md.convert("path-to-file.rtf")
print(result.text_content)
```

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
