//! PDF → Markdown converter.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_pdf_converter.py`.
//!
//! DEVIATION FROM PYTHON: the Python converter uses pdfminer for linear text
//! extraction *plus* pdfplumber word-position heuristics to reconstruct
//! borderless tables/forms into aligned Markdown tables. We deliberately SKIP
//! the table-reconstruction pass — there is no pure-Rust equivalent of
//! pdfplumber's layout analysis — and emit only linearized text via
//! `pdf_extract::extract_text_from_mem`, which mirrors pdfminer's behavior.
//!
//! `pdf-extract` can panic on malformed PDFs, so the extraction call is wrapped
//! in `catch_unwind` and any panic is mapped to a `FileConversion` error.
//!
//! When extraction yields only whitespace the PDF is almost certainly scanned /
//! image-only. We then return Ok with an HTML comment noting OCR requires the
//! optional Python engine; the empty-ish (whitespace-only) markdown trips the
//! Auto-engine fallback upstream (`markdown.trim().is_empty()`).

use crate::{ConvertError, ConvertOptions, ConvertResult, Converter, StreamInfo};
use std::panic::{catch_unwind, AssertUnwindSafe};

pub struct PdfConverter;

const ACCEPTED_EXTENSIONS: &[&str] = &[".pdf"];
const ACCEPTED_MIMETYPES: &[&str] = &["application/pdf", "application/x-pdf"];

/// Collapse 3+ consecutive newlines down to exactly 2.
fn normalize_newlines(text: &str) -> String {
    let mut out = String::with_capacity(text.len());
    let mut newline_run = 0usize;
    for ch in text.chars() {
        if ch == '\n' {
            newline_run += 1;
            if newline_run <= 2 {
                out.push('\n');
            }
        } else if ch == '\r' {
            // normalize away bare CRs; the following \n (if any) is handled above
            continue;
        } else {
            newline_run = 0;
            out.push(ch);
        }
    }
    out
}

impl Converter for PdfConverter {
    fn name(&self) -> &'static str {
        "pdf"
    }

    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_EXTENSIONS) || info.mimetype_is(ACCEPTED_MIMETYPES) {
            return true;
        }
        // Magic-byte sanity check: PDFs start with "%PDF-".
        data.starts_with(b"%PDF-")
    }

    fn convert(
        &self,
        data: &[u8],
        _info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        // pdf-extract may panic on malformed input; isolate it.
        let extracted = catch_unwind(AssertUnwindSafe(|| {
            pdf_extract::extract_text_from_mem(data)
        }));

        let text = match extracted {
            Ok(Ok(text)) => text,
            Ok(Err(e)) => {
                return Err(ConvertError::conversion(
                    "pdf",
                    format!("failed to extract text from PDF: {e}"),
                ))
            }
            Err(_) => {
                return Err(ConvertError::conversion(
                    "pdf",
                    "pdf-extract panicked while parsing the document (malformed PDF)",
                ))
            }
        };

        if text.trim().is_empty() {
            // Scanned / image-only PDF. Return whitespace-only markdown (an HTML
            // comment) so the Auto engine can fall back to the Python OCR path.
            let note = "<!-- This PDF appears to be scanned or image-only; no text \
                        layer was found. OCR requires the optional Python engine \
                        (set MARKITDOWN_PY_BIN). -->";
            return Ok(ConvertResult::new(note).with_degraded());
        }

        Ok(ConvertResult::new(normalize_newlines(&text)))
    }
}
