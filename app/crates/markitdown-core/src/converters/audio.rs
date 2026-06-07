//! Audio → Markdown converter.
//!
//! Port of `packages/markitdown/src/markitdown/converters/_audio_converter.py`.
//!
//! DEVIATION FROM PYTHON: Python shells out to `exiftool` for metadata and
//! optionally uses `speech_recognition` to transcribe. We read tags/properties
//! with `lofty` and emit `Key: value` lines (`Title`, `Artist`, `Album`,
//! `Genre`, `Track`, `Year`, plus a `Duration` line and audio properties).
//! Transcription is NOT ported — it requires the optional Python engine; this
//! is noted in a trailing HTML comment.
//!
//! Missing tags are not an error; whatever exists is emitted.

use crate::{ConvertError, ConvertOptions, ConvertResult, Converter, StreamInfo};
use lofty::file::{AudioFile, TaggedFileExt};
use lofty::prelude::{Accessor, ItemKey};
use lofty::probe::Probe;
use std::io::Cursor;

pub struct AudioConverter;

const ACCEPTED_EXTENSIONS: &[&str] = &[".wav", ".mp3", ".m4a", ".mp4", ".flac"];
const ACCEPTED_MIMETYPES: &[&str] = &[
    "audio/x-wav",
    "audio/wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/m4a",
    "audio/flac",
    "video/mp4",
];

fn push_field(md: &mut String, label: &str, value: Option<&str>) {
    if let Some(v) = value {
        let v = v.trim();
        if !v.is_empty() {
            md.push_str(&format!("{label}: {v}\n"));
        }
    }
}

fn fmt_duration(secs: u64) -> String {
    let h = secs / 3600;
    let m = (secs % 3600) / 60;
    let s = secs % 60;
    if h > 0 {
        format!("{h:02}:{m:02}:{s:02}")
    } else {
        format!("{m:02}:{s:02}")
    }
}

impl Converter for AudioConverter {
    fn name(&self) -> &'static str {
        "audio"
    }

    fn accepts(&self, info: &StreamInfo, _data: &[u8]) -> bool {
        info.extension_is(ACCEPTED_EXTENSIONS) || info.mimetype_is(ACCEPTED_MIMETYPES)
    }

    fn convert(
        &self,
        data: &[u8],
        _info: &StreamInfo,
        _opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError> {
        let mut cursor = Cursor::new(data);
        let tagged = Probe::new(&mut cursor)
            .guess_file_type()
            .map_err(|e| ConvertError::conversion("audio", format!("could not probe audio: {e}")))?
            .read()
            .map_err(|e| {
                ConvertError::conversion("audio", format!("could not read audio metadata: {e}"))
            })?;

        let mut md = String::new();

        if let Some(tag) = tagged.primary_tag().or_else(|| tagged.first_tag()) {
            push_field(&mut md, "Title", tag.title().as_deref());
            push_field(&mut md, "Artist", tag.artist().as_deref());
            push_field(&mut md, "Album", tag.album().as_deref());
            push_field(&mut md, "Genre", tag.genre().as_deref());
            if let Some(track) = tag.track() {
                md.push_str(&format!("Track: {track}\n"));
            }
            // Year may live under Year or RecordingDate depending on container.
            let year = tag
                .get_string(ItemKey::Year)
                .or_else(|| tag.get_string(ItemKey::RecordingDate));
            push_field(&mut md, "Year", year);
            push_field(&mut md, "Comment", tag.comment().as_deref());
        }

        // Audio properties.
        let props = tagged.properties();
        let secs = props.duration().as_secs();
        md.push_str(&format!("Duration: {}\n", fmt_duration(secs)));
        if let Some(br) = props.audio_bitrate() {
            md.push_str(&format!("Bitrate: {br} kbps\n"));
        }
        if let Some(sr) = props.sample_rate() {
            md.push_str(&format!("SampleRate: {sr} Hz\n"));
        }
        if let Some(ch) = props.channels() {
            md.push_str(&format!("Channels: {ch}\n"));
        }

        md.push_str(
            "\n<!-- Audio transcription requires the optional Python engine \
             (set MARKITDOWN_PY_BIN). -->\n",
        );

        // Degraded: the Python engine (audio-transcription extra) can add a
        // speech transcript on top of these tags.
        Ok(ConvertResult::new(md.trim_end().to_string()).with_degraded())
    }
}
