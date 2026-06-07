//! PPTX → Markdown converter.
//!
//! Port of `_pptx_converter.py`. Python uses `python-pptx`; we parse the OOXML
//! parts directly with quick-xml. For each slide (in numeric order) we emit a
//! `<!-- Slide number: N -->` marker, then walk the shape tree:
//!
//! * the title placeholder (`p:ph type="title"|"ctrTitle"`) becomes `# heading`;
//! * other text frames emit their paragraph text (one `a:p` per line);
//! * tables (`a:tbl`) become GFM tables (first row as the header);
//! * pictures (`p:pic`) become `![alt](src)` — alt text comes from the shape's
//!   `descr`/`name`, and `src` is `<name>.jpg` unless `keep_data_uris` is set,
//!   in which case the embedded image is emitted as a full `data:` URI (mirrors
//!   the Python image handling, minus LLM captioning);
//! * charts (`c:chart`) are rendered as a `### Chart` table built from the
//!   linked `ppt/charts/chartN.xml` part.
//!
//! Speaker notes (`ppt/notesSlides/`) are appended per slide as `### Notes:`.
//!
//! Simplification vs. Python: shapes are emitted in document order rather than
//! sorted by (top, left) position, and group shapes are flattened in place.
//! LLM captioning is not performed.

use std::collections::HashMap;
use std::io::Read;

use base64::Engine as _;
use quick_xml::escape::unescape;
use quick_xml::events::Event;
use quick_xml::Reader;

use crate::{text, Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};

const ACCEPTED_EXTENSIONS: &[&str] = &[".pptx"];
const ACCEPTED_MIME_PREFIXES: &[&str] =
    &["application/vnd.openxmlformats-officedocument.presentationml"];

pub struct PptxConverter;

impl Converter for PptxConverter {
    fn name(&self) -> &'static str {
        "pptx"
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
            .map_err(|e| ConvertError::conversion("pptx", format!("not a valid zip: {e}")))?;

        let mut slide_names: Vec<String> = (0..zip.len())
            .filter_map(|i| zip.by_index(i).ok().map(|f| f.name().to_string()))
            .filter(|n| {
                n.starts_with("ppt/slides/slide") && n.ends_with(".xml") && !n.contains("_rels")
            })
            .collect();
        slide_names.sort_by_key(|n| slide_index(n));

        // Preload every part so we can cross-reference rels/charts/media.
        let parts = read_all(&mut zip);

        let mut md = String::new();
        for (i, slide_name) in slide_names.iter().enumerate() {
            let slide_num = i + 1;
            let xml = match parts.get(slide_name) {
                Some(b) => String::from_utf8_lossy(b).into_owned(),
                None => continue,
            };
            let rels_name = format!("ppt/slides/_rels/{}.rels", basename(slide_name));
            let rels = parts
                .get(&rels_name)
                .map(|b| parse_relationships(&String::from_utf8_lossy(b)))
                .unwrap_or_default();

            md.push_str(&format!("\n\n<!-- Slide number: {slide_num} -->\n"));
            let slide_md = render_slide(&xml, &rels, &parts, opts.keep_data_uris);
            md.push_str(slide_md.trim());

            if let Some(notes) = slide_notes(slide_num, &parts) {
                if !notes.trim().is_empty() {
                    md.push_str("\n\n### Notes:\n");
                    md.push_str(notes.trim());
                }
            }
        }

        Ok(ConvertResult::new(md.trim().to_string()))
    }
}

fn slide_index(name: &str) -> u32 {
    name.trim_end_matches(".xml")
        .rsplit("slide")
        .next()
        .and_then(|s| s.parse().ok())
        .unwrap_or(0)
}

fn basename(path: &str) -> &str {
    path.rsplit('/').next().unwrap_or(path)
}

fn read_all(zip: &mut zip::ZipArchive<std::io::Cursor<&[u8]>>) -> HashMap<String, Vec<u8>> {
    let mut out = HashMap::new();
    let names: Vec<String> = (0..zip.len())
        .filter_map(|i| zip.by_index(i).ok().map(|f| f.name().to_string()))
        .collect();
    for name in names {
        if let Ok(mut f) = zip.by_name(&name) {
            let mut buf = Vec::new();
            if f.read_to_end(&mut buf).is_ok() {
                out.insert(name, buf);
            }
        }
    }
    out
}

