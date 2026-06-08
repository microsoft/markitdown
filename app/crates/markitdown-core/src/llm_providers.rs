//! Registry of known OpenAI-compatible LLM providers for image captioning.
//!
//! The captioner ([`crate::llm_caption`]) speaks the OpenAI
//! `POST {api_base}/chat/completions` protocol with `Authorization: Bearer`
//! and an `image_url` content part. ANY endpoint that implements that shape
//! works — this registry just gives the CLI / MCP / desktop the same friendly
//! presets (default base URL, whether a key is needed, example vision models)
//! while staying fully customizable: pick a provider and swap the model, or
//! supply a completely custom `api_base`.
//!
//! Providers that are NOT plain Bearer + `/chat/completions` (e.g. Azure
//! OpenAI, which uses `api-key` headers, deployment paths and an
//! `api-version` query) are intentionally excluded — they wouldn't work with
//! this client and would be a false promise. (Azure *document* conversion is a
//! separate feature via the Python engine + `MARKITDOWN_PY_ARGS`.)

/// A selectable LLM provider preset. `serde::Serialize` so the desktop app can
/// fetch the list over a Tauri command and render a dropdown.
#[derive(Debug, Clone, serde::Serialize)]
pub struct LlmProvider {
    /// Stable id used by `--llm-provider <id>` / `MARKITDOWN_LLM_PROVIDER`.
    pub id: &'static str,
    /// Human-friendly name for UIs.
    pub name: &'static str,
    /// Default OpenAI-compatible base URL.
    pub api_base: &'static str,
    /// Whether an API key is required (cloud) or optional (local servers).
    pub requires_key: bool,
    /// True for endpoints that run on the local machine (no data leaves it).
    pub local: bool,
    /// Example vision-capable models to get users started (not exhaustive).
    pub example_models: &'static [&'static str],
    /// One-line guidance.
    pub notes: &'static str,
}

/// All built-in providers. `custom` is the escape hatch for any other
/// OpenAI-compatible server (vLLM, llama.cpp server, LiteLLM proxy, …).
pub const LLM_PROVIDERS: &[LlmProvider] = &[
    LlmProvider {
        id: "openai",
        name: "OpenAI",
        api_base: "https://api.openai.com/v1",
        requires_key: true,
        local: false,
        example_models: &["gpt-4o-mini", "gpt-4o"],
        notes: "Cloud. Needs MARKITDOWN_LLM_API_KEY (or --llm-api-key).",
    },
    LlmProvider {
        id: "ollama",
        name: "Ollama (local)",
        api_base: "http://localhost:11434/v1",
        requires_key: false,
        local: true,
        example_models: &["llama3.2-vision", "llava", "minicpm-v", "qwen2.5vl"],
        notes: "Local, offline. `ollama pull llava` then run; no key needed.",
    },
    LlmProvider {
        id: "lmstudio",
        name: "LM Studio (local)",
        api_base: "http://localhost:1234/v1",
        requires_key: false,
        local: true,
        example_models: &["(the model id loaded in LM Studio)"],
        notes: "Local, offline. Start the LM Studio local server; no key needed.",
    },
    LlmProvider {
        id: "openrouter",
        name: "OpenRouter",
        api_base: "https://openrouter.ai/api/v1",
        requires_key: true,
        local: false,
        example_models: &["openai/gpt-4o-mini", "qwen/qwen-2-vl-7b-instruct"],
        notes: "Cloud aggregator. Needs an OpenRouter API key.",
    },
    LlmProvider {
        id: "groq",
        name: "Groq",
        api_base: "https://api.groq.com/openai/v1",
        requires_key: true,
        local: false,
        example_models: &["llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"],
        notes: "Cloud. Needs a Groq API key.",
    },
    LlmProvider {
        id: "anthropic",
        name: "Anthropic (Claude)",
        // Anthropic's OpenAI-compatible endpoint (Bearer auth + /chat/completions
        // + image_url). Not the native /v1/messages API.
        api_base: "https://api.anthropic.com/v1",
        requires_key: true,
        local: false,
        example_models: &["claude-sonnet-4-6", "claude-opus-4-8", "claude-3-5-sonnet-latest"],
        notes: "Cloud, vision-capable. Uses Anthropic's OpenAI-compatible endpoint; \
                see Anthropic docs for current model ids.",
    },
    LlmProvider {
        id: "qwen",
        name: "Alibaba Qwen-VL (DashScope)",
        // DashScope "compatible-mode" international endpoint. For mainland China
        // use https://dashscope.aliyuncs.com/compatible-mode/v1 (set --llm-api-base).
        api_base: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        requires_key: true,
        local: false,
        example_models: &["qwen-vl-max", "qwen-vl-plus", "qwen2.5-vl-72b-instruct"],
        notes: "Chinese cloud, vision. DashScope OpenAI-compatible mode; CN users \
                set --llm-api-base to the dashscope.aliyuncs.com endpoint.",
    },
    LlmProvider {
        id: "zhipu",
        name: "Zhipu GLM-4V (智谱)",
        api_base: "https://open.bigmodel.cn/api/paas/v4",
        requires_key: true,
        local: false,
        example_models: &["glm-4v-plus", "glm-4v"],
        notes: "Chinese cloud, vision. OpenAI-compatible v4 API; needs a Zhipu key.",
    },
    LlmProvider {
        id: "moonshot",
        name: "Moonshot Kimi (月之暗面)",
        api_base: "https://api.moonshot.cn/v1",
        requires_key: true,
        local: false,
        example_models: &["moonshot-v1-8k-vision-preview"],
        notes: "Chinese cloud, vision. OpenAI-compatible; needs a Moonshot key.",
    },
    LlmProvider {
        id: "custom",
        name: "Custom (OpenAI-compatible)",
        api_base: "",
        requires_key: false,
        local: false,
        example_models: &[],
        notes: "Any OpenAI-compatible server: set --llm-api-base / MARKITDOWN_LLM_API_BASE.",
    },
];

