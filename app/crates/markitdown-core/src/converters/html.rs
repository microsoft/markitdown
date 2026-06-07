//! HTML → Markdown converter. Port of `_html_converter.py` / `_markdownify.py`.
use crate::{text::decode_text, Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};
use htmd::HtmlToMarkdown;
use scraper::{Html, Selector};

const ACCEPTED_MIME_PREFIXES: &[&str] = &["text/html", "application/xhtml"];
const ACCEPTED_EXTENSIONS: &[&str] = &[".html", ".htm", ".xhtml"];

pub struct HtmlConverter;

impl Converter for HtmlConverter {
    fn name(&self) -> &'static str {
        "html"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_EXTENSIONS) {
            return true;
        }
        if let Some(mt) = &info.mimetype {
            let mt = mt.split(';').next().unwrap_or(mt).trim().to_ascii_lowercase();
            if ACCEPTED_MIME_PREFIXES.iter().any(|p| mt.starts_with(p)) {
                return true;
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
        let html = decode_text(data, info);
        let (markdown, title) = html_to_markdown(&html, opts.keep_data_uris);
        let mut result = ConvertResult::new(markdown);
        if let Some(t) = title {
            result = result.with_title(t);
        }
        Ok(result)
    }
}

/// Convert an HTML document (or fragment) to Markdown, returning the Markdown
/// body and the `<title>` text when present.
///
/// Mirrors the Python `_CustomMarkdownify` pipeline: strip `script`/`style`,
/// render the `<body>` (or the whole document when there is no body) to
/// Markdown, and—unless `keep_data_uris`—truncate long `data:` URIs.
///
/// Shared by the Wikipedia / Bing / YouTube / RSS converters (and, later, EPUB).
pub(crate) fn html_to_markdown(html: &str, keep_data_uris: bool) -> (String, Option<String>) {
    let title = extract_title(html);
    let markdown = render_fragment(html, keep_data_uris);
    (markdown, title)
}

/// Render an arbitrary HTML fragment to Markdown (no `<title>` extraction).
/// Used by converters that pass in an already-selected DOM subtree's inner HTML.
pub(crate) fn fragment_to_markdown(html: &str, keep_data_uris: bool) -> String {
    render_fragment(html, keep_data_uris)
}

fn render_fragment(html: &str, keep_data_uris: bool) -> String {
    let converter = HtmlToMarkdown::builder()
        .skip_tags(vec!["script", "style"])
        .build();
    let md = converter.convert(html).unwrap_or_default();
    let md = md.trim().to_string();
    if keep_data_uris {
        md
    } else {
        truncate_data_uris(&md)
    }
}

/// Extract the textual content of the first `<title>` element, if any.
fn extract_title(html: &str) -> Option<String> {
    let doc = Html::parse_document(html);
    extract_title_doc(&doc)
}

/// Extract the `<title>` text from an already-parsed document.
pub(crate) fn extract_title_doc(doc: &Html) -> Option<String> {
    let sel = Selector::parse("title").ok()?;
    let el = doc.select(&sel).next()?;
    let text: String = el.text().collect();
    let text = text.trim();
    if text.is_empty() {
        None
    } else {
        Some(text.to_string())
    }
}

/// Replicate Python's `src.split(",")[0] + "..."` truncation for `data:` URIs.
///
/// We scan the rendered Markdown for `data:` substrings and, when one is
/// followed by a comma, drop everything from the comma onward, replacing it
/// with `...`. This keeps the mime/encoding prefix (e.g. `data:image/png;base64`)
/// and appends `...` exactly as the Python converter does.
fn truncate_data_uris(md: &str) -> String {
    let bytes = md.as_bytes();
    let mut out = String::with_capacity(md.len());
    let mut i = 0;
    while i < bytes.len() {
        if md[i..].starts_with("data:") {
            // Find the end of the data URI payload. In Markdown the URI is
            // bounded by `)`, whitespace, or a quote (for titles).
            let mut j = i;
            let mut comma: Option<usize> = None;
            while j < bytes.len() {
                let c = bytes[j];
                if c == b')' || c == b'"' || c == b'\'' || c.is_ascii_whitespace() {
                    break;
                }
                if c == b',' && comma.is_none() {
                    comma = Some(j);
                }
                j += 1;
            }
            match comma {
                Some(cidx) => {
                    out.push_str(&md[i..cidx]);
                    out.push_str("...");
                }
                None => out.push_str(&md[i..j]),
            }
            i = j;
        } else {
            // Advance one UTF-8 char.
            let ch = md[i..].chars().next().unwrap();
            out.push(ch);
            i += ch.len_utf8();
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn truncates_data_uri_when_not_kept() {
        let html = r#"<html><body><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC" alt="x"></body></html>"#;
        let (md, _) = html_to_markdown(html, false);
        assert!(md.contains("data:image/png;base64..."), "got: {md}");
        assert!(!md.contains("iVBORw0KGgo"), "payload should be gone: {md}");
    }

    #[test]
    fn keeps_data_uri_when_requested() {
        let html = r#"<html><body><img src="data:image/png;base64,iVBORw0KGgoAAAANSU" alt="x"></body></html>"#;
        let (md, _) = html_to_markdown(html, true);
        assert!(md.contains("data:image/png;base64,iVBORw0KGgoAAAANSU"), "got: {md}");
    }

    #[test]
    fn extracts_title() {
        let html = "<html><head><title>Hello World</title></head><body><p>hi</p></body></html>";
        let (_, title) = html_to_markdown(html, false);
        assert_eq!(title.as_deref(), Some("Hello World"));
    }
}
