"""
Office Math Markup Language (OMML) to LaTeX conversion - Symbol definitions and utilities.
"""

from typing import Dict

OMML_NAMESPACE = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

# Minimal set of Unicode to LaTeX mappings for initial implementation
UNICODE_TO_LATEX: Dict[int, str] = {
    # Greek letters from latex_dict.T and other common symbols
    0x03B1: "\\alpha",
    0x03B2: "\\beta",
    0x0393: "\\Gamma",
    0x03B3: "\\gamma",
    0x0394: "\\Delta",
    0x03B4: "\\delta",
    0x0395: "\\Epsilon",
    0x03B5: "\\epsilon",
    0x03B6: "\\zeta",
    0x0397: "\\Eta",
    0x03B7: "\\eta",
    0x0398: "\\Theta",
    0x03B8: "\\theta",
    0x0399: "\\Iota",
    0x03B9: "\\iota",
    0x039A: "\\Kappa",
    0x03BA: "\\kappa",
    0x039B: "\\Lambda",
    0x03BB: "\\lambda",
    0x039C: "\\Mu",
    0x03BC: "\\mu",
    0x039D: "\\Nu",
    0x03BD: "\\nu",
    0x039E: "\\Xi",
    0x03BE: "\\xi",
    0x039F: "\\Omicron",
    0x03BF: "\\omicron",
    0x03A0: "\\Pi",
    0x03C0: "\\pi",
    0x03A1: "\\Rho",
    0x03C1: "\\rho",
    0x03A3: "\\Sigma",
    0x03C3: "\\sigma",
    0x03A4: "\\Tau",
    0x03C4: "\\tau",
    0x03A5: "\\Upsilon",
    0x03C5: "\\upsilon",
    0x03A6: "\\Phi",
    0x03C6: "\\phi",  # \\phi or \\varphi
    0x03A7: "\\Chi",
    0x03C7: "\\chi",
    0x03A8: "\\Psi",
    0x03C8: "\\psi",
    0x03A9: "\\Omega",
    0x03C9: "\\omega",
    0x2202: "\\partial",
    0x03F5: "\\varepsilon",
    0x03D1: "\\vartheta",
    0x03F0: "\\varkappa",
    0x03D5: "\\varphi",
    0x03F1: "\\varrho",
    0x03D6: "\\varpi",
    # Relation symbols
    0x2190: "\\leftarrow",
    0x2191: "\\uparrow",
    0x2192: "\\rightarrow",
    0x2193: "\\downarrow",
    0x2194: "\\leftrightarrow",
    0x2195: "\\updownarrow",
    0x2196: "\\nwarrow",
    0x2197: "\\nearrow",
    0x2198: "\\searrow",
    0x2199: "\\swarrow",
    0x22EE: "\\vdots",
    0x22EF: "\\cdots",
    0x22F0: "\\adots",  # amsmath
    0x22F1: "\\ddots",  # amsmath
    0x2260: "\\ne",  # or \\neq
    0x2264: "\\leq",
    0x2265: "\\geq",
    0x2266: "\\leqq",  # amsmath
    0x2267: "\\geqq",  # amsmath
    0x2268: "\\lneqq",  # amsmath
    0x2269: "\\gneqq",  # amsmath
    0x226A: "\\ll",
    0x226B: "\\gg",
    0x2208: "\\in",
    0x2209: "\\notin",
    0x220B: "\\ni",  # or \\owns
    0x220C: "\\nni",  # or \\not\\owns, amsmath
    # Ordinary symbols
    0x221E: "\\infty",
    # Binary relations
    0x00B1: "\\pm",
    0x2213: "\\mp",
    # Big operators (commonly used as symbols too)
    0x220F: "\\prod",  # N-Ary Product
    0x2210: "\\coprod",  # N-Ary Coproduct
    0x2211: "\\sum",  # N-Ary Summation
    0x222B: "\\int",  # Integral
    0x22C0: "\\bigwedge",  # N-Ary Logical And
    0x22C1: "\\bigvee",  # N-Ary Logical Or
    0x22C2: "\\bigcap",  # N-Ary Intersection
    0x22C3: "\\bigcup",  # N-Ary Union
    0x2A00: "\\bigodot",  # N-Ary Circled Dot Operator
    0x2A01: "\\bigoplus",  # N-Ary Circled Plus Operator
    0x2A02: "\\bigotimes",  # N-Ary Circled Times Operator
    0x2140: "\\Bbbsum",  # Double-Struck N-Ary Summation (requires package like amssymb)
    # Other common math symbols (add as identified)
    0x2026: "\\dots",  # Horizontal Ellipsis
    0x00D7: "\\times",  # Multiplication sign
    0x00F7: "\\div",  # Division sign
    0x221A: "\\sqrt",  # Square root (handled by OMMLRadical, but good to have)
    0x2261: "\\equiv",  # Identical to
    0x2248: "\\approx",  # Almost equal to
    0x2245: "\\cong",  # Approximately equal to
    0x2220: "\\angle",  # Angle
    0x22A5: "\\perp",  # Perpendicular
    0x2225: "\\parallel",  # Parallel
    0x2118: "\\wp",  # Weierstrass p
    0x210F: "\\hbar",  # Planck constant over 2 pi
    0x2200: "\\forall",  # For all
    0x2203: "\\exists",  # There exists
    0x2205: "\\emptyset",  # Empty set
    0x2207: "\\nabla",  # Nabla (del)
    0x2113: "\\ell",  # Script small l
    0x2111: "\\Im",  # Imaginary part
    0x211C: "\\Re",  # Real part
    # Mathematical Alphanumeric Symbols (U+1D400 - U+1D7FF)
    0x1D434: "A",  # MATHEMATICAL ITALIC CAPITAL A (Used as a placeholder, ideally handled by style)
    0x1D435: "B",
    0x1D436: "C",
    0x1D437: "D",
    0x1D438: "E",
    0x1D439: "F",
    0x1D43A: "G",
    0x1D43B: "H",
    0x1D43C: "I",
    0x1D43D: "J",
    0x1D43E: "K",
    0x1D43F: "L",
    0x1D440: "M",
    0x1D441: "N",
    0x1D442: "O",
    0x1D443: "P",
    0x1D444: "Q",
    0x1D445: "R",
    0x1D446: "S",
    0x1D447: "T",
    0x1D448: "U",
    0x1D449: "V",
    0x1D44A: "W",
    0x1D44B: "X",
    0x1D44C: "Y",
    0x1D44D: "Z",
    0x1D44E: "a",  # MATHEMATICAL ITALIC SMALL A
    0x1D44F: "b",
    0x1D450: "c",
    0x1D451: "d",
    0x1D452: "e",
    0x1D453: "f",
    0x1D454: "g",
    0x1D455: "h",
    0x1D456: "i",
    0x1D457: "j",
    0x1D458: "k",
    0x1D459: "l",
    0x1D45A: "m",
    0x1D45B: "n",
    0x1D45C: "o",
    0x1D45D: "p",
    0x1D45E: "q",
    0x1D45F: "r",
    0x1D460: "s",
    0x1D461: "t",
    0x1D462: "u",
    0x1D463: "v",
    0x1D464: "w",
    0x1D465: "x",
    0x1D466: "y",
    0x1D467: "z",
    # ... (many more italic, bold, script, fraktur, etc. letters)
    # Spacing
    0x2009: "\\,",  # Thin space
    0x200A: "\\:",  # Medium space (> \\,)
    0x200B: "",  # Zero-width space (ignore)
    0x00A0: "~",  # Non-breaking space -> LaTeX active ~
}

