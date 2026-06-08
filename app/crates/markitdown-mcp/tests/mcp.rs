//! End-to-end test of the MCP server: spawns the real binary and drives a
//! raw JSON-RPC session over stdio (newline-delimited JSON), exactly as an
//! MCP client like Claude would.

use serde_json::{json, Value};
use std::io::{BufRead, BufReader, Write};
use std::path::PathBuf;
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};

const BIN: &str = env!("CARGO_BIN_EXE_markitdown-mcp");

fn fixture(name: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

struct McpClient {
    child: Child,
    stdin: ChildStdin,
    stdout: BufReader<ChildStdout>,
    next_id: i64,
}

impl McpClient {
    fn start() -> Self {
        Self::start_with_env(&[])
    }

    /// Start the server with extra environment variables (e.g. MARKITDOWN_LLM_*).
    fn start_with_env(env: &[(&str, &str)]) -> Self {
        let mut cmd = Command::new(BIN);
        cmd.stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null());
        for (k, v) in env {
            cmd.env(k, v);
        }
        let mut child = cmd.spawn().expect("spawn markitdown-mcp");
        let stdin = child.stdin.take().unwrap();
        let stdout = BufReader::new(child.stdout.take().unwrap());
        let mut client = McpClient {
            child,
            stdin,
            stdout,
            next_id: 1,
        };
        // MCP handshake.
        let init = client.request(
            "initialize",
            json!({
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp-test", "version": "0.0.1"}
            }),
        );
        assert_eq!(init["serverInfo"]["name"].as_str().is_some(), true);
        client.notify("notifications/initialized", json!({}));
        client
    }

    fn request(&mut self, method: &str, params: Value) -> Value {
        let v = self.request_raw(method, params);
        assert!(
            v.get("error").is_none(),
            "{method} returned error: {}",
            v["error"]
        );
        v["result"].clone()
    }

    /// Like `request` but returns the whole response envelope without
    /// asserting success (for negative tests).
    fn request_raw(&mut self, method: &str, params: Value) -> Value {
        let id = self.next_id;
        self.next_id += 1;
        let msg = json!({"jsonrpc": "2.0", "id": id, "method": method, "params": params});
        writeln!(self.stdin, "{msg}").unwrap();
        self.stdin.flush().unwrap();
        // Read lines until the response with our id arrives (the server may
        // interleave notifications).
        loop {
            let mut line = String::new();
            let n = self.stdout.read_line(&mut line).unwrap();
            assert!(n > 0, "server closed stdout before responding to {method}");
            let v: Value = serde_json::from_str(line.trim()).expect("valid JSON from server");
            if v["id"] == json!(id) {
                return v;
            }
        }
    }

    fn notify(&mut self, method: &str, params: Value) {
        let msg = json!({"jsonrpc": "2.0", "method": method, "params": params});
        writeln!(self.stdin, "{msg}").unwrap();
        self.stdin.flush().unwrap();
    }

    fn call_tool(&mut self, name: &str, args: Value) -> String {
        let result = self.request("tools/call", json!({"name": name, "arguments": args}));
        assert_ne!(
            result["isError"],
            json!(true),
            "tool {name} errored: {result}"
        );
        result["content"][0]["text"]
            .as_str()
            .expect("text content")
            .to_string()
    }
}

impl Drop for McpClient {
    fn drop(&mut self) {
        let _ = self.child.kill();
        let _ = self.child.wait();
    }
}

#[test]
fn full_session_handshake_list_and_call() {
    let mut c = McpClient::start();

    // tools/list must expose exactly our 4 tools.
    let tools = c.request("tools/list", json!({}));
    let names: Vec<&str> = tools["tools"]
        .as_array()
        .unwrap()
        .iter()
        .map(|t| t["name"].as_str().unwrap())
        .collect();
    for expected in [
        "convert_to_markdown",
        "convert_file",
        "convert_batch",
        "list_supported_formats",
    ] {
        assert!(names.contains(&expected), "missing tool {expected}: {names:?}");
    }
    assert_eq!(names.len(), 4, "unexpected extra tools: {names:?}");

    // Every tool must carry a description and an input schema.
    for t in tools["tools"].as_array().unwrap() {
        assert!(t["description"].as_str().unwrap().len() > 20);
        assert!(t["inputSchema"].is_object());
    }

    // convert_to_markdown on a real DOCX fixture.
    let text = c.call_tool(
        "convert_to_markdown",
        json!({"uri": fixture("test.docx").to_str().unwrap()}),
    );
    assert!(text.contains("AutoGen"), "docx content expected, got: {:.200}", text);

    // Engine override parameter must be accepted.
    let text_rust = c.call_tool(
        "convert_to_markdown",
        json!({"uri": fixture("test.docx").to_str().unwrap(), "engine": "rust"}),
    );
    assert!(text_rust.contains("AutoGen"));

    // list_supported_formats now reports hybrid capabilities.
    let formats = c.call_tool("list_supported_formats", json!({}));
    assert!(formats.contains("PDF") && formats.contains(".docx"));
    assert!(formats.contains("python fallback engine"));
    assert!(formats.contains("llm image captions"));
}