fn parse_relationships(xml: &str) -> HashMap<String, String> {
    let mut map = HashMap::new();
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

fn render_slide(
    xml: &str,
    rels: &HashMap<String, String>,
    parts: &HashMap<String, Vec<u8>>,
    keep_data_uris: bool,
) -> String {
    let mut reader = Reader::from_str(xml);
    let mut out = String::new();

    // Shape-level state.
    let mut is_title_shape = false;
    let mut in_txbody = false;
    let mut sp_text_lines: Vec<String> = Vec::new();
    let mut cur_line = String::new();

    // Picture state.
    let mut pic_name: Option<String> = None;
    let mut pic_descr: Option<String> = None;
    let mut pic_embed: Option<String> = None;
    let mut in_pic = false;
    let mut in_pic_nvpr = false;

    // Table state.
    let mut in_table = false;
    let mut table_rows: Vec<Vec<String>> = Vec::new();
    let mut cur_row: Vec<String> = Vec::new();
    let mut cur_cell = String::new();
    let mut cell_depth = 0i32;

    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => match e.name().as_ref() {
                b"p:sp" => {
                    is_title_shape = false;
                    sp_text_lines.clear();
                }
                b"p:pic" => {
                    in_pic = true;
                    pic_name = None;
                    pic_descr = None;
                    pic_embed = None;
                }
                b"p:nvPicPr" if in_pic => in_pic_nvpr = true,
                b"p:cNvPr" if in_pic && in_pic_nvpr => {
                    pic_name = attr(&e, b"name");
                    pic_descr = attr(&e, b"descr");
                }
                b"a:tbl" => {
                    in_table = true;
                    table_rows.clear();
                }
                b"a:tr" if in_table => cur_row.clear(),
                b"a:tc" if in_table => {
                    cell_depth += 1;
                    if cell_depth == 1 {
                        cur_cell.clear();
                    }
                }
                b"p:txBody" | b"a:txBody" => {
                    if !in_table {
                        in_txbody = true;
                        sp_text_lines.clear();
                        cur_line.clear();
                    }
                }
                b"a:p" if in_txbody && !in_table => cur_line.clear(),
                _ => {}
            },
            Ok(Event::Empty(e)) => match e.name().as_ref() {
                b"p:ph" => {
                    if let Some(t) = attr(&e, b"type") {
                        if t == "title" || t == "ctrTitle" {
                            is_title_shape = true;
                        }
                    }
                }
                b"p:cNvPr" if in_pic && in_pic_nvpr => {
                    pic_name = attr(&e, b"name");
                    pic_descr = attr(&e, b"descr");
                }
                b"a:blip" if in_pic => {
                    pic_embed = attr(&e, b"r:embed");
                }
                b"c:chart" => {
                    if let Some(rid) = attr(&e, b"r:id") {
                        if let Some(chart_md) = render_chart(&rid, rels, parts) {
                            out.push_str(&chart_md);
                        }
                    }
                }
                _ => {}
            },
            Ok(Event::Text(t)) => {
                if in_txbody || cell_depth > 0 {
                    let raw = t.decode().unwrap_or_default();
                    let decoded = unescape(&raw)
                        .map(|c| c.into_owned())
                        .unwrap_or_else(|_| raw.into_owned());
                    if cell_depth > 0 {
                        cur_cell.push_str(&decoded);
                    } else {
                        cur_line.push_str(&decoded);
                    }
                }
            }
            Ok(Event::End(e)) => match e.name().as_ref() {
                b"a:p" if in_txbody && !in_table => {
                    sp_text_lines.push(std::mem::take(&mut cur_line));
                }
                b"p:txBody" | b"a:txBody" => {
                    if in_txbody && !in_table {
                        in_txbody = false;
                        let joined = sp_text_lines.join("\n");
                        let trimmed = joined.trim_matches('\n');
                        if is_title_shape {
                            out.push_str("# ");
                            out.push_str(trimmed.trim_start());
                            out.push('\n');
                        } else if !trimmed.is_empty() {
                            out.push_str(trimmed);
                            out.push('\n');
                        }
                        sp_text_lines.clear();
                    }
                }
                b"p:nvPicPr" => in_pic_nvpr = false,
                b"p:pic" => {
                    in_pic = false;
                    let name = pic_name.take().unwrap_or_default();
                    let descr = pic_descr.take().unwrap_or_default();
                    let embed = pic_embed.take();
                    let alt = clean_alt(if descr.is_empty() { &name } else { &descr });
                    let src = if keep_data_uris {
                        embed
                            .as_deref()
                            .and_then(|rid| pic_data_uri(rid, rels, parts))
                            .unwrap_or_else(|| placeholder_name(&name))
                    } else {
                        placeholder_name(&name)
                    };
                    out.push_str(&format!("\n![{alt}]({src})\n"));
                }
                b"a:tc" if in_table => {
                    cell_depth -= 1;
                    if cell_depth == 0 {
                        cur_row.push(cur_cell.trim().to_string());
                        cur_cell.clear();
                    }
                }
                b"a:tr" if in_table => {
                    if !cur_row.is_empty() {
                        table_rows.push(std::mem::take(&mut cur_row));
                    }
                }
                b"a:tbl" => {
                    in_table = false;
                    if !table_rows.is_empty() {
                        out.push_str(&text::rows_to_markdown_table(&table_rows));
                        out.push('\n');
                    }
                    table_rows.clear();
                }
                _ => {}
            },
            Ok(Event::Eof) => break,
            Err(_) => break,
            _ => {}
        }
    }

    out
}

