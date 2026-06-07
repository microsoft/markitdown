//! Shared text utilities: charset decoding and Markdown table emission.

use crate::StreamInfo;

/// Decode raw bytes to a `String` using the charset hint when present,
/// falling back to chardetng detection, then lossy UTF-8.
pub fn decode_text(data: &[u8], info: &StreamInfo) -> String {
    // BOM-aware fast path first.
    if let Some((enc, _)) = encoding_rs::Encoding::for_bom(data) {
        let (text, _, _) = enc.decode(data);
        return text.into_owned();
    }
    if let Some(label) = &info.charset {
        if let Some(enc) = encoding_rs::Encoding::for_label(label.as_bytes()) {
            let (text, _, _) = enc.decode(data);
            return text.into_owned();
        }
    }
    let mut det = chardetng::EncodingDetector::new(chardetng::Iso2022JpDetection::Allow);
    det.feed(&data[..data.len().min(64 * 1024)], data.len() <= 64 * 1024);
    let enc = det.guess(None, chardetng::Utf8Detection::Allow);
    let (text, _, _) = enc.decode(data);
    text.into_owned()
}

/// Escape a cell value for use inside a GitHub-flavored Markdown table.
pub fn escape_table_cell(value: &str) -> String {
    value
        .replace('\\', "\\\\")
        .replace('|', "\\|")
        .replace('\r', " ")
        .replace('\n', "<br>")
        .trim()
        .to_string()
}

/// Render rows as a GFM table. The first row is the header. Rows shorter than
/// the widest row are padded with empty cells.
pub fn rows_to_markdown_table(rows: &[Vec<String>]) -> String {
    if rows.is_empty() {
        return String::new();
    }
    let width = rows.iter().map(Vec::len).max().unwrap_or(0);
    if width == 0 {
        return String::new();
    }
    let mut out = String::new();
    let render = |row: &[String], out: &mut String| {
        out.push('|');
        for i in 0..width {
            let cell = row.get(i).map(|c| escape_table_cell(c)).unwrap_or_default();
            out.push(' ');
            out.push_str(&cell);
            out.push_str(" |");
        }
        out.push('\n');
    };
    render(&rows[0], &mut out);
    out.push('|');
    for _ in 0..width {
        out.push_str(" --- |");
    }
    out.push('\n');
    for row in &rows[1..] {
        render(row, &mut out);
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn table_rendering_pads_and_escapes() {
        let rows = vec![
            vec!["a".into(), "b|c".into()],
            vec!["1".into()],
        ];
        let md = rows_to_markdown_table(&rows);
        assert_eq!(md, "| a | b\\|c |\n| --- | --- |\n| 1 |  |\n");
    }

    #[test]
    fn decode_respects_charset_hint() {
        // "テスト" in Shift-JIS
        let sjis: &[u8] = &[0x83, 0x65, 0x83, 0x58, 0x83, 0x67];
        let info = StreamInfo::new().with_charset("shift_jis");
        assert_eq!(decode_text(sjis, &info), "テスト");
    }
}
