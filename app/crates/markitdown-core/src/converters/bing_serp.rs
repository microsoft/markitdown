//! Bing search-results converter. Port of `_bing_serp_converter.py`.
//!
//! Accepts HTML only when the source URL is a Bing SERP, then extracts the
//! organic (`b_algo`) results, decoding Bing's base64 redirect links.
use super::html::{extract_title_doc, fragment_to_markdown};
use crate::{text::decode_text, Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};
use base64::Engine;
use scraper::{Html, Selector};

const ACCEPTED_MIME_PREFIXES: &[&str] = &["text/html", "application/xhtml"];
const ACCEPTED_EXTENSIONS: &[&str] = &[".html", ".htm"];

pub struct BingSerpConverter;

impl Converter for BingSerpConverter {
    fn name(&self) -> &'static str {
        "bing_serp"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        let url = info.url.as_deref().unwrap_or("");
        if !url.starts_with("https://www.bing.com/search?q=") {
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
        let url = info
            .url
            .as_deref()
            .ok_or_else(|| ConvertError::conversion("bing_serp", "missing URL"))?;

        let raw_query = query_param(url, "q").unwrap_or_default();
        let query = url_decode(&raw_query);

        let html = decode_text(data, info);
        let doc = Html::parse_document(&html);
        let title = extract_title_doc(&doc);

        // Python matches `find_all(class_="b_algo")` (any tag with the class).
        let algo_sel = Selector::parse(".b_algo")
            .map_err(|e| ConvertError::conversion("bing_serp", e.to_string()))?;

        let mut results: Vec<String> = Vec::new();
        for result in doc.select(&algo_sel) {
            // Serialize the result, rewrite Bing redirect hrefs to their real
            // destinations, then convert to Markdown.
            let fragment = rewrite_redirect_hrefs(&result.inner_html());
            let md = fragment_to_markdown(&fragment, opts.keep_data_uris);
            let lines: Vec<&str> = md
                .split('\n')
                .map(|l| l.trim())
                .filter(|l| !l.is_empty())
                .collect();
            if !lines.is_empty() {
                results.push(lines.join("\n"));
            }
        }

        let webpage_text = format!(
            "## A Bing search for '{query}' found the following results:\n\n{}",
            results.join("\n\n")
        );

        let mut res = ConvertResult::new(webpage_text);
        if let Some(t) = title {
            res = res.with_title(t);
        }
        Ok(res)
    }
}

/// Scan a serialized HTML fragment for `href="..."` attributes and replace any
/// Bing `/ck/a?...&u=a1...` redirect with its decoded destination URL.
fn rewrite_redirect_hrefs(fragment: &str) -> String {
    let mut out = String::with_capacity(fragment.len());
    let mut rest = fragment;
    while let Some(pos) = rest.find("href=\"") {
        let attr_start = pos + "href=\"".len();
        out.push_str(&rest[..attr_start]);
        let after = &rest[attr_start..];
        let end = match after.find('"') {
            Some(e) => e,
            None => {
                // Unterminated attribute; emit the remainder verbatim.
                out.push_str(after);
                return out;
            }
        };
        let raw_href = &after[..end];
        // Attribute values are HTML-escaped in the serialized fragment.
        let href = raw_href.replace("&amp;", "&");
        match decode_bing_redirect(&href) {
            Some(decoded) => out.push_str(&decoded.replace('&', "&amp;")),
            None => out.push_str(raw_href),
        }
        out.push('"');
        rest = &after[end + 1..];
    }
    out.push_str(rest);
    out
}

/// Decode a Bing `/ck/a?...&u=a1<base64>` redirect into the real URL.
///
/// Python: `u = qs["u"][0][2:].strip() + "=="`, then
/// `base64.b64decode(u, altchars="-_").decode("utf-8")`.
fn decode_bing_redirect(href: &str) -> Option<String> {
    // The href may be HTML-escaped (&amp;) at this point; normalize for parsing.
    let normalized = href.replace("&amp;", "&");
    let u = query_param(&normalized, "u")?;
    let u = url_decode(&u);
    if u.len() < 2 {
        return None;
    }
    // Strip the "a1" prefix Bing prepends, then any existing base64 padding.
    let payload = u[2..].trim().trim_end_matches('=');
    // Pad to a multiple of 4 so the decoder accepts it (Python appends "==" and
    // relies on b64decode tolerating extra padding; we instead pad precisely).
    let mut buf = payload.to_string();
    while buf.len() % 4 != 0 {
        buf.push('=');
    }
    // RFC 4648 URL-safe alphabet (- and _), tolerant of padding quirks.
    let engine = base64::engine::general_purpose::GeneralPurpose::new(
        &base64::alphabet::URL_SAFE,
        base64::engine::general_purpose::GeneralPurposeConfig::new()
            .with_decode_padding_mode(base64::engine::DecodePaddingMode::Indifferent)
            .with_decode_allow_trailing_bits(true),
    );
    let bytes = engine.decode(buf.as_bytes()).ok()?;
    String::from_utf8(bytes).ok()
}

/// Extract the first value of query parameter `name` from a URL (raw, still
/// percent-encoded). Returns None if absent.
fn query_param(url: &str, name: &str) -> Option<String> {
    let q = url.split_once('?').map(|(_, q)| q)?;
    let q = q.split('#').next().unwrap_or(q);
    for pair in q.split('&') {
        let (k, v) = match pair.split_once('=') {
            Some(kv) => kv,
            None => (pair, ""),
        };
        if k == name {
            return Some(v.to_string());
        }
    }
    None
}

/// Minimal application/x-www-form-urlencoded decode: `+` → space and `%XX`.
fn url_decode(s: &str) -> String {
    let bytes = s.as_bytes();
    let mut out: Vec<u8> = Vec::with_capacity(bytes.len());
    let mut i = 0;
    while i < bytes.len() {
        match bytes[i] {
            b'+' => {
                out.push(b' ');
                i += 1;
            }
            b'%' if i + 2 < bytes.len() => {
                let hi = (bytes[i + 1] as char).to_digit(16);
                let lo = (bytes[i + 2] as char).to_digit(16);
                if let (Some(h), Some(l)) = (hi, lo) {
                    out.push((h * 16 + l) as u8);
                    i += 3;
                } else {
                    out.push(bytes[i]);
                    i += 1;
                }
            }
            b => {
                out.push(b);
                i += 1;
            }
        }
    }
    String::from_utf8_lossy(&out).into_owned()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn query_extraction() {
        assert_eq!(
            query_param("https://www.bing.com/search?q=microsoft+wikipedia&form=x", "q").as_deref(),
            Some("microsoft+wikipedia")
        );
        assert_eq!(url_decode("microsoft+wikipedia"), "microsoft wikipedia");
    }

    #[test]
    fn decodes_real_bing_redirect() {
        // From test_serp.html: u=a1Lz9zY29wZT13ZWImRk9STT1IRFJTQzE
        let href = "https://www.bing.com/ck/a?!&&p=x&u=a1Lz9zY29wZT13ZWImRk9STT1IRFJTQzE&ntb=1";
        let decoded = decode_bing_redirect(href).expect("should decode");
        assert!(decoded.starts_with('/'), "got: {decoded}");
    }
}