/// Look up a provider by id (case-insensitive).
pub fn provider(id: &str) -> Option<&'static LlmProvider> {
    let id = id.trim().to_ascii_lowercase();
    LLM_PROVIDERS.iter().find(|p| p.id == id)
}

/// Default base URL for a provider id, when known and non-empty.
pub fn api_base_for(id: &str) -> Option<&'static str> {
    provider(id).map(|p| p.api_base).filter(|b| !b.is_empty())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn lookup_is_case_insensitive() {
        assert_eq!(provider("Ollama").unwrap().id, "ollama");
        assert_eq!(provider("  OPENAI ").unwrap().id, "openai");
        assert!(provider("nope").is_none());
    }

    #[test]
    fn includes_claude_and_chinese_vision_providers() {
        // Claude via Anthropic's OpenAI-compatible endpoint.
        let claude = provider("anthropic").expect("anthropic provider");
        assert!(claude.api_base.contains("api.anthropic.com"));
        assert!(claude.example_models.iter().any(|m| m.starts_with("claude")));
        // Chinese vision providers.
        for id in ["qwen", "zhipu", "moonshot"] {
            let p = provider(id).unwrap_or_else(|| panic!("missing provider {id}"));
            assert!(p.requires_key && !p.local);
            assert!(!p.example_models.is_empty(), "{id} should list a vision model");
            assert!(!p.api_base.is_empty());
        }
    }

    #[test]
    fn local_providers_need_no_key() {
        assert!(!provider("ollama").unwrap().requires_key);
        assert!(provider("ollama").unwrap().local);
        assert!(provider("openai").unwrap().requires_key);
    }

    #[test]
    fn api_base_resolves_for_known_nonempty_only() {
        assert_eq!(api_base_for("ollama"), Some("http://localhost:11434/v1"));
        assert_eq!(api_base_for("custom"), None); // empty base
        assert_eq!(api_base_for("unknown"), None);
    }

    #[test]
    fn registry_is_serializable_for_the_desktop_command() {
        let json = serde_json::to_string(LLM_PROVIDERS).unwrap();
        assert!(json.contains("\"ollama\"") && json.contains("11434"));
    }
}
