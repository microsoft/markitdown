//! Integration tests for the media converters (PDF, image, audio, Outlook .msg)
//! against the shared Python test fixtures.
//!
//! Python's image/audio vectors are exiftool-specific (the upstream
//! `_test_vectors.py` has no fixed must_include strings for them), so here we
//! assert on stable content that genuinely originates from each fixture's
//! EXIF / tag metadata, discovered by running the converters.

use markitdown_core::{ConvertError, MarkItDown};
use std::path::PathBuf;

fn fixture(name: &str) -> PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../../packages/markitdown/tests/test_files")
        .join(name)
}

fn convert(name: &str) -> String {
    MarkItDown::new()
        .convert_path(fixture(name))
        .unwrap_or_else(|e| panic!("convert {name} failed: {e}"))
        .markdown
}

// ---------------------------------------------------------------------------
// PDF
// ---------------------------------------------------------------------------

#[test]
fn pdf_extracts_linear_text() {
    let md = convert("test.pdf");
    // Same must_include substring the Python vector asserts on.
    assert!(
        md.contains("While there is contemporaneous exploration of multi-agent approaches"),
        "PDF body text missing; got:\n{md}"
    );
}

#[test]
fn pdf_collapses_excess_blank_lines() {
    let md = convert("test.pdf");
    assert!(
        !md.contains("\n\n\n"),
        "newlines should be collapsed to at most 2"
    );
}

// ---------------------------------------------------------------------------
// Image (EXIF via kamadak-exif + dimensions via imagesize)
// ---------------------------------------------------------------------------

#[test]
fn image_emits_dimensions() {
    let md = convert("test.jpg");
    // 1615x1967 is the genuine pixel size of the fixture (from imagesize).
    assert!(md.contains("ImageSize: 1615x1967"), "got:\n{md}");
    assert!(md.contains("Format: JPEG"), "got:\n{md}");
}

#[test]
fn image_emits_exif_fields() {
    let md = convert("test.jpg");
    // DateTimeOriginal is a real EXIF tag embedded in the fixture.
    assert!(
        md.contains("DateTimeOriginal: 2024-03-14 22:10:00"),
        "expected real EXIF DateTimeOriginal; got:\n{md}"
    );
}

// ---------------------------------------------------------------------------
// Audio (tags + properties via lofty)
// ---------------------------------------------------------------------------

#[test]
fn wav_emits_properties() {
    let md = convert("test.wav");
    assert!(md.contains("Duration:"), "got:\n{md}");
    assert!(md.contains("SampleRate: 48000 Hz"), "got:\n{md}");
    assert!(md.contains("Channels: 2"), "got:\n{md}");
    assert!(
        md.contains("transcription requires the optional Python engine"),
        "missing transcription note; got:\n{md}"
    );
}

#[test]
fn mp3_emits_id3_tags() {
    let md = convert("test.mp3");
    // Genuine ID3 tags embedded in the fixture.
    assert!(
        md.contains("Artist: Artist Name Test String"),
        "got:\n{md}"
    );
    assert!(md.contains("Album: Album Name Test String"), "got:\n{md}");
    assert!(md.contains("Duration:"), "got:\n{md}");
}

#[test]
fn m4a_emits_properties() {
    let md = convert("test.m4a");
    assert!(md.contains("Duration:"), "got:\n{md}");
    assert!(md.contains("SampleRate: 48000 Hz"), "got:\n{md}");
}

// ---------------------------------------------------------------------------
// Outlook .msg
// ---------------------------------------------------------------------------

#[test]
fn outlook_msg_emits_headers_and_body() {
    let result = MarkItDown::new()
        .convert_path(fixture("test_outlook_msg.msg"))
        .expect("convert .msg");
    let md = &result.markdown;

    assert!(md.contains("# Email Message"), "got:\n{md}");
    // msg_parser exposes the sender display name; assert the email (stable).
    assert!(md.contains("**From:**"), "got:\n{md}");
    assert!(md.contains("test.sender@example.com"), "got:\n{md}");
    assert!(md.contains("**To:** test.recipient@example.com"), "got:\n{md}");
    assert!(md.contains("**Subject:** Test Email Message"), "got:\n{md}");
    assert!(md.contains("## Content"), "got:\n{md}");
    assert!(
        md.contains("This is the body of the test email message"),
        "got:\n{md}"
    );
    assert_eq!(result.title.as_deref(), Some("Test Email Message"));
}

// ---------------------------------------------------------------------------
// Negative: random bytes must be unsupported.
// ---------------------------------------------------------------------------

#[test]
fn random_bin_is_unsupported() {
    let err = MarkItDown::new()
        .convert_path(fixture("random.bin"))
        .expect_err("random.bin should not convert");
    assert!(
        matches!(err, ConvertError::UnsupportedFormat(_)),
        "expected UnsupportedFormat, got: {err:?}"
    );
}
