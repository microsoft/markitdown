---
component_id: 5.2
component_name: Plugin Extension Framework & Samples
---

# Plugin Extension Framework & Samples

## Component Description

Defines the standard interface and registration mechanism for external library extensions. It demonstrates how to add support for new file formats (like RTF) as standalone packages that integrate seamlessly with the core orchestrator.

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-sample-plugin/src/markitdown_sample_plugin/_plugin.py (lines 34-71)
```
class RtfConverter(DocumentConverter):
    """
    Converts an RTF file to in the simplest possible way.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Read the file stream into an str using hte provided charset encoding, or using the system default
        encoding = stream_info.charset or locale.getpreferredencoding()
        stream_data = file_stream.read().decode(encoding)

        # Return the result
        return DocumentConverterResult(
            title=None,
            markdown=rtf_to_text(stream_data),
        )
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown-sample-plugin/src/markitdown_sample_plugin/_plugin.py (lines 25-31)
```
def register_converters(markitdown: MarkItDown, **kwargs):
    """
    Called during construction of MarkItDown instances to register converters provided by plugins.
    """

    # Simply create and attach an RtfConverter instance
    markitdown.register_converter(RtfConverter())
```


## Source Files:

- `packages/markitdown-sample-plugin/src/markitdown_sample_plugin/_plugin.py`

