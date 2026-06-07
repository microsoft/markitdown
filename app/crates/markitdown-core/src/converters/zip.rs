//! ZIP → Markdown converter.
//!
//! Port of `_zip_converter.py`. Iterates the archive entries, recursively
//! converting each via a fresh [`crate::MarkItDown`] instance, and emits the
//! results under `## File: <name>` sections. Directories are skipped; per-file
//! failures append an error note rather than aborting the whole archive.
//!
//! Recursion (zips inside zips) is bounded by a thread-local depth counter
//! (max depth 4). The `MarkItDown` engine is constructed lazily *inside*
//! `convert` to avoid constructor recursion, since the registry itself creates
//! a `ZipConverter`.

use std::cell::Cell;
use std::io::Read;

use crate::{Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};

const ACCEPTED_EXTENSIONS: &[&str] = &[".zip"];
const ACCEPTED_MIME_PREFIXES: &[&str] = &["application/zip"];
const MAX_DEPTH: u32 = 4;

thread_local! {
    static DEPTH: Cell<u32> = const { Cell::new(0) };
}

pub struct ZipConverter;

impl Converter for ZipConverter {
    fn name(&self) -> &'static str {
        "zip"
    }

    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_EXTENSIONS) {
            return data.starts_with(b"PK");
        }
        if let Some(mt) = &info.mimetype {
            let mt = mt.split(';').next().unwrap_or(mt).trim();
            if ACCEPTED_MIME_PREFIXES.iter().any(|p| mt.starts_with(p)) {
                return data.starts_with(b"PK");
            }
        }
        false
    }

    fn convert(
        &self,
        data: &[u8],
        info: &StreamInfo,
        opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let label = info
            .url
            .clone()
            .or_else(|| info.local_path.as_ref().map(|p| p.display().to_string()))
            .or_else(|| info.filename.clone())
            .unwrap_or_else(|| "archive.zip".to_string());

        let mut md = format!("Content from the zip file `{label}`:\n\n");

        let depth = DEPTH.with(|d| d.get());
        if depth >= MAX_DEPTH {
            md.push_str("> Maximum archive recursion depth reached; contents not expanded.\n");
            return Ok(ConvertResult::new(md.trim().to_string()));
        }

        let mut zip = zip::ZipArchive::new(std::io::Cursor::new(data))
            .map_err(|e| ConvertError::conversion("zip", format!("not a valid zip: {e}")))?;

        // Build a fresh engine lazily, mirroring Python's recursive use of a
        // MarkItDown instance for the inner files.
        let engine = crate::MarkItDown::with_options(opts.clone());

        let names: Vec<String> = (0..zip.len())
            .filter_map(|i| zip.by_index(i).ok().map(|f| f.name().to_string()))
            .collect();
        let mut degraded = false;

        for name in names {
            // Skip directory entries.
            if name.ends_with('/') {
                continue;
            }
            let mut bytes = Vec::new();
            {
                let mut file = match zip.by_name(&name) {
                    Ok(f) => f,
                    Err(_) => continue,
                };
                if file.is_dir() {
                    continue;
                }
                if file.read_to_end(&mut bytes).is_err() {
                    md.push_str(&format!("## File: {name}\n\n> Failed to read entry.\n\n"));
                    continue;
                }
            }

            let ext = std::path::Path::new(&name)
                .extension()
                .and_then(|e| e.to_str())
                .map(|e| format!(".{e}"));
            let basename = std::path::Path::new(&name)
                .file_name()
                .and_then(|n| n.to_str())
                .unwrap_or(&name);

            let mut hints = StreamInfo::new().with_filename(basename);
            if let Some(e) = &ext {
                hints = hints.with_extension(e);
            }

            DEPTH.with(|d| d.set(depth + 1));
            let result = engine.convert_bytes(&bytes, hints);
            DEPTH.with(|d| d.set(depth));

            match result {
                Ok(r) => {
                    md.push_str(&format!("## File: {name}\n\n"));
                    md.push_str(r.markdown.trim());
                    md.push_str("\n\n");
                    // Children inherit our options and may already have
                    // fallen back individually; if one is still degraded
                    // (e.g. scanned PDF, no Python engine), surface it so
                    // Engine::Auto can retry the whole archive.
                    degraded |= r.degraded;
                }
                Err(_) => {
                    // Mirror Python: unsupported / failed inner files are
                    // silently skipped (no section emitted) — but flag the
                    // archive so a configured Python engine gets a shot at
                    // formats this port can't read.
                    degraded = true;
                }
            }
        }

        let mut result = ConvertResult::new(md.trim().to_string());
        if degraded {
            result = result.with_degraded();
        }
        Ok(result)
    }
}
