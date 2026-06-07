use thiserror::Error;

/// Errors produced while converting a stream to Markdown.
///
/// Mirrors `packages/markitdown/src/markitdown/_exceptions.py`.
#[derive(Debug, Error)]
pub enum ConvertError {
    /// No registered converter accepted the stream.
    #[error("unsupported format{}: could not convert stream to Markdown", fmt_ctx(.0))]
    UnsupportedFormat(Option<String>),

    /// One or more converters accepted the stream but every attempt failed.
    #[error("conversion failed ({converter}): {message}")]
    FileConversion {
        converter: &'static str,
        message: String,
    },

    /// The input itself was invalid (bad URI, undecodable data URI, …).
    #[error("invalid input: {0}")]
    InvalidInput(String),

    #[error("i/o error: {0}")]
    Io(#[from] std::io::Error),

    /// Network failure while fetching an http(s) input.
    #[error("network error: {0}")]
    Network(String),

    /// A feature that needs the optional Python engine (OCR, transcription)
    /// was requested but `MARKITDOWN_PY_BIN` is not configured / not found.
    #[error("missing dependency: {0}")]
    MissingDependency(String),
}

fn fmt_ctx(ctx: &Option<String>) -> String {
    match ctx {
        Some(c) => format!(" ({c})"),
        None => String::new(),
    }
}

impl ConvertError {
    /// Convenience constructor used by converters.
    pub fn conversion(converter: &'static str, message: impl Into<String>) -> Self {
        ConvertError::FileConversion {
            converter,
            message: message.into(),
        }
    }
}
