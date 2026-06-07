//! Integration tests for the web converters (HTML, Wikipedia, Bing SERP, RSS).
//!
//! URLs and `must_include` substrings are taken from the Python reference
//! vectors in `packages/markitdown/tests/_test_vectors.py`.
use markitdown_core::{MarkItDown, StreamInfo};

fn fixture(name: &str) -> std::path::PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

fn convert_with_url(name: &str, url: &str) -> String {
    let p = fixture(name);
    let data = std::fs::read(&p).expect("read fixture");
    let md = MarkItDown::new();
    let res = md
        .convert_bytes(
            &data,
            StreamInfo::new().with_extension(".html").with_url(url),
        )
        .expect("conversion should succeed");
    res.markdown
}

#[test]
fn blog_html_via_path() {
    // Plain HTML (no URL) goes through the generic HtmlConverter.
    let p = fixture("test_blog.html");
    let md = MarkItDown::new();
    let res = md.convert_path(&p).expect("convert blog");
    let out = res.markdown;
    // From _test_vectors.py must_include for test_blog.html.
    assert!(
        out.contains("Large language models (LLMs) are powerful tools that can generate natural language texts for various applications, such as chatbots, summarization, translation, and more. GPT-4 is currently the state of the art LLM in the world. Is model selection irrelevant? What about inference parameters?"),
        "missing intro paragraph"
    );
    assert!(
        out.contains("an example where high cost can easily prevent a generic complex"),
        "missing cost sentence"
    );
}

#[test]
fn wikipedia_html() {
    let out = convert_with_url("test_wikipedia.html", "https://en.wikipedia.org/wiki/Microsoft");
    // must_include from _test_vectors.py
    assert!(
        out.contains("Microsoft entered the operating system (OS) business in 1980 with its own version of [Unix]"),
        "missing OS-business sentence"
    );
    assert!(
        out.contains(r#"Microsoft was founded by [Bill Gates](/wiki/Bill_Gates "Bill Gates")"#),
        "missing founders link"
    );
    // must_not_include: chrome/navigation text outside #mw-content-text.
    assert!(!out.contains("You are encouraged to create an account and log in"));
    assert!(!out.contains("154 languages"));
    assert!(!out.contains("move to sidebar"));
}

#[test]
fn bing_serp_html() {
    let out = convert_with_url("test_serp.html", "https://www.bing.com/search?q=microsoft+wikipedia");
    // The exact Python heading.
    assert!(
        out.contains("## A Bing search for 'microsoft wikipedia' found the following results:"),
        "missing SERP heading"
    );
    // must_include from _test_vectors.py
    assert!(
        out.contains("](https://en.wikipedia.org/wiki/Microsoft"),
        "missing decoded wikipedia redirect link"
    );
    assert!(
        out.contains("Microsoft Corporation is **an American multinational corporation and technology company headquartered** in Redmond"),
        "missing snippet"
    );
    assert!(
        out.contains("1995–2007: Foray into the Web, Windows 95, Windows XP, and Xbox"),
        "missing toc snippet"
    );
    // must_not_include: undecoded redirect and data URIs.
    assert!(!out.contains("https://www.bing.com/ck/a?!&&p="), "redirect not decoded");
    assert!(!out.contains("data:image/svg+xml,%3Csvg%20width%3D"), "data uri not truncated");
}

#[test]
fn rss_xml() {
    // RSS has no URL; the candidate-XML branch keys off the .xml extension and
    // a feed byte-scan.
    let p = fixture("test_rss.xml");
    let data = std::fs::read(&p).expect("read fixture");
    let md = MarkItDown::new();
    let res = md
        .convert_bytes(
            &data,
            StreamInfo::new().with_extension(".xml").with_mimetype("text/xml"),
        )
        .expect("convert rss");
    let out = res.markdown;
    // must_include from _test_vectors.py
    assert!(out.contains("# The Official Microsoft Blog"), "missing feed title");
    assert!(
        out.contains("## Ignite 2024: Why nearly 70% of the Fortune 500 now use Microsoft 365 Copilot"),
        "missing item title"
    );
    assert!(
        out.contains("In the case of AI, it is absolutely true that the industry is moving incredibly fast"),
        "missing item content"
    );
    // must_not_include: raw feed markup.
    assert!(!out.contains("<rss"), "leaked rss tag");
    assert!(!out.contains("<feed"), "leaked feed tag");
}

#[test]
fn data_uri_truncation_in_html() {
    // Inline HTML with a long base64 data: URI is truncated by default.
    let html = r#"<html><head><title>T</title></head><body>
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ" alt="pixel">
    </body></html>"#;
    let md = MarkItDown::new();
    let res = md
        .convert_bytes(html.as_bytes(), StreamInfo::new().with_extension(".html"))
        .expect("convert inline html");
    assert!(
        res.markdown.contains("data:image/png;base64..."),
        "data uri should be truncated: {}",
        res.markdown
    );
    assert!(
        !res.markdown.contains("iVBORw0KGgo"),
        "base64 payload should be dropped: {}",
        res.markdown
    );
}