/// Mirror Python: `re.sub(r"[\r\n\[\]]", " ", alt)` then collapse whitespace.
fn clean_alt(s: &str) -> String {
    let replaced: String = s
        .chars()
        .map(|c| match c {
            '\r' | '\n' | '[' | ']' => ' ',
            other => other,
        })
        .collect();
    replaced.split_whitespace().collect::<Vec<_>>().join(" ")
}

/// Python: `re.sub(r"\W", "", shape.name) + ".jpg"`.
fn placeholder_name(name: &str) -> String {
    let cleaned: String = name
        .chars()
        .filter(|c| c.is_alphanumeric() || *c == '_')
        .collect();
    format!("{cleaned}.jpg")
}

/// Resolve a picture's embedded image to a full `data:` URI.
fn pic_data_uri(
    rid: &str,
    rels: &HashMap<String, String>,
    parts: &HashMap<String, Vec<u8>>,
) -> Option<String> {
    let target = rels.get(rid)?;
    let resolved = resolve_relative("ppt/slides", target);
    let bytes = parts.get(&resolved)?;
    let mime = mime_for(&resolved);
    Some(format!(
        "data:{mime};base64,{}",
        base64::engine::general_purpose::STANDARD.encode(bytes)
    ))
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
        _ => "image/jpeg",
    }
}

/// Render a chart part as a `### Chart` markdown table (mirrors Python).
fn render_chart(
    rid: &str,
    rels: &HashMap<String, String>,
    parts: &HashMap<String, Vec<u8>>,
) -> Option<String> {
    let target = rels.get(rid)?;
    let resolved = resolve_relative("ppt/slides", target);
    let bytes = parts.get(&resolved)?;
    let xml = String::from_utf8_lossy(bytes);

    let chart = parse_chart(&xml);
    if chart.categories.is_empty() && chart.series.is_empty() {
        return None;
    }

    let mut md = String::from("\n\n### Chart");
    if let Some(title) = &chart.title {
        md.push_str(&format!(": {title}"));
    }
    md.push_str("\n\n");

    let mut rows: Vec<Vec<String>> = Vec::new();
    let mut header = vec!["Category".to_string()];
    header.extend(chart.series.iter().map(|s| s.name.clone()));
    rows.push(header);
    for (i, cat) in chart.categories.iter().enumerate() {
        let mut row = vec![cat.clone()];
        for s in &chart.series {
            row.push(s.values.get(i).cloned().unwrap_or_default());
        }
        rows.push(row);
    }
    md.push_str(&text::rows_to_markdown_table(&rows));
    Some(md)
}

struct ChartData {
    title: Option<String>,
    categories: Vec<String>,
    series: Vec<ChartSeries>,
}

struct ChartSeries {
    name: String,
    values: Vec<String>,
}

