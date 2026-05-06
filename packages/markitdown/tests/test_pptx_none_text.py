"""Regression test for #1808.

``PptxConverter.convert`` performed unguarded ``+`` concatenation on
``shape.text`` and ``notes_frame.text``. python-pptx can return ``None``
for either when a text frame has a run with no ``<a:t>`` child, or when
a third-party deck represents a chart/SmartArt title text as ``None``.
A single such shape used to fail the entire .pptx conversion with::

    PptxConverter threw TypeError with message:
      can only concatenate str (not "NoneType") to str

The fix coerces ``shape.text`` / ``notes_frame.text`` to ``""`` before
concatenation. This pins both call sites.
"""

from __future__ import annotations

from io import BytesIO

import pytest

pptx = pytest.importorskip("pptx")  # markitdown[pptx] extra

from markitdown import MarkItDown


def _build_minimal_pptx_with_text(text: str) -> BytesIO:
    """Build a minimal one-slide .pptx that contains *text* in the body
    placeholder. Returns a BytesIO suitable for MarkItDown.convert_stream.
    """
    prs = pptx.Presentation()
    # Layout 1 = "Title and Content"
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Hello"
    body_placeholder = slide.placeholders[1]
    body_placeholder.text = text
    buf = BytesIO()
    prs.save(buf)
    buf.seek(0)
    return buf


def test_pptx_with_none_shape_text_does_not_crash(monkeypatch):
    """Regression for #1808: a shape whose ``.text`` returns ``None`` must
    not fail the whole conversion."""
    # Build the deck BEFORE monkey-patching — replacing ``text`` with a
    # getter-only property breaks the ``placeholder.text = ...`` setter.
    stream = _build_minimal_pptx_with_text("World")

    pptx_text_module = pptx.text.text
    original_text = pptx_text_module.TextFrame.text.fget

    def _none_for_world(self):  # type: ignore[no-untyped-def]
        value = original_text(self)
        return None if value == "World" else value

    monkeypatch.setattr(
        pptx_text_module.TextFrame,
        "text",
        property(_none_for_world),
    )

    md = MarkItDown()
    result = md.convert_stream(stream, file_extension=".pptx")

    # Conversion completes without raising. The deck's body shape resolved
    # to None and was treated as empty; the title row is still preserved
    # because it doesn't trip the None branch.
    assert "# Hello" in result.text_content


def test_pptx_with_none_notes_text_does_not_crash(monkeypatch):
    """Regression for #1808: ``notes_frame.text`` returning ``None`` must
    not fail conversion either."""
    # Build a deck and add a notes slide with text we'll monkey-patch to None.
    prs = pptx.Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Hello"
    notes = slide.notes_slide.notes_text_frame
    notes.text = "speaker note"
    buf = BytesIO()
    prs.save(buf)
    buf.seek(0)

    # Patch only the notes frame's TextFrame.text accessor to None.
    pptx_text_module = pptx.text.text
    original_text = pptx_text_module.TextFrame.text.fget

    def _none_for_speaker_note(self):  # type: ignore[no-untyped-def]
        value = original_text(self)
        return None if value == "speaker note" else value

    monkeypatch.setattr(
        pptx_text_module.TextFrame,
        "text",
        property(_none_for_speaker_note),
    )

    md = MarkItDown()
    result = md.convert_stream(buf, file_extension=".pptx")
    # Conversion completes; title still appears.
    assert "# Hello" in result.text_content


def test_pptx_normal_text_still_converts():
    """Regression guard: the coercion must not change behavior for normal
    decks where ``shape.text`` is a real string."""
    stream = _build_minimal_pptx_with_text("body content")
    md = MarkItDown()
    result = md.convert_stream(stream, file_extension=".pptx")
    assert "# Hello" in result.text_content
    assert "body content" in result.text_content
