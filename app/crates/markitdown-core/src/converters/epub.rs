//! EPUB → Markdown converter.
//!
//! Port of `_epub_converter.py`. We read `META-INF/container.xml` to find the
//! OPF package document, parse its Dublin Core metadata and the manifest/spine,
//! then convert each spine chapter (XHTML) to Markdown with `htmd`, stripping
//! `script`/`style`. A metadata block (`**Title:** …`, `**Authors:** …`, etc.)
//! is emitted first, exactly as the Python converter does.

use std::collections::HashMap;
use std::io::Read;

use htmd::options::{BulletListMarker, Options};
use htmd::HtmlToMarkdown;
use quick_xml::escape::unescape;
use quick_xml::events::Event;
use quick_xml::Reader;

use crate::{Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};

const ACCEPTED_EXTENSIONS: &[&str] = &[".epub"];
const ACCEPTED_MIME_PREFIXES: &[&str] = &[
    "application/epub",
    "application/epub+zip",
    "application/x-epub+zip",
];

pub struct EpubConverter;

impl Converter for EpubConverter {
    fn name(&self) -> &'static str {
        "epub"
    }

    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_EXTENSIONS) {
            return data.starts_with(b"PK");
        }
        if let Some(mt) = &info.mimetype {
            let mt = mt.split(';').next().unwrap_or(mt).trim();
            if ACCEPTED_MIME_PREFIXES.iter().any(|p| mt.starts_with(p)) {
                return data.starts_with(b"PK");
            }
        }
        false
    }

    fn convert(
        &self,
        data: &[u8],
        _info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let mut zip = zip::ZipArchive::new(std::io::Cursor::new(data))
            .map_err(|e| ConvertError::conversion("epub", format!("not a valid zip: {e}")))?;

        let container = read_entry(&mut zip, "META-INF/container.xml")
            .ok_or_else(|| ConvertError::conversion("epub", "missing META-INF/container.xml"))?;
        let opf_path = find_opf_path(&container)
            .ok_or_else(|| ConvertError::conversion("epub", "no rootfile in container.xml"))?;

        let opf = read_entry(&mut zip, &opf_path)
            .ok_or_else(|| ConvertError::conversion("epub", "missing OPF package document"))?;
        let pkg = parse_opf(&opf);

        let base_path = match opf_path.rfind('/') {
            Some(idx) => opf_path[..idx].to_string(),
            None => String::new(),
        };

        // Single space after the bullet marker, matching the Python
        // markdownify output (`* item`) rather than htmd's default 3 spaces.
        let options = Options {
            bullet_list_marker: BulletListMarker::Asterisk,
            ul_bullet_spacing: 1,
            ..Options::default()
        };
        let converter = HtmlToMarkdown::builder()
            .options(options)
            .skip_tags(vec!["script", "style"])
            .build();

        let mut chapters: Vec<String> = Vec::new();
        for idref in &pkg.spine {
            let Some(href) = pkg.manifest.get(idref) else {
                continue;
            };
            let full = if base_path.is_empty() {
                href.clone()
            } else {
                format!("{base_path}/{href}")
            };
            if let Some(html) = read_entry(&mut zip, &full) {
                if let Ok(markdown) = converter.convert(&html) {
                    chapters.push(markdown.trim().to_string());
                }
            }
        }

        let metadata_block = build_metadata_block(&pkg.metadata);
        let mut sections: Vec<String> = Vec::new();
        sections.push(metadata_block);
        sections.extend(chapters);

        let markdown = sections.join("\n\n");
        let title = pkg
            .metadata
            .get("title")
            .and_then(|v| v.first())
            .cloned();

        let mut result = ConvertResult::new(markdown);
        if let Some(t) = title {
            result = result.with_title(t);
        }
        Ok(result)
    }
}

fn read_entry(zip: &mut zip::ZipArchive<std::io::Cursor<&[u8]>>, name: &str) -> Option<String> {
    let mut file = zip.by_name(name).ok()?;
    let mut buf = String::new();
    file.read_to_string(&mut buf).ok()?;
    Some(buf)
}

