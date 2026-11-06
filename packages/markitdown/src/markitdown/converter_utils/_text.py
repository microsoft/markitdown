from charset_normalizer import from_bytes


_UTF_ENCODINGS = {
    "utf_8",
    "utf_8_sig",
    "utf_16",
    "utf_16_le",
    "utf_16_be",
    "utf_32",
    "utf_32_le",
    "utf_32_be",
}


def detect_charset(data: bytes) -> str:
    """Detect a charset without trusting zero-confidence guesses."""
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    detected = from_bytes(data).best()
    if detected is not None and (
        detected.percent_coherence > 0 or detected.encoding in _UTF_ENCODINGS
    ):
        return detected.encoding

    return "cp1252"


def decode_text(data: bytes) -> str:
    """Decode text while preserving UTF-8 and common Western encodings."""
    return data.decode(detect_charset(data), errors="replace")
