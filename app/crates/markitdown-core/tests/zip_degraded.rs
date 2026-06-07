//! ZIP archives must propagate the `degraded` flag from their children so
//! Engine::Auto can retry the whole archive through the Python engine
//! (e.g. a zip full of scanned PDFs).

use markitdown_core::{MarkItDown, StreamInfo};
use std::io::Write;

fn fixture_bytes(name: &str) -> Vec<u8> {
    std::fs::read(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../../../packages/markitdown/tests/test_files")
            .join(name),
    )
    .unwrap()
}

fn build_zip(entries: &[(&str, &[u8])]) -> Vec<u8> {
    let mut buf = std::io::Cursor::new(Vec::new());
    {
        let mut w = zip::ZipWriter::new(&mut buf);
        let opts = zip::write::SimpleFileOptions::default()
            .compression_method(zip::CompressionMethod::Stored);
        for (name, data) in entries {
            w.start_file(*name, opts).unwrap();
            w.write_all(data).unwrap();
        }
        w.finish().unwrap();
    }
    buf.into_inner()
}

#[test]
fn zip_with_degraded_child_is_degraded() {
    // mp3 children are degraded (no local transcription).
    let data = build_zip(&[
        ("notes.txt", b"hello world"),
        ("song.mp3", &fixture_bytes("test.mp3")),
    ]);
    let r = MarkItDown::new()
        .convert_bytes(&data, StreamInfo::new().with_extension(".zip"))
        .unwrap();
    assert!(r.markdown.contains("## File: notes.txt"));
    assert!(r.markdown.contains("## File: song.mp3"));
    assert!(r.degraded, "degraded child must propagate to the archive");
}

#[test]
fn zip_with_unreadable_child_is_degraded() {
    let data = build_zip(&[
        ("notes.txt", b"hello world"),
        ("mystery.bin", &fixture_bytes("random.bin")),
    ]);
    let r = MarkItDown::new()
        .convert_bytes(&data, StreamInfo::new().with_extension(".zip"))
        .unwrap();
    // Unsupported child silently skipped (Python parity) but flagged.
    assert!(!r.markdown.contains("mystery.bin"));
    assert!(r.degraded, "unconvertible child must flag the archive");
}

#[test]
fn zip_of_clean_files_is_not_degraded() {
    let data = build_zip(&[
        ("a.txt", b"alpha"),
        ("b.md", b"# beta"),
    ]);
    let r = MarkItDown::new()
        .convert_bytes(&data, StreamInfo::new().with_extension(".zip"))
        .unwrap();
    assert!(r.markdown.contains("alpha"));
    assert!(!r.degraded, "clean archives must stay on the fast path");
}
