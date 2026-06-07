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
