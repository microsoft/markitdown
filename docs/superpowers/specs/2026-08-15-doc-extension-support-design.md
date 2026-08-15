# `.doc` Extension Support Design

## Context

MarkItDown currently converts modern `.docx` files but does not recognize legacy binary Word `.doc` files. GitHub Issue #23 requests support for this format. The repository already uses optional dependencies and explicit converter registration, so legacy Word support should follow those conventions.

## Recommended approach

Add a dedicated `DocConverter` backed by the optional `unword` package. The converter will recognize only the `.doc` extension, read the binary stream into memory, call `unword.parse_doc`, and return the parser's body text as a `DocumentConverterResult`. The parser's text is plain text, so it will be normalized into Markdown-compatible output without attempting unsupported layout reconstruction.

Add a `doc` optional dependency and include it in the aggregate `all` feature. Register the converter alongside the existing Word converters, while preserving `.docx` handling in `DocxConverter`.

## Error handling and compatibility

The dependency will be imported optionally at module load time. If it is unavailable, conversion of a recognized `.doc` file will raise the existing `MissingDependencyException` with installation guidance for the `doc` feature. Other file types and existing `.docx` behavior are unchanged. Parser errors will propagate through the normal MarkItDown conversion error reporting.

## Testing

Add unit tests for:

1. `.doc` extension acceptance and rejection of `.docx`/unrelated extensions.
2. Successful conversion using a real in-memory binary stream and a small fake parser object that exercises the converter's output contract.
3. The missing-dependency error path.

The focused converter tests will run first, followed by the package test suite, type checking, and repository formatting/lint checks where available.

## Scope limits

This change does not add a checked-in binary `.doc` fixture, attempt MIME sniffing for extensionless legacy Word files, or implement tables, images, or rich layout extraction beyond the text returned by `unword`.
