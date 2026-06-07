//! MarkItDown desktop backend.
//!
//! Exposes a handful of Tauri commands to the vanilla-TS frontend:
//!   * `convert_files`  — runs each file/URL conversion on a background thread
//!     and emits a `job:update` event per status change.
//!   * `save_markdown`   — writes Markdown to a path chosen via the dialog plugin.
//!   * `list_supported`  — returns the engine's supported-format table.
//!   * `get_capabilities` — reports whether the optional Python engine and LLM
//!     captioning are configured in the current environment.
//!
//! Conversions never run on the UI/main thread: `convert_files` returns
//! immediately after spawning blocking tasks, and a bounded number run at once
//! so dropping hundreds of files doesn't exhaust threads.

use std::path::Path;
use std::sync::{Arc, Condvar, Mutex};

use markitdown_core::{
    llm_caption_available, python_engine_available, ConvertOptions, Engine, MarkItDown,
    SUPPORTED_FORMATS,
};
use serde::{Deserialize, Serialize};
use tauri::{AppHandle, Emitter};

/// A single conversion request coming from the frontend. The frontend assigns
/// the id so it can correlate `job:update` events with its queue entries.
///
/// `path` is either a filesystem path or an http(s) URL — `convert_uri` on the
/// engine handles both. `engine` is an optional `"auto"`/`"rust"`/`"python"`
/// hint; absent or unrecognized values fall back to [`Engine::Auto`].
#[derive(Debug, Clone, Deserialize)]
pub struct ConvertRequest {
    pub id: String,
    pub path: String,
    #[serde(default)]
    pub engine: Option<String>,
}

/// Map a frontend engine string to the core [`Engine`]. Unknown/absent values
/// default to [`Engine::Auto`] so the app degrades gracefully.
pub fn parse_engine(value: Option<&str>) -> Engine {
    match value.map(str::trim).map(str::to_ascii_lowercase).as_deref() {
        Some("rust") => Engine::Rust,
        Some("python") => Engine::Python,
        _ => Engine::Auto,
    }
}

/// Capability flags surfaced to the UI so it can show which optional features
/// are wired up in the current environment.
#[derive(Debug, Clone, Copy, Serialize)]
pub struct Capabilities {
    /// True when a usable Python fallback binary is configured (MARKITDOWN_PY_BIN).
    pub python_engine: bool,
    /// True when LLM image captioning is configured
    /// (MARKITDOWN_LLM_API_KEY + MARKITDOWN_LLM_MODEL).
    pub llm_captions: bool,
}

/// Per-job status, serialized as a lowercase string to match the TS union type.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum JobStatus {
    Queued,
    Converting,
    Done,
    Failed,
}

/// The event payload emitted on the `job:update` channel.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JobUpdate {
    pub id: String,
    pub path: String,
    pub status: JobStatus,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub size: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub markdown: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub title: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
    /// True when the conversion hit a known fidelity gap (no OCR/transcription
    /// available). Only meaningful on a `done` update; skipped when false.
    #[serde(default, skip_serializing_if = "std::ops::Not::not")]
    pub degraded: bool,
    /// Wall-clock conversion time in milliseconds. Set on `done`/`failed`.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub duration_ms: Option<u64>,
}

impl JobUpdate {
    fn new(id: &str, path: &str, status: JobStatus) -> Self {
        JobUpdate {
            id: id.to_string(),
            path: path.to_string(),
            status,
            size: None,
            markdown: None,
            title: None,
            error: None,
            degraded: false,
            duration_ms: None,
        }
    }
}

/// Format descriptor mirrored from the engine, serializable for the frontend.
#[derive(Debug, Clone, Serialize)]
pub struct FormatInfo {
    pub name: String,
    pub extensions: Vec<String>,
    pub notes: String,
}

/// The event channel the frontend listens on.
const JOB_EVENT: &str = "job:update";

/// Upper bound on simultaneous conversions. Keeps a flood of dropped files
/// from spawning unbounded blocking threads.
fn concurrency_limit() -> usize {
    std::thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(4)
        .clamp(1, 8)
}

/// A tiny counting semaphore built on std primitives (no extra deps).
#[derive(Clone)]
struct Semaphore {
    inner: Arc<(Mutex<usize>, Condvar)>,
}

impl Semaphore {
    fn new(permits: usize) -> Self {
        Semaphore {
            inner: Arc::new((Mutex::new(permits), Condvar::new())),
        }
    }
    fn acquire(&self) {
        let (lock, cvar) = &*self.inner;
        let mut avail = lock.lock().unwrap();
        while *avail == 0 {
            avail = cvar.wait(avail).unwrap();
        }
        *avail -= 1;
    }
    fn release(&self) {
        let (lock, cvar) = &*self.inner;
        let mut avail = lock.lock().unwrap();
        *avail += 1;
        cvar.notify_one();
    }
}