#[test]
fn paging_truncates_and_resumes() {
    let mut c = McpClient::start();
    let uri = fixture("test.docx").to_str().unwrap().to_string();

    let page1 = c.call_tool(
        "convert_to_markdown",
        json!({"uri": uri, "max_chars": 200}),
    );
    assert!(
        page1.contains("[truncated: chars 0..200 of"),
        "expected paging note, got: {:.300}",
        page1
    );

    let page2 = c.call_tool(
        "convert_to_markdown",
        json!({"uri": uri, "max_chars": 200, "offset": 200}),
    );
    assert!(page2.contains("chars 200..400 of") || !page2.contains("[truncated"));
    // Pages must differ (we actually advanced).
    assert_ne!(page1, page2);
}

#[test]
fn convert_file_with_output_path_returns_summary() {
    let mut c = McpClient::start();
    let dir = std::env::temp_dir().join(format!("mdmcp-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let dest = dir.join("out.md");

    let summary = c.call_tool(
        "convert_file",
        json!({
            "path": fixture("test.docx").to_str().unwrap(),
            "output_path": dest.to_str().unwrap()
        }),
    );
    assert!(summary.contains("written:"), "got: {summary}");
    assert!(summary.contains("chars:"));
    assert!(summary.len() < 1500, "summary must stay small, got {} chars", summary.len());
    let written = std::fs::read_to_string(&dest).unwrap();
    assert!(written.contains("AutoGen"));
    std::fs::remove_dir_all(&dir).ok();
}

#[test]
fn convert_batch_writes_all_outputs() {
    let mut c = McpClient::start();
    let dir = std::env::temp_dir().join(format!("mdmcp-batch-{}", std::process::id()));

    let report = c.call_tool(
        "convert_batch",
        json!({
            "paths": [
                fixture("test.docx").to_str().unwrap(),
                fixture("test.xlsx").to_str().unwrap()
            ],
            "output_dir": dir.to_str().unwrap()
        }),
    );
    assert_eq!(report.matches("ok: ").count(), 2, "report: {report}");
    assert!(dir.join("test.docx.md").exists());
    assert!(dir.join("test.xlsx.md").exists());
    std::fs::remove_dir_all(&dir).ok();
}

#[test]
fn tool_error_is_reported_not_crash() {
    let mut c = McpClient::start();
    let result = c.request_raw(
        "tools/call",
        json!({"name": "convert_to_markdown", "arguments": {"uri": "/nonexistent/x.pdf"}}),
    );
    // rmcp surfaces handler errors as protocol errors or isError results;
    // either way the server must keep serving afterwards.
    let still_alive = c.call_tool("list_supported_formats", json!({}));
    assert!(still_alive.contains("PDF"));
    let _ = result;
}

/// One-shot mock OpenAI-compatible endpoint that reads the full request
/// (headers + Content-Length body — the image POST is large) then replies with
/// a fixed caption. Returns the base URL.
fn mock_openai(caption: &'static str) -> String {
    use std::io::Read;
    let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
    let port = listener.local_addr().unwrap().port();
    std::thread::spawn(move || {
        if let Ok((mut s, _)) = listener.accept() {
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
        }
    });
    format!("http://127.0.0.1:{port}/v1")
}

#[test]
fn capabilities_report_llm_when_env_configured() {
    let base = mock_openai("ignored for the capability listing");
    let mut c = McpClient::start_with_env(&[
        ("MARKITDOWN_LLM_API_BASE", &base),
        ("MARKITDOWN_LLM_MODEL", "test-vision"),
        ("MARKITDOWN_LLM_API_KEY", "test-key"),
    ]);
    let formats = c.call_tool("list_supported_formats", json!({}));
    assert!(formats.contains("llm image captions: AVAILABLE"), "got: {formats}");
    assert!(formats.contains("model=test-vision"));
    assert!(!formats.contains("test-key"), "API key must never be reported");
}

#[test]
fn server_captions_image_via_llm_env() {
    // Simulate a real deployment: the server is launched with MARKITDOWN_LLM_*
    // pointing at a (mock) OpenAI-compatible endpoint; converting an image then
    // yields a '# Description:' section — proving the MCP path honors LLM env.
    let base = mock_openai("A simulated caption from the MCP integration test.");
    let mut c = McpClient::start_with_env(&[
        ("MARKITDOWN_LLM_API_BASE", &base),
        ("MARKITDOWN_LLM_MODEL", "test-vision"),
        ("MARKITDOWN_LLM_API_KEY", "test-key"),
    ]);
    let text = c.call_tool(
        "convert_to_markdown",
        json!({"uri": fixture("test.jpg").to_str().unwrap(), "engine": "rust"}),
    );
    assert!(text.contains("ImageSize:"), "EXIF metadata expected");
    assert!(
        text.contains("# Description:")
            && text.contains("A simulated caption from the MCP integration test."),
        "LLM caption expected, got: {text}"
    );
}
