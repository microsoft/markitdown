# markitdown-core

The conversion engine shared by the CLI, the MCP server and the desktop app.
Pure Rust, no system dependencies.

```rust
use markitdown_core::{MarkItDown, ConvertOptions, Engine, StreamInfo};

// Default engine
let md = MarkItDown::new();
let r = md.convert_path("report.pdf")?;            // local file
let r = md.convert_uri("https://example.com")?;    // http(s)/file:/data: URIs
let r = md.convert_bytes(&bytes, StreamInfo::new().with_extension(".docx"))?;
println!("{} (title: {:?})", r.markdown, r.title);

// With options (e.g. transparent Python-engine fallback for scanned PDFs)
let md = MarkItDown::with_options(ConvertOptions { engine: Engine::Auto, ..Default::default() });
```

## Design (mirrors the Python package)

| Piece | File | Python counterpart |
|---|---|---|
| `Converter` trait | `src/converter.rs` | `DocumentConverter` ABC |
| Registry + priorities | `src/markitdown.rs` | `_markitdown.py` |
| `StreamInfo` hints | `src/stream_info.rs` | `_stream_info.py` |
| Detection (magic bytes via `file-format`, charset via `chardetng`) | `src/detect.rs` | Magika + charset-normalizer |
| URI handling | `src/uri.rs` | `_uri_utils.py` |
| 18 converters | `src/converters/*.rs` | `converters/_*.py` |
| Optional Python delegation | `src/python_engine.rs` | — |

Converters are tried in priority order (`0.0` specific → `10.0` generic); the
first accepting converter that succeeds wins, identical to Python fallthrough.

Converters set `ConvertResult::degraded` when they hit a known fidelity gap
(scanned PDF, DOCX comments/equations, RTF-only `.msg` body, missing
OCR/transcription/transcript). With `Engine::Auto`, a degraded or failed
result is transparently retried through the optional Python engine
(`MARKITDOWN_PY_BIN`), and the richer output wins — see
`src/python_engine.rs` (deadlock-free piping, kill-on-timeout).

Feature flags: `net` (default) enables `http(s):` inputs via ureq/rustls;
`--no-default-features` gives a fully offline build.

## Tests

`cargo test -p markitdown-core` — unit tests per module plus integration
vectors (`tests/vectors_{data,containers,media,web}.rs`) that convert the real
fixtures from `packages/markitdown/tests/test_files/` and assert the same
substrings as the Python test suite.