fn find_opf_path(container_xml: &str) -> Option<String> {
    let mut reader = Reader::from_str(container_xml);
    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) | Ok(Event::Empty(e)) => {
                if e.name().as_ref().ends_with(b"rootfile") {
                    if let Some(p) = attr(&e, b"full-path") {
                        return Some(p);
                    }
                }
            }
            Ok(Event::Eof) => break,
            Err(_) => break,
            _ => {}
        }
    }
    None
}

struct Package {
    /// dc:* metadata; values are lists (creators may repeat).
    metadata: HashMap<String, Vec<String>>,
    /// manifest item id → href.
    manifest: HashMap<String, String>,
    /// spine idrefs, in order.
    spine: Vec<String>,
}

fn parse_opf(xml: &str) -> Package {
    let mut metadata: HashMap<String, Vec<String>> = HashMap::new();
    let mut manifest: HashMap<String, String> = HashMap::new();
    let mut spine: Vec<String> = Vec::new();

    let mut reader = Reader::from_str(xml);
    let mut cur_dc: Option<String> = None;
    let mut text_buf = String::new();

    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => {
                let name = e.name();
                let local = local_name(name.as_ref());
                if let Some(key) = dc_key(local) {
                    cur_dc = Some(key.to_string());
                    text_buf.clear();
                }
            }
            Ok(Event::Empty(e)) => {
                let name = e.name();
                let local = local_name(name.as_ref());
                if local == b"item" {
                    if let (Some(id), Some(href)) = (attr(&e, b"id"), attr(&e, b"href")) {
                        manifest.insert(id, href);
                    }
                } else if local == b"itemref" {
                    if let Some(idref) = attr(&e, b"idref") {
                        spine.push(idref);
                    }
                }
            }
            Ok(Event::Text(t)) => {
                if cur_dc.is_some() {
                    let raw = t.decode().unwrap_or_default();
                    text_buf.push_str(
                        &unescape(&raw).map(|c| c.into_owned()).unwrap_or_default(),
                    );
                }
            }
            Ok(Event::End(e)) => {
                let name = e.name();
                let local = local_name(name.as_ref());
                // Some manifest items use Start/End rather than Empty.
                if local == b"item" {
                    // handled at Empty for the common case; ignore here.
                }
                if let Some(key) = dc_key(local) {
                    if cur_dc.as_deref() == Some(key) {
                        let val = text_buf.trim().to_string();
                        if !val.is_empty() {
                            metadata.entry(key.to_string()).or_default().push(val);
                        }
                        cur_dc = None;
                        text_buf.clear();
                    }
                }
            }
            Ok(Event::Eof) => break,
            Err(_) => break,
            _ => {}
        }
    }

    Package {
        metadata,
        manifest,
        spine,
    }
}

/// Map a Dublin Core local element name to our metadata key.
fn dc_key(local: &[u8]) -> Option<&'static str> {
    match local {
        b"title" => Some("title"),
        b"creator" => Some("authors"),
        b"language" => Some("language"),
        b"publisher" => Some("publisher"),
        b"date" => Some("date"),
        b"description" => Some("description"),
        b"identifier" => Some("identifier"),
        _ => None,
    }
}

/// Strip an optional `prefix:` from a qualified name.
fn local_name(qname: &[u8]) -> &[u8] {
    match qname.iter().position(|&b| b == b':') {
        Some(i) => &qname[i + 1..],
        None => qname,
    }
}

fn attr(e: &quick_xml::events::BytesStart, key: &[u8]) -> Option<String> {
    e.try_get_attribute(key).ok().flatten().and_then(|a| {
        a.normalized_value(quick_xml::XmlVersion::Implicit1_0)
            .ok()
            .map(|c| c.into_owned())
    })
}

/// Emit the metadata block in the Python key order with capitalized labels.
fn build_metadata_block(metadata: &HashMap<String, Vec<String>>) -> String {
    const ORDER: &[(&str, &str)] = &[
        ("title", "Title"),
        ("authors", "Authors"),
        ("language", "Language"),
        ("publisher", "Publisher"),
        ("date", "Date"),
        ("description", "Description"),
        ("identifier", "Identifier"),
    ];
    let mut lines: Vec<String> = Vec::new();
    for (key, label) in ORDER {
        if let Some(values) = metadata.get(*key) {
            let joined = values.join(", ");
            if !joined.is_empty() {
                lines.push(format!("**{label}:** {joined}"));
            }
        }
    }
    lines.join("\n")
}
