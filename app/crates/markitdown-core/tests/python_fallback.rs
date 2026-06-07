//! Tests for the Auto-engine fallback chain using stub "Python engines"
//! (tiny shell scripts), so the real PyInstaller binary is not required.
//!
//! Covers every decision in the Auto matrix:
//!   rust Err            + python ok      -> python result
//!   rust Ok(degraded)   + python ok      -> python result
//!   rust Ok(degraded)   + python empty   -> rust result kept
//!   rust Ok(degraded)   + python fails   -> rust result kept
//!   rust Ok (clean)     -> python never invoked
//!   forced Engine::Python -> python result
//!   hung python         -> killed at MARKITDOWN_PY_TIMEOUT
#![cfg(unix)]

use markitdown_core::{ConvertOptions, Engine, MarkItDown};
use std::path::PathBuf;
use std::sync::Mutex;

/// Some tests mutate process-global env vars (MARKITDOWN_PY_ARGS/_TIMEOUT),
/// and `std::env::set_var` racing concurrent `env::var` reads is UB-adjacent
/// on macOS — serialize every test in this binary through one lock.
static ENV_LOCK: Mutex<()> = Mutex::new(());

fn guard() -> std::sync::MutexGuard<'static, ()> {
    ENV_LOCK.lock().unwrap_or_else(|e| e.into_inner())
}

