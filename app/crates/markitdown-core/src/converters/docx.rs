//! DOCX → Markdown converter.
//!
//! Port of `_docx_converter.py`. The Python implementation delegates to
//! `mammoth` (DOCX → HTML) then to the HTML→Markdown converter. We do not use
//! mammoth; instead we parse `word/document.xml` directly with quick-xml and
//! emit Markdown straight away. Supported fidelity: paragraphs; heading styles
//! (`Heading 1`..`Heading 9` → `#`..`######`, `Title` → `#`); bold (`w:b`) and
//! italic (`w:i`) run formatting; hyperlinks (resolved via
//! `word/_rels/document.xml.rels`); tables (`w:tbl` → GFM table, first row as
//! the header); and bulleted list paragraphs (`w:numPr`, nested by `w:ilvl`).
//!
//! Inline images become `![alt](src)` where `src` is a `data:` URI built from
//! the embedded media. When `keep_data_uris` is false the URI is truncated to
//! `data:<mime>;base64...` exactly like the Python markdownify path; otherwise
//! the full base64 payload is kept.

use std::collections::HashMap;
use std::io::Read;

use base64::Engine as _;
use quick_xml::escape::unescape;
use quick_xml::events::Event;
use quick_xml::Reader;

use crate::{text, Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};

const ACCEPTED_EXTENSIONS: &[&str] = &[".docx"];
const ACCEPTED_MIME_PREFIXES: &[&str] =
    &["application/vnd.openxmlformats-officedocument.wordprocessingml.document"];

pub struct DocxConverter;

impl Converter for DocxConverter {
    fn name(&self) -> &'static str {
        "docx"
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
        opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let mut zip = zip::ZipArchive::new(std::io::Cursor::new(data))
            .map_err(|e| ConvertError::conversion("docx", format!("not a valid zip: {e}")))?;

        let document = read_entry(&mut zip, "word/document.xml").ok_or_else(|| {
            ConvertError::conversion("docx", "missing word/document.xml")
        })?;
        let styles = read_entry(&mut zip, "word/styles.xml").unwrap_or_default();
        let rels = read_entry(&mut zip, "word/_rels/document.xml.rels").unwrap_or_default();

        let style_names = parse_style_names(&styles);
        let relationships = parse_relationships(&rels);
        let media: HashMap<String, Vec<u8>> = collect_media(&mut zip);

        let ctx = DocxContext {
            style_names: &style_names,
            relationships: &relationships,
            media: &media,
            keep_data_uris: opts.keep_data_uris,
        };

        let markdown = render_document(&document, &ctx)?;
        let title = first_nonempty_line(&markdown);
        let mut result = ConvertResult::new(markdown);
        // Features this parser does not render but the Python engine does
        // (mammoth extracts comments; Python converts OMML math to LaTeX):
        // flag them so Engine::Auto can retry with higher fidelity.
        if document.contains("<w:commentReference")
            || document.contains("<m:oMath")
            || read_entry(&mut zip, "word/comments.xml").is_some()
        {
            result = result.with_degraded();
        }
        if let Some(t) = title {
            result = result.with_title(t);
        }
        Ok(result)
    }
}

struct DocxContext<'a> {
    style_names: &'a HashMap<String, String>,
    relationships: &'a HashMap<String, String>,
    media: &'a HashMap<String, Vec<u8>>,
    keep_data_uris: bool,
}

fn read_entry(zip: &mut zip::ZipArchive<std::io::Cursor<&[u8]>>, name: &str) -> Option<String> {
    let mut file = zip.by_name(name).ok()?;
    let mut buf = String::new();
    file.read_to_string(&mut buf).ok()?;
    Some(buf)
}

fn collect_media(zip: &mut zip::ZipArchive<std::io::Cursor<&[u8]>>) -> HashMap<String, Vec<u8>> {
    let mut out = HashMap::new();
    let names: Vec<String> = (0..zip.len())
        .filter_map(|i| zip.by_index(i).ok().map(|f| f.name().to_string()))
        .filter(|n| n.starts_with("word/media/"))
        .collect();
    for name in names {
        if let Ok(mut f) = zip.by_name(&name) {
            let mut data = Vec::new();
            if f.read_to_end(&mut data).is_ok() {
                // Key on the basename so we can resolve "media/imageN.png" targets.
                let base = name.rsplit('/').next().unwrap_or(&name).to_string();
                out.insert(base, data);
            }
        }
    }
    out
}

