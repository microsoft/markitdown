---
name: markitdown-plugins
description: >-
  Write, package and test a third-party MarkItDown converter plugin using the
  markitdown.plugin entry point, DocumentConverter, accepts() and convert().
  Use when adding support for a new file format without changing MarkItDown
  itself, or when debugging why a plugin is not picked up.
---

# Writing a MarkItDown plugin

New formats are added to core sparingly. The preferred path is a separate
plugin package. Reference implementation:
`packages/markitdown-sample-plugin` (an RTF converter).

## Package layout

```
my-plugin/
  pyproject.toml
  src/markitdown_my_plugin/__init__.py
  src/markitdown_my_plugin/_plugin.py
```

`pyproject.toml` must declare the entry point MarkItDown scans for:

```toml
[project.entry-points."markitdown.plugin"]
my_plugin = "markitdown_my_plugin"
```

## Plugin module

```python
from typing import BinaryIO, Any
from markitdown import (
    MarkItDown, DocumentConverter, DocumentConverterResult, StreamInfo,
)

__plugin_interface_version__ = 1

def register_converters(markitdown: MarkItDown, **kwargs):
    markitdown.register_converter(MyConverter())

class MyConverter(DocumentConverter):
    def accepts(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any) -> bool:
        ext = (stream_info.extension or "").lower()
        mime = (stream_info.mimetype or "").lower()
        return ext == ".foo" or mime.startswith("application/x-foo")

    def convert(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any) -> DocumentConverterResult:
        text = file_stream.read().decode(stream_info.charset or "utf-8")
        return DocumentConverterResult(title=None, markdown=text)
```

Rules:

- `accepts()` must not consume the stream irreversibly; MarkItDown may try
  several converters on the same stream.
- Return Markdown, not HTML; keep tables and headings as Markdown.
- Export `__plugin_interface_version__ = 1`.

## Try it

```bash
pip install -e .
markitdown --list-plugins
markitdown --use-plugins sample.foo
```

In Python: `MarkItDown(enable_plugins=True)`. Plugins are disabled by default,
so a plugin that "does nothing" usually just was not enabled.

## Publish

Tag the repository `#markitdown-plugin` so others can find it.
