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
    capabilities as core_capabilities, llm_caption_available, python_engine_available,
    Capabilities as CoreCapabilities, ConvertOptions, Engine, LlmConfig, MarkItDown,
    LLM_PROVIDERS, SUPPORTED_FORMATS,
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
    /// Optional LLM image-caption settings supplied by the UI. Mapped to a core
    /// [`LlmConfig`] only when api_base + api_key + model are all non-empty.
    #[serde(default)]
    pub llm: Option<LlmCfg>,
}

/// LLM image-caption settings as sent from the frontend. Every field is
/// optional so a partially-filled settings form deserializes cleanly; the
/// mapping to a core [`LlmConfig`] only succeeds when the required trio
/// (api_base + api_key + model) is fully populated.
#[derive(Debug, Clone, Default, Deserialize)]
pub struct LlmCfg {
    #[serde(default)]
    pub api_base: Option<String>,
    #[serde(default)]
    pub api_key: Option<String>,
    #[serde(default)]
    pub model: Option<String>,
    #[serde(default)]
    pub prompt: Option<String>,
}

/// Build a core [`LlmConfig`] from the frontend settings. Returns `None` unless
/// api_base, api_key and model are all present and non-empty (after trimming),
/// so an empty or half-filled settings form leaves env-based config untouched.
pub fn to_llm_config(cfg: Option<&LlmCfg>) -> Option<LlmConfig> {
    /// Trimmed, non-empty value of an optional string field.
    fn trimmed(o: &Option<String>) -> Option<String> {
        o.as_deref().map(str::trim).filter(|s| !s.is_empty()).map(str::to_string)
    }
    let cfg = cfg?;
    Some(LlmConfig {
        api_base: trimmed(&cfg.api_base)?,
        api_key: trimmed(&cfg.api_key)?,
        model: trimmed(&cfg.model)?,
        prompt: trimmed(&cfg.prompt),
    })
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

/// An LLM provider preset surfaced to the UI for the Settings provider picker.
/// Mirrors the core [`markitdown_core::LlmProvider`] with owned strings so the
/// whole registry can cross the Tauri command boundary as JSON.
#[derive(Debug, Clone, Serialize)]
pub struct LlmProviderInfo {
    /// Stable id (matches the core registry id), persisted by the UI.
    pub id: String,
    /// Human-friendly name for the dropdown.
    pub name: String,
    /// Default OpenAI-compatible base URL (may be empty for "custom").
    pub api_base: String,
    /// Whether a cloud API key is required.
    pub requires_key: bool,
    /// True for endpoints that run on the local machine.
    pub local: bool,
    /// Example vision-capable models to seed the model datalist.
    pub example_models: Vec<String>,
    /// One-line guidance shown under the dropdown.
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
        llm: to_llm_config(req.llm.as_ref()),
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

/// Return the built-in LLM provider registry so the Settings modal can render a
/// provider dropdown (and model suggestions) instead of hardcoded presets.
#[tauri::command]
fn llm_providers() -> Vec<LlmProviderInfo> {
    LLM_PROVIDERS
        .iter()
        .map(|p| LlmProviderInfo {
            id: p.id.to_string(),
            name: p.name.to_string(),
            api_base: p.api_base.to_string(),
            requires_key: p.requires_key,
            local: p.local,
            example_models: p.example_models.iter().map(|m| m.to_string()).collect(),
            notes: p.notes.to_string(),
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

/// Richer capability report that folds in the UI's current LLM settings.
///
/// Builds [`ConvertOptions`] from the passed `llm` block (falling back to the
/// environment when it's empty) and returns the core [`Capabilities`], which
/// includes the resolved model + api_base for status display but — by design
/// of the core type — never the API key.
#[tauri::command]
fn capabilities(llm: Option<LlmCfg>) -> CoreCapabilities {
    let opts = ConvertOptions {
        llm: to_llm_config(llm.as_ref()),
        ..Default::default()
    };
    core_capabilities(&opts)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            convert_files,
            save_markdown,
            list_supported,
            get_capabilities,
            capabilities,
            llm_providers
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
    fn to_llm_config_none_when_empty_or_partial() {
        // No settings block at all.
        assert!(to_llm_config(None).is_none());
        // Empty block.
        assert!(to_llm_config(Some(&LlmCfg::default())).is_none());
        // Missing model.
        let partial = LlmCfg {
            api_base: Some("https://api.openai.com/v1".into()),
            api_key: Some("sk-x".into()),
            model: None,
            prompt: None,
        };
        assert!(to_llm_config(Some(&partial)).is_none());
        // Whitespace-only fields count as empty.
        let blanky = LlmCfg {
            api_base: Some("   ".into()),
            api_key: Some("sk-x".into()),
            model: Some("gpt-4o-mini".into()),
            prompt: None,
        };
        assert!(to_llm_config(Some(&blanky)).is_none());
    }

    #[test]
    fn to_llm_config_some_when_complete() {
        let full = LlmCfg {
            api_base: Some("  http://localhost:11434/v1  ".into()),
            api_key: Some("sk-secret".into()),
            model: Some("llava".into()),
            prompt: Some("  Describe this  ".into()),
        };
        let cfg = to_llm_config(Some(&full)).expect("complete config maps to Some");
        // Required fields are trimmed.
        assert_eq!(cfg.api_base, "http://localhost:11434/v1");
        assert_eq!(cfg.api_key, "sk-secret");
        assert_eq!(cfg.model, "llava");
        assert_eq!(cfg.prompt.as_deref(), Some("Describe this"));
    }

    #[test]
    fn to_llm_config_prompt_optional() {
        let full = LlmCfg {
            api_base: Some("https://api.openai.com/v1".into()),
            api_key: Some("k".into()),
            model: Some("gpt-4o-mini".into()),
            prompt: Some("   ".into()), // blank prompt -> None
        };
        let cfg = to_llm_config(Some(&full)).unwrap();
        assert!(cfg.prompt.is_none());
    }

    #[test]
    fn convert_request_deserializes_with_llm() {
        let req: ConvertRequest = serde_json::from_str(
            r#"{"id":"x","path":"/tmp/img.png","engine":"rust","llm":{"api_base":"http://localhost:1234/v1","api_key":"k","model":"llava","prompt":"hi"}}"#,
        )
        .unwrap();
        assert_eq!(req.engine.as_deref(), Some("rust"));
        let llm = req.llm.as_ref().expect("llm block present");
        assert_eq!(llm.api_base.as_deref(), Some("http://localhost:1234/v1"));
        assert_eq!(llm.model.as_deref(), Some("llava"));
        let cfg = to_llm_config(req.llm.as_ref()).unwrap();
        assert_eq!(cfg.api_key, "k");
        assert_eq!(cfg.model, "llava");
    }

    #[test]
    fn convert_request_llm_defaults_to_none() {
        // Absent llm block and absent individual fields both deserialize fine.
        let req: ConvertRequest =
            serde_json::from_str(r#"{"id":"x","path":"/p"}"#).unwrap();
        assert!(req.llm.is_none());
        let req2: ConvertRequest =
            serde_json::from_str(r#"{"id":"x","path":"/p","llm":{}}"#).unwrap();
        assert!(req2.llm.is_some());
        assert!(to_llm_config(req2.llm.as_ref()).is_none());
    }

    #[test]
    fn core_capabilities_never_serializes_api_key() {
        let opts = ConvertOptions {
            llm: to_llm_config(Some(&LlmCfg {
                api_base: Some("http://localhost:11434/v1".into()),
                api_key: Some("super-secret-key".into()),
                model: Some("llava".into()),
                prompt: None,
            })),
            ..Default::default()
        };
        let caps = core_capabilities(&opts);
        assert!(caps.llm_captions);
        assert_eq!(caps.llm_model.as_deref(), Some("llava"));
        assert_eq!(caps.llm_api_base.as_deref(), Some("http://localhost:11434/v1"));
        let json = serde_json::to_string(&caps).unwrap();
        assert!(!json.contains("super-secret-key"));
        assert!(!json.contains("api_key"));
    }

    #[test]
    fn llm_providers_returns_registry() {
        let providers = llm_providers();
        // The registry ships several presets; the UI relies on at least these.
        assert!(providers.len() >= 5, "expected >=5 providers");
        assert!(providers.iter().any(|p| p.id == "ollama"));
        assert!(providers.iter().any(|p| p.id == "openai"));
        // Ollama is local and needs no key — drives the UI hints.
        let ollama = providers.iter().find(|p| p.id == "ollama").unwrap();
        assert!(ollama.local && !ollama.requires_key);
        assert!(!ollama.example_models.is_empty());
        // The whole list must serialize for the Tauri command boundary.
        let json = serde_json::to_string(&providers).unwrap();
        assert!(json.contains("\"ollama\"") && json.contains("11434"));
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
