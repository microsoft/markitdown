# convert_to_markdown.py

Standalone CLI script that converts local files to Markdown using this repo's `markitdown` library (`packages/markitdown`, installed editable). Lives at the repo root, alongside `README.md`.

## What it does

- Accepts a folder path or a single file path, either as a CLI argument (`sys.argv[1]`) or via an interactive `input()` prompt if no argument is given.
- If given a folder, iterates every file directly inside it (not recursive — does not descend into subfolders) and attempts to convert each one.
- If given a single file, converts just that file.
- For each source file, writes a `.md` file with the same base name in the **same folder** as the source (`path.with_suffix(".md")`), overwriting any existing `.md` with that name.
- No file-type filtering: every file found is passed to `MarkItDown().convert()`. Files MarkItDown can't handle raise an exception that is caught and reported as `FAILED  <name>: <error>` — the script does not stop, it moves to the next file.
- Successful conversions print `OK      <name> -> <name>.md`.

## Current behavior / known gaps (for whoever picks this up next)

- **Not recursive.** Subfolders inside the target folder are ignored entirely (`target_path.iterdir()`, not `rglob`/`walk`). If recursive conversion is wanted, that's the first thing to add.
- **No extension filter, by design.** An earlier version filtered to `.pdf` / `.docx` / `.pptx` only; that filter was deliberately removed so the script now tries every file MarkItDown's installed converters support (whatever's registered in the local `MarkItDown()` instance — see below).
- **Overwrites silently.** If `foo.pdf` and `foo.docx` both exist in the same folder, the second conversion overwrites `foo.md` from the first, no warning.
- **No `--output-dir` option.** Output always lands next to the source file; there's no way to redirect output elsewhere without editing the script.
- **Single `MarkItDown()` instance, default config.** No custom `llm_client`, `llm_model`, `docintel_endpoint`, or `cu_endpoint` wired in — those are documented in the main [README.md](README.md) if richer conversion (e.g. image descriptions via an LLM, OCR) is ever needed. Also see `markitdown-ocr` under `packages/` for an OCR plugin (not installed here).

## Security note

This script inherits MarkItDown's own I/O security model: it accesses files with the privileges of the process running it, same as `open()`. Don't point it at untrusted input in an untrusted environment — see the [Security Considerations](README.md#security-considerations) section of the main README.

## Environment

- Repo has a local virtualenv at `.venv` (Python 3.12, installed via `brew install python@3.12` because the system default was 3.14, which has no `onnxruntime` wheel yet — `onnxruntime` is a transitive dependency of `magika`, which `markitdown` uses for content-based file-type sniffing).
- Installed into `.venv` via: `pip install -e "packages/markitdown[pdf,docx,pptx]"` — editable install pointing at this repo's own `packages/markitdown` source, not a separate PyPI fetch. Only the `pdf`, `docx`, `pptx` extras are installed (not the full `[all]` extra, which pulls in `youtube-transcript-api~=1.0.0` and other deps unavailable for this environment at setup time).
- Because only those three extras are installed, formats needing other optional deps (e.g. `.xlsx`, audio transcription, some image/OCR paths) will hit `FAILED` here even though the filter no longer blocks them — the underlying converter dependency just isn't installed. Installing more extras (see `packages/markitdown/pyproject.toml` for the full extras list) would unlock those.

## Run it

```bash
source .venv/bin/activate
python convert_to_markdown.py                       # prompts for a path
python convert_to_markdown.py /path/to/folder        # convert every file in folder (non-recursive)
python convert_to_markdown.py /path/to/file.pdf      # convert one file
```

## Tested with

Ran against a mixed test folder (`.pdf`, `.docx`, `.pptx`, `.txt` copied from `packages/markitdown/tests/test_files/`) — all four converted successfully, including plain `.txt` (passthrough, no extra deps needed).
