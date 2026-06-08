//! Cross-platform tests for `MARKITDOWN_LLM_PROVIDER` / `MARKITDOWN_LLM_*`
//! environment resolution, exercised through the public `capabilities()` API
//! (so no private items and no network are needed — CI-safe on every OS).
//!
//! These mutate process-global env vars. `std::env::set_var` racing a
//! concurrent `getenv` is UB-adjacent on macOS, so every test in this file is
//! serialized through one lock. Keeping them in their OWN integration binary
//! means no other test threads read the env concurrently.

use markitdown_core::{capabilities, ConvertOptions};
use std::sync::Mutex;

static ENV_LOCK: Mutex<()> = Mutex::new(());

const KEYS: &[&str] = &[
    "MARKITDOWN_LLM_PROVIDER",
    "MARKITDOWN_LLM_API_KEY",
    "MARKITDOWN_LLM_MODEL",
    "MARKITDOWN_LLM_API_BASE",
    "MARKITDOWN_LLM_PROMPT",
];

/// Run `body` with the given LLM env vars set and all others cleared, under the
/// serial lock, restoring a clean slate afterward.
fn with_env(vars: &[(&str, &str)], body: impl FnOnce(markitdown_core::Capabilities)) {
    let _g = ENV_LOCK.lock().unwrap_or_else(|e| e.into_inner());
    for k in KEYS {
        std::env::remove_var(k);
    }
    for (k, v) in vars {
        std::env::set_var(k, v);
    }
    let caps = capabilities(&ConvertOptions::default());
    for k in KEYS {
        std::env::remove_var(k);
    }
    body(caps);
}

#[test]
fn provider_env_selects_base_url() {
    with_env(
        &[
            ("MARKITDOWN_LLM_PROVIDER", "ollama"),
            ("MARKITDOWN_LLM_API_KEY", "x"),
            ("MARKITDOWN_LLM_MODEL", "llava"),
        ],
        |caps| {
            assert!(caps.llm_captions);
            assert_eq!(caps.llm_api_base.as_deref(), Some("http://localhost:11434/v1"));
            assert_eq!(caps.llm_model.as_deref(), Some("llava"));
        },
    );
}

#[test]
fn explicit_base_env_overrides_provider() {
    with_env(
        &[
            ("MARKITDOWN_LLM_PROVIDER", "ollama"),
            ("MARKITDOWN_LLM_API_BASE", "http://example.test/v1"),
            ("MARKITDOWN_LLM_API_KEY", "x"),
            ("MARKITDOWN_LLM_MODEL", "m"),
        ],
        |caps| assert_eq!(caps.llm_api_base.as_deref(), Some("http://example.test/v1")),
    );
}

#[test]
fn unknown_provider_falls_back_to_openai_default() {
    with_env(
        &[
            ("MARKITDOWN_LLM_PROVIDER", "does-not-exist"),
            ("MARKITDOWN_LLM_API_KEY", "x"),
            ("MARKITDOWN_LLM_MODEL", "m"),
        ],
        |caps| assert_eq!(caps.llm_api_base.as_deref(), Some("https://api.openai.com/v1")),
    );
}

#[test]
fn no_key_means_captions_unavailable() {
    with_env(
        &[("MARKITDOWN_LLM_PROVIDER", "ollama"), ("MARKITDOWN_LLM_MODEL", "llava")],
        // Missing API key -> resolve() returns None -> not available.
        |caps| assert!(!caps.llm_captions),
    );
}
