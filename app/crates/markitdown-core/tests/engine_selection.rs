//! Cross-platform engine-selection / Python-fallback DECISION tests.
//!
//! These run on EVERY OS — including Windows — because they never spawn a
//! shell stub: they exercise binary resolution, the "no fallback when the
//! Python binary is absent" path, and pure-Rust conversion. The actual
//! subprocess-exec fallback (shell-script stubs) is Unix-only and lives in
//! `python_fallback.rs` (`#![cfg(unix)]`); this file is its Windows-safe
//! counterpart so the fallback decision logic is regression-covered on all
//! platforms.

use markitdown_core::{ConvertOptions, Engine, MarkItDown};
use std::path::PathBuf;

fn fixture(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

/// A path that cannot exist on any platform, so binary resolution always fails
/// (and the `.exists()` filter short-circuits before any process is spawned).
fn missing_bin() -> PathBuf {
    PathBuf::from("this/path/does/not/exist/markitdown-py-nope")
}

#[test]
fn rust_engine_converts_locally_on_every_os() {
    let md = MarkItDown::with_options(ConvertOptions {
        engine: Engine::Rust,
        ..Default::default()
    });
    let r = md.convert_path(fixture("test.docx")).unwrap();
    assert!(r.markdown.contains("AutoGen"));
}

#[test]
fn auto_without_python_keeps_degraded_rust_result() {
    // Explicit nonexistent python_bin -> resolution returns None (an explicit
    // path wins over the env var, and it doesn't exist) -> no subprocess ->
    // the degraded Rust result is returned unchanged. Deterministic even if
    // MARKITDOWN_PY_BIN happens to be set in the CI environment.
    let md = MarkItDown::with_options(ConvertOptions {
        engine: Engine::Auto,
        python_bin: Some(missing_bin()),
        ..Default::default()
    });
    let r = md.convert_path(fixture("test.mp3")).unwrap();
    assert!(r.markdown.contains("Duration:"), "rust audio metadata expected");
    assert!(r.degraded, "audio is degraded without the Python engine");
}

#[test]
fn python_engine_available_is_false_for_missing_binary() {
    let opts = ConvertOptions {
        engine: Engine::Auto,
        python_bin: Some(missing_bin()),
        ..Default::default()
    };
    assert!(!markitdown_core::python_engine_available(&opts));
}

#[test]
fn llm_caption_unavailable_without_config() {
    // Only assert the negative when the environment is genuinely unset, so the
    // test is correct whether or not a runner exports MARKITDOWN_LLM_*.
    if std::env::var("MARKITDOWN_LLM_API_KEY").is_err() {
        assert!(!markitdown_core::llm_caption_available(&ConvertOptions::default()));
    }
}

#[test]
fn unsupported_input_errors_regardless_of_engine() {
    for engine in [Engine::Rust, Engine::Auto] {
        let md = MarkItDown::with_options(ConvertOptions {
            engine,
            python_bin: Some(missing_bin()), // no fallback available
            ..Default::default()
        });
        assert!(
            md.convert_path(fixture("random.bin")).is_err(),
            "random.bin must be rejected under {engine:?} with no Python engine"
        );
    }
}
