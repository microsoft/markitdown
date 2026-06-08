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

## LLM image captions (works everywhere — cloud or local LLM)

Python markitdown's image-description feature is library-only (no CLI flag);
here it's built into the Rust engine as a plain OpenAI-compatible REST call,
so the **CLI, MCP server and desktop app all expose it**. Images gain a
`# Description:` section identical to Python's output, and caption failures
never break a conversion (metadata is still returned). Any OpenAI-compatible
endpoint works — including **local LLMs** (no key/cloud needed).

Configure it three ways (CLI flags > environment > desktop settings):

**Environment** (used by all three apps):
```bash
export MARKITDOWN_LLM_API_KEY=sk-...
export MARKITDOWN_LLM_MODEL=gpt-4o-mini      # any vision model
export MARKITDOWN_LLM_PROVIDER=openai        # optional preset (sets the base URL)
export MARKITDOWN_LLM_API_BASE=https://api.openai.com/v1   # optional; overrides the preset
export MARKITDOWN_LLM_PROMPT="Describe this image."        # optional
```

**Provider presets** — instead of remembering base URLs, pick a provider with
`--llm-provider` (or `MARKITDOWN_LLM_PROVIDER`). `markitdown --list-llm-providers`
prints them:

| id | base URL | key? | example models |
|---|---|---|---|
| `openai` | `https://api.openai.com/v1` | yes | gpt-4o-mini, gpt-4o |
| `anthropic` | `https://api.anthropic.com/v1` | yes | claude-sonnet-4-6, claude-opus-4-8 |
| `ollama` | `http://localhost:11434/v1` | no (local) | llama3.2-vision, llava, minicpm-v |
| `lmstudio` | `http://localhost:1234/v1` | no (local) | (the loaded model) |
| `openrouter` | `https://openrouter.ai/api/v1` | yes | openai/gpt-4o-mini, qwen/qwen-2-vl-7b-instruct |
| `groq` | `https://api.groq.com/openai/v1` | yes | llama-3.2-11b-vision-preview |
| `qwen` | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | yes | qwen-vl-max, qwen2.5-vl-72b-instruct |
| `zhipu` | `https://open.bigmodel.cn/api/paas/v4` | yes | glm-4v-plus, glm-4v |
| `moonshot` | `https://api.moonshot.cn/v1` | yes | moonshot-v1-8k-vision-preview |
| `custom` | (set `--llm-api-base`) | — | any |

Claude uses Anthropic's **OpenAI-compatible** endpoint (not the native
`/v1/messages` API). The Chinese providers (Qwen/DashScope, Zhipu GLM-4V,
Moonshot Kimi) all expose OpenAI-compatible **vision** endpoints; for mainland
China, set `--llm-api-base` to the `dashscope.aliyuncs.com` endpoint for Qwen.
Only vision-capable, OpenAI-compatible providers are listed (e.g. Azure OpenAI
and text-only DeepSeek are intentionally excluded for captioning).

The registry is defined in `crates/markitdown-core/src/llm_providers.rs` — add
or edit providers there; the CLI, MCP and desktop all read the same list. Any
OpenAI-compatible server works even if it isn't listed (use `custom`).

**CLI flags** (override the env per-invocation):
```bash
# Cloud (OpenAI):
markitdown photo.jpg --llm-provider openai --llm-api-key sk-... --llm-model gpt-4o-mini

# Local LLM via Ollama (no key, fully offline — `ollama pull llava` first):
markitdown photo.jpg --llm-provider ollama --llm-model llava

# Swap models freely — any model the endpoint serves:
markitdown photo.jpg --llm-provider ollama --llm-model llama3.2-vision

# Fully custom OpenAI-compatible endpoint (vLLM, llama.cpp server, LiteLLM, …):
markitdown photo.jpg --llm-api-base http://my-host:8000/v1 --llm-model my-model --llm-api-key k
```

`--llm-api-base` always overrides a provider's default base.

**MCP server**: set the `MARKITDOWN_LLM_*` env in the server's launch config
(`claude mcp add markitdown -e MARKITDOWN_LLM_API_KEY=… -e MARKITDOWN_LLM_MODEL=… -- …`,
or the `env` block in `claude_desktop_config.json`).

