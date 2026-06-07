//! The converter registry and conversion entry points.
//! Port of `packages/markitdown/src/markitdown/_markitdown.py`.

use crate::options::Engine;
use crate::{
    converter::Converter, converters, detect, python_engine, uri, ConvertError, ConvertOptions,
    ConvertResult, StreamInfo, PRIORITY_GENERIC, PRIORITY_SPECIFIC,
};
use std::path::Path;

struct Registration {
    priority: f32,
    converter: Box<dyn Converter>,
}

/// The main conversion engine: a prioritized list of [`Converter`]s.
pub struct MarkItDown {
    registrations: Vec<Registration>,
    options: ConvertOptions,
}

impl Default for MarkItDown {
    fn default() -> Self {
        Self::new()
    }
}

impl MarkItDown {
    /// Engine with all built-in converters and default options.
    pub fn new() -> Self {
        Self::with_options(ConvertOptions::default())
    }

    /// Engine with all built-in converters and the given options.
    pub fn with_options(options: ConvertOptions) -> Self {
        let mut md = MarkItDown {
            registrations: Vec::new(),
            options,
        };
        // Specific formats first (priority 0.0). Order within a priority
        // class is the trial order, so URL-gated converters precede the
        // formats whose extensions they share (.html, .xml).
        md.register(PRIORITY_SPECIFIC, Box::new(converters::WikipediaConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::BingSerpConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::YouTubeConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::RssConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::DocxConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::XlsxConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::XlsConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::PptxConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::PdfConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::EpubConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::IpynbConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::CsvConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::OutlookMsgConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::ImageConverter));
        md.register(PRIORITY_SPECIFIC, Box::new(converters::AudioConverter));
        // Generic fallbacks (priority 10.0).
        md.register(PRIORITY_GENERIC, Box::new(converters::ZipConverter));
        md.register(PRIORITY_GENERIC, Box::new(converters::HtmlConverter));
        md.register(PRIORITY_GENERIC, Box::new(converters::PlainTextConverter));
        md
    }

    /// Register an additional converter. Lower priority values are tried
    /// first; converters with equal priority run in registration order.
    pub fn register(&mut self, priority: f32, converter: Box<dyn Converter>) {
        self.registrations.push(Registration {
            priority,
            converter,
        });
        self.registrations
            .sort_by(|a, b| a.priority.total_cmp(&b.priority));
    }

    pub fn options(&self) -> &ConvertOptions {
        &self.options
    }

    /// Convert a local file.
    pub fn convert_path(&self, path: impl AsRef<Path>) -> Result<ConvertResult, ConvertError> {
        let (data, info) = uri::read_path(path.as_ref())?;
        self.convert_bytes(&data, info)
    }

    /// Convert a path or `file:` / `data:` / `http(s):` URI.
    pub fn convert_uri(&self, src: &str) -> Result<ConvertResult, ConvertError> {
        let (data, info) = uri::read_source(src)?;
        self.convert_bytes(&data, info)
    }

    /// Convert in-memory bytes, with whatever stream hints the caller has.
    pub fn convert_bytes(
        &self,
        data: &[u8],
        hints: StreamInfo,
    ) -> Result<ConvertResult, ConvertError> {
        let info = detect::enrich(data, hints);

        match self.options.engine {
            Engine::Python => python_engine::convert_with_python(data, &info, &self.options),
            Engine::Rust => self.convert_rust(data, &info),
            Engine::Auto => {
                let rust_result = self.convert_rust(data, &info);
                // Fall back when Rust failed outright, produced nothing but
                // advisory comments (e.g. a scanned PDF), or flagged a known
                // fidelity gap (DOCX comments/equations, RTF-only .msg body,
                // missing transcript/OCR, …).
                let needs_fallback = match &rust_result {
                    Ok(r) => r.degraded || is_effectively_empty(&r.markdown),
                    Err(_) => true,
                };
                if needs_fallback && python_engine::python_engine_available(&self.options) {
                    match python_engine::convert_with_python(data, &info, &self.options) {
                        // Only adopt the Python output when it actually adds
                        // content; a degraded-but-useful Rust result beats an
                        // empty Python one (e.g. Python built without the
                        // needed extras).
                        Ok(py) if !is_effectively_empty(&py.markdown) => Ok(py),
                        _ => rust_result,
                    }
                } else {
                    rust_result
                }
            }
        }
    }

