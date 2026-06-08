//! markitdown-core — a pure-Rust port of Microsoft MarkItDown.
//!
//! Converts files and URIs (PDF, DOCX, XLSX/XLS, PPTX, HTML, CSV, EPUB, ZIP,
//! Jupyter notebooks, Outlook .msg, RSS/Atom, images, audio, Wikipedia/Bing/
//! YouTube pages, plain text) into clean Markdown suitable for LLM consumption.
//!
//! Architecture mirrors the Python implementation in
//! `packages/markitdown/src/markitdown/_markitdown.py`: a prioritized registry
//! of [`Converter`]s, each deciding via [`Converter::accepts`] whether it can
//! handle a stream described by [`StreamInfo`].
//!
//! ```no_run
//! use markitdown_core::MarkItDown;
//!
//! let md = MarkItDown::new();
//! let result = md.convert_path("report.pdf").unwrap();
//! println!("{}", result.markdown);
//! ```

mod capabilities;
mod converter;
mod detect;
mod error;
mod llm_caption;
mod llm_providers;
mod markitdown;
mod options;
mod python_engine;
mod result;
mod stream_info;
mod text;
mod uri;

pub mod converters;

pub use capabilities::{capabilities, Capabilities};
pub use converter::Converter;
pub use error::ConvertError;
pub use markitdown::{FormatInfo, MarkItDown, SUPPORTED_FORMATS};
pub use llm_caption::available as llm_caption_available;
pub use llm_providers::{provider as llm_provider, LlmProvider, LLM_PROVIDERS};
pub use options::{ConvertOptions, Engine, LlmConfig};
pub use python_engine::python_engine_available;
pub use result::ConvertResult;
pub use stream_info::StreamInfo;

/// Converters for specific file formats (tried first). Same constant as Python.
pub const PRIORITY_SPECIFIC: f32 = 0.0;
/// Generic / fallback converters such as plain text and HTML (tried last).
pub const PRIORITY_GENERIC: f32 = 10.0;
