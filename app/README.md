# MarkItDown — Rust suite (`app/`)

A self-contained, dependency-free reimplementation of [markitdown](../README.md)
in Rust: one shared engine, three deliverables. No Python, no Docker, no system
binaries (no exiftool/ffmpeg/tesseract); light enough for a 4 GB-RAM device.

```
app/
├── crates/
│   ├── markitdown-core/   # the engine: 18 converters, detection, registry (lib)
│   ├── markitdown-cli/    # `markitdown` binary (~6 MB) with embedded man page
│   └── markitdown-mcp/    # MCP server for Claude (rmcp, stdio) (~7 MB)
├── desktop/               # Tauri v2 app (vanilla TS, ~38 KB frontend, lucide icons)
├── python-engine/         # OPTIONAL PyInstaller fallback (OCR/transcription long tail)
└── skill/markitdown/      # token-efficient skill teaching Claude the MCP tools
```

## Supported formats

PDF · DOCX · XLSX/XLS · PPTX · HTML (incl. Wikipedia / Bing SERP / YouTube
pages) · CSV · EPUB · ZIP (recursive) · Jupyter `.ipynb` · Outlook `.msg` ·
RSS/Atom · images (EXIF + dimensions) · audio (tags + duration) · plain
text/Markdown/JSON. Inputs: paths, stdin, `file:`/`data:`/`http(s):` URIs.

## Nothing is unsupported: the Auto fallback

The pure-Rust engine handles everything above by itself. For the few fidelity
gaps it cannot close locally, every entry point runs in **`auto` mode by
default**: when a converter flags a degraded result — scanned/image-only PDF
(needs OCR), DOCX with comments or equations, RTF-only `.msg` body, audio
transcription, YouTube transcripts, image OCR — and the optional Python engine
is configured (`MARKITDOWN_PY_BIN`, see `python-engine/README.md`), the
conversion is transparently retried there and the better result wins. The
Python output is adopted **only if it actually adds content**; otherwise the
Rust result is kept, and when no Python binary is configured the fallback
costs nothing — clean conversions never touch it. A hung Python process is
killed after `MARKITDOWN_PY_TIMEOUT` (default 300 s), so batch jobs can't wedge.

`--engine python` forces full Python fidelity (e.g. PDF table reconstruction);
`--engine rust` pins pure Rust.

How the fallback hands work over (highest fidelity first): http(s)/data URLs
are passed to the Python engine **as URLs** (so its YouTube-transcript /
Wikipedia / Bing converters fully activate), local files as **paths**
(zero-copy), stdin bytes only as a last resort. Extra Python CLI args pass
through `MARKITDOWN_PY_ARGS` — e.g. Azure Document Intelligence:
`MARKITDOWN_PY_ARGS="-d -e https://<res>.cognitiveservices.azure.com/"`.

## LLM image captions (works everywhere, no Python needed)

Python markitdown's image-description feature is library-only (no CLI flag);
here it's built into the Rust engine as a plain OpenAI-compatible REST call,
so the CLI, MCP server and desktop app all get it via environment:

```bash
export MARKITDOWN_LLM_API_KEY=sk-...
export MARKITDOWN_LLM_MODEL=gpt-4o-mini          # any vision model
# optional: MARKITDOWN_LLM_API_BASE (default https://api.openai.com/v1 —
#           point it at any OpenAI-compatible server), MARKITDOWN_LLM_PROMPT
```

Images then gain a `# Description:` section identical to Python's output.
Caption failures never break a conversion (metadata is still returned).

## Build everything

```bash
cd app
cargo build --release          # → target/release/markitdown + markitdown-mcp
cargo test --workspace         # 67 tests against the real Python-suite fixtures
```

## 1. CLI

```bash
./target/release/markitdown report.pdf                  # → stdout
./target/release/markitdown a.pdf b.docx c.xlsx -O out/ # parallel batch (rayon)
cat doc.pdf | ./target/release/markitdown -x pdf        # stdin + hint
./target/release/markitdown --list-formats
./target/release/markitdown --emit-man | mandoc | less  # the man page
sudo sh -c './target/release/markitdown --emit-man > /usr/local/share/man/man1/markitdown.1'
```

