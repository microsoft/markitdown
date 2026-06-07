//! RSS / Atom feed converter. Port of `_rss_converter.py`.
//!
//! Builds a small DOM from the XML (via quick-xml), then mirrors the Python
//! minidom traversal: RSS 2.0 channels/items and Atom feeds/entries.
use super::html::fragment_to_markdown;
use crate::{text::decode_text, Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};
use quick_xml::events::Event;
use quick_xml::reader::Reader;

const PRECISE_MIME_PREFIXES: &[&str] = &[
    "application/rss",
    "application/rss+xml",
    "application/atom",
    "application/atom+xml",
];
const PRECISE_EXTENSIONS: &[&str] = &[".rss", ".atom"];
const CANDIDATE_MIME_PREFIXES: &[&str] = &["text/xml", "application/xml"];
const CANDIDATE_EXTENSIONS: &[&str] = &[".xml"];

pub struct RssConverter;

/// A minimal XML element tree.
#[derive(Debug, Default)]
struct Node {
    name: String,
    children: Vec<Node>,
    /// Concatenated text directly contained by this element (and CDATA).
    text: String,
}

impl Node {
    /// First descendant (depth-first, document order) with the given tag name.
    fn first_descendant(&self, tag: &str) -> Option<&Node> {
        for child in &self.children {
            if child.name == tag {
                return Some(child);
            }
            if let Some(found) = child.first_descendant(tag) {
                return Some(found);
            }
        }
        None
    }

    /// All descendants with the given tag name (document order).
    fn descendants<'a>(&'a self, tag: &str, out: &mut Vec<&'a Node>) {
        for child in &self.children {
            if child.name == tag {
                out.push(child);
            }
            child.descendants(tag, out);
        }
    }

    /// Text of the first descendant with `tag`, mirroring Python's
    /// `_get_data_by_tag_name` (firstChild text data).
    fn data_by_tag(&self, tag: &str) -> Option<String> {
        let node = self.first_descendant(tag)?;
        let t = node.text.clone();
        if t.is_empty() {
            // Python returns the firstChild's `.data`; an element with only
            // child elements (no text) yields None.
            None
        } else {
            Some(t)
        }
    }
}

/// Parse the XML bytes into a tree. Local (un-namespaced) tag names are used,
/// except `content:encoded` which we keep verbatim to match the Python lookup.
fn parse_tree(xml: &str) -> Result<Node, String> {
    let mut reader = Reader::from_str(xml);

    let mut root = Node {
        name: "#root".to_string(),
        ..Default::default()
    };
    let mut stack: Vec<Node> = Vec::new();
    let mut current = std::mem::take(&mut root);

    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => {
                let name = qname_to_string(e.name().as_ref());
                stack.push(std::mem::replace(
                    &mut current,
                    Node {
                        name,
                        ..Default::default()
                    },
                ));
            }
            Ok(Event::End(_)) => {
                if let Some(mut parent) = stack.pop() {
                    parent.children.push(std::mem::replace(&mut current, Node::default()));
                    current = parent;
                } else {
                    break;
                }
            }
            Ok(Event::Empty(e)) => {
                let name = qname_to_string(e.name().as_ref());
                current.children.push(Node {
                    name,
                    ..Default::default()
                });
            }
            Ok(Event::Text(e)) => {
                if let Ok(t) = e.decode() {
                    current.text.push_str(t.as_ref());
                }
            }
            Ok(Event::CData(e)) => {
                if let Ok(t) = std::str::from_utf8(e.as_ref()) {
                    current.text.push_str(t);
                }
            }
            Ok(Event::GeneralRef(e)) => {
                // Resolve numeric character references and the predefined XML
                // entities appearing in text.
                if let Ok(Some(ch)) = e.resolve_char_ref() {
                    current.text.push(ch);
                } else if let Ok(name) = e.decode() {
                    match name.as_ref() {
                        "amp" => current.text.push('&'),
                        "lt" => current.text.push('<'),
                        "gt" => current.text.push('>'),
                        "quot" => current.text.push('"'),
                        "apos" => current.text.push('\''),
                        _ => {}
                    }
                }
            }
            Ok(Event::Eof) => break,
            Ok(_) => {}
            Err(e) => return Err(e.to_string()),
        }
    }
    Ok(current)
}

