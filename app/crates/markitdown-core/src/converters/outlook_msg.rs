//! Outlook `.msg` → Markdown converter.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_outlook_msg_converter.py`.
//!
//! Python uses `olefile` to pull a fixed set of MAPI property streams
//! (From / To / Subject / plain-text body). We use the `msg_parser` crate,
//! which parses the OLE structure for us and exposes typed fields.
//!
//! Output layout mirrors Python exactly:
//!
//! ```text
//! # Email Message
//!
//! **From:** …
//! **To:** …
//! **Subject:** …
//!
//! ## Content
//!
//! <body>
//! ```
//!
//! DEVIATION: when a message has no plain-text body (only an RTF-compressed
//! body), Python would also come up empty for that stream. We emit the headers
//! plus a note, since no pure-Rust LZFu/RTF decompressor is wired in here.

use crate::{ConvertError, ConvertOptions, ConvertResult, Converter, StreamInfo};
use msg_parser::Outlook;

pub struct OutlookMsgConverter;

const ACCEPTED_EXTENSIONS: &[&str] = &[".msg"];
const ACCEPTED_MIMETYPES: &[&str] = &["application/vnd.ms-outlook"];

// OLE / Compound File Binary magic.
const OLE_MAGIC: [u8; 8] = [0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1];

/// Render a recipient as "Name <email>", "email", or "Name" depending on what
/// is present.
fn fmt_person(name: &str, email: &str) -> Option<String> {
    let name = name.trim();
    let email = email.trim();
    match (name.is_empty(), email.is_empty()) {
        (true, true) => None,
        (false, true) => Some(name.to_string()),
        (true, false) => Some(email.to_string()),
        (false, false) => {
            if name == email {
                Some(email.to_string())
            } else {
                Some(format!("{name} <{email}>"))
            }
        }
    }
}

impl Converter for OutlookMsgConverter {
    fn name(&self) -> &'static str {
        "outlook_msg"
    }

    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool {
        if info.extension_is(ACCEPTED_EXTENSIONS) || info.mimetype_is(ACCEPTED_MIMETYPES) {
            return true;
        }
        // OLE magic sanity check (a .msg is a Compound File). Not sufficient on
        // its own to prove it's an Outlook message, but the registry will fall
        // through to the next converter if parsing fails.
        data.starts_with(&OLE_MAGIC)
    }

    fn convert(
        &self,
        data: &[u8],
        _info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let outlook = Outlook::from_slice(data).map_err(|e| {
            ConvertError::conversion("outlook_msg", format!("failed to parse .msg: {e}"))
        })?;

        let mut md = String::from("# Email Message\n\n");

        if let Some(from) = fmt_person(&outlook.sender.name, &outlook.sender.email) {
            md.push_str(&format!("**From:** {from}\n"));
        }

        let to: Vec<String> = outlook
            .to
            .iter()
            .filter_map(|p| fmt_person(&p.name, &p.email))
            .collect();
        if !to.is_empty() {
            md.push_str(&format!("**To:** {}\n", to.join("; ")));
        }

        let subject = outlook.subject.trim();
        if !subject.is_empty() {
            md.push_str(&format!("**Subject:** {subject}\n"));
        }

        md.push_str("\n## Content\n\n");

        let mut degraded = false;
        let body = outlook.body.trim();
        if !body.is_empty() {
            md.push_str(body);
        } else if !outlook.html.trim().is_empty() {
            md.push_str(outlook.html.trim());
        } else {
            md.push_str(
                "<!-- This message has no plain-text body. Its body is RTF-compressed, \
                 which this pure-Rust converter does not decode. -->",
            );
            // The Python engine decodes compressed-RTF bodies; let Auto retry.
            degraded = true;
        }

        let title = if subject.is_empty() {
            None
        } else {
            Some(subject.to_string())
        };

        let mut result = ConvertResult::new(md.trim().to_string());
        if degraded {
            result = result.with_degraded();
        }
        if let Some(t) = title {
            result = result.with_title(t);
        }
        Ok(result)
    }
}