/// Map a style id (e.g. `"1"`) to its lower-cased display name (`"heading 1"`).
fn parse_style_names(xml: &str) -> HashMap<String, String> {
    let mut map = HashMap::new();
    if xml.is_empty() {
        return map;
    }
    let mut reader = Reader::from_str(xml);
    let mut current_id: Option<String> = None;
    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) | Ok(Event::Empty(e)) => {
                let name = e.name();
                let local = name.as_ref();
                if local == b"w:style" {
                    current_id = attr(&e, b"w:styleId");
                } else if local == b"w:name" {
                    if let (Some(id), Some(val)) = (&current_id, attr(&e, b"w:val")) {
                        map.insert(id.clone(), val.to_ascii_lowercase());
                    }
                }
            }
            Ok(Event::End(e)) if e.name().as_ref() == b"w:style" => current_id = None,
            Ok(Event::Eof) => break,
            Err(_) => break,
            _ => {}
        }
    }
    map
}

/// Map relationship id → target (e.g. `rId4` → `media/image1.png`).
fn parse_relationships(xml: &str) -> HashMap<String, String> {
    let mut map = HashMap::new();
    if xml.is_empty() {
        return map;
    }
    let mut reader = Reader::from_str(xml);
    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) | Ok(Event::Empty(e)) => {
                if e.name().as_ref() == b"Relationship" {
                    if let (Some(id), Some(target)) = (attr(&e, b"Id"), attr(&e, b"Target")) {
                        map.insert(id, target);
                    }
                }
            }
            Ok(Event::Eof) => break,
            Err(_) => break,
            _ => {}
        }
    }
    map
}

fn attr(e: &quick_xml::events::BytesStart, key: &[u8]) -> Option<String> {
    e.try_get_attribute(key).ok().flatten().and_then(|a| {
        a.normalized_value(quick_xml::XmlVersion::Implicit1_0)
            .ok()
            .map(|c| c.into_owned())
    })
}

/// Heading style name → markdown prefix.
fn heading_prefix(style_name: &str) -> Option<&'static str> {
    match style_name {
        "title" => Some("# "),
        "heading 1" => Some("# "),
        "heading 2" => Some("## "),
        "heading 3" => Some("### "),
        "heading 4" => Some("#### "),
        "heading 5" => Some("##### "),
        "heading 6" => Some("###### "),
        // Headings 7-9 collapse to level 6, matching mammoth's HTML output cap.
        "heading 7" | "heading 8" | "heading 9" => Some("###### "),
        _ => None,
    }
}

#[derive(Default)]
struct RunState {
    bold: bool,
    italic: bool,
}

/// Build the truncated-or-full data URI for an embedded image, matching the
/// Python markdownify behaviour (`src.split(",")[0] + "..."`).
fn image_data_uri(ctx: &DocxContext, rid: &str) -> Option<String> {
    let target = ctx.relationships.get(rid)?;
    let base = target.rsplit('/').next().unwrap_or(target);
    let bytes = ctx.media.get(base)?;
    let mime = mime_for(base);
    let full = format!(
        "data:{mime};base64,{}",
        base64::engine::general_purpose::STANDARD.encode(bytes)
    );
    if ctx.keep_data_uris {
        Some(full)
    } else {
        Some(format!("data:{mime};base64..."))
    }
}

fn mime_for(name: &str) -> &'static str {
    let ext = name.rsplit('.').next().unwrap_or("").to_ascii_lowercase();
    match ext.as_str() {
        "png" => "image/png",
        "jpg" | "jpeg" => "image/jpeg",
        "gif" => "image/gif",
        "bmp" => "image/bmp",
        "tif" | "tiff" => "image/tiff",
        "svg" => "image/svg+xml",
        "webp" => "image/webp",
        "emf" => "image/x-emf",
        "wmf" => "image/x-wmf",
        _ => "image/png",
    }
}