/// Strip any namespace prefix except for the `content:encoded` case the Python
/// converter explicitly looks up by its prefixed name.
fn qname_to_string(raw: &[u8]) -> String {
    let s = String::from_utf8_lossy(raw);
    if s == "content:encoded" {
        return s.into_owned();
    }
    match s.rsplit_once(':') {
        Some((_, local)) => local.to_string(),
        None => s.into_owned(),
    }
}

/// Detect the feed type from a parsed tree (mirrors Python `_feed_type`).
fn feed_type(root: &Node) -> Option<&'static str> {
    if root.first_descendant("rss").is_some() {
        return Some("rss");
    }
    if let Some(feed) = root.first_descendant("feed") {
        if feed.first_descendant("entry").is_some() {
            return Some("atom");
        }
    }
    None
}

/// Cheap byte-scan used by `accepts` for ambiguous XML inputs.
fn looks_like_feed(data: &[u8]) -> bool {
    let n = data.len().min(2048);
    let head = &data[..n];
    contains_subslice(head, b"<rss") || contains_subslice(head, b"<feed")
}

fn contains_subslice(haystack: &[u8], needle: &[u8]) -> bool {
    if needle.is_empty() || haystack.len() < needle.len() {
        return false;
    }
    haystack.windows(needle.len()).any(|w| w == needle)
}

