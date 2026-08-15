# SPDX-FileCopyrightText: 2026-present Ayush Chaugule
#
# SPDX-License-Identifier: MIT
"""Thin, UI-agnostic wrapper around the real `markitdown.MarkItDown` class.

This module deliberately contains no conversion logic of its own -- it exists
so `app.py` has exactly one narrow, typed call site for "convert this file",
and so a future MarkItDown API change only needs to be absorbed here. Nothing
in this file imports tkinter; it's plain enough to unit test headlessly.
"""

from __future__ import annotations

from markitdown import DocumentConverterResult, MarkItDown

_markitdown_instance: MarkItDown | None = None


def _get_markitdown() -> MarkItDown:
    """Lazily build (and cache) the MarkItDown instance.

    Cached rather than rebuilt per-conversion because construction re-loads
    the magika content-type-detection model; the app only ever converts one
    file at a time, so a single shared instance is safe to reuse.
    """
    global _markitdown_instance
    if _markitdown_instance is None:
        # enable_plugins=False: the GUI's "Supports: ..." label (see formats.py)
        # is built from this exact configuration, so plugins staying off here
        # keeps that claim accurate. enable_builtins defaults to True.
        _markitdown_instance = MarkItDown(enable_plugins=False)
    return _markitdown_instance


def convert_to_markdown(path: str) -> DocumentConverterResult:
    """Convert a local file to Markdown using the real MarkItDown class.

    Uses `convert_local()` rather than the more permissive `convert()`. Per
    this repo's own README security guidance, callers should use the
    narrowest conversion method that fits their use case -- a GUI file picker
    only ever produces local file paths, never URLs or arbitrary streams, so
    there's no reason to route through the code paths that also accept those.
    """
    return _get_markitdown().convert_local(path)
