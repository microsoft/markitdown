from typing import Optional

from charset_normalizer import CharsetMatch, from_bytes

# S and Z with caron share these bytes in cp1250 and cp1252. They are common in
# Central European text and rare in Western European text.
_CARON_BYTES = frozenset(b"\x8a\x8e\x9a\x9e")


def best_charset_match(data: bytes) -> Optional[CharsetMatch]:
    """Return the detector's best match, preferring cp1252 when it ties.

    Western European text in cp1252 often scores exactly like cp1250 (or a
    non-Latin code page), and the detector then picks by name, so "crème"
    comes out as "crčme". On a tie in both chaos and coherence, take cp1252,
    unless the data has S or Z with caron, which point to cp1250.
    """
    matches = from_bytes(data)
    best = matches.best()
    if best is None or not _CARON_BYTES.isdisjoint(data):
        return best

    for match in matches:
        if (
            match.encoding == "cp1252"
            and match.chaos == best.chaos
            and match.coherence == best.coherence
        ):
            return match
    return best