fn parse_chart(xml: &str) -> ChartData {
    let mut reader = Reader::from_str(xml);
    let mut title: Option<String> = None;
    let mut categories: Vec<String> = Vec::new();
    let mut series: Vec<ChartSeries> = Vec::new();

    let mut path: Vec<Vec<u8>> = Vec::new();
    let mut text_buf = String::new();
    let mut cur_series_name = String::new();
    let mut cur_series_vals: Vec<String> = Vec::new();
    let mut cur_cat: Vec<String> = Vec::new();
    let mut first_series_done = false;

    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => {
                let local = e.name().as_ref().to_vec();
                if local.as_slice() == b"c:ser" {
                    cur_series_name.clear();
                    cur_series_vals.clear();
                    cur_cat.clear();
                }
                path.push(local);
            }
            Ok(Event::Text(t)) => {
                let raw = t.decode().unwrap_or_default();
                text_buf = unescape(&raw)
                    .map(|c| c.into_owned())
                    .unwrap_or_else(|_| raw.into_owned());
            }
            Ok(Event::End(e)) => {
                let local = e.name().as_ref().to_vec();
                let in_title = path.iter().any(|p| p == b"c:title");
                // Chart title text lives in `a:t` runs inside `c:title/c:tx/c:rich`.
                if local == b"a:t" && in_title && title.is_none() {
                    let val = text_buf.trim().to_string();
                    if !val.is_empty() {
                        title = Some(val);
                    }
                }
                if local == b"c:v" {
                    let val = text_buf.trim().to_string();
                    // Series name: `c:tx` outside `c:title` (string reference).
                    let in_tx = path.iter().any(|p| p == b"c:tx");
                    let in_cat = path.iter().any(|p| p == b"c:cat");
                    let in_val = path.iter().any(|p| p == b"c:val");
                    if in_tx && !in_title {
                        cur_series_name = val.clone();
                    } else if in_cat && !first_series_done {
                        cur_cat.push(val.clone());
                    } else if in_val {
                        cur_series_vals.push(val.clone());
                    }
                }
                if local == b"c:ser" {
                    if !first_series_done {
                        categories = std::mem::take(&mut cur_cat);
                        first_series_done = true;
                    }
                    let name = if cur_series_name.is_empty() {
                        format!("Series {}", series.len() + 1)
                    } else {
                        std::mem::take(&mut cur_series_name)
                    };
                    series.push(ChartSeries {
                        name,
                        values: std::mem::take(&mut cur_series_vals),
                    });
                }
                text_buf.clear();
                path.pop();
            }
            Ok(Event::Eof) => break,
            Err(_) => break,
            _ => {}
        }
    }

    ChartData {
        title,
        categories,
        series,
    }
}

/// Resolve a relationship target relative to a part's directory.
fn resolve_relative(base_dir: &str, target: &str) -> String {
    let mut segments: Vec<&str> = base_dir.split('/').collect();
    for part in target.split('/') {
        match part {
            "." | "" => {}
            ".." => {
                segments.pop();
            }
            other => segments.push(other),
        }
    }
    segments.join("/")
}

fn slide_notes(slide_num: usize, parts: &HashMap<String, Vec<u8>>) -> Option<String> {
    let name = format!("ppt/notesSlides/notesSlide{slide_num}.xml");
    let bytes = parts.get(&name)?;
    let xml = String::from_utf8_lossy(bytes);
    Some(extract_text(&xml))
}

/// Concatenate all `a:t` text runs, separating `a:p` paragraphs with newlines.
fn extract_text(xml: &str) -> String {
    let mut reader = Reader::from_str(xml);
    let mut out = String::new();
    let mut line = String::new();
    let mut in_t = false;
    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => {
                if e.name().as_ref() == b"a:t" {
                    in_t = true;
                }
            }
            Ok(Event::Text(t)) if in_t => {
                let raw = t.decode().unwrap_or_default();
                line.push_str(&unescape(&raw).map(|c| c.into_owned()).unwrap_or_default());
            }
            Ok(Event::End(e)) => match e.name().as_ref() {
                b"a:t" => in_t = false,
                b"a:p" => {
                    out.push_str(line.trim());
                    out.push('\n');
                    line.clear();
                }
                _ => {}
            },
            Ok(Event::Eof) => break,
            Err(_) => break,
            _ => {}
        }
    }
    if !line.trim().is_empty() {
        out.push_str(line.trim());
    }
    out
}
