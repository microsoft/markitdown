# MarkItDown Converter Capability Matrix

> Auto-generated from 22 converters in `packages/markitdown/src/markitdown/converters/`
> Last updated: 2026-05-18 | Darwin R2 · D5 Documentation

## Overview

| # | Converter | Class | Formats | Extensions | Dependencies | Try/Except | LLM | OCR | Network |
|---|-----------|-------|---------|------------|-------------|------------|-----|-----|---------|
| 1 | **Audio** | `AudioConverter` | audio/* | `.mp3,.wav,.flac,.m4a,.ogg,.opus,.aiff` | `speech_recognition`, `pydub` | 2 | — | — | — |
| 2 | **BingSerp** | `BingSerpConverter` | text/html (Bing) | `.html,.htm` | `base64`, `BeautifulSoup` | 2 | — | — | ✅ |
| 3 | **CSV** | `CsvConverter` | text/csv | `.csv` | `csv`, `charset_normalizer` | 3 🆕 | — | — | — |
| 4 | **DocIntel** | `DocumentIntelligenceConverter` | * (Azure AI) | * | `azure-ai-documentintelligence` | 3 | ✅ | ✅ | ✅ |
| 5 | **DOCX** | `DocxConverter` | application/vnd.openxmlformats-officedocument.wordprocessingml.document | `.docx` | `mammoth` | 3 | — | — | — |
| 6 | **EPUB** | `EpubConverter` | application/epub+zip | `.epub` | `zipfile`, `defusedxml` | 4 🆕 | — | — | — |
| 7 | **HTML** | `HtmlConverter` | text/html | `.html,.htm` | `BeautifulSoup` | 2 🆕 | — | — | — |
| 8 | **Image** | `ImageConverter` | image/jpeg, image/png | `.jpg,.jpeg,.png` | `exiftool`† | 1 | ✅ | — | — |
| 9 | **IPYNB** | `IpynbConverter` | application/x-ipynb+json | `.ipynb` | `json` | 2 | — | — | — |
| 10 | **LLM Caption** | `LlmCaption`†† | — | — | `base64`, `mimetypes` | 1 | ✅ | — | ✅ |
| 11 | **Outlook MSG** | `OutlookMsgConverter` | application/vnd.ms-outlook | `.msg` | `olefile` | 7 | — | — | — |
| 12 | **PDF** | `PdfConverter` | application/pdf | `.pdf` | `pdfminer`, `pdfplumber` | 3 | — | — | — |
| 13 | **Plain Text** | `PlainTextConverter` | text/* | `.txt,.md,.json,.jsonl` | `charset_normalizer` | 1 🆕 | — | — | — |
| 14 | **PPTX** | `PptxConverter` | application/vnd.openxmlformats-officedocument.presentationml.presentation | `.pptx` | `python-pptx` | 8 | — | — | — |
| 15 | **RSS/Atom** | `RssConverter` | application/rss+xml, application/atom+xml | `.rss,.atom,.xml` | `defusedxml`, `BeautifulSoup` | 2 🆕 | — | — | ✅ |
| 16 | **Transcribe** | `TranscribeAudio`†† | — | — | `speech_recognition` | 3 | ✅ | — | ✅ |
| 17 | **Wikipedia** | `WikipediaConverter` | text/html (Wikipedia) | `.html,.htm` | `BeautifulSoup` | 2 🆕 | — | — | ✅ |
| 18 | **XLSX** | `XlsxConverter` | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | `.xlsx` | `pandas`, `openpyxl` | 4 | — | — | — |
| 19 | **XLS** | `XlsConverter` | application/vnd.ms-excel | `.xls` | `pandas`, `xlrd` | (shared with XLSX) | — | — | — |
| 20 | **YouTube** | `YouTubeConverter` | text/html (YouTube) | `.html,.htm` | `yt-dlp`† | 5 | — | — | ✅ |
| 21 | **ZIP** | `ZipConverter` | application/zip | `.zip` | `zipfile` + all sub-converters | 3 | varies | varies | — |

> 🆕 = error handling upgraded in Darwin R1 (D3 Robustness)
> † = external CLI tool, not a Python package
> †† = utility class, not a standalone converter

## Dependency Map

```
                    ┌─────────────┐
                    │ MarkItDown  │
                    │   Engine     │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌─────▼─────┐ ┌───────▼──────┐
    │  Pipeline   │ │ Stream    │ │  Converter    │
    │  (magika,   │ │ Info      │ │  Registry     │
    │   charset)  │ │           │ │               │
    └─────────────┘ └───────────┘ └───────┬───────┘
                                          │
        ┌─────────┬─────────┬─────────────┼─────────────┬─────────┬─────────┐
        │         │         │             │             │         │         │
   ┌────▼────┐ ┌──▼──┐ ┌───▼───┐ ┌──────▼──────┐ ┌───▼───┐ ┌──▼──┐ ┌───▼────┐
   │  Text   │ │Audio│ │ Image │ │   Office    │ │  Web  │ │Data │ │Archive │
   │  Group  │ │     │ │       │ │   Group     │ │ Group │ │     │ │        │
   └────┬────┘ └──┬──┘ └───┬───┘ └──────┬──────┘ └───┬───┘ └──┬──┘ └───┬────┘
        │         │         │             │             │         │         │
  ┌─────┼─────┐   │    ┌────┼────┐   ┌────┼────┐   ┌───┼───┐     │    ┌───┼───┐
  │     │     │   │    │    │    │   │    │    │   │   │   │     │    │   │   │
 Plain CSV IPYNB Audio Image LLM  DOCX PPTX XLSX  HTML Wiki RSS  XLS  ZIP EPUB
 Text                         Caption     XLS  PDF  Bing YouTube
                                          EPUB     Serp

  Key:
  ─── = converter class      ··· = inherited from
  Audio ─── uses TranscribeAudio internally
  EpubConverter ─── extends HtmlConverter
  DocxConverter ─── extends HtmlConverter
```

## Feature Matrix

| Converter | Metadata Extraction | Table Support | Image Extraction | Link Preservation | Encoding Detection | Streaming |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| Audio | ✅ (duration) | — | — | — | — | ✅ |
| BingSerp | ✅ (title) | — | — | — | ✅ | — |
| CSV | — | ✅ (native) | — | — | ✅ | — |
| DocIntel | ✅ (full) | ✅ | ✅ | ✅ | — | — |
| DOCX | — | ✅ | — | ✅ | — | — |
| EPUB | ✅ (meta) | ✅ | — | ✅ | — | — |
| HTML | ✅ (title) | ✅ | — | ✅ | ✅ | — |
| Image | ✅ (EXIF) | — | — | — | — | — |
| IPYNB | — | — | ✅ (base64) | — | ✅ | — |
| Outlook MSG | ✅ (sender/date) | — | — | — | — | — |
| PDF | ✅ | ✅ | — | — | — | — |
| Plain Text | — | — | — | — | ✅ | — |
| PPTX | — | — | ✅ | — | — | — |
| RSS/Atom | ✅ (title/date) | — | — | — | — | — |
| Wikipedia | ✅ (title) | ✅ | — | ✅ | ✅ | — |
| XLSX | — | ✅ (native) | — | — | — | — |
| YouTube | ✅ (title/desc) | — | — | ✅ | ✅ | — |
| ZIP | varies | varies | varies | varies | varies | — |

## Error Handling Quality (post-R1)

| Converter | Pre-R1 | Post-R1 | Encoding | Parse | Network | File I/O |
|-----------|:------:|:-------:|:--------:|:-----:|:-------:|:--------:|
| CSV | ❌ 0 | ✅ 3 | ✅ | ✅ | — | — |
| Wikipedia | ❌ 0 | ✅ 2 | ✅ | ✅ | — | — |
| EPUB | ❌ 0 | ✅ 4 | — | ✅ | — | ✅ |
| Plain Text | ❌ 0 | ✅ 1 | ✅ | — | — | — |
| HTML | ⚠️ 1 | ✅ 2 | ✅ | ✅ | — | — |
| RSS | ⚠️ 2* | ✅ 2 | — | ✅ | — | — |
| Image | ✅ 1 | ✅ 1 | — | — | — | — |
| IPYNB | ✅ 2 | ✅ 2 | — | — | — | — |
| **Legend** | ❌=none | ⚠️=too broad | ✅=specific | — | — | — |
| *RSS used `except BaseException` | `except Exception` (anti-patterns) | — | — | — | — |

## Known Limitations

| Converter | Limitation | Workaround |
|-----------|-----------|------------|
| **Audio** | Requires `speech_recognition` + FFmpeg | Install `markitdown[all]` or `markitdown[audio]` |
| **BingSerp** | Requires network access; Bing HTML format may change | None (network-dependent) |
| **DocIntel** | Requires Azure subscription + `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` | Use PDF converter as fallback |
| **DOCX** | Requires `mammoth`; complex formatting may be lost | Install `markitdown[docx]` |
| **EPUB** | DRM-protected EPUBs not supported | Remove DRM before conversion |
| **Image** | LLM description requires `llm_client` + `llm_model` in kwargs | Falls back to EXIF-only output |
| **IPYNB** | Embedded images output as base64 data URIs (large) | None |
| **Outlook MSG** | Requires `olefile`; attachments not extracted | Install `markitdown[msg]` |
| **PDF** | Scanned PDFs require OCR (DocIntel); complex layouts may degrade | Use DocIntel for scanned PDFs |
| **PPTX** | Requires `python-pptx`; charts/SmartArt not converted | Install `markitdown[pptx]` |
| **RSS/Atom** | Network-dependent; some feeds use non-standard XML | None (structured feed required) |
| **Wikipedia** | Network-dependent; only standard Wikipedia article layout | Use HtmlConverter for other wiki engines |
| **XLS/XLSX** | Requires `pandas` + `openpyxl`/`xlrd`; merged cells flattened | Install `markitdown[xlsx]` |
| **YouTube** | Requires `yt-dlp` CLI or `pip install yt-dlp`; subject to rate limiting | Install `markitdown[youtube]` |
| **ZIP** | Nested archives not deeply recursed; password-protected ZIPs fail | Extract manually for complex cases |

## Optional Dependency Groups

| Group | pip extra | Converters enabled |
|-------|-----------|-------------------|
| **all** | `markitdown[all]` | All converters |
| **audio** | `markitdown[audio]` | Audio, Transcribe |
| **docx** | `markitdown[docx]` | DOCX |
| **xlsx** | `markitdown[xlsx]` | XLSX, XLS |
| **pptx** | `markitdown[pptx]` | PPTX |
| **pdf** | `markitdown[pdf]` | PDF |
| **msg** | `markitdown[msg]` | Outlook MSG |
| **youtube** | `markitdown[youtube]` | YouTube |
| **docintel** | `markitdown[docintel]` | DocIntel |
