# MarkItDown Reference

**Version:** 0.1.4  
**Last Updated:** December 17, 2025  
**Python Requirements:** >=3.10

This document provides a comprehensive technical reference for all public classes, methods, functions, exceptions, and other code constructs in the MarkItDown library.

MarkItDown is a utility for converting various document formats (PDF, DOCX, PPTX, images, audio, etc.) to Markdown text.

---

## Table of Contents

- [Installation](#installation)
- [Core Classes](#core-classes)
  - [MarkItDown](#markitdown)
  - [DocumentConverter](#documentconverter)
  - [DocumentConverterResult](#documentconverterresult)
- [Built-in Converters](#built-in-converters)
- [Data Classes](#data-classes)
  - [DocumentIntelligenceFileType](#documentintelligencefiletype)
  - [StreamInfo](#streaminfo)
  - [ConverterRegistration](#converterregistration)
- [Exception Classes](#exception-classes)
  - [MarkItDownException](#markitdownexception)
  - [MissingDependencyException](#missingdependencyexception)
  - [UnsupportedFormatException](#unsupportedformatexception)
  - [FileConversionException](#fileconversionexception)
  - [FailedConversionAttempt](#failedconversionattempt)
- [Utility Functions](#utility-functions)
- [Constants](#constants)
- [CLI Reference](#cli-reference)
- [Creating Custom Converters](#creating-custom-converters)
- [Plugin System](#plugin-system)

---

## Installation

```bash
# Basic installation
pip install markitdown

# With all optional dependencies
pip install "markitdown[all]"
```

### Optional Dependencies

Different converters require different optional dependencies:

- **Office Documents:** `python-pptx`, `mammoth`, `pandas`, `openpyxl`, `xlrd`
- **PDF:** `pdfminer.six`
- **Images (metadata + optional caption):** `exiftool` for metadata, `llm_client` (with `llm_model`) for LLM-generated captions
- **Audio (metadata + optional transcription):** `exiftool` for metadata, `pydub`, `SpeechRecognition` for transcription
- **Outlook MSG:** `olefile`
- **Azure Document Intelligence:** `azure-ai-documentintelligence`, `azure-identity`
- **YouTube:** `youtube-transcript-api`

---

## Core Classes

### `MarkItDown`

**Module:** `markitdown._markitdown`

The main class for converting various document formats to Markdown. This is the primary entry point for using the library.

#### Constructor

```python
MarkItDown(
    *,
    enable_builtins: Union[None, bool] = None,
    enable_plugins: Union[None, bool] = None,
    **kwargs
)
```

**Parameters:**
- `enable_builtins` (bool, optional): Enable built-in converters. Default: `True` (enabled by default)
- `enable_plugins` (bool, optional): Enable third-party plugin converters. Default: `False` (disabled by default)
- `**kwargs`: Additional configuration options passed to converters:
  - **General Options:**
    - `requests_session`: Optional `requests.Session` object to reuse for HTTP/HTTPS fetching. Used by all converters that fetch content from URLs.
    - `exiftool_path`: Optional path to the `exiftool` executable. Used by `ImageConverter` and `AudioConverter` for metadata extraction. Also supports `EXIFTOOL_PATH` environment variable.
  - **LLM / Image Captioning:**
    - `llm_client`: Language model client object. Used by `ImageConverter` for generating image descriptions.
    - `llm_model`: Model identifier string to use with `llm_client`. Used by `ImageConverter`.
    - `llm_prompt`: Optional prompt string to override the default image description prompt. Used by `ImageConverter`.
  - **Office Formats:**
    - `style_map`: Optional style-map string. Used by `DocxConverter` (via `mammoth`) to control how styles are mapped to HTML/Markdown.
  - **Azure Document Intelligence:**
    - `docintel_endpoint`: Optional endpoint URL. If provided, the `DocumentIntelligenceConverter` is registered.
    - `docintel_credential`: Optional Azure credential object. Defaults to `AZURE_API_KEY` environment variable or `DefaultAzureCredential`.
    - `docintel_file_types`: Optional list of `DocumentIntelligenceFileType` enum values to route to Document Intelligence. See [`DocumentIntelligenceFileType`](#documentintelligencefiletype) for available values. If not specified, defaults to all supported types except HTML.
    - `docintel_api_version`: Optional API version string for the Document Intelligence client (default: `2024-07-31-preview`).

**Example:**
```python
from markitdown import MarkItDown

# Basic usage with defaults
md = MarkItDown()

# With custom LLM client for image processing
md = MarkItDown(llm_client=my_llm_client)

# Disable built-ins, use only plugins
md = MarkItDown(enable_builtins=False, enable_plugins=True)
```

---

#### Methods

##### `enable_builtins(**kwargs) -> None`

Enable and register all built-in converters. Called automatically during initialization unless `enable_builtins=False` is specified.

**Parameters:**
- `**kwargs`: Converter-specific configuration options

**Raises:**
- `RuntimeWarning`: If built-in converters are already enabled

**Example:**
```python
md = MarkItDown(enable_builtins=False)
# Later, enable built-ins
md.enable_builtins(llm_client=my_client)
```

---

##### `enable_plugins(**kwargs) -> None`

Enable and register converters provided by installed plugins. Plugins are discovered via Python entry points in the `markitdown.plugin` group.

**Parameters:**
- `**kwargs`: Plugin-specific configuration options

**Raises:**
- `RuntimeWarning`: If plugins are already enabled

**Example:**
```python
md = MarkItDown(enable_plugins=True)
```

---

##### `convert(source, *, stream_info=None, **kwargs) -> DocumentConverterResult`

Convert a document from various sources to Markdown. This is the main conversion method that automatically detects the source type and delegates to the appropriate specialized method.

**Parameters:**
- `source` (str | Path | BinaryIO | requests.Response): The source to convert. Can be:
  - File path (str or Path)
  - URI (file://, data://, http://, https://)
  - Binary stream (file-like object)
  - HTTP Response object
- `stream_info` (StreamInfo, optional): Additional metadata about the stream (mimetype, extension, charset, etc.)
- `**kwargs`: Additional converter-specific options

**Returns:**
- `DocumentConverterResult`: Object containing the converted Markdown text and optional metadata

**Raises:**
- `TypeError`: If source type is not supported
- `FileConversionException`: If conversion fails
- `UnsupportedFormatException`: If no suitable converter is found
- `MissingDependencyException`: If required optional dependency is not installed

**Example:**
```python
# Convert local file
result = md.convert("document.pdf")

# Convert from URL
result = md.convert("https://example.com/page.html")

# Convert from stream
with open("file.docx", "rb") as f:
    result = md.convert(f)

# Access results
print(result.markdown)
print(result.title)
```

---

##### `convert_local(path, *, stream_info=None, file_extension=None, url=None, **kwargs) -> DocumentConverterResult`

Convert a local file to Markdown.

**Parameters:**
- `path` (str | Path): Path to the local file
- `stream_info` (StreamInfo, optional): Additional stream metadata
- `file_extension` (str, optional): **Deprecated.** Override file extension (e.g., ".pdf"). Use `stream_info` instead.
- `url` (str, optional): **Deprecated.** Mock URL for converters that need URL context. Use `stream_info` instead.
- `**kwargs`: Additional converter options

**Returns:**
- `DocumentConverterResult`: The conversion result

**Raises:**
- `FileNotFoundError`: If file does not exist
- `FileConversionException`: If conversion fails
- `UnsupportedFormatException`: If format is not supported

**Example:**
```python
result = md.convert_local("/path/to/document.pdf")
result = md.convert_local("file.txt", file_extension=".md")
```

---

##### `convert_stream(stream, *, stream_info=None, file_extension=None, url=None, **kwargs) -> DocumentConverterResult`

Convert a binary stream to Markdown.

**Parameters:**
- `stream` (BinaryIO): The binary stream to convert. Must support `seek()`, `tell()`, and `read()` methods
- `stream_info` (StreamInfo, optional): Stream metadata (mimetype, extension, etc.)
- `file_extension` (str, optional): **Deprecated.** Hint for file type (e.g., ".docx"). Use `stream_info` instead.
- `url` (str, optional): **Deprecated.** Mock URL for converters that need URL context. Use `stream_info` instead.
- `**kwargs`: Additional converter options

**Returns:**
- `DocumentConverterResult`: The conversion result

**Important:** The stream position may be modified during conversion.

**Example:**
```python
with open("document.docx", "rb") as f:
    result = md.convert_stream(f, file_extension=".docx")
```

---

##### `convert_uri(uri, *, stream_info=None, file_extension=None, mock_url=None, **kwargs) -> DocumentConverterResult`

Convert content from a URI to Markdown. Supports:
- `file://` - Local file URIs
- `data://` - Data URIs (embedded content)
- `http://` and `https://` - Remote URLs

**Parameters:**
- `uri` (str): The URI to convert
- `stream_info` (StreamInfo, optional): Additional stream metadata
- `file_extension` (str, optional): **Deprecated.** File extension override. Use `stream_info` instead.
- `mock_url` (str, optional): Alternative URL for converter context
- `**kwargs`: Additional converter options

**Returns:**
- `DocumentConverterResult`: The conversion result

**Raises:**
- `ValueError`: If URI scheme is unsupported
- `requests.RequestException`: If HTTP request fails

**Example:**
```python
# Local file URI
result = md.convert_uri("file:///Users/user/doc.pdf")

# Data URI
result = md.convert_uri("data:text/plain;base64,SGVsbG8gV29ybGQ=")

# HTTP URL
result = md.convert_uri("https://example.com/page.html")
```

---

##### `convert_url(url, *, stream_info=None, file_extension=None, mock_url=None, **kwargs) -> DocumentConverterResult`

⚠️ **Deprecated:** Use `convert_uri()` instead. This method is an alias maintained for backward compatibility.

---

##### `convert_response(response, *, stream_info=None, file_extension=None, url=None, **kwargs) -> DocumentConverterResult`

Convert an HTTP Response object to Markdown.

**Parameters:**
- `response` (requests.Response): The HTTP response object
- `stream_info` (StreamInfo, optional): Stream metadata override
- `file_extension` (str, optional): **Deprecated.** File extension hint. Use `stream_info` instead.
- `url` (str, optional): **Deprecated.** URL override (uses response.url by default). Use `stream_info` instead.
- `**kwargs`: Additional converter options

**Returns:**
- `DocumentConverterResult`: The conversion result

**Example:**
```python
import requests

response = requests.get("https://example.com/document.pdf")
result = md.convert_response(response)
```

---

##### `register_converter(converter, *, priority=PRIORITY_SPECIFIC_FILE_FORMAT) -> None`

Register a custom document converter.

**Parameters:**
- `converter` (DocumentConverter): The converter instance to register
- `priority` (float, optional): Converter priority. Lower values = higher priority. Default: `0.0`

**Priority Guidelines:**
- `PRIORITY_SPECIFIC_FILE_FORMAT` (0.0) - For specific formats (e.g., .pdf, .docx)
- `PRIORITY_GENERIC_FILE_FORMAT` (10.0) - For generic/fallback converters (e.g., plain text)

**Example:**
```python
from markitdown import MarkItDown, DocumentConverter

class MyConverter(DocumentConverter):
    def accepts(self, file_stream, stream_info, **kwargs):
        return stream_info.extension == ".custom"
    
    def convert(self, file_stream, stream_info, **kwargs):
        # Conversion logic
        return DocumentConverterResult(markdown="# Converted")

md = MarkItDown()
md.register_converter(MyConverter(), priority=0.0)
```

---

##### `register_page_converter(converter) -> None`

⚠️ **Deprecated:** Use `register_converter()` instead. This method is maintained for backward compatibility.

---

### `DocumentConverter`

**Module:** `markitdown._base_converter`

Abstract base class for all document converters. Custom converters must inherit from this class and implement both required methods.

#### Abstract Methods

##### `accepts(file_stream, stream_info, **kwargs) -> bool`

Determine if the converter can handle the given document. This method should make a quick determination based primarily on `stream_info` metadata.

**Parameters:**
- `file_stream` (BinaryIO): The file stream to check. Must support `seek()`, `tell()`, and `read()`
- `stream_info` (StreamInfo): Metadata about the file (mimetype, extension, charset, url, filename)
- `**kwargs`: Additional options (same as will be passed to `convert()`)

**Returns:**
- `bool`: `True` if this converter can handle the document, `False` otherwise

**Important Notes:**
- Method signature matches `convert()` to ensure consistency
- If you need to read from the stream for detection, you **must** reset the position:
  ```python
  cur_pos = file_stream.tell()
  data = file_stream.read(100)  # Peek at data
  file_stream.seek(cur_pos)     # Reset position!
  ```
- Primary determination should be based on `stream_info.mimetype` or `stream_info.extension`
- For special URLs (Wikipedia, YouTube), check `stream_info.url`
- For well-known files (Dockerfile, Makefile), check `stream_info.filename`

**Example:**
```python
def accepts(self, file_stream, stream_info, **kwargs):
    # Check extension
    if stream_info.extension == ".myformat":
        return True
    
    # Check MIME type
    if stream_info.mimetype == "application/x-myformat":
        return True
    
    return False
```

---

##### `convert(file_stream, stream_info, **kwargs) -> DocumentConverterResult`

Convert a document to Markdown text.

**Parameters:**
- `file_stream` (BinaryIO): The file stream to convert. Must support `seek()`, `tell()`, and `read()`
- `stream_info` (StreamInfo): Metadata about the file
- `**kwargs`: Additional converter-specific options

**Returns:**
- `DocumentConverterResult`: The conversion result with markdown text and optional title

**Raises:**
- `FileConversionException`: If the format is recognized but conversion fails
- `MissingDependencyException`: If a required optional dependency is not installed

**Example:**
```python
def convert(self, file_stream, stream_info, **kwargs):
    try:
        content = file_stream.read().decode('utf-8')
        markdown = f"# Document\n\n{content}"
        return DocumentConverterResult(
            markdown=markdown,
            title="My Document"
        )
    except Exception as e:
        raise FileConversionException(f"Failed to convert: {e}")
```

---

### `DocumentConverterResult`

**Module:** `markitdown._base_converter`

Represents the result of a document conversion operation.

#### Constructor

```python
DocumentConverterResult(markdown: str, *, title: Optional[str] = None)
```

**Parameters:**
- `markdown` (str, required): The converted Markdown text
- `title` (str, optional): Optional title of the document

**Example:**
```python
result = DocumentConverterResult(
    markdown="# Hello\n\nThis is markdown content.",
    title="My Document"
)
```

---

#### Attributes

- `markdown` (str): The converted Markdown text
- `title` (str | None): Optional document title

---

#### Properties

##### `text_content` (str)

⚠️ **Soft-deprecated:** Alias for `markdown`. New code should use `.markdown` attribute or `str(result)` instead.

**Getter:** Returns the markdown text  
**Setter:** Sets the markdown text

**Example:**
```python
# Old way (deprecated)
text = result.text_content

# New way (preferred)
text = result.markdown
# or
text = str(result)
```

---

#### Methods

##### `__str__() -> str`

Return the converted Markdown text. Allows the result to be used directly as a string.

**Returns:**
- `str`: The markdown content

**Example:**
```python
result = md.convert("file.pdf")
print(result)  # Prints the markdown
```

---

## Built-in Converters

All built-in converters are automatically registered when `enable_builtins=True` (default). Each converter inherits from [`DocumentConverter`](#documentconverter).

**Module:** `markitdown.converters`

**See also:** [`DocumentIntelligenceConverter`](#azure-integration) for Azure Document Intelligence integration.

### Document Converters

| Converter | Supported Formats | MIME Types | Optional Dependencies |
|-----------|------------------|------------|---------------------|
| `PlainTextConverter` | Plain text, Markdown, JSON | `text/plain`, `application/json`, `application/markdown` | None |
| `HtmlConverter` | HTML documents | `text/html`, `application/xhtml` | None (uses beautifulsoup4) |
| `PdfConverter` | PDF documents | `application/pdf`, `application/x-pdf` | `pdfminer.six` |
| `DocxConverter` | Word documents | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | `mammoth` |
| `XlsxConverter` | Excel spreadsheets | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | `pandas`, `openpyxl` |
| `XlsConverter` | Legacy Excel | `application/vnd.ms-excel`, `application/excel` | `pandas`, `xlrd` |
| `PptxConverter` | PowerPoint | `application/vnd.openxmlformats-officedocument.presentationml.presentation` | `python-pptx` |
| `ImageConverter` | Images (JPG, PNG) | `image/jpeg`, `image/png` | `exiftool` (metadata), `llm_client` (description) |
| `AudioConverter` | Audio files (WAV, MP3, MP4) | `audio/x-wav`, `audio/mpeg`, `video/mp4` | `pydub`, `SpeechRecognition` |
| `OutlookMsgConverter` | Outlook messages | `application/vnd.ms-outlook` | `olefile` |
| `ZipConverter` | ZIP archives | `application/zip` | None |
| `EpubConverter` | EPUB ebooks | `application/epub+zip`, `application/x-epub+zip` | `defusedxml`, `beautifulsoup4` |
| `CsvConverter` | CSV files | `text/csv`, `application/csv` | None |
| `IpynbConverter` | Jupyter notebooks | `application/x-ipynb+json` | None |

### Web & Special Converters

| Converter | Description | Optional Dependencies |
|-----------|-------------|---------------------|
| `RssConverter` | RSS/Atom feeds | None |
| `WikipediaConverter` | Wikipedia pages | None |
| `YouTubeConverter` | YouTube video transcripts | `youtube-transcript-api` |
| `BingSerpConverter` | Bing search result pages | None |

### Azure Integration

| Converter | Supported Formats | Optional Dependencies |
|-----------|-------------------|---------------------|
| `DocumentIntelligenceConverter` | PDF; Office (DOCX/PPTX/XLSX); Images (JPEG/PNG/BMP/TIFF) | `azure-ai-documentintelligence`, `azure-identity` |

**Note:** Converters are tried in priority order. More specific converters have higher priority (lower priority number).

**Document Intelligence note:** HTML is only routed to Document Intelligence when `docintel_file_types` explicitly includes `DocumentIntelligenceFileType.HTML`.

---

## Data Classes

### `DocumentIntelligenceFileType`

**Module:** `markitdown.converters._doc_intel_converter`

Enum of file types supported by the Azure Document Intelligence Converter.

#### Enum Values

**Office Formats (No OCR):**
- `DocumentIntelligenceFileType.DOCX` - Word documents (`.docx`)
- `DocumentIntelligenceFileType.PPTX` - PowerPoint presentations (`.pptx`)
- `DocumentIntelligenceFileType.XLSX` - Excel spreadsheets (`.xlsx`)
- `DocumentIntelligenceFileType.HTML` - HTML documents (`.html`)

**Document & Image Formats (With OCR):**
- `DocumentIntelligenceFileType.PDF` - PDF documents (`.pdf`)
- `DocumentIntelligenceFileType.JPEG` - JPEG images (`.jpg`, `.jpeg`)
- `DocumentIntelligenceFileType.PNG` - PNG images (`.png`)
- `DocumentIntelligenceFileType.BMP` - BMP images (`.bmp`)
- `DocumentIntelligenceFileType.TIFF` - TIFF images (`.tiff`)

**Example:**
```python
from markitdown import MarkItDown
from markitdown.converters import DocumentIntelligenceFileType

# Use Document Intelligence only for PDFs and images
md = MarkItDown(
    docintel_endpoint="https://your-endpoint.cognitiveservices.azure.com/",
    docintel_file_types=[
        DocumentIntelligenceFileType.PDF,
        DocumentIntelligenceFileType.JPEG,
        DocumentIntelligenceFileType.PNG
    ]
)
```

**Notes:**
- Office formats (DOCX, PPTX, XLSX, HTML) do not support OCR features
- Document and image formats support high-resolution OCR, formulas, and font style extraction
- By default, if `docintel_file_types` is not specified, all types except HTML are enabled

---

### `StreamInfo`

**Module:** `markitdown._stream_info`

Immutable dataclass containing metadata about a file stream. Used to provide context to converters about the file being processed.

#### Constructor

```python
@dataclass(frozen=True)
StreamInfo(
    *,
    mimetype: Optional[str] = None,
    extension: Optional[str] = None,
    charset: Optional[str] = None,
    filename: Optional[str] = None,
    local_path: Optional[str] = None,
    url: Optional[str] = None
)
```

**Parameters:**
- `mimetype` (str, optional): MIME type (e.g., `"application/pdf"`, `"text/html"`)
- `extension` (str, optional): File extension with leading dot (e.g., `".pdf"`, `".docx"`)
- `charset` (str, optional): Character encoding (e.g., `"utf-8"`, `"iso-8859-1"`)
- `filename` (str, optional): Filename (from path, URL, or Content-Disposition header)
- `local_path` (str, optional): Local filesystem path if applicable
- `url` (str, optional): URL if content was retrieved from the web

**All parameters are optional and keyword-only.**

**Example:**
```python
from markitdown import StreamInfo

info = StreamInfo(
    mimetype="application/pdf",
    extension=".pdf",
    filename="document.pdf",
    local_path="/path/to/document.pdf"
)
```

---

#### Attributes

All constructor parameters are available as read-only attributes (frozen dataclass):
- `mimetype` (str | None)
- `extension` (str | None)
- `charset` (str | None)
- `filename` (str | None)
- `local_path` (str | None)
- `url` (str | None)

---

#### Methods

##### `copy_and_update(*args, **kwargs) -> StreamInfo`

Create a copy of the StreamInfo with updated fields. Useful for creating variations with some fields overridden.

**Parameters:**
- `*args` (StreamInfo): Zero or more StreamInfo instances to merge. Later instances override earlier ones
- `**kwargs`: Additional fields to update (e.g., `mimetype="text/html"`)

**Returns:**
- `StreamInfo`: New instance with updated fields

**Example:**
```python
base_info = StreamInfo(extension=".txt", charset="utf-8")

# Update one field
new_info = base_info.copy_and_update(mimetype="text/plain")

# Merge with another StreamInfo
other_info = StreamInfo(filename="document.txt")
merged = base_info.copy_and_update(other_info, url="http://example.com")
```

---

### `ConverterRegistration`

**Module:** `markitdown._markitdown`

Internal dataclass representing a registered converter with its priority. Used internally by MarkItDown to manage the converter registry.

#### Attributes

- `converter` (DocumentConverter): The converter instance
- `priority` (float): Converter priority (lower = higher priority)

**Note:** This is primarily an internal class. Users typically don't interact with it directly.

---

## Exception Classes

All MarkItDown exceptions inherit from `MarkItDownException`, which inherits from Python's built-in `Exception`.

### `MarkItDownException`

**Module:** `markitdown._exceptions`

Base exception class for all MarkItDown-specific exceptions.

**Inherits:** `Exception`

**Usage:**
```python
try:
    result = md.convert("file.pdf")
except MarkItDownException as e:
    # Catch any MarkItDown-specific error
    print(f"Conversion error: {e}")
```

---

### `MissingDependencyException`

**Module:** `markitdown._exceptions`

**Inherits:** `MarkItDownException`

Raised when a converter requires an optional dependency that is not installed.

#### Constructor

```python
MissingDependencyException(message: str)
```

**Parameters:**
- `message` (str): Error message describing the missing dependency

**Example:**
```python
from markitdown import MarkItDown, MissingDependencyException

md = MarkItDown()

try:
    result = md.convert("presentation.pptx")
except MissingDependencyException as e:
    print(f"Missing dependency: {e}")
    print('Install with: pip install "markitdown[all]"')
```

**Common Causes:**
- Trying to convert PPTX without `python-pptx`
- Trying to convert DOCX without `mammoth`
- Trying to convert Excel without `pandas` and `openpyxl`/`xlrd`
- Trying to use audio transcription without `pydub` and `SpeechRecognition`

---

### `UnsupportedFormatException`

**Module:** `markitdown._exceptions`

**Inherits:** `MarkItDownException`

Raised when no suitable converter is found for the given file format.

#### Constructor

```python
UnsupportedFormatException(message: str)
```

**Parameters:**
- `message` (str): Error message describing the unsupported format

**Example:**
```python
from markitdown import MarkItDown, UnsupportedFormatException

md = MarkItDown()

try:
    result = md.convert("file.xyz")
except UnsupportedFormatException as e:
    print(f"Unsupported format: {e}")
    print("Consider writing a custom converter")
```

**Common Causes:**
- File extension not recognized by any converter
- MIME type not supported
- File type detection failed

**Solution:**
- Register a custom converter for the format
- Convert the file to a supported format first

---

### `FileConversionException`

**Module:** `markitdown._exceptions`

**Inherits:** `MarkItDownException`

Raised when a suitable converter is found but the conversion process fails for some reason.

#### Constructor

```python
FileConversionException(
    message: Optional[str] = None,
    attempts: Optional[List[FailedConversionAttempt]] = None
)
```

**Parameters:**
- `message` (str, optional): Error message
- `attempts` (List[FailedConversionAttempt], optional): List of failed conversion attempts

---

#### Attributes

- `attempts` (List[FailedConversionAttempt] | None): List of failed conversion attempts with details

**Example:**
```python
from markitdown import MarkItDown, FileConversionException

md = MarkItDown()

try:
    result = md.convert("corrupted.pdf")
except FileConversionException as e:
    print(f"Conversion failed: {e}")
    
    # Inspect failed attempts
    if e.attempts:
        for attempt in e.attempts:
            print(f"  Converter: {attempt.converter}")
            if attempt.exc_info:
                exc_type, exc_value, exc_tb = attempt.exc_info
                print(f"  Error: {exc_value}")
```

**Common Causes:**
- Corrupted file
- File is password-protected
- File uses unsupported features
- Encoding issues
- Network errors (for URL conversions)

---

### `FailedConversionAttempt`

**Module:** `markitdown._exceptions`

Represents a single failed conversion attempt. Contains information about which converter failed and why.

#### Constructor

```python
FailedConversionAttempt(converter: Any, exc_info: Optional[tuple] = None)
```

**Parameters:**
- `converter` (Any): The converter instance that failed
- `exc_info` (tuple, optional): Exception information from `sys.exc_info()` as `(type, value, traceback)`

---

#### Attributes

- `converter` (DocumentConverter): The converter instance that failed
- `exc_info` (tuple | None): Exception information tuple `(type, value, traceback)`

**Example:**
```python
import sys
from markitdown import FailedConversionAttempt

try:
    # Conversion logic
    pass
except Exception:
    attempt = FailedConversionAttempt(
        converter=my_converter,
        exc_info=sys.exc_info()
    )
```

---

## Utility Functions

**Module:** `markitdown._uri_utils`

### `file_uri_to_path(file_uri: str) -> Tuple[str | None, str]`

Convert a `file://` URI to a local filesystem path.

**Parameters:**
- `file_uri` (str): URI with `file://` scheme

**Returns:**
- `tuple`: `(netloc, path)` where:
  - `netloc` (str | None): Network location (hostname) or `None` for local files
  - `path` (str): Absolute filesystem path

**Raises:**
- `ValueError`: If URI scheme is not `file://`

**Example:**
```python
from markitdown._uri_utils import file_uri_to_path

# Local file
netloc, path = file_uri_to_path("file:///home/user/document.pdf")
# netloc = None, path = "/home/user/document.pdf"

# Windows path
netloc, path = file_uri_to_path("file:///C:/Users/user/document.pdf")
# netloc = None, path = "C:/Users/user/document.pdf"

# Network location
netloc, path = file_uri_to_path("file://server/share/document.pdf")
# netloc = "server", path = "/share/document.pdf"
```

---

### `parse_data_uri(uri: str) -> Tuple[str | None, Dict[str, str], bytes]`

Parse a `data:` URI into its components.

**Parameters:**
- `uri` (str): URI with `data:` scheme

**Returns:**
- `tuple`: `(mime_type, attributes, content)` where:
  - `mime_type` (str | None): MIME type (default: `"text/plain"` if not specified)
  - `attributes` (dict): Additional attributes like `{"charset": "utf-8"}`
  - `content` (bytes): Decoded content (handles base64 encoding)

**Raises:**
- `ValueError`: If URI is not a valid data URI

**Example:**
```python
from markitdown._uri_utils import parse_data_uri

# Base64 encoded
mime, attrs, content = parse_data_uri(
    "data:text/plain;base64,SGVsbG8gV29ybGQ="
)
# mime = "text/plain", attrs = {}, content = b"Hello World"

# With charset
mime, attrs, content = parse_data_uri(
    "data:text/html;charset=utf-8,<h1>Hello</h1>"
)
# mime = "text/html", attrs = {"charset": "utf-8"}, content = b"<h1>Hello</h1>"
```

---

## Constants

**Module:** `markitdown._markitdown`

### `PRIORITY_SPECIFIC_FILE_FORMAT`

**Type:** `float`  
**Value:** `0.0`

Priority value for specific file format converters (e.g., PDF, DOCX, XLSX). Converters with lower priority numbers are tried first.

**Usage:**
```python
md.register_converter(MySpecificConverter(), priority=PRIORITY_SPECIFIC_FILE_FORMAT)
```

---

### `PRIORITY_GENERIC_FILE_FORMAT`

**Type:** `float`  
**Value:** `10.0`

Priority value for generic/catch-all converters (e.g., plain text, HTML). These should be tried after more specific converters.

**Usage:**
```python
md.register_converter(MyGenericConverter(), priority=PRIORITY_GENERIC_FILE_FORMAT)
```

---

### Priority Guidelines

- **Specialized converters (0.0):** Converters for specific file formats with unique structure
- **Generic converters (10.0):** Fallback converters that can handle multiple formats
- **Custom priorities:** Use values in between for fine-grained control

Lower values = higher priority (tried first)

---

## CLI Reference

MarkItDown includes a command-line interface for converting files to Markdown.

### Basic Usage

```bash
# Convert file to stdout
markitdown document.pdf

# Convert and save to file
markitdown document.pdf -o output.md

# Convert from URL
markitdown https://example.com/page.html

# Convert from stdin
cat document.html | markitdown

# Specify file extension hint
markitdown - --extension .html < input.html
```

### Command Line Options

```
usage: markitdown [-h] [-v] [-o OUTPUT] [-x EXTENSION] [-m MIME_TYPE]
                  [-c CHARSET] [-d] [-e ENDPOINT] [-p] [--list-plugins]
                  [--keep-data-uris]
                  [filename]

Convert various file formats to markdown.

positional arguments:
  filename              Path, URL, or '-' for stdin

optional arguments:
  -h, --help            show help message and exit
  -v, --version         show the version number and exit
  -o OUTPUT, --output OUTPUT
                        Output file name. If not provided, output is written to stdout.
  -x EXTENSION, --extension EXTENSION
                        Provide a hint about the file extension (e.g., when reading from stdin).
  -m MIME_TYPE, --mime-type MIME_TYPE
                        Provide a hint about the file's MIME type.
  -c CHARSET, --charset CHARSET
                        Provide a hint about the file's charset (e.g, UTF-8).
  -d, --use-docintel    Use Document Intelligence to extract text instead of offline conversion. Requires a valid Document Intelligence Endpoint.
  -e ENDPOINT, --endpoint ENDPOINT
                        Document Intelligence Endpoint. Required if using Document Intelligence.
  -p, --use-plugins     Use 3rd-party plugins to convert files. Use --list-plugins to see installed plugins.
  --list-plugins        List installed 3rd-party plugins. Plugins are loaded when using the -p or --use-plugins option.
  --keep-data-uris      Keep data URIs (like base64-encoded images) in the output. By default, data URIs are truncated.
```

### Examples

```bash
# Convert PDF and save
markitdown report.pdf -o report.md

# Convert Word document
markitdown document.docx

# Process multiple files
for file in *.pdf; do
    markitdown "$file" -o "${file%.pdf}.md"
done

# Convert webpage
markitdown https://en.wikipedia.org/wiki/Markdown

# Pipe through other tools
markitdown document.html | grep "important"
```

---

## Creating Custom Converters

You can extend MarkItDown by creating custom converters for unsupported formats.

### Step 1: Inherit from DocumentConverter

```python
from markitdown import DocumentConverter, DocumentConverterResult
from markitdown._stream_info import StreamInfo
from typing import BinaryIO, Any

class MyCustomConverter(DocumentConverter):
    """Convert custom file format to Markdown."""
    
    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any
    ) -> bool:
        """Check if this converter can handle the file."""
        # Check by extension
        if stream_info.extension == ".custom":
            return True
        
        # Check by MIME type
        if stream_info.mimetype == "application/x-custom":
            return True
        
        # Check by content (remember to reset position!)
        cur_pos = file_stream.tell()
        header = file_stream.read(4)
        file_stream.seek(cur_pos)
        
        if header == b"CUST":
            return True
        
        return False
    
    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any
    ) -> DocumentConverterResult:
        """Convert the file to Markdown."""
        try:
            # Read file content
            content = file_stream.read()
            
            # Your conversion logic here
            text = content.decode('utf-8')
            markdown = f"# Custom File\n\n{text}"
            
            return DocumentConverterResult(
                markdown=markdown,
                title="Custom Document"
            )
        except Exception as e:
            from markitdown import FileConversionException
            raise FileConversionException(f"Failed to convert: {e}")
```

### Step 2: Register the Converter

```python
from markitdown import MarkItDown, PRIORITY_SPECIFIC_FILE_FORMAT

md = MarkItDown()
md.register_converter(
    MyCustomConverter(),
    priority=PRIORITY_SPECIFIC_FILE_FORMAT
)

# Now you can use it
result = md.convert("file.custom")
```

### Best Practices

1. **Quick `accepts()` check:** Make the check as fast as possible
2. **Reset stream position:** If you read from the stream in `accepts()`, reset it
3. **Handle errors gracefully:** Raise appropriate exceptions
4. **Optional dependencies:** Check for dependencies and raise `MissingDependencyException`
5. **Document your converter:** Add docstrings explaining what it handles
6. **Set appropriate priority:** Use `PRIORITY_SPECIFIC_FILE_FORMAT` for specific formats

### Advanced Example: Converter with Options

```python
class AdvancedConverter(DocumentConverter):
    def __init__(self, custom_option: str = "default"):
        self.custom_option = custom_option
    
    def accepts(self, file_stream, stream_info, **kwargs):
        return stream_info.extension == ".adv"
    
    def convert(self, file_stream, stream_info, **kwargs):
        # Access custom option
        option = kwargs.get('custom_option', self.custom_option)
        
        content = file_stream.read().decode('utf-8')
        markdown = f"# {option}\n\n{content}"
        
        return DocumentConverterResult(markdown=markdown)

# Register with custom option
md = MarkItDown()
md.register_converter(AdvancedConverter(custom_option="production"))

# Use with override
result = md.convert("file.adv", custom_option="debug")
```

---

## Plugin System

MarkItDown supports a plugin system for third-party converters using Python entry points.

### Creating a Plugin

1.  **Implement the plugin logic:**

    Create a module (e.g., `_plugin.py`) with your converter and a `register_converters` function.

    ```python
    # my_plugin/_plugin.py
    from markitdown import MarkItDown, DocumentConverter, DocumentConverterResult, StreamInfo
    from typing import BinaryIO, Any

    class MyPluginConverter(DocumentConverter):
        def accepts(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any) -> bool:
            return stream_info.extension == ".myplugin"
        
        def convert(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any) -> DocumentConverterResult:
            content = file_stream.read().decode('utf-8')
            return DocumentConverterResult(
                markdown=f"# Plugin Converted\n\n{content}"
            )

    def register_converters(markitdown: MarkItDown, **kwargs: Any):
        """
        Called by MarkItDown to register the plugin's converters.
        """
        markitdown.register_converter(MyPluginConverter())
    ```

2.  **Expose the registration function:**

    Import `register_converters` in your package's `__init__.py` so MarkItDown can find it.

    ```python
    # my_plugin/__init__.py
    from ._plugin import register_converters

    __all__ = ["register_converters"]
    ```

3.  **Register as entry point in `pyproject.toml`:**

    Point to the module containing `register_converters`. Note the group name is `markitdown.plugin` (singular).

    ```toml
    [project.entry-points."markitdown.plugin"]
    my_plugin = "my_plugin"
    ```

4.  **Install your plugin:**

    ```bash
    pip install my-markitdown-plugin
    ```

5.  **Enable plugins when using MarkItDown:**

    ```python
    from markitdown import MarkItDown

    md = MarkItDown(enable_plugins=True)
    result = md.convert("file.myplugin")
    ```

### Plugin Discovery

Plugins are discovered automatically via Python's entry point system. MarkItDown looks for entry points in the `markitdown.plugin` group. The entry point must point to a module that exports a `register_converters(markitdown, **kwargs)` function.

### Example Plugin Package Structure

```
my-markitdown-plugin/
├── pyproject.toml
├── README.md
└── src/
    └── my_plugin/
        ├── __init__.py
        └── _plugin.py
```

**pyproject.toml:**
```toml
[project]
name = "markitdown-my-plugin"
version = "0.1.0"
dependencies = ["markitdown"]

[project.entry-points."markitdown.plugin"]
my_plugin = "my_plugin"
```

---

## See Also

- [README.md](../packages/markitdown/README.md) - Getting started guide and overview
- [SUPPORT.md](../SUPPORT.md) - Support resources and getting help
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) - Community guidelines
- [SECURITY.md](../SECURITY.md) - Security policy
- [LICENSE](../LICENSE) - MIT License

---

## Version History

- **0.1.4** (Current) - Latest stable release
- See [PyPI](https://pypi.org/project/markitdown/) for full version history

---

**Note:** This reference documents the public API. Internal/private methods and classes (prefixed with `_`) are implementation details and may change without notice.
