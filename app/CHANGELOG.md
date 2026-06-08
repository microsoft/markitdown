# Changelog — MarkItDown Rust suite (`app/`)

All notable changes to the Rust suite (core engine, CLI, MCP server, desktop
app, and the optional Python fallback). Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); the suite is pre-1.0.

## [Unreleased]

### Added
- **LLM provider registry** (`crates/markitdown-core/src/llm_providers.rs`) —
  one customizable list of OpenAI-compatible **vision** providers: OpenAI,
  **Anthropic/Claude** (OpenAI-compatible endpoint), Ollama, LM Studio,
  OpenRouter, Groq, **Qwen-VL (Alibaba DashScope)**, **Zhipu GLM-4V**,
  **Moonshot Kimi**, and custom — each with default base URL, key requirement,
  local flag and example vision models. Shared by CLI, MCP and desktop:
  - CLI: `--llm-provider <id>` (sets the base URL) and `--list-llm-providers`.
  - Env: `MARKITDOWN_LLM_PROVIDER` (base URL preset; `MARKITDOWN_LLM_API_BASE`
    overrides it).
  - Desktop: a provider dropdown + model datalist (swap models freely).
- **LLM image captions exposed everywhere** (OpenAI-compatible, cloud **or
  local**):
  - CLI flags `--llm-api-key`, `--llm-model`, `--llm-api-base`, `--llm-prompt`
    (override the `MARKITDOWN_LLM_*` env). Local LLMs supported by pointing
    `--llm-api-base` at Ollama (`http://localhost:11434/v1`) or LM Studio
    (`http://localhost:1234/v1`).
  - MCP server honors `MARKITDOWN_LLM_*` from its launch environment.
  - Desktop app: Settings panel for key/model/base/prompt with OpenAI / Ollama
    / LM Studio presets and live capability status.
- **`markitdown --check`** ("doctor"): reports Python-fallback and LLM-caption
  availability (model + endpoint) **without printing secrets**.
- Shared `markitdown_core::capabilities()` used by the CLI `--check`, the MCP
  `list_supported_formats` tool, and the desktop status badges.
- **Optional Python fallback binaries packaged in releases**
  (`markitdown-py-<platform>` for Linux x86_64/aarch64, Windows x86_64, macOS
  Apple Silicon), built best-effort and smoke-tested; Intel macOS builds
  locally.

### Tests
- CLI: end-to-end LLM caption via a mock OpenAI server; `--check` reporting and
  no-secret-leak assertions; stub-Python-bin detection.
- MCP: LLM-via-env **simulation** (server launched with `MARKITDOWN_LLM_*` →
  image gains `# Description:`); capability reporting.
- Core: `capabilities()` unit tests incl. secret-redaction.
- Cross-platform `engine_selection.rs` (runs on Windows); the subprocess-stub
  fallback suite stays `#![cfg(unix)]`.

### Changed
- CLI default engine is `auto` (transparent Python fallback when configured).

## Earlier

- Initial Rust suite: pure-Rust engine with 18 converters; `markitdown` CLI
  (man page, parallel batch); `markitdown-mcp` server (rmcp, stdio, 4 tools);
  Tauri v2 desktop app (drag/drop, queue, progress, retry, logs, editable
  preview); hybrid Python fallback via `--engine auto` / `MARKITDOWN_PY_BIN`
  (URLs/paths handed over at full fidelity; `MARKITDOWN_PY_ARGS` for Azure).
- BrokenPipe handled gracefully (`… | head`/`grep -q` no longer panics).
- Windows-safe batch output naming.
- UPX compression of the Linux/Windows standalone binaries in releases.
- CI (`app-ci.yml`) + native multi-OS release pipeline (`app-release.yml`) with
  a shared per-format regression smoke test (`.github/scripts/smoke.sh`).