**Desktop app**: the header ⚙ Settings panel takes the key/model/base/prompt
(API key is a password field, never logged), with one-click **OpenAI / Ollama /
LM Studio** presets and a live caption-status pill. Settings persist locally and
are sent with each conversion.

### Check what's available

```bash
markitdown --check
# python fallback engine : not configured  (set MARKITDOWN_PY_BIN or --python-bin)
# llm image captions     : available  (model=llava, endpoint=http://localhost:11434/v1)
```

`--check` (and the MCP `list_supported_formats` tool, and the desktop status
badges) report engine + LLM availability — model and endpoint, **never the
API key**.

## Engine support vs. upstream optional dependencies

How each upstream `markitdown[...]` optional-dependency group maps to this
suite. **Rust** = the pure-Rust engine (default, zero dependencies);
**Hybrid** = Rust with the optional Python binary configured
(`MARKITDOWN_PY_BIN`, built from `markitdown[all]` — see `python-engine/`),
used automatically by `--engine auto`.

| Upstream group | Rust engine | Hybrid (Rust + Python) | How |
|---|---|---|---|
| `[pptx]` PowerPoint | ✅ native | ✅ | custom OOXML parser (`converters/pptx.rs`) |
| `[docx]` Word | ✅ native | ✅ full | OOXML parser; comments/equations are *degraded* → Python fills them in |
| `[xlsx]` Excel | ✅ native | ✅ | `calamine` |
| `[xls]` legacy Excel | ✅ native | ✅ | `calamine` (BIFF) |
| `[pdf]` PDF | ✅ text | ✅ full | `pdf-extract`; scanned/OCR + complex tables are *degraded* → Python (OCR plugin / pdfplumber) |
| `[outlook]` `.msg` | ✅ native | ✅ full | `msg_parser` (headers + plain-text body); RTF-only body *degraded* → Python |
| `[audio-transcription]` wav/mp3 | ⚠️ tags only | ✅ transcription | audio is *degraded* → Python (`audio-transcription` extra) auto-runs |
| `[youtube-transcription]` | ⚠️ page metadata | ✅ transcript | YouTube page is *degraded* → Python (`youtube-transcript-api`) auto-runs |
| `[az-doc-intel]` Azure DI | ❌ (cloud) | ✅ | `MARKITDOWN_PY_ARGS="-d -e https://<res>.cognitiveservices.azure.com/"` |
| `[az-content-understanding]` Azure CU | ❌ (cloud) | ✅ | `MARKITDOWN_PY_ARGS="--use-cu --cu-endpoint <endpoint>"` |
| `[all]` everything | ✅ all local formats | ✅ everything | Rust handles local formats; Python adds OCR, transcription, Azure |
| LLM image captions *(library-only upstream)* | ✅ native | ✅ | `MARKITDOWN_LLM_API_KEY` + `MARKITDOWN_LLM_MODEL` (see above) |

Legend: ✅ supported · ⚠️ partial (metadata, no transcription/OCR) without the
Python engine · ❌ not available in pure Rust.

In short: every **local document format** (`pptx`, `docx`, `xlsx`, `xls`,
`pdf`, `outlook`) works out of the box in pure Rust. The **cloud and
transcription** groups (`az-doc-intel`, `az-content-understanding`,
`audio-transcription`, `youtube-transcription`) require the hybrid Python
engine and are reached automatically by `--engine auto` once it is configured —
nothing is permanently unsupported.

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

Two GitHub Actions workflows live in `.github/workflows/`. They listen to
**different events on purpose** (this trips people up — see *Why only CI ran*
below):

| Workflow | Triggers on | Does |
|---|---|---|
| `app-ci.yml` | push to **branch** `main` + pull requests touching `app/**` | tests + debug build + headless smoke test on Linux, Windows, macOS (Apple Silicon) |
| `app-release.yml` | push of a **tag** `app-v*` or `v*`, **or** manual *Run workflow* | native build on 5 OS/arch runners → test → smoke-test → publish a GitHub Release |

