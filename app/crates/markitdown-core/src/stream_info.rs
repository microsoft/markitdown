use std::path::PathBuf;

/// Everything we know (or can guess) about an input stream.
///
/// Port of `packages/markitdown/src/markitdown/_stream_info.py`. Hints flow
/// from the caller (CLI flags, HTTP headers, file name) and are enriched by
/// magic-byte / charset detection in [`crate::detect`].
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct StreamInfo {
    /// IANA media type, e.g. `application/pdf`.
    pub mimetype: Option<String>,
    /// Lower-case extension *with* leading dot, e.g. `.pdf`.
    pub extension: Option<String>,
    /// Text charset label understood by `encoding_rs`, e.g. `utf-8`, `shift_jis`.
    pub charset: Option<String>,
    /// Bare file name, e.g. `report.pdf`.
    pub filename: Option<String>,
    /// Path on disk, when the stream came from a local file.
    pub local_path: Option<PathBuf>,
    /// Source URL, when the stream came from http(s)/file/data URIs.
    pub url: Option<String>,
}

impl StreamInfo {
    /// New empty info; fill in fields with the builder-style helpers.
    pub fn new() -> Self {
        Self::default()
    }

    pub fn with_extension(mut self, ext: &str) -> Self {
        self.extension = Some(normalize_extension(ext));
        self
    }

    pub fn with_mimetype(mut self, mt: &str) -> Self {
        self.mimetype = Some(mt.trim().to_ascii_lowercase());
        self
    }

    pub fn with_charset(mut self, cs: &str) -> Self {
        self.charset = Some(cs.trim().to_ascii_lowercase());
        self
    }

    pub fn with_filename(mut self, name: &str) -> Self {
        self.filename = Some(name.to_string());
        self
    }

    pub fn with_url(mut self, url: &str) -> Self {
        self.url = Some(url.to_string());
        self
    }

    /// True when the mimetype equals `exact` or starts with `prefix/`-style
    /// patterns. Parameters use full mimetypes like `application/pdf`.
    pub fn mimetype_is(&self, candidates: &[&str]) -> bool {
        match &self.mimetype {
            Some(mt) => {
                // Strip any `; charset=...` parameters before comparing.
                let mt = mt.split(';').next().unwrap_or(mt).trim();
                candidates.iter().any(|c| mt.eq_ignore_ascii_case(c))
            }
            None => false,
        }
    }

    /// True when the extension matches one of `candidates` (given with dots).
    pub fn extension_is(&self, candidates: &[&str]) -> bool {
        match &self.extension {
            Some(ext) => candidates.iter().any(|c| ext.eq_ignore_ascii_case(c)),
            None => false,
        }
    }
}

/// Normalize `pdf` / `.PDF` / ` .pdf ` → `.pdf`.
pub fn normalize_extension(ext: &str) -> String {
    let e = ext.trim().trim_start_matches('.').to_ascii_lowercase();
    format!(".{e}")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn extension_normalization() {
        assert_eq!(normalize_extension("PDF"), ".pdf");
        assert_eq!(normalize_extension(".pdf"), ".pdf");
        assert_eq!(normalize_extension(" .Md "), ".md");
    }

    #[test]
    fn mimetype_matching_ignores_params() {
        let info = StreamInfo::new().with_mimetype("text/html; charset=utf-8");
        assert!(info.mimetype_is(&["text/html"]));
        assert!(!info.mimetype_is(&["text/plain"]));
    }
}
