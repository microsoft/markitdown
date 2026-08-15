# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
"""Discover which file extensions this build of MarkItDown can actually
convert, straight from the registered converters -- never a hand-maintained
list that can silently drift out of sync with the real library.

How it works: every built-in converter module in `markitdown.converters`
defines its accepted extensions as a module-level constant whose name ends in
"EXTENSIONS" (e.g. `ACCEPTED_FILE_EXTENSIONS`, `ACCEPTED_XLSX_FILE_EXTENSIONS`,
`PRECISE_FILE_EXTENSIONS`). We instantiate a real `MarkItDown()` -- the exact
object the app calls `.convert_local()` on -- and, for each converter it
actually registered, scan that converter's defining module for those
constants. That also means cloud-only converters (Document Intelligence /
Content Understanding) are naturally excluded: they're only registered when
their endpoint kwargs are supplied, which this offline GUI never does.
"""

from __future__ import annotations

import re
from typing import List

from markitdown import MarkItDown

_EXTENSION_CONST_RE = re.compile(r"EXTENSIONS$")


def get_supported_extensions() -> List[str]:
    """Return a sorted, deduplicated list of extensions (e.g. ['.csv', '.docx', ...])
    that the currently-registered MarkItDown converters advertise support for.
    """
    md = MarkItDown(enable_builtins=True, enable_plugins=False)

    extensions = set()
    # NOTE: `_converters` is a private attribute of MarkItDown. We read it
    # (never write it) purely to enumerate what's registered -- it's the
    # single most accurate source of "what will convert() actually try",
    # short of forking the library to add a public introspection API.
    for registration in md._converters:  # noqa: SLF001
        module_name = type(registration.converter).__module__
        module = __import__(module_name, fromlist=["*"])
        for name, value in vars(module).items():
            if not _EXTENSION_CONST_RE.search(name):
                continue
            if not isinstance(value, (list, tuple)):
                continue
            for ext in value:
                if isinstance(ext, str) and ext.startswith("."):
                    extensions.add(ext.lower())

    return sorted(extensions)


# A few well-known extensions to prefer showing first, so the summary line
# reads as recognizable formats rather than an arbitrary alphabetical prefix
# (".atom, .csv, .docx" leads with two formats most users won't recognize).
# Purely cosmetic ordering -- has no effect on which extensions are counted.
_PREFERRED_DISPLAY_ORDER = [
    ".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".html", ".txt", ".png", ".jpg"
]


def format_supported_extensions_label(max_shown: int = 6) -> str:
    """A short, human-friendly summary line for the GUI that fits on one
    line in a small, fixed-size window, e.g.
    'Supports: .csv, .docx, .html, .pdf, .pptx, .xlsx, +22 more'

    Still fully accurate/live: both the shown extensions and the "+N more"
    count come straight from get_supported_extensions() every time this is
    called, never a hand-maintained list -- we just don't print all ~28 of
    them verbatim, since that wraps to multiple lines and doesn't fit
    comfortably in the app's small, fixed-size window.
    """
    extensions = get_supported_extensions()
    if not extensions:
        return "Supported formats: none detected"
    if len(extensions) <= max_shown:
        return "Supports: " + ", ".join(extensions)

    shown = [ext for ext in _PREFERRED_DISPLAY_ORDER if ext in extensions][:max_shown]
    remaining = [ext for ext in extensions if ext not in shown]
    while len(shown) < max_shown and remaining:
        shown.append(remaining.pop(0))
    shown.sort()

    more = len(extensions) - len(shown)
    return "Supports: " + ", ".join(shown) + f", +{more} more"
