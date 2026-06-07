//! Integration tests for the container/OOXML converters (DOCX, PPTX, EPUB, ZIP).
//!
//! The `must_include` substrings are taken from the Python reference test
//! vectors in `packages/markitdown/tests/_test_vectors.py`. Where our Rust port
//! deviates from the Python output the deviation is documented inline.

use markitdown_core::MarkItDown;

fn fixture(name: &str) -> std::path::PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

fn convert(name: &str) -> String {
    MarkItDown::new()
        .convert_path(fixture(name))
        .unwrap_or_else(|e| panic!("conversion of {name} failed: {e}"))
        .markdown
}

fn assert_includes(md: &str, needles: &[&str], file: &str) {
    for n in needles {
        assert!(
            md.contains(n),
            "expected `{n}` in {file} output, got:\n{md}"
        );
    }
}

#[test]
fn docx_test_vectors() {
    let md = convert("test.docx");
    // Substrings from GENERAL_TEST_VECTORS["test.docx"].
    assert_includes(
        &md,
        &[
            "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
            "49e168b7-d2ae-407f-a055-2167576f39a1",
            "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
            "# Abstract",
            "# Introduction",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            // Truncated data URI (keep_data_uris is off by default).
            "data:image/png;base64...",
        ],
        "test.docx",
    );
    // must_not_include: the full base64 payload must not leak when truncating.
    assert!(
        !md.contains("data:image/png;base64,iVBORw0KGgoAAAANSU"),
        "default conversion must not emit the full base64 image payload"
    );
}

#[test]
fn docx_with_comment_converts() {
    // The Python vectors for test_with_comment.docx exercise comment extraction,
    // which is a Python-only (mammoth) feature we do not implement. We instead
    // assert the body text the file shares with test.docx and that it converts
    // without error. (Deviation: no comment text in output.)
    let md = convert("test_with_comment.docx");
    assert_includes(
        &md,
        &[
            "# Abstract",
            "# Introduction",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
        ],
        "test_with_comment.docx",
    );
}

#[test]
fn docx_equations_converts_without_error() {
    // OMML math fidelity is out of scope; we only require that the file converts
    // without error and yields non-empty output.
    let md = convert("equations.docx");
    assert!(!md.trim().is_empty(), "equations.docx produced empty output");
}

#[test]
fn docx_hyperlinks_converts() {
    // rlink.docx exercises hyperlink resolution; require it converts cleanly.
    let md = convert("rlink.docx");
    assert!(!md.trim().is_empty(), "rlink.docx produced empty output");
}

#[test]
fn pptx_test_vectors() {
    let md = convert("test.pptx");
    // Substrings from GENERAL_TEST_VECTORS["test.pptx"].
    assert_includes(
        &md,
        &[
            "2cdda5c8-e50e-4db4-b5f0-9722a649f455",
            "04191ea8-5c73-4215-a1d3-1cfb43aaaf12",
            "44bf7d06-5e7a-4a40-a2e1-a2e42ef28c8a",
            "1b92870d-e3b5-4e65-8153-919f4ff45592",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            "a3f6004b-6f4f-4ea8-bee3-3741f4dc385f", // chart title
            "2003",                                 // chart category value
            "![This phrase of the caption is Human-written.](Picture4.jpg)",
        ],
        "test.pptx",
    );
    // Slide markers must be present and in order.
    assert!(md.contains("<!-- Slide number: 1 -->"));
    // must_not_include: no full base64 image when keep_data_uris is off.
    assert!(
        !md.contains("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE"),
        "default conversion must not emit the full base64 image payload"
    );
}

#[test]
fn epub_test_vectors() {
    let md = convert("test.epub");
    // Substrings from GENERAL_TEST_VECTORS["test.epub"].
    assert_includes(
        &md,
        &[
            "**Authors:** Test Author",
            "A test EPUB document for MarkItDown testing",
            "# Chapter 1: Test Content",
            "This is a **test** paragraph with some formatting",
            "* A bullet point",
            "* Another point",
            "# Chapter 2: More Content",
            "*different* style",
            "> This is a blockquote for testing",
        ],
        "test.epub",
    );
}

#[test]
fn zip_test_vectors() {
    let md = convert("test_files.zip");
    // Substrings from GENERAL_TEST_VECTORS["test_files.zip"] that are covered by
    // the container converters under test (docx + pptx + xlsx content). The
    // Wikipedia HTML substrings depend on the HTML converter (owned elsewhere)
    // so we assert the document-format ones here.
    assert_includes(
        &md,
        &[
            "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
            "49e168b7-d2ae-407f-a055-2167576f39a1",
            "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
            "# Abstract",
            "# Introduction",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            "2cdda5c8-e50e-4db4-b5f0-9722a649f455",
            "04191ea8-5c73-4215-a1d3-1cfb43aaaf12",
            "44bf7d06-5e7a-4a40-a2e1-a2e42ef28c8a",
            "1b92870d-e3b5-4e65-8153-919f4ff45592",
        ],
        "test_files.zip",
    );
    // The recursive listing should produce per-file sections.
    assert!(md.contains("## File: "), "zip output missing file sections");
}
