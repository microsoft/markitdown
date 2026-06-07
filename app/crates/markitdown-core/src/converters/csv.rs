//! CSV → Markdown table converter.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_csv_converter.py`.
//! Charset is auto-detected (honoring an explicit hint) via [`crate::text::decode_text`],
//! then parsed with the `csv` crate and rendered as a single GFM table whose first
//! row is the header.

use crate::text::{decode_text, rows_to_markdown_table};
use crate::{ConvertError, ConvertOptions, ConvertResult, Converter, StreamInfo};

const ACCEPTED_MIME_TYPE_PREFIXES: &[&str] = &["text/csv", "application/csv"];
const ACCEPTED_FILE_EXTENSIONS: &[&str] = &[".csv"];

pub struct CsvConverter;

impl Converter for CsvConverter {
    fn name(&self) -> &'static str {
        "csv"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_FILE_EXTENSIONS) {
            return true;
        }
        // Python matches on a mimetype *prefix* (e.g. "text/csv; charset=utf-8").
        if let Some(mt) = &info.mimetype {
            let mt = mt.split(';').next().unwrap_or(mt).trim().to_ascii_lowercase();
            if ACCEPTED_MIME_TYPE_PREFIXES
                .iter()
                .any(|p| mt.starts_with(p))
            {
                return true;
            }
        }
        false
    }

    fn convert(
        &self,
        data: &[u8],
        info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let content = decode_text(data, info);

        let mut reader = csv::ReaderBuilder::new()
            .has_headers(false)
            .flexible(true)
            .from_reader(content.as_bytes());

        let mut rows: Vec<Vec<String>> = Vec::new();
        for record in reader.records() {
            let record =
                record.map_err(|e| ConvertError::conversion("csv", e.to_string()))?;
            rows.push(record.iter().map(|f| f.to_string()).collect());
        }

        if rows.is_empty() {
            return Ok(ConvertResult::new(String::new()));
        }

        // rows_to_markdown_table emits the standard `| a | b |` GFM layout with the
        // first row as the header and pads short rows — matching the Python output.
        let md = rows_to_markdown_table(&rows);
        Ok(ConvertResult::new(md.trim_end().to_string()))
    }
}
