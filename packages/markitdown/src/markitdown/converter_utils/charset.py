from typing import Optional

from charset_normalizer import from_bytes


def decode_text(data: bytes, charset: Optional[str]) -> str:
    """
    Decode bytes to text, re-detecting the charset when the supplied one does not fit.

    Charset detection inspects only the first 4k of a stream, so a file whose non-ASCII
    bytes appear later can be labeled with a charset that fails on the full content.
    Re-running detection over every byte recovers those files instead of raising
    UnicodeDecodeError.
    """
    if charset:
        try:
            return data.decode(charset)
        except UnicodeDecodeError:
            pass

    best_match = from_bytes(data).best()
    if best_match is None:
        # Detection found no viable encoding; keep the readable parts rather than failing.
        return data.decode("utf-8", errors="replace")
    return str(best_match)
