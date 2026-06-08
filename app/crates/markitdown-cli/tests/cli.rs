//! Integration tests for the `markitdown` binary, driven through the real
//! executable (CARGO_BIN_EXE) against the real fixtures from the Python
//! package — mirroring packages/markitdown/tests/test_cli_vectors.py.

use std::io::Write;
use std::path::PathBuf;
use std::process::{Command, Stdio};

const BIN: &str = env!("CARGO_BIN_EXE_markitdown");

fn fixture(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

fn run(args: &[&str]) -> std::process::Output {
    Command::new(BIN).args(args).output().expect("spawn binary")
}

/// Minimal one-shot mock of an OpenAI-compatible `chat/completions` endpoint,
/// so the LLM-caption path can be tested with no network and no real key.
/// Returns the base URL (`http://127.0.0.1:<port>/v1`).
fn mock_openai(caption: &'static str) -> String {
    use std::io::{Read, Write};
    let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
    let port = listener.local_addr().unwrap().port();
    std::thread::spawn(move || {
        if let Ok((mut s, _)) = listener.accept() {
            // Read the full request: headers, then exactly Content-Length bytes
            // of body. The image POST is large, so responding before the client
            // finishes writing would reset the connection and fail the request.
            let mut buf = Vec::new();
            let mut tmp = [0u8; 4096];
            let header_end = loop {
                let n = s.read(&mut tmp).unwrap_or(0);
                if n == 0 {
                    break buf.len();
                }
                buf.extend_from_slice(&tmp[..n]);
                if let Some(p) = buf.windows(4).position(|w| w == b"\r\n\r\n") {
                    break p + 4;
                }
            };
            let headers = String::from_utf8_lossy(&buf[..header_end]).to_lowercase();
            let len: usize = headers
                .lines()
                .find_map(|l| l.strip_prefix("content-length:").map(|v| v.trim().parse().unwrap_or(0)))
                .unwrap_or(0);
            while buf.len() < header_end + len {
                let n = s.read(&mut tmp).unwrap_or(0);
                if n == 0 {
                    break;
                }
                buf.extend_from_slice(&tmp[..n]);
            }
            let body = format!(r#"{{"choices":[{{"message":{{"content":"{caption}"}}}}]}}"#);
            let resp = format!(
                "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
                body.len(),
                body
            );
            let _ = s.write_all(resp.as_bytes());
            let _ = s.flush();
        }
    });
    format!("http://127.0.0.1:{port}/v1")
}

#[test]
fn version_flag() {
    let out = run(&["--version"]);
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.starts_with("markitdown "), "got: {s}");
}

#[test]
fn emit_man_renders_roff() {
    let out = run(&["--emit-man"]);
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains(".TH"), "man page must contain a .TH macro");
    assert!(s.to_lowercase().contains("markitdown"));
    // roff escapes hyphens: --output-dir renders as \-\-output\-dir
    assert!(s.contains(r"\-\-output\-dir"), "options must be documented");
}

#[test]
fn list_formats() {
    let out = run(&["--list-formats"]);
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("PDF") && s.contains(".docx") && s.contains(".epub"));
}

#[test]
fn convert_file_to_stdout() {
    let out = run(&[fixture("test.docx").to_str().unwrap()]);
    assert!(out.status.success(), "stderr: {}", String::from_utf8_lossy(&out.stderr));
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("AutoGen"), "docx body text expected, got: {:.200}", s);
}

#[test]
fn convert_stdin_with_extension_hint() {
    let mut child = Command::new(BIN)
        .args(["-x", "csv"])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    child
        .stdin
        .take()
        .unwrap()
        .write_all(b"name,age\nalice,30\n")
        .unwrap();
    let out = child.wait_with_output().unwrap();
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("| name | age |"), "got: {s}");
    assert!(s.contains("| alice | 30 |"));
}

#[test]
fn convert_to_output_file() {
    let dir = std::env::temp_dir().join(format!("mdcli-o-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let dest = dir.join("out.md");
    let out = run(&[
        fixture("test.json").to_str().unwrap(),
        "-o",
        dest.to_str().unwrap(),
    ]);
    assert!(out.status.success());
    let written = std::fs::read_to_string(&dest).unwrap();
    assert!(!written.trim().is_empty());
    std::fs::remove_dir_all(&dir).ok();
}

#[test]
fn batch_mode_parallel() {
    let dir = std::env::temp_dir().join(format!("mdcli-batch-{}", std::process::id()));
    let out = run(&[
        fixture("test.docx").to_str().unwrap(),
        fixture("test.xlsx").to_str().unwrap(),
        fixture("test_blog.html").to_str().unwrap(),
        "-O",
        dir.to_str().unwrap(),
    ]);
    assert!(out.status.success(), "stderr: {}", String::from_utf8_lossy(&out.stderr));
    // test.docx and test.xlsx share a stem → original extensions preserved.
    for name in ["test.docx.md", "test.xlsx.md", "test_blog.md"] {
        let p = dir.join(name);
        assert!(p.exists(), "missing {}", p.display());
        assert!(!std::fs::read_to_string(&p).unwrap().trim().is_empty());
    }
    std::fs::remove_dir_all(&dir).ok();
}

#[test]
fn batch_without_output_dir_fails() {
    let out = run(&[
        fixture("test.docx").to_str().unwrap(),
        fixture("test.xlsx").to_str().unwrap(),
    ]);
    assert!(!out.status.success());
    assert!(String::from_utf8_lossy(&out.stderr).contains("--output-dir"));
}

#[test]
fn unsupported_binary_fails() {
    let out = run(&[fixture("random.bin").to_str().unwrap()]);
    assert!(!out.status.success());
    let err = String::from_utf8_lossy(&out.stderr);
    assert!(err.contains("error"), "got: {err}");
}

#[test]
fn missing_file_fails() {
    let out = run(&["/nonexistent/definitely-not-here.pdf"]);
    assert!(!out.status.success());
}

#[test]
fn check_reports_unconfigured_without_secrets() {
    // Force "not configured" deterministically regardless of ambient env.
    let out = Command::new(BIN)
        .args(["--check", "--python-bin", "/no/such/bin"])
        .env_remove("MARKITDOWN_LLM_API_KEY")
        .env_remove("MARKITDOWN_LLM_MODEL")
        .output()
        .unwrap();
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("python fallback engine"));
    assert!(s.contains("llm image captions"));
}

#[test]
fn check_reports_llm_endpoint_and_model_without_key() {
    let out = run(&[
        "--check",
        "--llm-api-base",
        "http://localhost:11434/v1",
        "--llm-model",
        "llava",
        "--llm-api-key",
        "sk-DO-NOT-LEAK",
    ]);
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("model=llava"));
    assert!(s.contains("http://localhost:11434/v1"));
    assert!(!s.contains("sk-DO-NOT-LEAK"), "API key must never be printed");
}

