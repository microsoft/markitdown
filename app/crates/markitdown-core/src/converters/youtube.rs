//! YouTube watch-page converter. Port of `_youtube_converter.py`.
//!
//! Accepts HTML only when the source URL is a YouTube watch page. Extracts the
//! title, metadata (views / keywords / runtime) and description from meta tags
//! plus the embedded `ytInitialData` JSON. Transcripts are NOT supported.
use super::html::extract_title_doc;
use crate::{text::decode_text, Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};
use scraper::{Html, Selector};
use std::collections::HashMap;

pub struct YouTubeConverter;

impl Converter for YouTubeConverter {
    fn name(&self) -> &'static str {
        "youtube"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        let url = info.url.as_deref().unwrap_or("");
        // Mirror Python's unescaping of `\?` / `\=` before the prefix check.
        let url = url.replace("\\?", "?").replace("\\=", "=");
        url.starts_with("https://www.youtube.com/watch?")
    }

    fn convert(
        &self,
        data: &[u8],
        info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let html = decode_text(data, info);
        let doc = Html::parse_document(&html);

        let mut metadata: HashMap<String, String> = HashMap::new();

        // <title>
        if let Some(t) = extract_title_doc(&doc) {
            metadata.insert("title".to_string(), t);
        }

        // <meta> tags keyed by itemprop / property / name.
        if let Ok(meta_sel) = Selector::parse("meta") {
            for meta in doc.select(&meta_sel) {
                let attrs = meta.value();
                let content = match attrs.attr("content") {
                    Some(c) if !c.is_empty() => c,
                    _ => continue,
                };
                for key_attr in ["itemprop", "property", "name"] {
                    if let Some(key) = attrs.attr(key_attr) {
                        if !key.is_empty() {
                            metadata
                                .entry(key.to_string())
                                .or_insert_with(|| content.to_string());
                        }
                        break;
                    }
                }
            }
        }

        // Description from ytInitialData (best-effort).
        if !metadata.contains_key("description") {
            if let Some(desc) = description_from_yt_initial_data(&doc) {
                metadata.insert("description".to_string(), desc);
            }
        }

        // Build the page.
        let mut webpage_text = String::from("# YouTube\n");

        let title = get(&metadata, &["title", "og:title", "name"]).unwrap_or_default();
        if !title.is_empty() {
            webpage_text.push_str(&format!("\n## {title}\n"));
        }

        let mut stats = String::new();
        if let Some(views) = get(&metadata, &["interactionCount"]) {
            stats.push_str(&format!("- **Views:** {views}\n"));
        }
        if let Some(keywords) = get(&metadata, &["keywords"]) {
            stats.push_str(&format!("- **Keywords:** {keywords}\n"));
        }
        if let Some(runtime) = get(&metadata, &["duration"]) {
            stats.push_str(&format!("- **Runtime:** {runtime}\n"));
        }
        if !stats.is_empty() {
            webpage_text.push_str(&format!("\n### Video Metadata\n{stats}\n"));
        }

        if let Some(description) = get(&metadata, &["description", "og:description"]) {
            webpage_text.push_str(&format!("\n### Description\n{description}\n"));
        }

        // Transcripts are not supported by the pure-Rust port.
        webpage_text.push_str("\n<!-- Transcripts are not supported by the Rust port. -->\n");

        // Degraded: the Python engine (youtube-transcript-api extra) can add
        // the full video transcript, which this port does not fetch.
        let mut result = ConvertResult::new(webpage_text).with_degraded();
        if !title.is_empty() {
            result = result.with_title(title);
        }
        Ok(result)
    }
}

/// First non-empty metadata value matching any of `keys`.
fn get(metadata: &HashMap<String, String>, keys: &[&str]) -> Option<String> {
    for k in keys {
        if let Some(v) = metadata.get(*k) {
            if !v.is_empty() {
                return Some(v.clone());
            }
        }
    }
    None
}

/// Best-effort extraction of `attributedDescriptionBodyText.content` from the
/// embedded `ytInitialData` JSON inside a `<script>` tag.
fn description_from_yt_initial_data(doc: &Html) -> Option<String> {
    let script_sel = Selector::parse("script").ok()?;
    for script in doc.select(&script_sel) {
        let text: String = script.text().collect();
        if !text.contains("ytInitialData") {
            continue;
        }
        // Find `var ytInitialData = {...};` and parse the JSON object.
        let start = text.find("ytInitialData")?;
        let after = &text[start..];
        let brace = after.find('{')?;
        let json_str = balanced_json(&after[brace..])?;
        if let Ok(value) = serde_json::from_str::<serde_json::Value>(json_str) {
            if let Some(node) = find_key(&value, "attributedDescriptionBodyText") {
                if let Some(content) = node.get("content").and_then(|c| c.as_str()) {
                    return Some(content.to_string());
                }
            }
        }
        break;
    }
    None
}

/// Return the substring spanning a balanced `{...}` object starting at `s[0]`.
fn balanced_json(s: &str) -> Option<&str> {
    let bytes = s.as_bytes();
    if bytes.first() != Some(&b'{') {
        return None;
    }
    let mut depth = 0i32;
    let mut in_str = false;
    let mut escaped = false;
    for (i, &b) in bytes.iter().enumerate() {
        if in_str {
            if escaped {
                escaped = false;
            } else if b == b'\\' {
                escaped = true;
            } else if b == b'"' {
                in_str = false;
            }
            continue;
        }
        match b {
            b'"' => in_str = true,
            b'{' => depth += 1,
            b'}' => {
                depth -= 1;
                if depth == 0 {
                    return Some(&s[..=i]);
                }
            }
            _ => {}
        }
    }
    None
}

/// Recursively search a JSON value for the first object holding `key`.
fn find_key<'a>(value: &'a serde_json::Value, key: &str) -> Option<&'a serde_json::Value> {
    match value {
        serde_json::Value::Object(map) => {
            if let Some(v) = map.get(key) {
                return Some(v);
            }
            for v in map.values() {
                if let Some(found) = find_key(v, key) {
                    return Some(found);
                }
            }
            None
        }
        serde_json::Value::Array(arr) => {
            for v in arr {
                if let Some(found) = find_key(v, key) {
                    return Some(found);
                }
            }
            None
        }
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn balanced_object() {
        assert_eq!(balanced_json(r#"{"a":1}rest"#), Some(r#"{"a":1}"#));
        assert_eq!(balanced_json(r#"{"a":{"b":"}"}}x"#), Some(r#"{"a":{"b":"}"}}"#));
    }

    #[test]
    fn builds_page_from_meta() {
        let html = r#"<html><head>
            <title>My Video - YouTube</title>
            <meta property="og:title" content="My Video">
            <meta name="keywords" content="rust, test">
            <meta itemprop="duration" content="PT5M">
            <meta property="og:description" content="A great video.">
        </head><body></body></html>"#;
        let info = StreamInfo::new()
            .with_url("https://www.youtube.com/watch?v=abc")
            .with_extension(".html");
        let res = YouTubeConverter
            .convert(html.as_bytes(), &info, &ConvertOptions::default())
            .unwrap();
        assert!(res.markdown.contains("# YouTube"));
        assert!(res.markdown.contains("### Description\nA great video."));
        assert!(res.markdown.contains("- **Keywords:** rust, test"));
        assert!(res.markdown.contains("- **Runtime:** PT5M"));
    }
}