# OMML function names to LaTeX
OMML_FUNCTION_NAMES_TO_LATEX: Dict[str, str] = {
    "sin": "\\sin",
    "cos": "\\cos",
    "tan": "\\tan",
    "arcsin": "\\arcsin",
    "arccos": "\\arccos",
    "arctan": "\\arctan",
    "arccot": "\\arccot",  # Not standard LaTeX, often acot or from package
    "sinh": "\\sinh",
    "cosh": "\\cosh",
    "tanh": "\\tanh",
    "coth": "\\coth",
    "sec": "\\sec",
    "csc": "\\csc",
    "cot": "\\cot",
    "exp": "\\exp",
    "ln": "\\ln",
    "log": "\\log",
    "det": "\\det",
    "dim": "\\dim",
    "lim": "\\lim",
    "min": "\\min",
    "max": "\\max",
    "gcd": "\\gcd",  # requires amsmath
    "Pr": "\\Pr",  # Probability (requires amsmath or similar)
    "arg": "\\arg",  # Argument of complex number
    "deg": "\\deg",  # Degree symbol (requires gensymb or similar for \\degree)
    "hom": "\\hom",  # Homomorphism
    "ker": "\\ker",  # Kernel
    # TODO: Add more from common usage if necessary
    # "lim inf": "\\liminf", # These are usually handled by n-ary construction
    # "lim sup": "\\limsup",
}

# Minimal set of accent characters to LaTeX command templates
ACCENT_CHAR_TO_LATEX: Dict[str, str] = {
    "0300": "\\grave{{{0}}}",  # Combining Grave Accent
    "0301": "\\acute{{{0}}}",  # Combining Acute Accent
    "0302": "\\hat{{{0}}}",  # Combining Circumflex Accent
    # Add more accents as needed
}

# Minimal set of delimiter characters
DELIMITER_MAP: Dict[str, str] = {
    "(": "(",
    ")": ")",
    "[": "[",
    "]": "]",
    "{": "\\{",
    "}": "\\}",
    "|": "|",
    # Add more delimiters as needed
}

# LaTeX special characters that need escaping
LATEX_SPECIAL_CHARS = {
    "&": "\\&",
    "%": "\\%",
    "$": "\\$",
    "#": "\\#",
    "_": "\\_",
    "{": "\\{",
    "}": "\\}",
    "~": "\\textasciitilde{}",
    "^": "\\textasciicircum{}",
    "\\": "\\textbackslash{}",
    "\n": "\\\\",  # Newline
}


def escape_latex_text(text: str) -> str:
    """
    Escapes LaTeX special characters in a given text string.
    """
    if not isinstance(text, str):
        return ""
    escaped_text = text
    for char, escaped_char in LATEX_SPECIAL_CHARS.items():
        escaped_text = escaped_text.replace(char, escaped_char)
    return escaped_text
