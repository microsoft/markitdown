from typing import Optional

from charset_normalizer import CharsetMatch, from_bytes

# S and Z with caron share these bytes in cp1250 and cp1252. They are common in
# Central European text and rare in Western European text.
_CARON_BYTES = frozenset(b"\x8a\x8e\x9a\x9e")
# Letters in cp1250 that are symbols in cp1252: Ł Ą Ż ł ą Ľ ľ ż read as
# £ ¥ ¯ ³ ¹ ¼ ¾ ¿. Followed by a letter, they point to cp1250, except ¿, which
# opens Spanish questions ("¿Qué") and counts only between two letters.
_CP1250_LETTER_BYTES = frozenset(b"\xa3\xa5\xaf\xb3\xb9\xbc\xbe\xbf")
_INVERTED_QUESTION_MARK = 0xBF
# ő in cp1250, õ in cp1252. Portuguese, the Western language that uses õ,
# has it only before "e" ("razões", "põe").
_O_DOUBLE_ACUTE = 0xF5


def _is_ascii_letter(byte: int) -> bool:
    return 0x41 <= byte <= 0x5A or 0x61 <= byte <= 0x7A


def _looks_like_cp1250(data: bytes) -> bool:
    if not _CARON_BYTES.isdisjoint(data):
        return True
    for i, byte in enumerate(data):
        following = data[i + 1] if i + 1 < len(data) else None
        if (
            byte in _CP1250_LETTER_BYTES
            and following is not None
            and _is_ascii_letter(following)
            and (
                byte != _INVERTED_QUESTION_MARK
                or (i > 0 and _is_ascii_letter(data[i - 1]))
            )
        ):
            return True
        if byte == _O_DOUBLE_ACUTE and following not in (ord("e"), ord("E")):
            return True
    return False


def best_charset_match(data: bytes) -> Optional[CharsetMatch]:
    """Return the detector's best match, breaking ties between cp1252 and cp1250.

    Western European text in cp1252 often scores exactly like cp1250 (or a
    non-Latin code page), and the detector then picks by name, so "crème"
    comes out as "crčme". On a tie in both chaos and coherence, take cp1250 if
    the bytes point to it, and cp1252 otherwise. Text with no such bytes, such
    as Czech "Česká" or Croatian without š or ž, stays ambiguous and goes to
    cp1252.
    """
    matches = from_bytes(data)
    best = matches.best()
    if best is None:
        return best

    preferred = "cp1250" if _looks_like_cp1250(data) else "cp1252"
    for match in matches:
        if (
            match.encoding == preferred
            and match.chaos == best.chaos
            and match.coherence == best.coherence
        ):
            return match
    return best
