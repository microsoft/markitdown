# MarkItDown DICOM Plugin (`markitdown-dicom`)

This is a plugin for [MarkItDown](https://github.com/microsoft/markitdown) that adds support for converting DICOM (`.dcm`) files into LLM-friendly Markdown metadata representations. 

The plugin is designed to be highly memory-efficient (using deferred loading for pixel data) and token-efficient, ignoring raw pixel arrays while extracting clinically-relevant metadata.

## Features

- **Efficient Stream Peeking**: Fast detection of `.dcm` files by peeking at the `DICM` file preamble/magic bytes at offset 128.
- **Memory Safety**: Uses `pydicom` with deferred value loading (`defer_size="1 KB"`) to parse headers of large multi-frame DICOM files without loading gigabytes of pixel data.
- **PII-Aware by Default**: Automatically redacts Patient Name, Patient ID, and Patient Birth Date.
- **Formatted Metadata**: Standardizes dates to `YYYY-MM-DD` and times to `HH:MM:SS` for downstream RAG and vector database ingestion.
- **Custom Tag Support**: Automatically extracts additional standard metadata fields. Private/vendor tags can optionally be included and are filtered to avoid binary, sequence, and other high-volume data types.

## Installation

Install the plugin along with MarkItDown:

```bash
pip install markitdown-dicom
```

## Usage

### Command Line Interface

Use the `-p` (or `--use-plugins`) option to enable third-party plugins:

```bash
markitdown --use-plugins patient_scan.dcm -o patient_scan.md
```

### Python API

```python
from markitdown import MarkItDown

# Initialize MarkItDown with plugins enabled
md = MarkItDown(enable_plugins=True)

# Convert a DICOM file
result = md.convert("patient_scan.dcm")
print(result.text_content)
```

### Disabling PII Redaction

If you are working in a fully de-identified or secure clinical environment and want to retain Patient Name and Patient ID, you can disable redaction:

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True, redact_pii=False)
result = md.convert("patient_scan.dcm")
```

## Example Output

```markdown
# DICOM File

## Patient Information

* **Patient Name**: [REDACTED]
* **Patient ID**: [REDACTED]
* **Patient Birth Date**: [REDACTED]
* **Patient Sex**: M
* **Patient Age**: 045Y

## Study Information

* **Study Instance UID**: 1.2.840.113619.2.134.1.20230612.98765432
* **Study ID**: STUDY-1
* **Study Date**: 2023-06-12
* **Study Time**: 11:44:27
* **Study Description**: Chest X-Ray
* **Accession Number**: ACC-98765

## Series Information

* **Series Instance UID**: 1.2.840.113619.2.134.2.20230612.98765432
* **Series Number**: 1
* **Series Description**: PA View
* **Series Date**: 2023-06-12
* **Series Time**: 11:45:00

## Acquisition Parameters

* **Modality**: DX
* **Protocol Name**: Chest PA
* **Exposure**: 2
* **Exposure Time**: 10
* **KVP**: 120
* **Acquisition Date**: 2023-06-12
* **Acquisition Time**: 11:45:00

## Equipment

* **Manufacturer**: GE Medical Systems
* **Manufacturer Model Name**: Discovery
* **Device Serial Number**: SN-12345
* **Software Versions**: v1.2.3

## Image Properties

* **Rows**: 2048
* **Columns**: 1500
* **Samples Per Pixel**: 1
* **Bits Allocated**: 16
* **Bits Stored**: 12
* **High Bit**: 11
* **Pixel Representation**: 0
* **Photometric Interpretation**: MONOCHROME2
* **Frame Count**: 1
* **Instance Number**: 42
* **SOP Class UID**: 1.2.840.10008.5.1.4.1.1.2
* **SOP Instance UID**: 1.2.840.113619.2.134.2.20230612.98765432.1
* **Pixel Data Present**: Yes
```
