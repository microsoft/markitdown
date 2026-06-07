use std::path::PathBuf;

/// Which engine handles a conversion.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum Engine {
    /// Pure-Rust converters only (the default; no external dependencies).
    #[default]
    Rust,
    /// Force the optional PyInstaller-compiled Python markitdown binary.
    Python,
    /// Try Rust first; fall back to the Python binary (when configured) for
    /// streams Rust cannot handle (e.g. scanned PDFs needing OCR).
    Auto,
}

/// Configuration for LLM image captioning (any OpenAI-compatible
/// `chat/completions` endpoint). Mirrors the Python library's
/// `llm_client`/`llm_model` feature, which has no CLI equivalent — this is
/// the only way to get image descriptions on any platform.
#[derive(Debug, Clone)]
pub struct LlmConfig {
    /// Base URL, e.g. `https://api.openai.com/v1` (no trailing slash needed).
    pub api_base: String,
    pub api_key: String,
    /// Vision-capable model, e.g. `gpt-4o-mini`.
    pub model: String,
    /// Caption prompt; defaults to Python's
    /// "Write a detailed caption for this image."
    pub prompt: Option<String>,
}

/// Conversion options shared by CLI, MCP server and the desktop app.
#[derive(Debug, Clone, Default)]
pub struct ConvertOptions {
    /// Keep base64 `data:` URIs in the output instead of truncating them
    /// (mirrors the Python CLI's `--keep-data-uris`).
    pub keep_data_uris: bool,
    /// Engine selection; see [`Engine`].
    pub engine: Engine,
    /// Explicit path to the optional Python fallback binary. When `None`,
    /// the `MARKITDOWN_PY_BIN` environment variable is consulted.
    pub python_bin: Option<PathBuf>,
    /// LLM captioning for images. When `None`, the `MARKITDOWN_LLM_API_KEY` /
    /// `MARKITDOWN_LLM_MODEL` / `MARKITDOWN_LLM_API_BASE` /
    /// `MARKITDOWN_LLM_PROMPT` environment variables are consulted.
    pub llm: Option<LlmConfig>,
}
