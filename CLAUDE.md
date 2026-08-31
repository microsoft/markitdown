# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository layout

This is a monorepo of independent Python packages, each with its own `pyproject.toml` (hatch-based):

- `packages/markitdown` — the core library and CLI (`markitdown` command). All conversion logic lives here.
- `packages/markitdown-mcp` — an MCP server exposing `convert_to_markdown` over stdio/SSE/streamable-HTTP; depends on `markitdown[all]`.
- `packages/markitdown-ocr` — an optional plugin adding LLM-vision OCR to the PDF/DOCX/PPTX/XLSX converters.
- `packages/markitdown-sample-plugin` — a minimal reference plugin (RTF converter) demonstrating the 3rd-party plugin interface.

Each package is developed independently — `cd` into the relevant package directory before running hatch commands.

## Commands

All commands below assume `cd packages/<package>` first (e.g. `cd packages/markitdown`).

```bash
pip install hatch          # one-time
hatch shell                # enter the package's env
hatch test                 # run the full test suite
hatch test tests/test_module_vectors.py::test_convert_local   # single test
hatch test -k "some_pattern"                                  # filter by name
hatch run types:check      # mypy (packages that define a `types` env: markitdown, markitdown-mcp)
```

Repo-wide pre-commit (Black formatting only):

```bash
pre-commit run --all-files
```

CI (`.github/workflows/tests.yml`) runs `hatch test` inside `packages/markitdown` only, across Python 3.10–3.12. Tests tagged as remote (network-dependent) are skipped automatically when `GITHUB_ACTIONS` is set.

Install core lib from source for local development against optional dependency groups:

```bash
pip install -e 'packages/markitdown[all]'
```

## Core architecture (`packages/markitdown`)

### Conversion pipeline

`MarkItDown` (`_markitdown.py`) is a registry + dispatcher over `DocumentConverter` subclasses (`_base_converter.py`). There is no format-specific branching in the core — all format handling lives in individual converters under `converters/`.

- **`convert()`** dispatches based on the input type (local path, `Path`, URL string, `requests.Response`, binary stream) to one of `convert_local` / `convert_uri` / `convert_response` / `convert_stream`, all of which funnel into `_convert()`.
- **`StreamInfo`** (`_stream_info.py`) is an immutable, frozen dataclass carrying `mimetype`, `extension`, `charset`, `filename`, `local_path`, `url`. It's threaded through the whole pipeline instead of passing raw file paths/URLs around. `copy_and_update()` layers new non-`None` fields onto a copy.
- **`_get_stream_info_guesses()`** builds a *list* of candidate `StreamInfo` guesses: it starts from whatever the caller supplied (extension/mimetype/url) and enriches it using `magika` (content-based detection) and `charset_normalizer` (encoding detection). Because format detection is inherently ambiguous, multiple guesses can be produced and are tried in order.
- **`_convert()`** iterates `stream_info_guesses + [StreamInfo()]` (the empty fallback lets converters that don't care about type, e.g. plain text, still get a chance). For each guess, it iterates registered converters sorted by priority (stable sort — same-priority converters keep insertion order, and later registrations are inserted at index 0, so they're tried before earlier ones), calling `converter.accepts(...)` then `converter.convert(...)`. First successful result wins. Any exceptions during `convert()` are collected as `FailedConversionAttempt`s and only raised (`FileConversionException`) if nothing succeeds at all.
- The file stream position is asserted not to move across `accepts()` calls or between guess iterations — converters that need to peek ahead (e.g. `OutlookMsgConverter`) must save/restore `file_stream.tell()`.

### Priority system

Two priority constants control ordering: `PRIORITY_SPECIFIC_FILE_FORMAT` (0, default — most format converters) and `PRIORITY_GENERIC_FILE_FORMAT` (10 — catch-alls: `PlainTextConverter`, `HtmlConverter`, `ZipConverter`). Lower priority runs first. Plugins can register at arbitrary priorities (e.g. 9 to run before plain-text but after built-ins) — see `register_converter()`'s docstring in `_markitdown.py` for the exact tie-breaking rules.

`DocumentIntelligenceConverter` and `ContentUnderstandingConverter` are only registered when `docintel_endpoint` / `cu_endpoint` is passed to `MarkItDown(...)`, and are inserted so they take priority over the built-ins for the file types they cover.

### Converters (`converters/`)

Each converter is a small, independent `DocumentConverter` subclass implementing `accepts()` (cheap check on mimetype/extension/url) and `convert()` (does the actual work, returns `DocumentConverterResult`). New format support means adding a new converter here and registering it in `MarkItDown.enable_builtins()` — converters don't need to know about each other.

Converters that need to recurse into MarkItDown (e.g. `ZipConverter` unpacking archives) receive the owning `MarkItDown` instance via constructor injection (`ZipConverter(markitdown=self)`) rather than importing it globally. `_kwargs["_parent_converters"]` is threaded through `_convert()` so nested conversions can reuse the same converter registry.

Global options (`llm_client`, `llm_model`, `llm_prompt`, `style_map`, `exiftool_path`) are stored once on the `MarkItDown` instance and merged into `**kwargs` for every converter call in `_convert()`, so individual converters just read them from kwargs rather than each managing their own config plumbing.

### Plugin system

Plugins are discovered via the `markitdown.plugin` entry-point group (`importlib.metadata.entry_points`), lazily loaded once into a module-level `_plugins` cache, and disabled by default (`enable_plugins=False`). Each plugin module must export a `register_converters(markitdown, **kwargs)` function that calls `markitdown.register_converter(...)`. A plugin failing to load or register never aborts the process — it's caught and surfaced as a `warn()`. See `packages/markitdown-sample-plugin` for the minimal shape, and `packages/markitdown-ocr` for a more involved example that wraps/replaces built-in converters (`_pdf_converter_with_ocr.py` etc.) rather than adding a new format.

### Exceptions

`_exceptions.py` defines `UnsupportedFormatException` (no converter accepted the stream), `FileConversionException` (wraps one or more `FailedConversionAttempt`s — every converter that accepted the stream but raised), and `MissingDependencyException` (an optional dependency for a specific format isn't installed).

## Security note

MarkItDown does I/O with the privileges of the calling process (like `open()`/`requests.get()`). When adding features that call `convert()` on untrusted input, prefer the narrowest entrypoint (`convert_local`, `convert_stream`, `convert_response`) over the permissive `convert()`/`convert_uri`, which will happily fetch arbitrary URLs.
