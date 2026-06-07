//! Input acquisition: local paths and `file:` / `data:` / `http(s):` URIs.
//! Port of `packages/markitdown/src/markitdown/_uri_utils.py`.

use crate::{ConvertError, StreamInfo};
use base64::Engine as _;
use percent_encoding::percent_decode_str;
use std::path::{Path, PathBuf};

/// Fetch the bytes behind `src` (path or URI) plus everything we learned
/// about the stream along the way.
pub fn read_source(src: &str) -> Result<(Vec<u8>, StreamInfo), ConvertError> {
    if let Some(rest) = src.strip_prefix("data:") {
        return read_data_uri(rest, src);
    }
    if let Some(rest) = src.strip_prefix("file://") {
        let path = file_uri_to_path(rest)?;
        return read_path(&path);
    }
    if src.starts_with("http://") || src.starts_with("https://") {
        return read_http(src);
    }
    read_path(Path::new(src))
}

/// Read a local file into memory with path-derived stream info.
pub fn read_path(path: &Path) -> Result<(Vec<u8>, StreamInfo), ConvertError> {
    let data = std::fs::read(path)?;
    let mut info = StreamInfo::new();
    info.local_path = Some(path.to_path_buf());
    if let Some(name) = path.file_name() {
        info.filename = Some(name.to_string_lossy().into_owned());
    }
    Ok((data, info))
}

fn file_uri_to_path(rest: &str) -> Result<PathBuf, ConvertError> {
    // file://host/path — we only support empty/localhost hosts.
    let (host, path) = match rest.find('/') {
        Some(i) => (&rest[..i], &rest[i..]),
        None => ("", rest),
    };
    if !host.is_empty() && host != "localhost" {
        return Err(ConvertError::InvalidInput(format!(
            "unsupported file URI host: {host}"
        )));
    }
    let decoded = percent_decode_str(path)
        .decode_utf8()
        .map_err(|e| ConvertError::InvalidInput(format!("bad file URI encoding: {e}")))?;
    Ok(PathBuf::from(decoded.into_owned()))
}

fn read_data_uri(rest: &str, full: &str) -> Result<(Vec<u8>, StreamInfo), ConvertError> {
    // data:[<mediatype>][;base64],<data>
    let (meta, payload) = rest
        .split_once(',')
        .ok_or_else(|| ConvertError::InvalidInput("malformed data: URI (no comma)".into()))?;

    let mut is_base64 = false;
    let mut mimetype: Option<String> = None;
    let mut charset: Option<String> = None;
    for (i, part) in meta.split(';').enumerate() {
        let part = part.trim();
        if part.eq_ignore_ascii_case("base64") {
            is_base64 = true;
        } else if let Some(cs) = part.strip_prefix("charset=") {
            charset = Some(cs.to_ascii_lowercase());
        } else if i == 0 && !part.is_empty() {
            mimetype = Some(part.to_ascii_lowercase());
        }
    }

    let data = if is_base64 {
        base64::engine::general_purpose::STANDARD
            .decode(payload.trim())
            .map_err(|e| ConvertError::InvalidInput(format!("bad base64 in data URI: {e}")))?
    } else {
        percent_decode_str(payload).collect()
    };

    let mut info = StreamInfo::new().with_url(full);
    info.mimetype = mimetype;
    info.charset = charset;
    Ok((data, info))
}

#[cfg(feature = "net")]
fn read_http(url: &str) -> Result<(Vec<u8>, StreamInfo), ConvertError> {
    let mut resp = ureq::get(url)
        .header("User-Agent", concat!("markitdown-rs/", env!("CARGO_PKG_VERSION")))
        .call()
        .map_err(|e| ConvertError::Network(e.to_string()))?;

    let content_type = resp
        .headers()
        .get("content-type")
        .and_then(|v| v.to_str().ok())
        .map(str::to_string);

    let data = resp
        .body_mut()
        .with_config()
        .limit(512 * 1024 * 1024) // hard cap: 512 MiB
        .read_to_vec()
        .map_err(|e| ConvertError::Network(e.to_string()))?;

    let mut info = StreamInfo::new().with_url(url);
    if let Some(ct) = content_type {
        let mut parts = ct.split(';');
        if let Some(mt) = parts.next() {
            let mt = mt.trim();
            if !mt.is_empty() {
                info.mimetype = Some(mt.to_ascii_lowercase());
            }
        }
        for p in parts {
            if let Some(cs) = p.trim().strip_prefix("charset=") {
                info.charset = Some(cs.trim_matches('"').to_ascii_lowercase());
            }
        }
    }
    // Filename from the last path segment, for extension hints.
    if let Some(path_part) = url
        .splitn(4, '/')
        .nth(3)
        .map(|p| p.split(['?', '#']).next().unwrap_or(""))
    {
        if let Some(seg) = path_part.rsplit('/').next() {
            if !seg.is_empty() {
                info.filename = Some(seg.to_string());
            }
        }
    }
    Ok((data, info))
}

#[cfg(not(feature = "net"))]
fn read_http(_url: &str) -> Result<(Vec<u8>, StreamInfo), ConvertError> {
    Err(ConvertError::MissingDependency(
        "http(s) inputs require the `net` feature".into(),
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn data_uri_base64() {
        let (data, info) = read_source("data:text/plain;base64,aGVsbG8=").unwrap();
        assert_eq!(data, b"hello");
        assert_eq!(info.mimetype.as_deref(), Some("text/plain"));
    }

    #[test]
    fn data_uri_percent_encoded() {
        let (data, info) = read_source("data:text/plain;charset=utf-8,hi%20there").unwrap();
        assert_eq!(data, b"hi there");
        assert_eq!(info.charset.as_deref(), Some("utf-8"));
    }

    #[test]
    fn file_uri_decodes_percent_escapes() {
        let p = file_uri_to_path("/tmp/my%20file.txt").unwrap();
        assert_eq!(p, PathBuf::from("/tmp/my file.txt"));
    }

    #[test]
    fn rejects_remote_file_uri_host() {
        assert!(file_uri_to_path("evilhost/share/x").is_err());
    }
}
