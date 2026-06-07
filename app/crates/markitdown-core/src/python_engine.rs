//! Optional delegation to a PyInstaller-compiled Python markitdown binary.
//!
//! This is the escape hatch for the long tail the pure-Rust engine does not
//! cover locally (OCR for scanned documents, audio transcription, Azure
//! converters, Python plugins). It is strictly opt-in: nothing here runs
//! unless the caller selects [`crate::options::Engine::Python`]/`Auto` *and*
//! a binary is configured. See `app/python-engine/README.md` for how to build
//! one.

use crate::{ConvertError, ConvertOptions, ConvertResult, StreamInfo};
use std::io::Write;
use std::path::PathBuf;
use std::process::{Command, Stdio};

pub const PY_BIN_ENV: &str = "MARKITDOWN_PY_BIN";
/// Override the fallback timeout (seconds). Default: 300.
pub const PY_TIMEOUT_ENV: &str = "MARKITDOWN_PY_TIMEOUT";
/// Extra whitespace-separated args appended to every Python-engine call,
/// e.g. Azure Document Intelligence: `-d -e https://<res>.cognitiveservices.azure.com/`.
pub const PY_ARGS_ENV: &str = "MARKITDOWN_PY_ARGS";

const DEFAULT_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(300);

fn timeout() -> std::time::Duration {
    std::env::var(PY_TIMEOUT_ENV)
        .ok()
        .and_then(|v| v.parse::<u64>().ok())
        .map(std::time::Duration::from_secs)
        .unwrap_or(DEFAULT_TIMEOUT)
}

/// Resolve the configured Python engine binary, if any.
pub fn resolve_python_bin(opts: &ConvertOptions) -> Option<PathBuf> {
    opts.python_bin
        .clone()
        .or_else(|| std::env::var_os(PY_BIN_ENV).map(PathBuf::from))
        .filter(|p| p.exists())
}

/// True when a usable Python fallback binary is configured.
pub fn python_engine_available(opts: &ConvertOptions) -> bool {
    resolve_python_bin(opts).is_some()
}

/// Convert by piping the stream through the Python markitdown binary.
pub fn convert_with_python(
    data: &[u8],
    info: &StreamInfo,
    opts: &ConvertOptions,
) -> Result<ConvertResult, ConvertError> {
    let bin = resolve_python_bin(opts).ok_or_else(|| {
        ConvertError::MissingDependency(format!(
            "python engine requested but no binary found (set {PY_BIN_ENV} or --python-bin; \
             build one with app/python-engine/build_binary.sh)"
        ))
    })?;

    let mut cmd = Command::new(&bin);
    // Enable Python plugins (e.g. markitdown-ocr) when the binary was built
    // with them; harmless otherwise.
    cmd.arg("-p");
    // Extra pass-through args, e.g. Azure Document Intelligence:
    //   MARKITDOWN_PY_ARGS="-d -e https://<resource>.cognitiveservices.azure.com/"
    if let Ok(extra) = std::env::var(PY_ARGS_ENV) {
        cmd.args(extra.split_whitespace());
    }

    // Choose how to hand the input over, in order of fidelity:
    // 1. http(s)/file/data URL as an argument — the Python engine re-fetches
    //    it itself, which keeps its URL-gated converters working (YouTube
    //    transcripts, Wikipedia, Bing SERP).
    // 2. Local path as an argument — zero-copy for large files.
    // 3. Raw bytes over stdin with -x/-m hints — last resort.
    enum Input<'a> {
        Arg(String),
        Stdin(&'a [u8]),
    }
    let input = if let Some(url) = info.url.as_ref().filter(|u| {
        u.starts_with("http:") || u.starts_with("https:") || u.starts_with("data:")
    }) {
        Input::Arg(url.clone())
    } else if let Some(path) = info.local_path.as_ref().filter(|p| p.is_file()) {
        Input::Arg(path.to_string_lossy().into_owned())
    } else {
        Input::Stdin(data)
    };

    if opts.keep_data_uris {
        cmd.arg("--keep-data-uris");
    }
    match &input {
        Input::Arg(src) => {
            cmd.arg(src);
            cmd.stdin(Stdio::null());
        }
        Input::Stdin(_) => {
            if let Some(ext) = &info.extension {
                cmd.arg("-x").arg(ext);
            }
            if let Some(mt) = &info.mimetype {
                cmd.arg("-m").arg(mt);
            }
            cmd.stdin(Stdio::piped());
        }
    }
    cmd.stdout(Stdio::piped()).stderr(Stdio::piped());

    let mut child = cmd
        .spawn()
        .map_err(|e| ConvertError::conversion("python-engine", format!("spawn failed: {e}")))?;

    // Feed stdin from a separate thread: writing the input and draining the
    // output concurrently is the only deadlock-free shape when both pipes
    // can fill up.
    let writer = match input {
        Input::Stdin(bytes) => {
            let mut stdin = child.stdin.take().expect("stdin piped");
            let payload = bytes.to_vec();
            Some(std::thread::spawn(move || {
                let _ = stdin.write_all(&payload);
                // stdin drops here, closing the pipe so the child sees EOF.
            }))
        }
        Input::Arg(_) => None,
    };

    let out = wait_with_timeout(child, timeout())?;
    if let Some(w) = writer {
        let _ = w.join();
    }

    if !out.status.success() {
        return Err(ConvertError::conversion(
            "python-engine",
            format!(
                "exit {}: {}",
                out.status,
                String::from_utf8_lossy(&out.stderr).trim()
            ),
        ));
    }
    Ok(ConvertResult::new(String::from_utf8_lossy(&out.stdout).into_owned()))
}