Both are *context-aware* of GitHub-runner limits: all tests are offline (the
LLM-caption test uses a local mock server; web converters use local fixtures),
the GUI is never launched (no display server — only built + command-layer unit
tested), and the `#![cfg(unix)]` Python-fallback suite compiles away on
Windows so it never needs a real Python binary.

### Cut a release (recommended: a tag)

```bash
# 1. Make sure the workflow file is already committed & pushed to your branch.
#    (A tag only triggers a workflow if the file exists in the commit the tag
#     points to — tag AFTER the workflow is in history, never before.)
git push

# 2. Tag a commit that contains the workflow, and push the tag.
git tag v0.1.0            # or app-v0.1.0
git push origin v0.1.0
```

This runs `app-release`, which on each of the five runners runs the full test
suite, builds the binaries + desktop installers, smoke-tests them, and then
publishes one GitHub Release with every asset.

### Cut a release without tagging (manual)

GitHub → **Actions → app-release → Run workflow**. This builds everything and
publishes a **prerelease** named by the `tag` input (default `app-dev`), so the
assets show up on the Releases page without creating a permanent tag. Use this
to smoke-test the whole pipeline end-to-end.

### What a release contains

On the repo's **Releases** page (one release, all platforms):

- **Standalone binaries** (CLI + MCP, no dependencies) —
  `markitdown-cli-mcp-{linux-x86_64,linux-aarch64,windows-x86_64,macos-x86_64,macos-aarch64}.{tar.gz,zip}`.
- **Desktop app installers** — macOS `.dmg` **and** a zipped ready-to-run
  `.app` (Intel & Apple Silicon); Linux `.deb` (x86_64 & aarch64) + `.AppImage`
  (x86_64); Windows `.msi` + `-setup.exe`.
- **Optional Python fallback binaries** (`markitdown-py-<platform>`) — only
  needed to enable OCR / transcription / Azure via `--engine auto`; large, so
  download only if you want those extras. Built best-effort for Linux
  (x86_64/aarch64), Windows (x86_64) and macOS Apple Silicon; Intel macOS users
  build locally with `python-engine/build_binary.sh` (PyInstaller can't
  cross-compile, and an arm64 Python binary can't run on Intel).

> The macOS **Intel (x86_64)** artifacts are *cross-compiled on the Apple
> Silicon runner* (`macos-14`), not on an Intel runner. GitHub's Intel macOS
> runners (`macos-13`) are scarce and jobs can queue for hours; cross-building
> on the plentiful arm64 runner avoids that. Rosetta 2 is installed in CI so
> the x86_64 binary is still actually run in the smoke test before release.
- `SHA256SUMS.txt` — checksums for every asset.

macOS builds are **unsigned** (no certs in CI): right-click → Open, or
`xattr -dr com.apple.quarantine <app>` on first launch.

### Why only CI ran when I pushed a tag

A tag push does **not** match a `branches:` filter, so `app-ci` cannot fire
from a tag — if you saw it run, it was triggered by the branch commits you
pushed alongside the tag. If `app-release` *didn't* run, the cause is almost
always one of:

1. **Tag name** didn't match `app-v*` / `v*` (e.g. `app-0.1.0` without the `v`).
2. **The tag points to a commit that doesn't contain `app-release.yml`** — push
   the workflow first, then tag (see the steps above).

`app-release` already runs the full test suite before building, so you do *not*
need `app-ci` to also run on tags — a tagged release is test → build → publish
in one workflow.

## Tests

- **Unit**: converter/helper logic inside each module (`cargo test -p markitdown-core --lib`).
- **Integration**: every supported file type converts a *real* fixture from
  `packages/markitdown/tests/test_files/` with the same expected substrings the
  Python suite asserts (`tests/vectors_*.rs`); `random.bin` must be rejected.
- **CLI**: drives the actual binary — stdout/stdin/`-o`/batch/man/errors.
- **MCP**: spawns the actual server and runs a raw JSON-RPC session
  (initialize → tools/list → tools/call → paging → batch → error recovery).
- **Desktop**: command-layer tests in `desktop/src-tauri` (`cargo test`).