    fn convert_rust(&self, data: &[u8], info: &StreamInfo) -> Result<ConvertResult, ConvertError> {
        let mut last_err: Option<ConvertError> = None;
        let mut any_accepted = false;
        for reg in &self.registrations {
            if !reg.converter.accepts(info, data) {
                continue;
            }
            any_accepted = true;
            match reg.converter.convert(data, info, &self.options) {
                Ok(result) => return Ok(result),
                Err(e) => last_err = Some(e),
            }
        }
        if any_accepted {
            Err(last_err.expect("accepted converter recorded an error"))
        } else {
            Err(ConvertError::UnsupportedFormat(describe(info)))
        }
    }
}

/// True when the markdown contains no real content — only whitespace and/or
/// HTML comments (advisory notes emitted by converters).
fn is_effectively_empty(markdown: &str) -> bool {
    let mut rest = markdown.trim();
    while let Some(open) = rest.find("<!--") {
        if !rest[..open].trim().is_empty() {
            return false;
        }
        match rest[open..].find("-->") {
            Some(close) => rest = rest[open + close + 3..].trim_start(),
            None => return rest[..open].trim().is_empty(),
        }
    }
    rest.trim().is_empty()
}

fn describe(info: &StreamInfo) -> Option<String> {
    match (&info.extension, &info.mimetype) {
        (Some(e), Some(m)) => Some(format!("{e}, {m}")),
        (Some(e), None) => Some(e.clone()),
        (None, Some(m)) => Some(m.clone()),
        (None, None) => None,
    }
}

/// A supported input format, for `--list-formats`, the MCP
/// `list_supported_formats` tool and the desktop app.
#[derive(Debug, Clone, serde::Serialize)]
pub struct FormatInfo {
    pub name: &'static str,
    pub extensions: &'static [&'static str],
    pub notes: &'static str,
}

pub const SUPPORTED_FORMATS: &[FormatInfo] = &[
    FormatInfo { name: "PDF", extensions: &[".pdf"], notes: "text extraction; scanned PDFs need the optional Python engine (OCR)" },
    FormatInfo { name: "Word", extensions: &[".docx"], notes: "headings, tables, lists, hyperlinks" },
    FormatInfo { name: "Excel", extensions: &[".xlsx", ".xls"], notes: "each sheet becomes a Markdown table" },
    FormatInfo { name: "PowerPoint", extensions: &[".pptx"], notes: "slide text, tables, notes" },
    FormatInfo { name: "HTML", extensions: &[".html", ".htm", ".xhtml"], notes: "incl. Wikipedia / Bing SERP / YouTube specializations" },
    FormatInfo { name: "CSV", extensions: &[".csv"], notes: "charset auto-detected, rendered as a table" },
    FormatInfo { name: "Jupyter", extensions: &[".ipynb"], notes: "markdown + code cells" },
    FormatInfo { name: "EPUB", extensions: &[".epub"], notes: "metadata + chapters in spine order" },
    FormatInfo { name: "ZIP", extensions: &[".zip"], notes: "recursively converts contained files" },
    FormatInfo { name: "Outlook email", extensions: &[".msg"], notes: "headers + plain-text body" },
    FormatInfo { name: "RSS/Atom", extensions: &[".rss", ".atom", ".xml"], notes: "feed items as sections" },
    FormatInfo { name: "Images", extensions: &[".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff"], notes: "EXIF metadata + dimensions (no OCR)" },
    FormatInfo { name: "Audio", extensions: &[".mp3", ".m4a", ".wav", ".flac"], notes: "tags + duration (no transcription)" },
    FormatInfo { name: "Text / Markdown / JSON", extensions: &[".txt", ".md", ".markdown", ".json", ".jsonl"], notes: "charset auto-detected" },
];
