//! Image → Markdown converter.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_image_converter.py`.
//!
//! DEVIATION FROM PYTHON: Python shells out to `exiftool` to gather metadata
//! and emits a fixed list of keys (`ImageSize`, `Title`, `Caption`,
//! `Description`, `Keywords`, `Artist`, `Author`, `DateTimeOriginal`,
//! `CreateDate`, `GPSPosition`). We have no exiftool; instead we read EXIF with
//! `kamadak-exif` and emit every EXIF field as `TagName: value` (the tag names
//! kamadak uses are the canonical EXIF names, e.g. `Model`, `DateTimeOriginal`,
//! `ImageDescription`, `GPSLatitude`, …). We additionally emit an `ImageSize:
//! WIDTHxHEIGHT` line derived from `imagesize::blob_size` (mirroring Python's
//! `ImageSize` key) plus a `Format:` line.
//!
//! LLM-based image description (Python's `_get_llm_description`) is NOT ported;
//! it requires a multimodal LLM client.
//!
//! Missing EXIF is not an error — PNGs frequently carry none. We still emit the
//! dimensions and format.

use crate::{ConvertError, ConvertOptions, ConvertResult, Converter, StreamInfo};
use std::io::Cursor;

pub struct ImageConverter;

// Python accepts only jpg/jpeg/png; we additionally accept gif/webp/tiff/bmp
// since `imagesize` handles them and EXIF absence is non-fatal.
const ACCEPTED_EXTENSIONS: &[&str] = &[
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".tif", ".bmp",
];
const ACCEPTED_MIMETYPES: &[&str] = &[
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/tiff",
    "image/bmp",
];

fn detect_format(data: &[u8]) -> Option<&'static str> {
    if data.starts_with(&[0xFF, 0xD8, 0xFF]) {
        Some("JPEG")
    } else if data.starts_with(b"\x89PNG\r\n\x1a\n") {
        Some("PNG")
    } else if data.starts_with(b"GIF87a") || data.starts_with(b"GIF89a") {
        Some("GIF")
    } else if data.len() >= 12 && &data[0..4] == b"RIFF" && &data[8..12] == b"WEBP" {
        Some("WEBP")
    } else if data.starts_with(b"II*\x00") || data.starts_with(b"MM\x00*") {
        Some("TIFF")
    } else if data.starts_with(b"BM") {
        Some("BMP")
    } else {
        None
    }
}

impl Converter for ImageConverter {
    fn name(&self) -> &'static str {
        "image"
    }

    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_EXTENSIONS) || info.mimetype_is(ACCEPTED_MIMETYPES) {
            return true;
        }
        detect_format(data).is_some()
    }

    fn convert(
        &self,
        data: &[u8],
        info: &StreamInfo,
        opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let mut md = String::new();

        // Dimensions via imagesize (mirrors Python's `ImageSize` key).
        if let Ok(size) = imagesize::blob_size(data) {
            md.push_str(&format!("ImageSize: {}x{}\n", size.width, size.height));
        }

        // Format line (derived from magic bytes).
        if let Some(fmt) = detect_format(data) {
            md.push_str(&format!("Format: {fmt}\n"));
        }

        // EXIF metadata — absence is not an error.
        let mut cursor = Cursor::new(data);
        if let Ok(exif) = exif::Reader::new().read_from_container(&mut cursor) {
            for field in exif.fields() {
                let value = field.display_value().with_unit(&exif).to_string();
                let value = value.trim();
                if value.is_empty() {
                    continue;
                }
                md.push_str(&format!("{}: {}\n", field.tag, value));
            }
        }

        // LLM caption (OpenAI-compatible API), mirroring Python's
        // `# Description:` section. Library-only in Python; env/option
        // driven here — see crate::llm_caption.
        let mut captioned = false;
        if let Some(cfg) = crate::llm_caption::resolve(opts) {
            let mimetype = info
                .mimetype
                .clone()
                .or_else(|| {
                    detect_format(data).map(|f| match f {
                        "JPEG" => "image/jpeg".to_string(),
                        "PNG" => "image/png".to_string(),
                        "GIF" => "image/gif".to_string(),
                        "WEBP" => "image/webp".to_string(),
                        "TIFF" => "image/tiff".to_string(),
                        "BMP" => "image/bmp".to_string(),
                        other => format!("image/{}", other.to_ascii_lowercase()),
                    })
                })
                .unwrap_or_else(|| "application/octet-stream".to_string());
            if let Some(caption) = crate::llm_caption::caption_image(data, &mimetype, &cfg) {
                md.push_str(&format!("\n# Description:\n{caption}\n"));
                captioned = true;
            }
        }

        // Degraded (unless captioned): the Python engine (markitdown-ocr
        // plugin) can add OCR text on top of this metadata.
        let result = ConvertResult::new(md);
        Ok(if captioned {
            result
        } else {
            result.with_degraded()
        })
    }
}
