//! Stream-type detection: extension map + magic bytes (`file-format` crate,
//! replacing Python's Magika model) + charset sniffing (`chardetng`).

use crate::stream_info::{normalize_extension, StreamInfo};
use file_format::FileFormat;

/// Map a file extension (with dot, lowercase) to a mimetype.
pub fn mimetype_for_extension(ext: &str) -> Option<&'static str> {
    Some(match ext {
        ".pdf" => "application/pdf",
        ".docx" => "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx" => "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls" => "application/vnd.ms-excel",
        ".pptx" => "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".html" | ".htm" => "text/html",
        ".xhtml" => "application/xhtml+xml",
        ".csv" => "text/csv",
        ".json" => "application/json",
        ".jsonl" => "application/json",
        ".ipynb" => "application/json",
        ".md" | ".markdown" => "text/markdown",
        ".txt" | ".text" => "text/plain",
        ".xml" => "text/xml",
        ".rss" => "application/rss+xml",
        ".atom" => "application/atom+xml",
        ".epub" => "application/epub+zip",
        ".zip" => "application/zip",
        ".msg" => "application/vnd.ms-outlook",
        ".jpg" | ".jpeg" => "image/jpeg",
        ".png" => "image/png",
        ".gif" => "image/gif",
        ".webp" => "image/webp",
        ".tiff" | ".tif" => "image/tiff",
        ".wav" => "audio/x-wav",
        ".mp3" => "audio/mpeg",
        ".m4a" => "audio/mp4",
        ".flac" => "audio/flac",
        ".mp4" => "video/mp4",
        _ => return None,
    })
}

/// Enrich `info` using the file name, magic bytes and charset detection.
/// Caller-provided hints always win over detection (same as Python).
pub fn enrich(data: &[u8], mut info: StreamInfo) -> StreamInfo {
    // 1. Extension from filename / local path.
    if info.extension.is_none() {
        let name = info
            .filename
            .clone()
            .or_else(|| {
                info.local_path
                    .as_ref()
                    .and_then(|p| p.file_name().map(|n| n.to_string_lossy().into_owned()))
            })
            .or_else(|| {
                info.url
                    .as_ref()
                    .map(|u| u.split(['?', '#']).next().unwrap_or(u).to_string())
            });
        if let Some(name) = name {
            if let Some((_, ext)) = name.rsplit_once('.') {
                if !ext.is_empty() && ext.len() <= 10 && !ext.contains('/') {
                    info.extension = Some(normalize_extension(ext));
                }
            }
        }
    }

    // 2. Mimetype from extension.
    if info.mimetype.is_none() {
        if let Some(ext) = &info.extension {
            info.mimetype = mimetype_for_extension(ext).map(str::to_string);
        }
    }

    // 3. Magic-byte detection fills any remaining gaps (and catches files
    //    whose extension lies about a binary container).
    if info.mimetype.is_none() || info.extension.is_none() {
        let fmt = FileFormat::from_bytes(data);
        // `from_bytes` falls back to ARBITRARY_BINARY_DATA / PLAIN_TEXT when
        // nothing matches; both are still useful hints here.
        if info.mimetype.is_none() {
            info.mimetype = Some(fmt.media_type().to_string());
        }
        if info.extension.is_none() {
            info.extension = Some(normalize_extension(fmt.extension()));
        }
    }

    // 4. Charset sniffing for text-like streams.
    if info.charset.is_none() && looks_textual(&info) {
        let mut det = chardetng::EncodingDetector::new(chardetng::Iso2022JpDetection::Allow);
        let sample = &data[..data.len().min(64 * 1024)];
        det.feed(sample, data.len() <= 64 * 1024);
        let enc = det.guess(None, chardetng::Utf8Detection::Allow);
        info.charset = Some(enc.name().to_ascii_lowercase());
    }

    info
}

fn looks_textual(info: &StreamInfo) -> bool {
    if let Some(mt) = &info.mimetype {
        let mt = mt.split(';').next().unwrap_or(mt).trim();
        return mt.starts_with("text/")
            || matches!(
                mt,
                "application/json"
                    | "application/xml"
                    | "application/xhtml+xml"
                    | "application/rss+xml"
                    | "application/atom+xml"
                    | "application/markdown"
                    | "application/x-ipynb+json"
            );
    }
    false
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn extension_drives_mimetype() {
        let info = enrich(b"hello", StreamInfo::new().with_filename("a.pdf"));
        assert_eq!(info.extension.as_deref(), Some(".pdf"));
        assert_eq!(info.mimetype.as_deref(), Some("application/pdf"));
    }

    #[test]
    fn magic_bytes_detect_png() {
        let png = b"\x89PNG\r\n\x1a\n\0\0\0\rIHDR";
        let info = enrich(png, StreamInfo::new());
        assert_eq!(info.mimetype.as_deref(), Some("image/png"));
    }

    #[test]
    fn charset_detected_for_text() {
        let info = enrich(
            "héllo wörld".as_bytes(),
            StreamInfo::new().with_mimetype("text/plain"),
        );
        assert_eq!(info.charset.as_deref(), Some("utf-8"));
    }
}
