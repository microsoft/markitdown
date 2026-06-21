"""Font-keyed CID -> Unicode tables for LaTeX (Computer Modern / Latin Modern) PDFs.

When a PDF embeds a math font without a ``ToUnicode`` CMap, pdfminer emits the
glyph as the literal token ``(cid:N)``, where ``N`` is the glyph's code in the
font's *native* encoding -- not Unicode. The same code means different glyphs in
different fonts (e.g. code 12 is ``|`` in CMEX10 but unrelated in CMSY10), so
resolution must be keyed by font name.

Tables are expressed as ``code -> glyph-name`` (the stable native encoding) plus a
shared ``glyph-name -> Unicode`` map. The CMEX10 table is verified glyph-by-glyph
against the bundled fixture (``test_math_cid.pdf``); its encoding was confirmed by
reading the embedded Type1 font's built-in ``Encoding`` array. CMSY10 / CMMI10
carry the standard Computer Modern encodings (not exercised by the bundled fixture)
to generalise the feature to other LaTeX PDFs.

These native encodings are stable across documents -- unlike subset *CID* fonts,
CM/LM Type1 math fonts are not renumbered per document -- so a static table is
reliable. Codes that are not present here fall through to the decoder's
confidence/fallback path rather than being mistranslated.
"""

# --- glyph name -> Unicode -------------------------------------------------

_GLYPH_TO_UNICODE: dict[str, str] = {
    # delimiters (all size variants collapse to the base character)
    "parenleft": "(",
    "parenright": ")",
    "bracketleft": "[",
    "bracketright": "]",
    "braceleft": "{",
    "braceright": "}",
    "floorleft": "⌊",
    "floorright": "⌋",
    "ceilingleft": "⌈",
    "ceilingright": "⌉",
    "angbracketleft": "⟨",
    "angbracketright": "⟩",
    "slash": "/",
    "backslash": "\\",
    "bar": "|",
    "doublebar": "‖",
    # operators
    "summation": "∑",
    "product": "∏",
    "integral": "∫",
    "union": "∪",
    "intersection": "∩",
    "radical": "√",
    # Greek
    "Gamma": "Γ",
    "Delta": "Δ",
    "Theta": "Θ",
    "Lambda": "Λ",
    "Xi": "Ξ",
    "Pi": "Π",
    "Sigma": "Σ",
    "Upsilon": "Υ",
    "Phi": "Φ",
    "Psi": "Ψ",
    "Omega": "Ω",
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ϵ",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "pi": "π",
    "rho": "ρ",
    "sigma": "σ",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "ϕ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",
    "epsilon1": "ε",
    "theta1": "ϑ",
    "pi1": "ϖ",
    "rho1": "ϱ",
    "sigma1": "ς",
    "phi1": "φ",
    # symbols
    "minus": "−",
    "periodcentered": "·",
    "multiply": "×",
    "asteriskmath": "∗",
    "divide": "÷",
    "plusminus": "±",
    "minusplus": "∓",
    "circleplus": "⊕",
    "circleminus": "⊖",
    "circletimes": "⊗",
    "circlemultiply": "⊗",
    "circledivide": "⊘",
    "circledot": "⊙",
    "circlecopyrt": "©",
    "openbullet": "◦",
    "bullet": "•",
    "partialdiff": "∂",
    "nabla": "∇",
    "negationslash": "̸",  # combining long solidus overlay; renders on the preceding glyph
    "vector": "",  # \vec accent: dropped, the base letter is emitted separately
    "equivalence": "≡",
    "lessequal": "≤",
    "greaterequal": "≥",
    "similar": "∼",
    "approxequal": "≈",
    "propersubset": "⊂",
    "propersuperset": "⊃",
    "reflexsubset": "⊆",
    "reflexsuperset": "⊇",
    "lessmuch": "≪",
    "greatermuch": "≫",
    "arrowleft": "←",
    "arrowright": "→",
    "arrowup": "↑",
    "arrowdown": "↓",
    "arrowboth": "↔",
    "similarequal": "≃",
    "arrowdblright": "⇒",
    "arrowdblleft": "⇐",
    "arrowdblboth": "⇔",
    "proportional": "∝",
    "prime": "′",
    "infinity": "∞",
    "element": "∈",
    "owner": "∋",
    "universal": "∀",
    "existential": "∃",
    "logicalnot": "¬",
    "emptyset": "∅",
}


