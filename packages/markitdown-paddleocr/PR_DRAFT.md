# Draft PR: Add `markitdown-paddleocr` as a plugin-first scanned-PDF OCR package

## Suggested Title

`Add a plugin-first PaddleOCR package for scanned PDF fallback`

## Draft Body

## Summary

This PR adds a new package, `markitdown-paddleocr`, as an opt-in OCR plugin for scanned PDFs.

The scope is intentionally narrow:

- PDF only
- plugin-first
- opt-in only
- no changes to MarkItDown core APIs
- no changes to default converter behavior

## Why this package exists

MarkItDown already has two strong paths:

- built-in extraction for machine-readable PDFs
- an OCR plugin path based on LLM vision models

This package targets a different use case that is not fully covered by those two paths:

- local / offline OCR
- CPU-friendly deployments
- no dependency on an LLM API
- stronger practical support for Chinese report-style scanned pages

In local testing with Chinese report, table, textbook, and handwritten-note samples, the current built-in MarkItDown flow returned empty output for these scanned pages, while a PaddleOCR-based fallback recovered meaningful text. The strongest results were on report-style and table-heavy pages.

## Design

This package is implemented as a separate plugin package under `packages/markitdown-paddleocr`.

The converter strategy is deliberately conservative:

1. run the built-in `PdfConverter` first
2. if it returns non-empty markdown, return that result unchanged
3. only if the built-in result is empty, render full pages to images and run PaddleOCR

That means:

- default behavior is preserved
- normal machine-readable PDFs still use the existing built-in extraction path
- OCR is only used as a scanned-document fallback

## Why plugin-first

This package follows the plugin-first guidance already reflected in the project:

- OCR backends are optional
- they may carry significant backend-specific dependencies
- different users may prefer very different OCR tradeoffs

Keeping this functionality in a separate package avoids changing core behavior and keeps the dependency boundary explicit.

## Scope

Included in this PR:

- a new plugin package: `markitdown-paddleocr`
- a PDF-only converter with scanned-PDF fallback behavior
- a lazy `PaddleOCRService`
- unit tests for the fallback strategy and plugin registration
- demo and documentation materials

Explicitly not included:

- DOCX / PPTX / XLSX support
- any core API changes
- any automatic OCR for all PDFs
- any attempt to replace `markitdown-ocr`
- any cloud-provider-specific configuration

## Why PaddleOCR

PaddleOCR is a mature and widely adopted OCR project with strong practical performance on Chinese documents. For this contribution, the motivation is not vendor branding; it is that PaddleOCR fills a useful gap in the current extension landscape:

- offline operation
- CPU-friendly deployment options
- strong Chinese OCR performance

## Tests and demo

This package includes unit tests that verify:

- the built-in PDF result wins when text is already available
- OCR fallback is only used when the built-in result is empty
- plugin registration is opt-in and passes configuration through kwargs
- OCR result normalization works against nested PaddleOCR outputs

Local demo notes are included to show before/after behavior on representative Chinese scanned pages.

## Backward compatibility

This PR does not modify MarkItDown core runtime behavior.

Users only get this behavior if they install the plugin package and opt in to it.

## Related discussion

- #1650
