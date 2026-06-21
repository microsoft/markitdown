"""Resolve pdfminer ``(cid:N)`` tokens in extracted PDF text to Unicode.

Two stages:

* :func:`build_cid_map` makes a single low-level pdfminer pass over the document,
  reading each unmapped glyph's ``fontname`` so the correct per-font encoding table
  is used (see :mod:`.cid_fonts`). The result is a document-specific
  ``cid -> Unicode`` map; a cid that resolves to conflicting glyphs across fonts in
  the same document is dropped (ambiguous -> left for the fallback path).

* :func:`decode_cids` substitutes those tokens in the already-extracted markdown.
  Tokens are grouped into *clusters* (a cluster ≈ one math expression). Each cluster
  gets a confidence score = resolved / total tokens; clusters below the threshold are
  wrapped in an HTML comment instead of being partly mistranslated, so downstream
  consumers still see the raw signal.
"""

import re
from typing import BinaryIO

from .cid_fonts import lookup

# Matches a pdfminer unmapped-glyph token, e.g. "(cid:88)".
_CID_TOKEN = re.compile(r"\(cid:(\d+)\)")
# Same, anchored, for testing a single LTChar's rendered text.
_CID_EXACT = re.compile(r"^\(cid:(\d+)\)$")

# Max length of intervening (non-blank-line) text for two cid tokens to count as
# the same cluster. Formula fragments like "Q−1 (Q(x))" sit between delimiters.
_MAX_CLUSTER_GAP = 40


def build_cid_map(pdf_bytes: BinaryIO) -> dict[int, str]:
    """Build a document-specific ``cid -> Unicode`` map via a font-aware pass.

    Reads ``LTChar.fontname`` for every unmapped ``(cid:N)`` glyph and resolves it
    through the per-font tables. Conflicting resolutions for the same cid are
    discarded so they are never guessed.
    """
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTChar

    pdf_bytes.seek(0)

    candidates: dict[int, set[str]] = {}

    def walk(obj: object) -> None:
        for element in obj:  # type: ignore[attr-defined]
            if isinstance(element, LTChar):
                match = _CID_EXACT.match(element.get_text())
                if match:
                    cid = int(match.group(1))
                    resolved = lookup(element.fontname, cid)
                    if resolved is not None:
                        candidates.setdefault(cid, set()).add(resolved)
            if hasattr(element, "__iter__"):
                walk(element)

    for page in extract_pages(pdf_bytes):
        walk(page)

    # Keep only unambiguous resolutions.
    return {cid: next(iter(chars)) for cid, chars in candidates.items() if len(chars) == 1}


def _same_cluster(gap: str) -> bool:
    """True if the text between two cid tokens keeps them in one formula cluster."""
    if "\n\n" in gap:  # a blank line ends the formula
        return False
    return len(gap.strip()) <= _MAX_CLUSTER_GAP


def decode_cids(
    markdown: str,
    cid_map: dict[int, str],
    *,
    confidence_threshold: float = 0.6,
) -> str:
    """Replace ``(cid:N)`` tokens in *markdown* using *cid_map*.

    High-confidence clusters are substituted (unresolved tokens within them are left
    untouched). Clusters whose resolved ratio falls below *confidence_threshold* are
    wrapped as ``<!-- FORMULA: ... -->`` rather than partially decoded.
    """
    matches = list(_CID_TOKEN.finditer(markdown))
    if not matches:
        return markdown

    # Group token matches into clusters by proximity.
    clusters: list[list[re.Match[str]]] = [[matches[0]]]
    for match in matches[1:]:
        gap = markdown[clusters[-1][-1].end() : match.start()]
        if _same_cluster(gap):
            clusters[-1].append(match)
        else:
            clusters.append([match])

    out: list[str] = []
    last = 0
    for cluster in clusters:
        start, end = cluster[0].start(), cluster[-1].end()
        out.append(markdown[last:start])
        span = markdown[start:end]

        resolved = sum(1 for m in cluster if int(m.group(1)) in cid_map)
        confidence = resolved / len(cluster)

        if confidence >= confidence_threshold:
            out.append(
                _CID_TOKEN.sub(
                    lambda m: cid_map.get(int(m.group(1)), m.group(0)), span
                )
            )
        else:
            out.append(f"<!-- FORMULA: {span} -->")
        last = end

    out.append(markdown[last:])
    return "".join(out)
