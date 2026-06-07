//! LLM image-caption tests against a local mock OpenAI-compatible server —
//! no network, no API key, fully deterministic.

use markitdown_core::{ConvertOptions, LlmConfig, MarkItDown};
use std::io::{Read, Write};
use std::net::TcpListener;
use std::path::PathBuf;
use std::sync::mpsc;

fn fixture(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

/// One-shot mock `chat/completions` endpoint. Returns (api_base, request_rx).
fn mock_openai(caption: &'static str) -> (String, mpsc::Receiver<String>) {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let port = listener.local_addr().unwrap().port();
    let (tx, rx) = mpsc::channel();

    std::thread::spawn(move || {
        let (mut stream, _) = listener.accept().unwrap();
        // Read headers, then exactly Content-Length body bytes.
        let mut buf = Vec::new();
        let mut tmp = [0u8; 4096];
        let body_start;
        loop {
            let n = stream.read(&mut tmp).unwrap();
            buf.extend_from_slice(&tmp[..n]);
            if let Some(pos) = find(&buf, b"\r\n\r\n") {
                body_start = pos + 4;
                break;
            }
        }
        let headers = String::from_utf8_lossy(&buf[..body_start]).to_string();
        let content_length: usize = headers
            .lines()
            .find_map(|l| {
                l.to_ascii_lowercase()
                    .strip_prefix("content-length:")
                    .map(|v| v.trim().parse().unwrap())
            })
            .unwrap_or(0);
        while buf.len() < body_start + content_length {
            let n = stream.read(&mut tmp).unwrap();
            buf.extend_from_slice(&tmp[..n]);
        }
        let request = String::from_utf8_lossy(&buf).to_string();

        let body = format!(
            r#"{{"choices":[{{"message":{{"role":"assistant","content":"{caption}"}}}}]}}"#
        );
        let resp = format!(
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
            body.len(),
            body
        );
        stream.write_all(resp.as_bytes()).unwrap();
        let _ = tx.send(request);
    });

    (format!("http://127.0.0.1:{port}/v1"), rx)
}

fn find(haystack: &[u8], needle: &[u8]) -> Option<usize> {
    haystack.windows(needle.len()).position(|w| w == needle)
}

#[test]
fn image_gets_llm_description_section() {
    let (api_base, rx) = mock_openai("A test photograph used by the suite.");
    let md = MarkItDown::with_options(ConvertOptions {
        llm: Some(LlmConfig {
            api_base,
            api_key: "test-key".into(),
            model: "gpt-4o-mini".into(),
            prompt: None,
        }),
        ..Default::default()
    });

    let r = md.convert_path(fixture("test.jpg")).unwrap();
    assert!(
        r.markdown.contains("# Description:\nA test photograph used by the suite."),
        "caption section expected, got tail: …{}",
        &r.markdown[r.markdown.len().saturating_sub(200)..]
    );
    // EXIF metadata must still be present alongside the caption.
    assert!(r.markdown.contains("ImageSize:"));
    // A captioned image is no longer a degraded result.
    assert!(!r.degraded);

    // Verify the request matched Python's _llm_caption.py shape.
    let request = rx.recv_timeout(std::time::Duration::from_secs(5)).unwrap();
    assert!(request.contains("authorization: Bearer test-key")
        || request.contains("Authorization: Bearer test-key"));
    // ureq may pretty-print the JSON body; compare whitespace-insensitively.
    let compact: String = request.chars().filter(|c| !c.is_whitespace()).collect();
    assert!(compact.contains(r#""model":"gpt-4o-mini""#));
    assert!(request.contains("Write a detailed caption for this image."));
    assert!(request.contains("data:image/jpeg;base64,"));
}

#[test]
fn llm_failure_keeps_metadata_and_degraded_flag() {
    // Unreachable endpoint: caption must fail silently.
    let md = MarkItDown::with_options(ConvertOptions {
        llm: Some(LlmConfig {
            api_base: "http://127.0.0.1:1/v1".into(),
            api_key: "k".into(),
            model: "m".into(),
            prompt: None,
        }),
        ..Default::default()
    });
    let r = md.convert_path(fixture("test.jpg")).unwrap();
    assert!(r.markdown.contains("ImageSize:"));
    assert!(!r.markdown.contains("# Description:"));
    assert!(r.degraded);
}