fn render_document(xml: &str, ctx: &DocxContext) -> Result<String, ConvertError> {
    let mut reader = Reader::from_str(xml);
    let mut out = String::new();

    // Block-building state.
    let mut in_table = false;
    let mut table_rows: Vec<Vec<String>> = Vec::new();
    let mut cur_row: Vec<String> = Vec::new();
    let mut cur_cell = String::new();
    let mut cell_depth: i32 = 0; // nesting of w:tc; cell text accumulates while >0

    // Paragraph state.
    let mut para = String::new();
    let mut para_style: Option<String> = None;
    let mut is_list = false;
    let mut ilvl: usize = 0;
    let mut in_ppr = false;

    // Run state.
    let mut run = RunState::default();
    let mut in_rpr = false;
    let mut hyperlink: Option<String> = None;

    macro_rules! flush_para {
        () => {{
            let text = para.trim_end().to_string();
            let style = para_style.take();
            let prefix = style
                .as_deref()
                .and_then(|s| ctx.style_names.get(s).map(String::as_str))
                .and_then(heading_prefix);

            if cell_depth > 0 {
                // Inside a table cell: append paragraph text to the cell.
                if !cur_cell.is_empty() && !text.is_empty() {
                    cur_cell.push(' ');
                }
                cur_cell.push_str(text.trim());
            } else if let Some(p) = prefix {
                if !text.trim().is_empty() {
                    out.push_str(p);
                    out.push_str(text.trim());
                    out.push_str("\n\n");
                }
            } else if is_list {
                let indent = "  ".repeat(ilvl);
                out.push_str(&indent);
                out.push_str("- ");
                out.push_str(text.trim());
                out.push('\n');
            } else if !text.trim().is_empty() {
                out.push_str(text.trim());
                out.push_str("\n\n");
            }
            para.clear();
            is_list = false;
            ilvl = 0;
        }};
    }

    loop {
        let ev = reader.read_event();
        match ev {
            Ok(Event::Start(e)) => {
                let name = e.name();
                match name.as_ref() {
                    b"w:tbl" => {
                        in_table = true;
                        table_rows.clear();
                    }
                    b"w:tr" if in_table => cur_row.clear(),
                    b"w:tc" if in_table => {
                        cell_depth += 1;
                        if cell_depth == 1 {
                            cur_cell.clear();
                        }
                    }
                    b"w:p" => {
                        para.clear();
                        para_style = None;
                        is_list = false;
                        ilvl = 0;
                    }
                    b"w:pPr" => in_ppr = true,
                    b"w:rPr" => in_rpr = true,
                    b"w:hyperlink" => {
                        if let Some(rid) = attr(&e, b"r:id") {
                            hyperlink = ctx.relationships.get(&rid).cloned();
                        }
                    }
                    b"w:r" => run = RunState::default(),
                    _ => {}
                }
            }
            Ok(Event::Empty(e)) => {
                let name = e.name();
                match name.as_ref() {
                    b"w:pStyle" if in_ppr => para_style = attr(&e, b"w:val"),
                    b"w:numPr" if in_ppr => is_list = true,
                    b"w:ilvl" if in_ppr => {
                        if let Some(v) = attr(&e, b"w:val") {
                            ilvl = v.parse().unwrap_or(0);
                        }
                    }
                    b"w:b" if in_rpr => run.bold = true,
                    b"w:i" if in_rpr => run.italic = true,
                    b"a:blip" => {
                        if let Some(rid) = attr(&e, b"r:embed") {
                            if let Some(src) = image_data_uri(ctx, &rid) {
                                para.push_str(&format!("![]({src})"));
                            }
                        }
                    }
                    b"w:br" | b"w:cr" => para.push(' '),
                    b"w:tab" => para.push('\t'),
                    _ => {}
                }
            }
            Ok(Event::Text(t)) => {
                let raw = t.decode().unwrap_or_default();
                let decoded = unescape(&raw).map(|c| c.into_owned()).unwrap_or_else(|_| raw.into_owned());
                if decoded.is_empty() {
                    continue;
                }
                let mut piece = decoded;
                if run.bold {
                    piece = format!("**{}**", piece);
                }
                if run.italic {
                    piece = format!("*{}*", piece);
                }
                if let Some(href) = &hyperlink {
                    piece = format!("[{piece}]({href})");
                }
                para.push_str(&piece);
            }
            Ok(Event::End(e)) => {
                let name = e.name();
                match name.as_ref() {
                    b"w:rPr" => in_rpr = false,
                    b"w:pPr" => in_ppr = false,
                    b"w:r" => run = RunState::default(),
                    b"w:hyperlink" => hyperlink = None,
                    b"w:p" => flush_para!(),
                    b"w:tc" if in_table => {
                        cell_depth -= 1;
                        if cell_depth == 0 {
                            cur_row.push(cur_cell.trim().to_string());
                            cur_cell.clear();
                        }
                    }
                    b"w:tr" if in_table => {
                        if !cur_row.is_empty() {
                            table_rows.push(std::mem::take(&mut cur_row));
                        }
                    }
                    b"w:tbl" => {
                        in_table = false;
                        if !table_rows.is_empty() {
                            out.push_str(&text::rows_to_markdown_table(&table_rows));
                            out.push('\n');
                        }
                        table_rows.clear();
                    }
                    _ => {}
                }
            }
            Ok(Event::Eof) => break,
            Err(e) => {
                return Err(ConvertError::conversion(
                    "docx",
                    format!("xml parse error: {e}"),
                ))
            }
            _ => {}
        }
    }

    Ok(normalize_blank_lines(out.trim()))
}

fn first_nonempty_line(md: &str) -> Option<String> {
    for line in md.lines() {
        let l = line.trim().trim_start_matches('#').trim();
        if !l.is_empty() {
            return Some(l.to_string());
        }
    }
    None
}

/// Collapse runs of 3+ newlines down to a blank-line separator.
fn normalize_blank_lines(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    let mut newlines = 0usize;
    for ch in s.chars() {
        if ch == '\n' {
            newlines += 1;
            if newlines <= 2 {
                out.push('\n');
            }
        } else {
            newlines = 0;
            out.push(ch);
        }
    }
    out
}