impl Converter for RssConverter {
    fn name(&self) -> &'static str {
        "rss"
    }

    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool {
        if info.extension_is(PRECISE_EXTENSIONS) {
            return true;
        }
        if let Some(mt) = &info.mimetype {
            let mt = mt.split(';').next().unwrap_or(mt).trim().to_ascii_lowercase();
            if PRECISE_MIME_PREFIXES.iter().any(|p| mt.starts_with(p)) {
                return true;
            }
        }
        if info.extension_is(CANDIDATE_EXTENSIONS) {
            return looks_like_feed(data);
        }
        if let Some(mt) = &info.mimetype {
            let mt = mt.split(';').next().unwrap_or(mt).trim().to_ascii_lowercase();
            if CANDIDATE_MIME_PREFIXES.iter().any(|p| mt.starts_with(p)) {
                return looks_like_feed(data);
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
        let xml = decode_text(data, info);
        let root = parse_tree(&xml).map_err(|e| ConvertError::conversion("rss", e))?;

        match feed_type(&root) {
            Some("rss") => parse_rss(&root, opts.keep_data_uris),
            Some("atom") => parse_atom(&root, opts.keep_data_uris),
            _ => Err(ConvertError::conversion("rss", "Unknown feed type")),
        }
    }
}

/// Convert an item's HTML-bearing content to Markdown (Python `_parse_content`).
fn parse_content(content: &str, keep_data_uris: bool) -> String {
    fragment_to_markdown(content, keep_data_uris)
}

fn parse_rss(root: &Node, keep_data_uris: bool) -> Result<ConvertResult, ConvertError> {
    let rss = root
        .first_descendant("rss")
        .ok_or_else(|| ConvertError::conversion("rss", "No rss element"))?;
    let channel = rss
        .first_descendant("channel")
        .ok_or_else(|| ConvertError::conversion("rss", "No channel found in RSS feed"))?;

    let channel_title = channel.data_by_tag("title");
    let channel_description = channel.data_by_tag("description");

    let mut md = String::new();
    if let Some(t) = &channel_title {
        md.push_str(&format!("# {t}\n"));
    }
    if let Some(d) = &channel_description {
        md.push_str(&format!("{d}\n"));
    }

    let mut items: Vec<&Node> = Vec::new();
    channel.descendants("item", &mut items);
    for item in items {
        let title = item.data_by_tag("title");
        let description = item.data_by_tag("description");
        let pub_date = item.data_by_tag("pubDate");
        let content = item.data_by_tag("content:encoded");

        if let Some(t) = title {
            md.push_str(&format!("\n## {t}\n"));
        }
        if let Some(d) = pub_date {
            md.push_str(&format!("Published on: {d}\n"));
        }
        if let Some(d) = description {
            md.push_str(&parse_content(&d, keep_data_uris));
        }
        if let Some(c) = content {
            md.push_str(&parse_content(&c, keep_data_uris));
        }
    }

    let mut result = ConvertResult::new(md);
    if let Some(t) = channel_title {
        result = result.with_title(t);
    }
    Ok(result)
}

fn parse_atom(root: &Node, keep_data_uris: bool) -> Result<ConvertResult, ConvertError> {
    let feed = root
        .first_descendant("feed")
        .ok_or_else(|| ConvertError::conversion("rss", "No feed element"))?;

    let title = feed.data_by_tag("title");
    let subtitle = feed.data_by_tag("subtitle");

    let mut md = format!("# {}\n", title.clone().unwrap_or_default());
    if let Some(s) = &subtitle {
        md.push_str(&format!("{s}\n"));
    }

    let mut entries: Vec<&Node> = Vec::new();
    feed.descendants("entry", &mut entries);
    for entry in entries {
        let entry_title = entry.data_by_tag("title");
        let entry_summary = entry.data_by_tag("summary");
        let entry_updated = entry.data_by_tag("updated");
        let entry_content = entry.data_by_tag("content");

        if let Some(t) = entry_title {
            md.push_str(&format!("\n## {t}\n"));
        }
        if let Some(u) = entry_updated {
            md.push_str(&format!("Updated on: {u}\n"));
        }
        if let Some(s) = entry_summary {
            md.push_str(&parse_content(&s, keep_data_uris));
        }
        if let Some(c) = entry_content {
            md.push_str(&parse_content(&c, keep_data_uris));
        }
    }

    let mut result = ConvertResult::new(md);
    if let Some(t) = title {
        result = result.with_title(t);
    }
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rss_roundtrip() {
        let xml = r#"<?xml version="1.0"?>
        <rss version="2.0"><channel>
            <title>My Feed</title>
            <description>About things</description>
            <item><title>First</title><pubDate>Mon, 01 Jan 2024</pubDate>
              <description>&lt;p&gt;Hello &lt;b&gt;world&lt;/b&gt;&lt;/p&gt;</description></item>
        </channel></rss>"#;
        let info = StreamInfo::new().with_extension(".rss");
        let res = RssConverter
            .convert(xml.as_bytes(), &info, &ConvertOptions::default())
            .unwrap();
        assert!(res.markdown.contains("# My Feed"));
        assert!(res.markdown.contains("## First"));
        assert!(res.markdown.contains("Published on: Mon, 01 Jan 2024"));
        assert!(res.markdown.contains("Hello **world**"));
        assert_eq!(res.title.as_deref(), Some("My Feed"));
    }

    #[test]
    fn atom_roundtrip() {
        let xml = r#"<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <title>Atom Feed</title><subtitle>sub</subtitle>
            <entry><title>E1</title><updated>2024-01-01</updated>
              <summary>A summary</summary></entry>
        </feed>"#;
        let info = StreamInfo::new().with_extension(".atom");
        let res = RssConverter
            .convert(xml.as_bytes(), &info, &ConvertOptions::default())
            .unwrap();
        assert!(res.markdown.contains("# Atom Feed"));
        assert!(res.markdown.contains("## E1"));
        assert!(res.markdown.contains("Updated on: 2024-01-01"));
        assert!(res.markdown.contains("A summary"));
    }

    #[test]
    fn accepts_xml_only_when_feed() {
        let feed = b"<?xml version=\"1.0\"?><rss><channel></channel></rss>";
        let notfeed = b"<?xml version=\"1.0\"?><root><a/></root>";
        let info = StreamInfo::new().with_extension(".xml");
        assert!(RssConverter.accepts(&info, feed));
        assert!(!RssConverter.accepts(&info, notfeed));
    }
}
