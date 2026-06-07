//! XLSX / XLS → Markdown converter.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_xlsx_converter.py`
//! (both `XlsxConverter` and `XlsConverter`). Each worksheet is emitted as
//! `## <SheetName>` followed by a GFM table whose first row is the header,
//! mirroring pandas' `read_excel(...).to_html(index=False)` round-trip.
//!
//! Parsing is done with `calamine` instead of openpyxl/xlrd.

use std::io::Cursor;

use calamine::{open_workbook_auto_from_rs, Data, Reader};

use crate::text::rows_to_markdown_table;
use crate::{ConvertError, ConvertOptions, ConvertResult, Converter, StreamInfo};

const ACCEPTED_XLSX_MIME_TYPE_PREFIXES: &[&str] =
    &["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
const ACCEPTED_XLSX_FILE_EXTENSIONS: &[&str] = &[".xlsx"];

const ACCEPTED_XLS_MIME_TYPE_PREFIXES: &[&str] =
    &["application/vnd.ms-excel", "application/excel"];
const ACCEPTED_XLS_FILE_EXTENSIONS: &[&str] = &[".xls"];

pub struct XlsxConverter;
pub struct XlsConverter;

fn mimetype_has_prefix(info: &StreamInfo, prefixes: &[&str]) -> bool {
    if let Some(mt) = &info.mimetype {
        let mt = mt.split(';').next().unwrap_or(mt).trim().to_ascii_lowercase();
        return prefixes.iter().any(|p| mt.starts_with(p));
    }
    false
}

/// Render a `calamine` cell exactly like the Display impl, but treat the
/// empty cell as an empty string (so `rows_to_markdown_table` pads correctly).
fn cell_to_string(cell: &Data) -> String {
    match cell {
        Data::Empty => String::new(),
        other => other.to_string(),
    }
}

/// Convert the spreadsheet bytes into Markdown: one `## sheet` + table per sheet.
fn convert_workbook(name: &'static str, data: &[u8]) -> Result<ConvertResult, ConvertError> {
    let mut workbook = open_workbook_auto_from_rs(Cursor::new(data.to_vec()))
        .map_err(|e| ConvertError::conversion(name, e.to_string()))?;

    let mut md = String::new();
    for sheet in workbook.sheet_names() {
        let range = workbook
            .worksheet_range(&sheet)
            .map_err(|e| ConvertError::conversion(name, e.to_string()))?;

        md.push_str("## ");
        md.push_str(&sheet);
        md.push('\n');

        let rows: Vec<Vec<String>> = range
            .rows()
            .map(|row| row.iter().map(cell_to_string).collect())
            .collect();

        let table = rows_to_markdown_table(&rows);
        md.push_str(table.trim());
        md.push_str("\n\n");
    }

    Ok(ConvertResult::new(md.trim().to_string()))
}

impl Converter for XlsxConverter {
    fn name(&self) -> &'static str {
        "xlsx"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        info.extension_is(ACCEPTED_XLSX_FILE_EXTENSIONS)
            || mimetype_has_prefix(info, ACCEPTED_XLSX_MIME_TYPE_PREFIXES)
    }

    fn convert(
        &self,
        data: &[u8],
        _info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        convert_workbook("xlsx", data)
    }
}

impl Converter for XlsConverter {
    fn name(&self) -> &'static str {
        "xls"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        info.extension_is(ACCEPTED_XLS_FILE_EXTENSIONS)
            || mimetype_has_prefix(info, ACCEPTED_XLS_MIME_TYPE_PREFIXES)
    }

    fn convert(
        &self,
        data: &[u8],
        _info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        convert_workbook("xls", data)
    }
}