/// Drain the child's pipes on a worker thread and enforce a wall-clock
/// timeout; the child is killed when it expires so a hung Python process can
/// never wedge a batch job.
fn wait_with_timeout(
    mut child: std::process::Child,
    limit: std::time::Duration,
) -> Result<std::process::Output, ConvertError> {
    use std::sync::mpsc;

    let (tx, rx) = mpsc::channel();
    // `wait_with_output` reads stdout/stderr to EOF, which only happens when
    // the child exits or is killed — so killing on timeout also unblocks
    // this thread.
    let stdout = child.stdout.take().expect("stdout piped");
    let stderr = child.stderr.take().expect("stderr piped");
    let drain = std::thread::spawn(move || {
        use std::io::Read;
        let mut out = Vec::new();
        let mut stdout = stdout;
        let mut stderr = stderr;
        let t = std::thread::spawn(move || {
            let mut v = Vec::new();
            let _ = stderr.read_to_end(&mut v);
            v
        });
        let _ = stdout.read_to_end(&mut out);
        let err = t.join().unwrap_or_default();
        let _ = tx.send((out, err));
    });

    let deadline = std::time::Instant::now() + limit;
    let status = loop {
        match child.try_wait() {
            Ok(Some(status)) => break status,
            Ok(None) => {
                if std::time::Instant::now() >= deadline {
                    let _ = child.kill();
                    let _ = child.wait();
                    // Do NOT join `drain` here: grandchildren (e.g. a shell's
                    // forked subprocess) may still hold the pipe's write end,
                    // so the reader could stay blocked long after the kill.
                    // The detached thread exits once the pipe finally closes.
                    drop(drain);
                    return Err(ConvertError::conversion(
                        "python-engine",
                        format!("timed out after {}s (set {PY_TIMEOUT_ENV} to adjust)", limit.as_secs()),
                    ));
                }
                std::thread::sleep(std::time::Duration::from_millis(25));
            }
            Err(e) => {
                return Err(ConvertError::conversion(
                    "python-engine",
                    format!("wait failed: {e}"),
                ))
            }
        }
    };
    // Bounded wait for the drained output; same grandchild caveat as above,
    // hence recv_timeout + detach instead of an unbounded join.
    let (stdout, stderr) = rx
        .recv_timeout(std::time::Duration::from_secs(5))
        .unwrap_or_default();
    drop(drain);
    Ok(std::process::Output {
        status,
        stdout,
        stderr,
    })
}
