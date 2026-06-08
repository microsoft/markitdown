//! Runtime capability reporting shared by the CLI (`--check`), the MCP server
//! (`list_supported_formats`) and the desktop app. Reports which optional
//! engines are wired up *without leaking secrets* (no API keys).

use crate::{llm_caption, python_engine, ConvertOptions};

/// What the engine can currently do, given options + environment.
#[derive(Debug, Clone, serde::Serialize)]
pub struct Capabilities {
    /// The optional Python fallback binary is configured and present on disk.
    pub python_engine: bool,
    /// Resolved path to that binary, when found.
    pub python_engine_path: Option<String>,
    /// LLM image captioning is configured (key + model present).
    pub llm_captions: bool,
    /// The vision model that would be used (non-secret).
    pub llm_model: Option<String>,
    /// The OpenAI-compatible base URL that would be used (non-secret) — e.g.
    /// `https://api.openai.com/v1` or a local `http://localhost:11434/v1`.
    pub llm_api_base: Option<String>,
}

/// Inspect the effective capabilities for the given options (env-aware).
pub fn capabilities(opts: &ConvertOptions) -> Capabilities {
    let py = python_engine::resolve_python_bin(opts);
    let llm = llm_caption::resolve(opts);
    Capabilities {
        python_engine: py.is_some(),
        python_engine_path: py.map(|p| p.display().to_string()),
        llm_captions: llm.is_some(),
        llm_model: llm.as_ref().map(|c| c.model.clone()),
        llm_api_base: llm.map(|c| c.api_base),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{Engine, LlmConfig};
    use std::path::PathBuf;

    #[test]
    fn reports_nothing_when_unconfigured() {
        let opts = ConvertOptions {
            engine: Engine::Auto,
            // Explicit missing path so an ambient MARKITDOWN_PY_BIN can't flake it.
            python_bin: Some(PathBuf::from("nope/not/here")),
            ..Default::default()
        };
        let c = capabilities(&opts);
        assert!(!c.python_engine);
        assert!(c.python_engine_path.is_none());
    }

    #[test]
    fn reports_llm_without_leaking_key() {
        let opts = ConvertOptions {
            llm: Some(LlmConfig {
                api_base: "http://localhost:11434/v1".into(),
                api_key: "secret-should-not-appear".into(),
                model: "llava".into(),
                prompt: None,
            }),
            ..Default::default()
        };
        let c = capabilities(&opts);
        assert!(c.llm_captions);
        assert_eq!(c.llm_model.as_deref(), Some("llava"));
        assert_eq!(c.llm_api_base.as_deref(), Some("http://localhost:11434/v1"));
        // The serialized form must never contain the API key.
        let json = serde_json::to_string(&c).unwrap();
        assert!(!json.contains("secret-should-not-appear"));
    }
}