fn emit(app: &AppHandle, update: &JobUpdate) {
    // Emit failures only matter for liveness; log and continue.
    if let Err(e) = app.emit(JOB_EVENT, update) {
        eprintln!("failed to emit {JOB_EVENT}: {e}");
    }
}

/// Derive the suggested `.md` output name for an input path (logic also used
/// by the frontend's Save dialog; unit-tested below).
pub fn output_name(input: &str) -> String {
    let stem = Path::new(input)
        .file_stem()
        .and_then(|s| s.to_str())
        .filter(|s| !s.is_empty())
        .unwrap_or("output");
    format!("{stem}.md")
}

/// A source is treated as a URL (converted via `convert_uri`) when it begins
/// with an http(s) scheme; everything else is a local filesystem path.
fn is_url(src: &str) -> bool {
    src.starts_with("http://") || src.starts_with("https://")
}

/// Convert one file or URL on the current (blocking) thread, emitting status
/// events.
fn run_one(app: &AppHandle, req: &ConvertRequest) {
    emit(app, &JobUpdate::new(&req.id, &req.path, JobStatus::Converting));
    let started = std::time::Instant::now();

    let url = is_url(&req.path);
    // URLs have no local size; only stat real files.
    let size = if url {
        None
    } else {
        std::fs::metadata(&req.path).map(|m| m.len()).ok()
    };

    let md = MarkItDown::with_options(ConvertOptions {
        engine: parse_engine(req.engine.as_deref()),
        ..Default::default()
    });

    let outcome = if url {
        md.convert_uri(&req.path)
    } else {
        md.convert_path(&req.path)
    };

    let mut update = match outcome {
        Ok(result) => {
            let mut u = JobUpdate::new(&req.id, &req.path, JobStatus::Done);
            u.markdown = Some(result.markdown);
            u.title = result.title;
            u.degraded = result.degraded;
            u
        }
        Err(err) => {
            let mut u = JobUpdate::new(&req.id, &req.path, JobStatus::Failed);
            u.error = Some(err.to_string());
            u
        }
    };
    update.size = size;
    update.duration_ms = Some(started.elapsed().as_millis() as u64);
    emit(app, &update);
}

#[tauri::command]
fn convert_files(app: AppHandle, requests: Vec<ConvertRequest>) {
    let sem = Semaphore::new(concurrency_limit());
    for req in requests {
        // Mark queued immediately so the UI reflects the full batch at once.
        emit(&app, &JobUpdate::new(&req.id, &req.path, JobStatus::Queued));
        let app = app.clone();
        let sem = sem.clone();
        // spawn_blocking: conversions are CPU/IO heavy and must stay off the
        // main thread. Returns immediately; events drive the UI.
        tauri::async_runtime::spawn_blocking(move || {
            sem.acquire();
            run_one(&app, &req);
            sem.release();
        });
    }
}

#[tauri::command]
fn save_markdown(path: String, contents: String) -> Result<(), String> {
    std::fs::write(&path, contents).map_err(|e| format!("could not save {path}: {e}"))
}

#[tauri::command]
fn list_supported() -> Vec<FormatInfo> {
    SUPPORTED_FORMATS
        .iter()
        .map(|f| FormatInfo {
            name: f.name.to_string(),
            extensions: f.extensions.iter().map(|e| e.to_string()).collect(),
            notes: f.notes.to_string(),
        })
        .collect()
}

