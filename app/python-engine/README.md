# Optional Python fallback engine

The Rust binary, MCP server and desktop app are fully self-contained and cover
every default markitdown format. This folder exists for the **long tail** the
pure-Rust engine intentionally does not bundle:

| Capability | Why Rust skips it | Python engine |
|---|---|---|
| OCR for scanned PDFs / images | no pure-Rust OCR; Tesseract would break the zero-dependency, phone-class footprint | via plugins (e.g. `markitdown-ocr`) |
| Audio transcription | needs cloud APIs or ~100MB+ local models | `markitdown[audio-transcription]` |
| Azure Document Intelligence / Content Understanding | cloud-only optional extras | `markitdown[all]` |
| Python plugins | Python-only mechanism | yes |

## Trade-offs (read before building)

- The PyInstaller one-file binary is **~80–200 MB** and has a **1–3 s cold
  start** (it self-extracts). The Rust binary is ~5–10 MB with ms startup.
- Image/audio **metadata** extraction in Python markitdown shells out to the
  system `exiftool` — that is *not* bundled. (The Rust engine has its own
  pure-Rust EXIF/tag readers, so this only matters for Python-engine runs.)
- Build per-OS; no cross-compilation.

## Prebuilt binaries

The release pipeline already publishes `markitdown-py-<platform>` binaries
(Linux x86_64/aarch64, Windows x86_64, macOS Apple Silicon) on the GitHub
Releases page — download one and point `MARKITDOWN_PY_BIN` at it instead of
building. Intel macOS isn't prebuilt (PyInstaller can't cross-compile and an
arm64 Python binary won't run on Intel), so build it locally there.

## Build

```bash
./build_binary.sh        # macOS / Linux
# or on Windows:
pwsh ./build_binary.ps1
```

Produces `dist/markitdown-py`.

## Enable

```bash
export MARKITDOWN_PY_BIN="$PWD/dist/markitdown-py"
```

- **CLI / MCP server / desktop app** all default to `auto` mode: Rust converts
  everything it can; the Python engine is invoked **only** when a converter
  reports a fidelity gap (scanned PDF → OCR, DOCX comments/equations, RTF-only
  `.msg` body, audio transcription, YouTube transcript, image OCR) or rejects
  the file outright. The Python output is used only if it adds content —
  otherwise the Rust result is kept.
- `markitdown --engine python file.pdf` forces Python for full fidelity
  (e.g. PDF table reconstruction). `--python-bin PATH` overrides the env var.
- A hung engine is killed after `MARKITDOWN_PY_TIMEOUT` seconds (default 300).
- The engine is invoked with `-p` (plugins enabled), so an OCR plugin baked
  into the binary (see the commented line in `build_binary.sh`) works
  automatically.
- Inputs are handed over at maximum fidelity: **http(s) URLs as URLs** (so the
  Python YouTube-transcript/Wikipedia/Bing converters fully activate), **local
  files as paths** (zero-copy), stdin bytes only as a last resort.
- `MARKITDOWN_PY_ARGS` appends extra args to every engine call — this is how
  you reach the Azure converters through the hybrid:
  `MARKITDOWN_PY_ARGS="-d -e https://<res>.cognitiveservices.azure.com/"`
  (Document Intelligence) or `MARKITDOWN_PY_ARGS="--use-cu --cu-endpoint …"`
  (Content Understanding).
- Converting many scanned files? Build with `BUILD_MODE=onedir` — cold start
  drops from ~1–3 s (onefile self-extraction) to ~50 ms.

Without `MARKITDOWN_PY_BIN`, everything still works — the fallback is simply
never attempted and costs nothing.
