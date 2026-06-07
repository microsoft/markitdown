//! Jupyter Notebook (.ipynb) → Markdown converter.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_ipynb_converter.py`.
//! Markdown cells are emitted verbatim, code cells as ```python fenced blocks,
//! raw cells as bare fenced blocks; cells are joined by a blank line. The title
//! is the first `# ` heading (overridden by `metadata.title` when present).
//!
//! Note: the Python reference always labels code-cell fences `python` regardless
//! of the notebook's declared language, so this port does the same for parity.

use serde_json::Value;

use crate::text::decode_text;
use crate::{ConvertError, ConvertOptions, ConvertResult, Converter, StreamInfo};

const CANDIDATE_MIME_TYPE_PREFIXES: &[&str] = &["application/json"];
const ACCEPTED_FILE_EXTENSIONS: &[&str] = &[".ipynb"];

pub struct IpynbConverter;

/// Join an ipynb cell `source`, which is either a list of line strings or a
/// single string, into one string.
fn join_source(source: &Value) -> String {
    match source {
        Value::Array(lines) => lines
            .iter()
            .filter_map(|l| l.as_str())
            .collect::<String>(),
        Value::String(s) => s.clone(),
        _ => String::new(),
    }
}

impl Converter for IpynbConverter {
    fn name(&self) -> &'static str {
        "ipynb"
    }

    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_FILE_EXTENSIONS) {
            return true;
        }
        // For application/json streams, peek at the content to confirm it really
        // is a notebook (matches the Python "nbformat"/"nbformat_minor" check).
        if let Some(mt) = &info.mimetype {
            let mt = mt.split(';').next().unwrap_or(mt).trim().to_ascii_lowercase();
            if CANDIDATE_MIME_TYPE_PREFIXES
                .iter()
                .any(|p| mt.starts_with(p))
            {
                let content = decode_text(data, info);
                return content.contains("nbformat") && content.contains("nbformat_minor");
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
        let notebook: Value = serde_json::from_str(&content)
            .map_err(|e| ConvertError::conversion("ipynb", e.to_string()))?;

        let mut blocks: Vec<String> = Vec::new();
        let mut title: Option<String> = None;

        if let Some(cells) = notebook.get("cells").and_then(Value::as_array) {
            for cell in cells {
                let cell_type = cell.get("cell_type").and_then(Value::as_str).unwrap_or("");
                let source = cell.get("source").cloned().unwrap_or(Value::Null);
                let src = join_source(&source);

                match cell_type {
                    "markdown" => {
                        // Extract the first `# ` heading as title if not found yet.
                        if title.is_none() {
                            if let Value::Array(lines) = &source {
                                for line in lines.iter().filter_map(|l| l.as_str()) {
                                    if let Some(rest) = line.strip_prefix("# ") {
                                        title = Some(
                                            rest.trim_start_matches(['#', ' ']).trim().to_string(),
                                        );
                                        break;
                                    }
                                }
                            } else if let Value::String(s) = &source {
                                if let Some(rest) = s.strip_prefix("# ") {
                                    title =
                                        Some(rest.trim_start_matches(['#', ' ']).trim().to_string());
                                }
                            }
                        }
                        blocks.push(src);
                    }
                    "code" => blocks.push(format!("```python\n{src}\n```")),
                    "raw" => blocks.push(format!("```\n{src}\n```")),
                    _ => {}
                }
            }
        }

        let md_text = blocks.join("\n\n");

        // metadata.title overrides the extracted heading when present.
        if let Some(meta_title) = notebook
            .get("metadata")
            .and_then(|m| m.get("title"))
            .and_then(Value::as_str)
        {
            title = Some(meta_title.to_string());
        }

        let mut result = ConvertResult::new(md_text);
        if let Some(t) = title {
            result = result.with_title(t);
        }
        Ok(result)
    }
}