#[tauri::command]
fn get_capabilities() -> Capabilities {
    // The desktop app relies on environment configuration only (no per-call
    // overrides), so an empty options set reflects the live environment.
    let opts = ConvertOptions::default();
    Capabilities {
        python_engine: python_engine_available(&opts),
        llm_captions: llm_caption_available(&opts),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            convert_files,
            save_markdown,
            list_supported,
            get_capabilities
        ])
        .run(tauri::generate_context!())
        .expect("error while running MarkItDown desktop");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn job_status_serializes_lowercase() {
        assert_eq!(serde_json::to_string(&JobStatus::Done).unwrap(), "\"done\"");
        assert_eq!(
            serde_json::to_string(&JobStatus::Converting).unwrap(),
            "\"converting\""
        );
    }

    #[test]
    fn job_update_roundtrips() {
        let mut u = JobUpdate::new("job-1", "/tmp/a.pdf", JobStatus::Done);
        u.markdown = Some("# Hi".into());
        u.title = Some("Hi".into());
        u.size = Some(123);
        let json = serde_json::to_string(&u).unwrap();
        let back: JobUpdate = serde_json::from_str(&json).unwrap();
        assert_eq!(back.id, "job-1");
        assert_eq!(back.status, JobStatus::Done);
        assert_eq!(back.markdown.as_deref(), Some("# Hi"));
        assert_eq!(back.size, Some(123));
    }

    #[test]
    fn optional_fields_are_skipped_when_none() {
        let u = JobUpdate::new("j", "/p", JobStatus::Queued);
        let json = serde_json::to_string(&u).unwrap();
        assert!(!json.contains("markdown"));
        assert!(!json.contains("error"));
        assert!(!json.contains("title"));
        assert!(!json.contains("size"));
        assert!(json.contains("\"queued\""));
    }

    #[test]
    fn convert_request_deserializes() {
        let req: ConvertRequest =
            serde_json::from_str(r#"{"id":"x","path":"/tmp/file.txt"}"#).unwrap();
        assert_eq!(req.id, "x");
        assert_eq!(req.path, "/tmp/file.txt");
        // engine is optional and defaults to None.
        assert_eq!(req.engine, None);
    }

    #[test]
    fn convert_request_deserializes_with_engine() {
        let req: ConvertRequest =
            serde_json::from_str(r#"{"id":"x","path":"/tmp/file.txt","engine":"python"}"#).unwrap();
        assert_eq!(req.engine.as_deref(), Some("python"));
    }

    #[test]
    fn parse_engine_maps_known_values() {
        assert_eq!(parse_engine(Some("rust")), Engine::Rust);
        assert_eq!(parse_engine(Some("python")), Engine::Python);
        assert_eq!(parse_engine(Some("auto")), Engine::Auto);
        // Case-insensitive and whitespace-tolerant.
        assert_eq!(parse_engine(Some("  Python ")), Engine::Python);
        assert_eq!(parse_engine(Some("RUST")), Engine::Rust);
    }

    #[test]
    fn parse_engine_defaults_to_auto() {
        assert_eq!(parse_engine(None), Engine::Auto);
        assert_eq!(parse_engine(Some("")), Engine::Auto);
        assert_eq!(parse_engine(Some("nonsense")), Engine::Auto);
    }

    #[test]
    fn is_url_detects_http_schemes() {
        assert!(is_url("http://example.com"));
        assert!(is_url("https://example.com/a.pdf"));
        assert!(!is_url("/tmp/file.txt"));
        assert!(!is_url("file:///tmp/file.txt"));
        assert!(!is_url("ftp://example.com"));
    }

    #[test]
    fn capabilities_serializes_both_flags() {
        let caps = Capabilities {
            python_engine: true,
            llm_captions: false,
        };
        let json = serde_json::to_string(&caps).unwrap();
        // Confirm exact shape with the field names the frontend reads.
        let v: serde_json::Value = serde_json::from_str(&json).unwrap();
        assert_eq!(v["python_engine"], serde_json::json!(true));
        assert_eq!(v["llm_captions"], serde_json::json!(false));
    }

    #[test]
    fn job_update_degraded_skipped_when_false() {
        let mut u = JobUpdate::new("j", "/p", JobStatus::Done);
        u.markdown = Some("# Hi".into());
        let json = serde_json::to_string(&u).unwrap();
        assert!(!json.contains("degraded"));
        u.degraded = true;
        let json = serde_json::to_string(&u).unwrap();
        assert!(json.contains("\"degraded\":true"));
    }

    #[test]
    fn output_name_replaces_extension() {
        assert_eq!(output_name("/a/b/report.pdf"), "report.md");
        assert_eq!(output_name("notes.docx"), "notes.md");
        assert_eq!(output_name("/x/archive.tar.gz"), "archive.tar.md");
    }

    #[test]
    fn output_name_handles_no_stem() {
        assert_eq!(output_name(""), "output.md");
        assert_eq!(output_name("/"), "output.md");
    }

    #[test]
    fn semaphore_bounds_permits() {
        let sem = Semaphore::new(2);
        sem.acquire();
        sem.acquire();
        sem.release();
        // A third acquire after one release must succeed without blocking.
        sem.acquire();
    }

    #[test]
    fn list_supported_is_populated() {
        let formats = list_supported();
        assert!(!formats.is_empty());
        assert!(formats.iter().any(|f| f.name == "PDF"));
        assert!(formats
            .iter()
            .any(|f| f.extensions.iter().any(|e| e == ".pdf")));
    }
}
