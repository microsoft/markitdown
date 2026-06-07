/// The result of a successful conversion.
///
/// Port of Python's `DocumentConverterResult`.
#[derive(Debug, Clone, Default, serde::Serialize)]
pub struct ConvertResult {
    /// The converted Markdown text.
    pub markdown: String,
    /// Document title, when one could be extracted (HTML `<title>`, EPUB
    /// metadata, first notebook heading, …).
    pub title: Option<String>,
    /// True when the converter hit a known fidelity gap of the pure-Rust
    /// engine (scanned PDF, DOCX comments/equations, RTF-only .msg body,
    /// missing transcript/OCR, …). [`crate::Engine::Auto`] uses this to
    /// decide whether the optional Python engine could do better; the result
    /// is still valid on its own.
    #[serde(skip_serializing_if = "std::ops::Not::not")]
    pub degraded: bool,
}

impl ConvertResult {
    pub fn new(markdown: impl Into<String>) -> Self {
        Self {
            markdown: markdown.into(),
            title: None,
            degraded: false,
        }
    }

    /// Mark this result as degraded (see the field docs).
    pub fn with_degraded(mut self) -> Self {
        self.degraded = true;
        self
    }

    pub fn with_title(mut self, title: impl Into<String>) -> Self {
        let t = title.into();
        if !t.trim().is_empty() {
            self.title = Some(t);
        }
        self
    }
}
