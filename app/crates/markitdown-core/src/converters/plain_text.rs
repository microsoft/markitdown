//! Plain text / Markdown / JSON passthrough.
//! Port of `_plain_text_converter.py`: decode with the detected charset and
//! return the text as-is (Markdown is already Markdown; JSON is readable).

use crate::text::decode_text;
use crate::{Converter, ConvertError, ConvertOptions, ConvertResult, StreamInfo};

const EXTENSIONS: &[&str] = &[".txt", ".text", ".md", ".markdown", ".json", ".jsonl"];
const MIMETYPES: &[&str] = &[
    "application/json",
    "application/markdown",
    "application/x-ndjson",
];

pub struct PlainTextConverter;

impl Converter for PlainTextConverter {
    fn name(&self) -> &'static str {
        "plain-text"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        if info.extension_is(EXTENSIONS) || info.mimetype_is(MIMETYPES) {
            return true;
        }
        // Any text/* mimetype that a more specific converter didn't claim.
        matches!(&info.mimetype, Some(mt) if mt.starts_with("text/"))
    }

    fn convert(
        &self,
        data: &[u8],
        info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        Ok(ConvertResult::new(decode_text(data, info)))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn accepts_text_and_json() {
        let c = PlainTextConverter;
        assert!(c.accepts(&StreamInfo::new().with_extension(".md"), b""));
        assert!(c.accepts(&StreamInfo::new().with_mimetype("text/plain"), b""));
        assert!(c.accepts(&StreamInfo::new().with_mimetype("application/json"), b""));
        assert!(!c.accepts(&StreamInfo::new().with_mimetype("application/pdf"), b""));
    }

    #[test]
    fn passthrough_utf8() {
        let c = PlainTextConverter;
        let info = StreamInfo::new().with_charset("utf-8");
        let r = c
            .convert("# héllo".as_bytes(), &info, &ConvertOptions::default())
            .unwrap();
        assert_eq!(r.markdown, "# héllo");
    }
}