#[test]
fn check_reports_python_engine_when_present() {
    // Any existing executable file counts as "present" for resolution.
    let out = Command::new(BIN)
        .args(["--check", "--python-bin", BIN]) // BIN is a real executable
        .output()
        .unwrap();
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("python fallback engine : available"), "got: {s}");
}

#[test]
fn list_llm_providers_shows_local_and_cloud() {
    let out = run(&["--list-llm-providers"]);
    assert!(out.status.success());
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("ollama") && s.contains("11434"), "local provider listed");
    assert!(s.contains("openai") && s.contains("groq"), "cloud providers listed");
    assert!(s.contains("custom"), "custom escape hatch listed");
}

#[test]
fn llm_provider_sets_base_url() {
    // --llm-provider ollama must select the Ollama base URL without --llm-api-base.
    let out = run(&[
        "--check",
        "--llm-provider",
        "ollama",
        "--llm-model",
        "llava",
        "--llm-api-key",
        "x",
    ]);
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("http://localhost:11434/v1"), "got: {s}");
    assert!(s.contains("model=llava"));
}

#[test]
fn explicit_base_overrides_provider() {
    let out = run(&[
        "--check",
        "--llm-provider",
        "ollama",
        "--llm-api-base",
        "http://example.test/v1",
        "--llm-model",
        "m",
        "--llm-api-key",
        "x",
    ]);
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("http://example.test/v1"), "explicit base must win: {s}");
}

#[test]
fn caption_via_provider_custom_and_mock_server() {
    // Use the `custom` provider with a mock base — proves provider selection +
    // captioning compose. CI-safe: localhost ephemeral port, no real network.
    let base = mock_openai("Caption via the custom provider.");
    let out = run(&[
        fixture("test.jpg").to_str().unwrap(),
        "--engine",
        "rust",
        "--llm-provider",
        "custom",
        "--llm-api-base",
        &base,
        "--llm-model",
        "test-vision",
        "--llm-api-key",
        "test-key",
    ]);
    assert!(out.status.success(), "stderr: {}", String::from_utf8_lossy(&out.stderr));
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("# Description:") && s.contains("Caption via the custom provider."), "got:\n{s}");
}

#[test]
fn llm_flags_caption_an_image_via_mock_server() {
    let base = mock_openai("A mocked caption for the CI test image.");
    let out = run(&[
        fixture("test.jpg").to_str().unwrap(),
        "--engine",
        "rust", // keep it deterministic; no python fallback
        "--llm-api-base",
        &base,
        "--llm-model",
        "test-vision",
        "--llm-api-key",
        "test-key",
    ]);
    assert!(out.status.success(), "stderr: {}", String::from_utf8_lossy(&out.stderr));
    let s = String::from_utf8_lossy(&out.stdout);
    assert!(s.contains("ImageSize:"), "EXIF metadata still present");
    assert!(
        s.contains("# Description:") && s.contains("A mocked caption for the CI test image."),
        "LLM caption section expected, got:\n{s}"
    );
}

/// A reader that closes early (like `| head` or `| grep -q`) must not make the
/// CLI panic with "failed printing to stdout: Broken pipe". We simulate it by
/// giving the child a stdout pipe and dropping our read end immediately.
#[test]
fn broken_pipe_does_not_panic() {
    use std::process::Stdio;
    // --list-formats writes many lines; drop the pipe before reading.
    let mut child = Command::new(BIN)
        .arg("--list-formats")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    drop(child.stdout.take()); // close the read end right away
    let out = child.wait_with_output().unwrap();
    let err = String::from_utf8_lossy(&out.stderr);
    assert!(
        !err.contains("panic") && !err.contains("Broken pipe"),
        "CLI panicked on a closed pipe: {err}"
    );
    // Killed-by-SIGPIPE would be a signal exit; we expect a graceful code.
    assert!(out.status.code().is_some(), "should exit normally, not via signal");
}
