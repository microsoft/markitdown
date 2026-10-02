# Test organization

Prefer the shared conversion matrix when a regression can be expressed as an
input file and expected or forbidden output strings:

- Put input files in `test_files/` and define cases in `_test_vectors.py`.
- `test_cli_vectors.py` exercises the applicable vectors through the CLI.
- `test_module_vectors.py` exercises them through library file, stream, and URI
  entry points.

Tests that need custom setup, mocks, conversion options, or structural assertions
belong in the existing file for their format. Keep helpers and fixtures in that
file unless multiple suites actually need to share them. Add related tests to the
appropriate section instead of creating a file for each bug or feature.

| Test file | Scope |
| --- | --- |
| `test_docx.py` | Word documents, math, styles, comments, and image hooks |
| `test_pptx.py` | PowerPoint slides, titles, notes, charts, SVGs, and image hooks |
| `test_xlsx.py` | Spreadsheet compatibility and image hooks, including XLS boundaries |
| `test_pdf.py` | PDF tables, numbering, page cleanup, and extraction fallback |
| `test_csv.py` | CSV escaping, blank rows, and line endings |
| `test_html.py` | HTML rendering, links, images, and Wikipedia pages |
| `test_rss.py` | RSS and Atom bodies, titles, metadata, and links |
| `test_epub.py` | EPUB archive paths, metadata, and embedded images |
| `test_outlook_msg.py` | Outlook MSG properties and encodings |
| `test_image.py` | Image captions and media metadata |
| `test_youtube.py` | YouTube URLs, extraction, transcripts, and fallback |
| `test_zip.py` | ZIP entries and nested conversion options |
| `test_docintel.py` | Document Intelligence routing and client options |
| `test_cu.py` | Content Understanding routing, conversion, and registration |
| `test_cli_misc.py` | CLI behavior outside the vector matrix, including service flags |
| `test_module_misc.py` | Library infrastructure, cross-format options, and formats without a dedicated suite |

`test_module_misc.py` includes stream metadata, URI handling, charset detection,
cross-format LLM options, and the existing notebook and audio regressions.
Format-specific tests belong in their dedicated suite when one exists.

Run the suite from `packages/markitdown`:

```sh
hatch test
```

To run a single format:

```sh
hatch test tests/test_docx.py
```

The existing remote, credential, platform, and optional-dependency skip conditions
apply. A consolidation should preserve test bodies, parametrization, fixtures,
and skip conditions; compare collected cases as well as test results to catch
accidentally dropped or overwritten tests.
