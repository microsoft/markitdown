//! Integration tests for the data-format converters (xlsx, xls, csv, ipynb)
//! plus a JSON fixture that falls through to the plain-text converter.
//!
//! Each test converts a real fixture from the Python test suite through the
//! full `MarkItDown` registry and asserts the same `must_include` substrings
//! used by `packages/markitdown/tests/_test_vectors.py`.

use markitdown_core::MarkItDown;

fn fixture(name: &str) -> std::path::PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

fn convert(name: &str) -> markitdown_core::ConvertResult {
    MarkItDown::new()
        .convert_path(fixture(name))
        .unwrap_or_else(|e| panic!("conversion of {name} failed: {e}"))
}

#[test]
fn xlsx_emits_sheet_headers_and_values() {
    let md = convert("test.xlsx").markdown;
    // Sheet headers are rendered as `## <SheetName>`.
    assert!(
        md.contains("## 09060124-b5e7-4717-9d07-3c046eb"),
        "missing xlsx sheet header in:\n{md}"
    );
    assert!(md.contains("6ff4173b-42a5-4784-9b19-f49caff4d93d"), "missing cell value");
    assert!(md.contains("affc7dad-52dc-4b98-9b5d-51e65d8a8ad0"), "missing cell value");
    // A GFM table separator should be present.
    assert!(md.contains("---"), "expected a markdown table separator");
}

#[test]
fn xls_emits_sheet_headers_and_values() {
    let md = convert("test.xls").markdown;
    assert!(
        md.contains("## 09060124-b5e7-4717-9d07-3c046eb"),
        "missing xls sheet header in:\n{md}"
    );
    assert!(md.contains("6ff4173b-42a5-4784-9b19-f49caff4d93d"), "missing cell value");
    assert!(md.contains("affc7dad-52dc-4b98-9b5d-51e65d8a8ad0"), "missing cell value");
}

#[test]
fn csv_shift_jis_decodes_and_tabulates() {
    // test_mskanji.csv is Shift-JIS / cp932 encoded; charset is auto-detected.
    let md = convert("test_mskanji.csv").markdown;
    assert!(md.contains("| 名前 | 年齢 | 住所 |"), "missing header row in:\n{md}");
    assert!(md.contains("| --- | --- | --- |"), "missing separator row");
    assert!(md.contains("| 佐藤太郎 | 30 | 東京 |"), "missing data row");
    assert!(md.contains("| 三木英子 | 25 | 大阪 |"), "missing data row");
    assert!(md.contains("| 髙橋淳 | 35 | 名古屋 |"), "missing data row");
}

#[test]
fn ipynb_renders_cells_and_strips_nbformat() {
    let result = convert("test_notebook.ipynb");
    let md = result.markdown;
    assert!(md.contains("# Test Notebook"), "missing markdown heading in:\n{md}");
    assert!(md.contains("```python"), "missing python code fence");
    assert!(md.contains("print(\"markitdown\")"), "missing code cell content");
    assert!(md.contains("## Code Cell Below"), "missing later markdown cell");
    // Notebook JSON metadata must not leak into the output.
    assert!(!md.contains("nbformat"), "nbformat leaked into output");
    assert!(!md.contains("nbformat_minor"), "nbformat_minor leaked into output");
    // `metadata.title` overrides the first `# ` heading (Python parity).
    assert_eq!(result.title.as_deref(), Some("Test Notebook Title"));
}

#[test]
fn json_falls_through_to_plain_text() {
    // test.json is application/json but not a notebook, so it is emitted as-is
    // by the plain-text fallback converter.
    let md = convert("test.json").markdown;
    assert!(md.contains("5b64c88c-b3c3-4510-bcb8-da0b200602d8"), "missing json value in:\n{md}");
    assert!(md.contains("9700dc99-6685-40b4-9a3a-5e406dcb37f3"), "missing json value");
}