# --- native font encodings: code -> glyph name -----------------------------

# CMEX10 (math extension): delimiters in graded sizes + big operators.
# Verified against the embedded Type1 encoding of the bundled fixture; the
# 0-47 delimiter block and the scattered Big variants / operators / radicals
# below were all confirmed code-by-code.
_CMEX10_CODES: dict[int, str] = {
    0: "parenleftbig",
    1: "parenrightbig",
    2: "bracketleftbig",
    3: "bracketrightbig",
    4: "floorleftbig",
    5: "floorrightbig",
    6: "ceilingleftbig",
    7: "ceilingrightbig",
    8: "braceleftbig",
    9: "bracerightbig",
    10: "angbracketleftbig",
    11: "angbracketrightbig",
    12: "vextendsingle",
    13: "vextenddouble",
    14: "slashbig",
    15: "backslashbig",
    16: "parenleftBig",
    17: "parenrightBig",
    18: "parenleftbigg",
    19: "parenrightbigg",
    20: "bracketleftbigg",
    21: "bracketrightbigg",
    22: "floorleftbigg",
    23: "floorrightbigg",
    24: "ceilingleftbigg",
    25: "ceilingrightbigg",
    26: "braceleftbigg",
    27: "bracerightbigg",
    28: "angbracketleftbigg",
    29: "angbracketrightbigg",
    30: "slashbigg",
    31: "backslashbigg",
    32: "parenleftBigg",
    33: "parenrightBigg",
    34: "bracketleftBigg",
    35: "bracketrightBigg",
    36: "floorleftBigg",
    37: "floorrightBigg",
    38: "ceilingleftBigg",
    39: "ceilingrightBigg",
    40: "braceleftBigg",
    41: "bracerightBigg",
    42: "angbracketleftBigg",
    43: "angbracketrightBigg",
    44: "slashBigg",
    45: "backslashBigg",
    46: "slashBig",
    47: "backslashBig",
    50: "bracketlefttp",
    51: "bracketrighttp",
    52: "bracketleftbt",
    53: "bracketrightbt",
    54: "bracketleftex",
    55: "bracketrightex",
    68: "angbracketleftBig",
    69: "angbracketrightBig",
    80: "summationtext",
    81: "producttext",
    82: "integraltext",
    83: "uniontext",
    88: "summationdisplay",
    89: "productdisplay",
    90: "integraldisplay",
    91: "uniondisplay",
    92: "intersectiondisplay",
    104: "bracketleftBig",
    105: "bracketrightBig",
    110: "braceleftBig",
    111: "bracerightBig",
    112: "radicalbig",
    113: "radicalBig",
    114: "radicalbigg",
    115: "radicalBigg",
}

# CMMI10 (math italic): Greek letters live at codes 0-39 (the high-value part;
# ASCII letters carry their own ToUnicode and are left alone).
_CMMI10_CODES: dict[int, str] = {
    0: "Gamma",
    1: "Delta",
    2: "Theta",
    3: "Lambda",
    4: "Xi",
    5: "Pi",
    6: "Sigma",
    7: "Upsilon",
    8: "Phi",
    9: "Psi",
    10: "Omega",
    11: "alpha",
    12: "beta",
    13: "gamma",
    14: "delta",
    15: "epsilon",
    16: "zeta",
    17: "eta",
    18: "theta",
    19: "iota",
    20: "kappa",
    21: "lambda",
    22: "mu",
    23: "nu",
    24: "xi",
    25: "pi",
    26: "rho",
    27: "sigma",
    28: "tau",
    29: "upsilon",
    30: "phi",
    31: "chi",
    32: "psi",
    33: "omega",
    34: "epsilon1",
    35: "theta1",
    36: "pi1",
    37: "rho1",
    38: "sigma1",
    39: "phi1",
    64: "partialdiff",
    126: "vector",
}

