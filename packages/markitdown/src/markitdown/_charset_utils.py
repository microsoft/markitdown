import codecs

from typing import Optional
from charset_normalizer import from_bytes


def normalize_charset(charset: Optional[str]) -> Optional[str]:
    """
    Normalize a charset string to a canonical form.
    """
    if charset is None:
        return None
    try:
        return codecs.lookup(charset).name
    except LookupError:
        return charset


def decode_bytes(data: bytes, charset: Optional[str] = None) -> str:
    """
    Decode data to text, tolerating an incorrect charset.

    Charsets reaching the converters are guesses: sniffed from the first few
    kilobytes of a stream, or read from a Content-Type header that may be wrong.
    Decoding an entire document with such a guess can fail on bytes the guess
    never saw -- e.g. an otherwise-ASCII file whose first non-ASCII character
    appears past the sniffed window. Rather than fail the conversion, re-detect
    over the full data, and finally fall back to a lossy decode.
    """
    if charset:
        try:
            return data.decode(charset)
        except (UnicodeDecodeError, LookupError):
            pass

    detected = from_bytes(data).best()
    if detected is not None:
        return str(detected)

    return data.decode("utf-8", errors="replace")
