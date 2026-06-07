use crate::{ConvertError, ConvertOptions, ConvertResult, StreamInfo};

/// A single file-format converter.
///
/// Port of Python's `DocumentConverter` ABC. Implementations must be cheap to
/// construct and stateless; the registry holds one boxed instance of each.
///
/// `data` is the complete input (the registry buffers streams up front, as the
/// Python implementation does) so converters are free to parse it repeatedly.
pub trait Converter: Send + Sync {
    /// Stable identifier used in error messages, e.g. `"pdf"`.
    fn name(&self) -> &'static str;

    /// Fast check: can this converter plausibly handle the stream?
    /// Should only inspect `info` and (cheaply) the first bytes of `data`.
    fn accepts(&self, info: &StreamInfo, data: &[u8]) -> bool;

    /// Perform the conversion. Returning an error lets the registry try the
    /// next accepting converter (same fallthrough semantics as Python).
    fn convert(
        &self,
        data: &[u8],
        info: &StreamInfo,
        opts: &ConvertOptions,
    ) -> Result<ConvertResult, ConvertError>;
}