# CMSY10 (math symbols): standard Computer Modern encoding.
_CMSY10_CODES: dict[int, str] = {
    0: "minus",
    1: "periodcentered",
    2: "multiply",
    3: "asteriskmath",
    4: "divide",
    6: "plusminus",
    7: "minusplus",
    8: "circleplus",
    9: "circleminus",
    10: "circlemultiply",
    11: "circledivide",
    12: "circledot",
    13: "circlecopyrt",
    14: "openbullet",
    15: "bullet",
    17: "equivalence",
    18: "reflexsubset",
    19: "reflexsuperset",
    20: "lessequal",
    21: "greaterequal",
    24: "similar",
    25: "approxequal",
    26: "propersubset",
    27: "propersuperset",
    28: "lessmuch",
    29: "greatermuch",
    32: "arrowleft",
    33: "arrowright",
    34: "arrowup",
    35: "arrowdown",
    36: "arrowboth",
    39: "similarequal",
    40: "arrowdblleft",
    41: "arrowdblright",
    44: "arrowdblboth",
    47: "proportional",
    48: "prime",
    49: "infinity",
    50: "element",
    51: "owner",
    54: "negationslash",
    56: "universal",
    57: "existential",
    58: "logicalnot",
    59: "emptyset",
    106: "bar",
    114: "nabla",
}


def _build(codes: dict[int, str]) -> dict[int, str]:
    """Resolve a code->glyph-name table to code->Unicode, dropping unknown names."""
    table: dict[int, str] = {}
    for code, glyph in codes.items():
        unicode_char = _GLYPH_TO_UNICODE.get(glyph)
        if unicode_char is None:
            # Size-/style-suffixed glyph (e.g. "parenleftbig",
            # "summationdisplay"): fall back to the base name by stripping the
            # suffix.
            for suffix in (
                "bigg",
                "Bigg",
                "big",
                "Big",
                "display",
                "text",
                "tp",
                "bt",
                "ex",
                "mid",  # extensible delimiter pieces
            ):
                if glyph.endswith(suffix):
                    unicode_char = _GLYPH_TO_UNICODE.get(glyph[: -len(suffix)])
                    break
        if unicode_char is None and glyph.startswith("vextend"):
            unicode_char = _GLYPH_TO_UNICODE[
                "bar" if glyph == "vextendsingle" else "doublebar"
            ]
        if unicode_char is not None:
            table[code] = unicode_char
    return table


CMEX = _build(_CMEX10_CODES)
CMMI = _build(_CMMI10_CODES)
CMSY = _build(_CMSY10_CODES)

# Tables are keyed by *family*, not design size. A Computer Modern math font
# shares its encoding across every point size (CMSY10, CMSY8, CMSY7, ...) and
# with its Latin Modern equivalent (LMSY10, ...), so all collapse to one table.
FONT_TABLES: dict[str, dict[int, str]] = {
    "CMEX": CMEX,
    "CMMI": CMMI,
    "CMSY": CMSY,
}

# Family prefix (after subset-prefix stripping) -> FONT_TABLES key.
_FAMILY_PREFIXES = {
    "CMEX": "CMEX",
    "LMEX": "CMEX",
    "CMMI": "CMMI",  # also matches CMMIB (bold math italic): same OML encoding
    "LMMI": "CMMI",
    "CMSY": "CMSY",
    "LMSY": "CMSY",
}


def normalize_fontname(fontname: str | None) -> str:
    """Normalise a pdfminer fontname to a FONT_TABLES family key.

    Strips the 6-letter subset prefix (e.g. ``UXDKUK+CMEX10`` -> ``CMEX10``) and
    maps any design-size/Latin-Modern variant to its family
    (``CMSY8`` / ``LMSY10`` -> ``CMSY``). Returns ``""`` if no math family matches.
    """
    if not fontname:
        return ""
    name = fontname.split("+", 1)[1] if "+" in fontname else fontname
    name = name.upper()
    for prefix, family in _FAMILY_PREFIXES.items():
        if name.startswith(prefix):
            return family
    return ""


def lookup(fontname: str | None, cid: int) -> str | None:
    """Resolve a single ``(font, cid)`` to Unicode, or ``None`` if unknown."""
    table = FONT_TABLES.get(normalize_fontname(fontname))
    if table is None:
        return None
    return table.get(cid)
