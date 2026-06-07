//! LLM image captioning via any OpenAI-compatible `chat/completions` API.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_llm_caption.py`.
//! In Python this is a library-only feature (no CLI flag); implementing it
//! here makes image descriptions available to the CLI, the MCP server and
//! the desktop app alike. Pure REST over ureq — no SDK weight.
//!
//! Configuration (programmatic [`LlmConfig`] wins over environment):
//! - `MARKITDOWN_LLM_API_KEY`  (required)
//! - `MARKITDOWN_LLM_MODEL`    (required, vision-capable, e.g. `gpt-4o-mini`)
//! - `MARKITDOWN_LLM_API_BASE` (default `https://api.openai.com/v1`)
//! - `MARKITDOWN_LLM_PROMPT`   (default: Python's caption prompt)

use crate::options::LlmConfig;
use crate::ConvertOptions;

pub const LLM_API_KEY_ENV: &str = "MARKITDOWN_LLM_API_KEY";
pub const LLM_MODEL_ENV: &str = "MARKITDOWN_LLM_MODEL";
pub const LLM_API_BASE_ENV: &str = "MARKITDOWN_LLM_API_BASE";
pub const LLM_PROMPT_ENV: &str = "MARKITDOWN_LLM_PROMPT";

const DEFAULT_API_BASE: &str = "https://api.openai.com/v1";
/// Same default prompt as Python's `_llm_caption.py`.
const DEFAULT_PROMPT: &str = "Write a detailed caption for this image.";

/// Resolve the effective LLM configuration, if any.
pub fn resolve(opts: &ConvertOptions) -> Option<LlmConfig> {
    if let Some(cfg) = &opts.llm {
        return Some(cfg.clone());
    }
    let api_key = std::env::var(LLM_API_KEY_ENV).ok().filter(|v| !v.is_empty())?;
    let model = std::env::var(LLM_MODEL_ENV).ok().filter(|v| !v.is_empty())?;
    Some(LlmConfig {
        api_base: std::env::var(LLM_API_BASE_ENV)
            .ok()
            .filter(|v| !v.is_empty())
            .unwrap_or_else(|| DEFAULT_API_BASE.to_string()),
        api_key,
        model,
        prompt: std::env::var(LLM_PROMPT_ENV).ok().filter(|v| !v.is_empty()),
    })
}

/// True when captioning is configured (used for capability reporting).
pub fn available(opts: &ConvertOptions) -> bool {
    resolve(opts).is_some()
}

/// Request a caption for the image. Returns `None` on any failure — caption
/// errors must never break a conversion (metadata is still returned).
#[cfg(feature = "net")]
pub fn caption_image(data: &[u8], mimetype: &str, cfg: &LlmConfig) -> Option<String> {
    use base64::Engine as _;

    let data_uri = format!(
        "data:{};base64,{}",
        mimetype,
        base64::engine::general_purpose::STANDARD.encode(data)
    );
    let prompt = cfg.prompt.as_deref().unwrap_or(DEFAULT_PROMPT);

    // Exact request shape of Python's _llm_caption.py (OpenAI chat
    // completions with an image_url content part).
    let body = serde_json::json!({
        "model": cfg.model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": data_uri}},
            ],
        }],
    });

    let url = format!("{}/chat/completions", cfg.api_base.trim_end_matches('/'));
    let mut resp = ureq::post(&url)
        .header("Authorization", &format!("Bearer {}", cfg.api_key))
        .header("Content-Type", "application/json")
        .send_json(&body)
        .ok()?;
    let parsed: serde_json::Value = resp.body_mut().read_json().ok()?;
    let caption = parsed["choices"][0]["message"]["content"].as_str()?;
    let caption = caption.trim();
    if caption.is_empty() {
        None
    } else {
        Some(caption.to_string())
    }
}

#[cfg(not(feature = "net"))]
pub fn caption_image(_data: &[u8], _mimetype: &str, _cfg: &LlmConfig) -> Option<String> {
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn resolve_prefers_programmatic_config() {
        let opts = ConvertOptions {
            llm: Some(LlmConfig {
                api_base: "http://x".into(),
                api_key: "k".into(),
                model: "m".into(),
                prompt: None,
            }),
            ..Default::default()
        };
        assert_eq!(resolve(&opts).unwrap().model, "m");
    }
}