Engine selection: `--engine auto` (default: Rust, transparent Python fallback
for fidelity gaps) | `rust` | `python` (+ `--python-bin` / `MARKITDOWN_PY_BIN`,
see `python-engine/`).

Fully static Linux build: `cargo build --release --target x86_64-unknown-linux-musl`.

## 2. MCP server (Claude)

```bash
claude mcp add markitdown -- "$PWD/target/release/markitdown-mcp"
```

Tools: `convert_to_markdown` (paged), `convert_file` (write-to-disk summary
mode), `convert_batch`, `list_supported_formats`. Full docs + Claude Desktop
config + smoke test: [`crates/markitdown-mcp/README.md`](crates/markitdown-mcp/README.md).
Install the companion skill by copying `skill/markitdown/` into
`~/.claude/skills/` (or a project's `.claude/skills/`).

## 3. Desktop app

```bash
cd desktop
npm install
npm run tauri dev      # development
npm run tauri build    # installable bundle
```

Drag files in, watch the queue convert in parallel, preview rendered/raw
Markdown, copy or save. Details: [`desktop/README.md`](desktop/README.md).

## Architecture

`markitdown-core` mirrors the Python design: a prioritized registry of
`Converter`s over a `StreamInfo` (mimetype/extension/charset hints enriched by
magic-byte + charset detection). CLI, MCP server and the Tauri app are thin
shells over the same crate — conversions always run in-process and heavy jobs
are parallelized (rayon / blocking thread pools).

Every dependency is pure-Rust (or statically vendored), version-pinned in the
workspace `Cargo.toml`. The release profile is size-tuned (LTO, `opt-level=s`,
strip): ~6 MB CLI, ~7 MB MCP server.

## Binary size & compression

Two layers, chosen so nothing regresses:

1. **Compile-time** (always on, in `[profile.release]`): `lto`,
   `codegen-units=1`, `strip`, `opt-level="s"`. We deliberately *keep*
   `opt-level="s"` (not `"z"`, which can slow PDF-heavy throughput) and
   `panic="unwind"` (the PDF parser relies on `catch_unwind`).
2. **Post-build** (release CI only): the standalone `markitdown` and
   `markitdown-mcp` binaries are packed with **UPX `--best --lzma`** on Linux
   and Windows (≈50% smaller; self-extracts in a few ms at launch). macOS is
   intentionally left unpacked — UPX's Mach-O / Apple-Silicon support is
   unreliable and packed binaries trip Gatekeeper. CI re-runs the smoke test
   on the *packed* binary, so a release never ships a binary that can't start.

Desktop installers use each bundler's native compression: the Windows NSIS
installer already defaults to `lzma` (the strongest setting); `.dmg`, `.deb`
and `.AppImage` use their standard compressed formats. They are not re-packed
by hand (that would risk breaking installation).

## Releases & CI

- `.github/workflows/app-ci.yml` — runs on every PR/push touching `app/`:
  tests + a debug build + a headless smoke test on Linux, Windows and macOS
  (Apple Silicon). It is context-aware of runner limits: offline tests, no GUI
  launch, and the `cfg(unix)` Python-fallback suite compiles away on Windows.
- `.github/workflows/app-release.yml` — on an `app-v*` tag (or manual
  dispatch), builds **natively** on five OS/arch runners (Linux x86_64 &
  aarch64, Windows x86_64, macOS Intel & Apple Silicon), tests + smoke-tests
  each, then publishes the CLI/MCP archives and the desktop installers
  (`.dmg`/`.deb`/`.AppImage`/`.msi`/`.exe`) plus `SHA256SUMS.txt` to a GitHub
  Release. Tag example: `git tag app-v0.1.0 && git push origin app-v0.1.0`.

## Tests

- **Unit**: converter/helper logic inside each module (`cargo test -p markitdown-core --lib`).
- **Integration**: every supported file type converts a *real* fixture from
  `packages/markitdown/tests/test_files/` with the same expected substrings the
  Python suite asserts (`tests/vectors_*.rs`); `random.bin` must be rejected.
- **CLI**: drives the actual binary — stdout/stdin/`-o`/batch/man/errors.
- **MCP**: spawns the actual server and runs a raw JSON-RPC session
  (initialize → tools/list → tools/call → paging → batch → error recovery).
- **Desktop**: command-layer tests in `desktop/src-tauri` (`cargo test`).
