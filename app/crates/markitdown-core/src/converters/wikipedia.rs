//! Wikipedia page converter. Port of `_wikipedia_converter.py`.
//!
//! Accepts HTML only when the source URL is a Wikipedia article, then renders
//! just the `#mw-content-text` main column, prefixed with the page title.
use super::html::{extract_title_doc, fragment_to_markdown};
use crate::{text::decode_text, Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};
use scraper::{Html, Selector};

const ACCEPTED_MIME_PREFIXES: &[&str] = &["text/html", "application/xhtml"];
const ACCEPTED_EXTENSIONS: &[&str] = &[".html", ".htm"];

pub struct WikipediaConverter;

/// Match the Python regex `^https?://[a-zA-Z]{2,3}\.wikipedia.org/` without a
/// regex crate.
fn is_wikipedia_url(url: &str) -> bool {
    let rest = if let Some(r) = url.strip_prefix("https://") {
        r
    } else if let Some(r) = url.strip_prefix("http://") {
        r
    } else {
        return false;
    };
    // <lang>.wikipedia.org/ where lang is 2-3 ASCII letters.
    let host_end = match rest.find('/') {
        Some(i) => i,
        None => return false,
    };
    let host = &rest[..host_end];
    let lang = match host.strip_suffix(".wikipedia.org") {
        Some(l) => l,
        None => return false,
    };
    (2..=3).contains(&lang.len()) && lang.bytes().all(|b| b.is_ascii_alphabetic())
}

impl Converter for WikipediaConverter {
    fn name(&self) -> &'static str {
        "wikipedia"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        let url = info.url.as_deref().unwrap_or("");
        if !is_wikipedia_url(url) {
            return false;
        }
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
        let doc = Html::parse_document(&html);

        let content_sel = Selector::parse("#mw-content-text")
            .map_err(|e| ConvertError::conversion("wikipedia", e.to_string()))?;
        let title_sel = Selector::parse("span.mw-page-title-main")
            .map_err(|e| ConvertError::conversion("wikipedia", e.to_string()))?;

        // Default title from <title>, overridden by the page-title span.
        let mut main_title = extract_title_doc(&doc);
        if let Some(t) = doc.select(&title_sel).next() {
            let txt: String = t.text().collect();
            let txt = txt.trim();
            if !txt.is_empty() {
                main_title = Some(txt.to_string());
            }
        }

        let markdown = match doc.select(&content_sel).next() {
            Some(content) => {
                let inner = content.inner_html();
                let body = fragment_to_markdown(&inner, opts.keep_data_uris);
                let title_str = main_title.clone().unwrap_or_default();
                format!("# {title_str}\n\n{body}")
            }
            None => fragment_to_markdown(&html, opts.keep_data_uris),
        };

        let mut result = ConvertResult::new(markdown);
        if let Some(t) = main_title {
            result = result.with_title(t);
        }
        Ok(result)
    }
}

#[cfg(test)]
mod tests {
    use super::is_wikipedia_url;

    #[test]
    fn url_matching() {
        assert!(is_wikipedia_url("https://en.wikipedia.org/wiki/Microsoft"));
        assert!(is_wikipedia_url("http://de.wikipedia.org/wiki/Foo"));
        assert!(is_wikipedia_url("https://www.wikipedia.org/")); // 3-letter "www"
        assert!(!is_wikipedia_url("https://example.com/wiki/Microsoft"));
        assert!(!is_wikipedia_url("https://wikipedia.org/wiki/Foo")); // no lang
        assert!(!is_wikipedia_url(""));
    }
}