fn fixture(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

/// Write an executable stub engine script and return its path.
fn stub_engine(name: &str, body: &str) -> PathBuf {
    use std::os::unix::fs::PermissionsExt;
    let dir = std::env::temp_dir().join(format!("md-stub-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join(name);
    std::fs::write(&path, format!("#!/bin/sh\n{body}\n")).unwrap();
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o755)).unwrap();
    path
}

fn auto_with(stub: PathBuf) -> MarkItDown {
    MarkItDown::with_options(ConvertOptions {
        engine: Engine::Auto,
        python_bin: Some(stub),
        ..Default::default()
    })
}

#[test]
fn unsupported_format_falls_back_to_python() {
    let _g = guard();
    let stub = stub_engine("ok.sh", r#"cat >/dev/null; echo "PYTHON ENGINE OUTPUT""#);
    let md = auto_with(stub);
    // random.bin is rejected by every Rust converter -> Python gets a shot.
    let r = md.convert_path(fixture("random.bin")).unwrap();
    assert!(r.markdown.contains("PYTHON ENGINE OUTPUT"));
}

#[test]
fn degraded_docx_with_comments_retries_python() {
    let _g = guard();
    let stub = stub_engine("ok2.sh", r#"cat >/dev/null; echo "PY DOCX WITH COMMENTS""#);
    let md = auto_with(stub);
    // This fixture contains a Word comment, which the Rust parser flags as a
    // fidelity gap (mammoth extracts comments; we don't).
    let r = md.convert_path(fixture("test_with_comment.docx")).unwrap();
    assert!(
        r.markdown.contains("PY DOCX WITH COMMENTS"),
        "expected python output, got: {:.200}",
        r.markdown
    );
}

#[test]
fn clean_docx_never_invokes_python() {
    let _g = guard();
    // Stub records an invocation marker; a clean docx must not trigger it.
    let marker = std::env::temp_dir().join(format!("md-marker-{}", std::process::id()));
    let _ = std::fs::remove_file(&marker);
    let stub = stub_engine(
        "spy.sh",
        &format!(r#"cat >/dev/null; touch "{}"; echo "PY""#, marker.display()),
    );
    let md = auto_with(stub);
    let r = md.convert_path(fixture("test.docx")).unwrap();
    assert!(r.markdown.contains("AutoGen"), "rust output expected");
    assert!(
        !marker.exists(),
        "python engine must not run for a clean conversion"
    );
}

#[test]
fn empty_python_output_keeps_rust_result() {
    let _g = guard();
    let stub = stub_engine("empty.sh", r#"cat >/dev/null; echo """#);
    let md = auto_with(stub);
    // Audio is always degraded (no transcription) -> python tried -> empty ->
    // the rust tags must be kept.
    let r = md.convert_path(fixture("test.mp3")).unwrap();
    assert!(
        r.markdown.contains("Artist:"),
        "rust metadata must survive an empty python result: {:.200}",
        r.markdown
    );
}

#[test]
fn failing_python_keeps_rust_result() {
    let _g = guard();
    let stub = stub_engine("fail.sh", "exit 1");
    let md = auto_with(stub);
    let r = md.convert_path(fixture("test.mp3")).unwrap();
    assert!(r.markdown.contains("Duration:"));
}

#[test]
fn forced_python_engine_is_used_even_for_clean_files() {
    let _g = guard();
    let stub = stub_engine("forced.sh", r#"cat >/dev/null; echo "FORCED PY""#);
    let md = MarkItDown::with_options(ConvertOptions {
        engine: Engine::Python,
        python_bin: Some(stub),
        ..Default::default()
    });
    let r = md.convert_path(fixture("test.json")).unwrap();
    assert!(r.markdown.contains("FORCED PY"));
}

#[test]
fn hung_python_engine_is_killed_at_timeout() {
    let _g = guard();
    // Scope the override to this test; the other stubs finish in
    // milliseconds, so a short global timeout cannot break them even if the
    // env var leaks across threads briefly.
    std::env::set_var("MARKITDOWN_PY_TIMEOUT", "2");
    let stub = stub_engine("hang.sh", "sleep 30");
    let md = MarkItDown::with_options(ConvertOptions {
        engine: Engine::Python,
        python_bin: Some(stub),
        ..Default::default()
    });
    let start = std::time::Instant::now();
    let err = md.convert_path(fixture("test.json")).unwrap_err();
    assert!(
        start.elapsed() < std::time::Duration::from_secs(10),
        "must not wait for the full sleep"
    );
    assert!(err.to_string().contains("timed out"), "got: {err}");
    std::env::remove_var("MARKITDOWN_PY_TIMEOUT");
}

/// Stub that records its argv to a file, ignores stdin, prints a marker.
fn recording_stub(name: &str, argv_file: &std::path::Path) -> PathBuf {
    stub_engine(
        name,
        &format!(
            r#"echo "$@" > "{}"
cat >/dev/null 2>/dev/null || true
echo "RECORDED""#,
            argv_file.display()
        ),
    )
}

#[test]
fn url_inputs_are_passed_as_argument_not_stdin() {
    let _g = guard();
    // URL-gated converters in the Python engine (YouTube transcripts,
    // Wikipedia, Bing) only activate when given the URL itself.
    let argv = std::env::temp_dir().join(format!("md-argv-url-{}", std::process::id()));
    let stub = recording_stub("rec-url.sh", &argv);
    let md = auto_with(stub);

    let html = r#"<html><head><title>T - YouTube</title>
        <meta property="og:title" content="T"></head><body></body></html>"#;
    let url = "https://www.youtube.com/watch?v=test123";
    let hints = markitdown_core::StreamInfo::new()
        .with_extension(".html")
        .with_url(url);
    let r = md.convert_bytes(html.as_bytes(), hints).unwrap();
    assert!(r.markdown.contains("RECORDED"), "python output expected");

    let recorded = std::fs::read_to_string(&argv).unwrap();
    assert!(recorded.contains(url), "URL must be an argument: {recorded}");
    assert!(!recorded.contains("-x"), "no stdin hints when URL is passed: {recorded}");
    std::fs::remove_file(&argv).ok();
}

#[test]
fn local_files_are_passed_as_path_argument() {
    let _g = guard();
    let argv = std::env::temp_dir().join(format!("md-argv-path-{}", std::process::id()));
    let stub = recording_stub("rec-path.sh", &argv);
    let md = auto_with(stub);

    // mp3 is always degraded -> python invoked -> must receive the path.
    let r = md.convert_path(fixture("test.mp3")).unwrap();
    assert!(r.markdown.contains("RECORDED"));
    let recorded = std::fs::read_to_string(&argv).unwrap();
    assert!(
        recorded.contains("test.mp3"),
        "local path must be an argument (zero-copy): {recorded}"
    );
    std::fs::remove_file(&argv).ok();
}

#[test]
fn py_args_env_is_appended() {
    let _g = guard();
    let argv = std::env::temp_dir().join(format!("md-argv-extra-{}", std::process::id()));
    let stub = recording_stub("rec-extra.sh", &argv);
    // Env leak to parallel stub tests is harmless: stubs ignore their argv.
    std::env::set_var("MARKITDOWN_PY_ARGS", "-d -e https://di.example.com/");
    let md = auto_with(stub);
    let r = md.convert_path(fixture("test.mp3")).unwrap();
    std::env::remove_var("MARKITDOWN_PY_ARGS");
    assert!(r.markdown.contains("RECORDED"));
    let recorded = std::fs::read_to_string(&argv).unwrap();
    assert!(
        recorded.contains("-d") && recorded.contains("https://di.example.com/"),
        "MARKITDOWN_PY_ARGS must pass through: {recorded}"
    );
    std::fs::remove_file(&argv).ok();
}

#[test]
fn no_python_configured_means_no_fallback_attempt() {
    let _g = guard();
    let md = MarkItDown::with_options(ConvertOptions {
        engine: Engine::Auto,
        python_bin: Some(PathBuf::from("/definitely/not/here")),
        ..Default::default()
    });
    // Nonexistent binary -> resolve fails -> degraded rust result returned as-is.
    let r = md.convert_path(fixture("test.mp3")).unwrap();
    assert!(r.markdown.contains("Duration:"));
    assert!(r.degraded);
}
