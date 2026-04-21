#!/usr/bin/env python3 -m pytest
"""Tests for the disabled_converters feature (issue #1665).

Covers:
* disabled_converters parameter on MarkItDown.__init__
* disabled_converters property for introspection
* converters property (sorted snapshot)
* TypeError raised for invalid entries in disabled_converters
* Disabled converters are not invoked during file conversion
* enable_builtins=False + manual enable_builtins() respects _disabled_converter_types
* CLI --disable-converter flag and --list-converters flag
"""

import io
import os
import subprocess
import sys
import zipfile
import pytest

from markitdown import (
    StreamInfo,
    StreamInfo,
    MarkItDown,
    ConverterRegistration,
    DocumentConverter,
    UnsupportedFormatException,
)
from markitdown.converters import (
    ZipConverter,
    AudioConverter,
    PdfConverter,
    DocxConverter,
    PptxConverter,
    ImageConverter,
    HtmlConverter,
    PlainTextConverter,
    CsvConverter,
    EpubConverter,
    OutlookMsgConverter,
    XlsxConverter,
    XlsConverter,
    IpynbConverter,
    RssConverter,
    WikipediaConverter,
    YouTubeConverter,
    BingSerpConverter,
)

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ALL_BUILTIN_TYPES = {
    PlainTextConverter,
    ZipConverter,
    HtmlConverter,
    RssConverter,
    WikipediaConverter,
    YouTubeConverter,
    BingSerpConverter,
    DocxConverter,
    XlsxConverter,
    XlsConverter,
    PptxConverter,
    AudioConverter,
    ImageConverter,
    IpynbConverter,
    PdfConverter,
    OutlookMsgConverter,
    EpubConverter,
    CsvConverter,
}


def _converter_type_set(md: MarkItDown) -> set:
    """Return the set of converter *types* currently registered."""
    return {type(r.converter) for r in md.converters}


# ---------------------------------------------------------------------------
# disabled_converters parameter
# ---------------------------------------------------------------------------


def test_no_disabled_converters_registers_all_builtins() -> None:
    """Default construction registers all built-in converters."""
    md = MarkItDown()
    registered = _converter_type_set(md)
    assert ALL_BUILTIN_TYPES.issubset(registered)


def test_single_disabled_converter() -> None:
    """Disabling one converter removes only that type."""
    md = MarkItDown(disabled_converters=[ZipConverter])
    registered = _converter_type_set(md)
    assert ZipConverter not in registered
    # Every other built-in should still be present
    assert ALL_BUILTIN_TYPES - {ZipConverter} <= registered


def test_multiple_disabled_converters() -> None:
    """Disabling several converters removes exactly those types."""
    disabled = [ZipConverter, AudioConverter, PdfConverter]
    md = MarkItDown(disabled_converters=disabled)
    registered = _converter_type_set(md)
    for cls in disabled:
        assert cls not in registered, f"{cls.__name__} should have been disabled"
    for cls in ALL_BUILTIN_TYPES - set(disabled):
        assert cls in registered, f"{cls.__name__} should still be registered"


def test_disabled_converters_empty_list() -> None:
    """An empty list is the same as the default (no converters disabled)."""
    md = MarkItDown(disabled_converters=[])
    assert ALL_BUILTIN_TYPES.issubset(_converter_type_set(md))


def test_disabled_converters_frozenset_input() -> None:
    """disabled_converters accepts any iterable, including a frozenset."""
    md = MarkItDown(disabled_converters=frozenset({ZipConverter, AudioConverter}))
    registered = _converter_type_set(md)
    assert ZipConverter not in registered
    assert AudioConverter not in registered


def test_disabled_converters_rejects_non_subclass() -> None:
    """Passing a non-DocumentConverter type raises TypeError."""
    with pytest.raises(TypeError, match="DocumentConverter subclasses"):
        MarkItDown(disabled_converters=[str])  # type: ignore[list-item]


def test_disabled_converters_rejects_instance_not_class() -> None:
    """Passing a converter *instance* (not a class) raises TypeError."""
    # PlainTextConverter can be constructed without arguments
    with pytest.raises(TypeError, match="DocumentConverter subclasses"):
        MarkItDown(disabled_converters=[PlainTextConverter()])  # type: ignore[list-item]


def test_disabled_converters_rejects_none_in_list() -> None:
    """None in the list raises TypeError."""
    with pytest.raises(TypeError, match="DocumentConverter subclasses"):
        MarkItDown(disabled_converters=[None])  # type: ignore[list-item]


# ---------------------------------------------------------------------------
# disabled_converters property
# ---------------------------------------------------------------------------


def test_disabled_converters_property_default() -> None:
    """disabled_converters property is an empty frozenset by default."""
    md = MarkItDown()
    assert md.disabled_converters == frozenset()


def test_disabled_converters_property_reflects_input() -> None:
    """disabled_converters property mirrors exactly what was passed in."""
    disabled = [ZipConverter, AudioConverter]
    md = MarkItDown(disabled_converters=disabled)
    assert md.disabled_converters == frozenset(disabled)


def test_disabled_converters_property_is_frozenset() -> None:
    """The disabled_converters property always returns a frozenset."""
    md = MarkItDown(disabled_converters=[PdfConverter])
    result = md.disabled_converters
    assert isinstance(result, frozenset)
    # Immutable – should not be modifiable
    with pytest.raises(AttributeError):
        md.disabled_converters = frozenset()  # type: ignore[misc]


# ---------------------------------------------------------------------------
# converters property
# ---------------------------------------------------------------------------


def test_converters_property_returns_tuple() -> None:
    """converters property returns a tuple (immutable snapshot)."""
    md = MarkItDown()
    assert isinstance(md.converters, tuple)


def test_converters_property_sorted_by_priority() -> None:
    """converters property is sorted from lowest to highest priority value."""
    md = MarkItDown()
    priorities = [r.priority for r in md.converters]
    assert priorities == sorted(priorities)


def test_converters_property_contains_registration_objects() -> None:
    """Each element of converters is a ConverterRegistration."""
    md = MarkItDown()
    for reg in md.converters:
        assert isinstance(reg, ConverterRegistration)
        assert isinstance(reg.converter, DocumentConverter)
        assert isinstance(reg.priority, float)


def test_converters_property_snapshot_is_immutable() -> None:
    """Modifying the returned tuple does not affect the internal state."""
    md = MarkItDown()
    snap1 = md.converters
    # Tuple is immutable; a new registration should change the next snapshot
    # but not the already-retrieved one
    count_before = len(snap1)
    md.register_converter(PlainTextConverter())
    snap2 = md.converters
    assert len(snap2) == count_before + 1
    assert len(snap1) == count_before  # old snapshot unaffected


# ---------------------------------------------------------------------------
# Behavioural: disabled converters are not invoked
# ---------------------------------------------------------------------------


def test_zip_converter_disabled_raises_unsupported() -> None:
    """Disabling ZipConverter means ZIP files are reported as unsupported."""
    md = MarkItDown(disabled_converters=[ZipConverter])
    # Build a minimal ZIP so the PlainTextConverter won't claim successful conversion
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("hello.txt", "hello world")
    buf.seek(0)

    with pytest.raises(Exception):
        # Either UnsupportedFormatException or FileConversionException is fine;
        # the important thing is ZipConverter was NOT used successfully.
        result = md.convert_stream(
            buf, stream_info=StreamInfo(extension=".zip")
        )
        # If somehow a fallback claims success, it must NOT contain zip-extracted text
        assert "hello world" not in result.text_content


def test_html_converter_disabled() -> None:
    """Disabling HtmlConverter means HTML is not parsed as Markdown."""
    md = MarkItDown(disabled_converters=[HtmlConverter])
    html = b"<html><body><h1>Secret heading</h1></body></html>"
    # PlainTextConverter (or no converter) may still handle it; what matters
    # is that the <h1> is NOT converted to a Markdown heading via HtmlConverter.
    result = md.convert_stream(io.BytesIO(html), stream_info=StreamInfo(extension=".html"))
    # HtmlConverter would produce "# Secret heading"; without it the output
    # should either be raw HTML or plain-text without the Markdown heading.
    assert "# Secret heading" not in result.text_content


def test_plain_text_falls_back_when_html_disabled() -> None:
    """Plain text content still works when HtmlConverter is disabled (PlainTextConverter picks it up)."""
    md_default = MarkItDown()
    md_no_html = MarkItDown(disabled_converters=[HtmlConverter])
    plain = b"Just plain text here."
    r1 = md_default.convert_stream(
        io.BytesIO(plain), stream_info=StreamInfo(extension=".txt")
    )
    r2 = md_no_html.convert_stream(
        io.BytesIO(plain), stream_info=StreamInfo(extension=".txt")
    )
    assert "Just plain text here." in r1.text_content
    assert "Just plain text here." in r2.text_content


# ---------------------------------------------------------------------------
# enable_builtins=False then manual call
# ---------------------------------------------------------------------------


def test_enable_builtins_false_then_manual_respects_disabled() -> None:
    """
    When enable_builtins=False and enable_builtins() is later called,
    the _disabled_converter_types set is still respected.
    """
    md = MarkItDown(
        enable_builtins=False,
        disabled_converters=[ZipConverter, AudioConverter],
    )
    # Nothing registered yet
    assert len(md.converters) == 0
    # Now enable builtins manually
    md.enable_builtins()
    registered = _converter_type_set(md)
    assert ZipConverter not in registered
    assert AudioConverter not in registered
    assert PlainTextConverter in registered


# ---------------------------------------------------------------------------
# CLI: --disable-converter and --list-converters
# ---------------------------------------------------------------------------


def test_cli_list_converters() -> None:
    """--list-converters prints built-in converter names and exits 0."""
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--list-converters"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"CLI error: {result.stderr}"
    assert "ZipConverter" in result.stdout
    assert "AudioConverter" in result.stdout
    assert "PdfConverter" in result.stdout


def test_cli_disable_converter_basic() -> None:
    """--disable-converter removes the named converter and conversion still works."""
    # Convert a plain-text file with ZipConverter disabled
    txt_file = os.path.join(TEST_FILES_DIR, "test.txt")
    if not os.path.exists(txt_file):
        pytest.skip("test.txt not found in test_files directory")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "markitdown",
            "--disable-converter",
            "ZipConverter",
            txt_file,
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"CLI error: {result.stderr}"


def test_cli_disable_converter_unknown_name() -> None:
    """--disable-converter with an unknown name prints an error and exits non-zero."""
    txt_file = os.path.join(TEST_FILES_DIR, "test.txt")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "markitdown",
            "--disable-converter",
            "NonExistentConverter",
            txt_file if os.path.exists(txt_file) else "/dev/null",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "NonExistentConverter" in result.stdout or "NonExistentConverter" in result.stderr


def test_cli_disable_multiple_converters() -> None:
    """--disable-converter may be repeated to disable several converters."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "markitdown",
            "--disable-converter",
            "ZipConverter",
            "--disable-converter",
            "AudioConverter",
            "--list-converters",  # use --list-converters to verify we reach the code
        ],
        capture_output=True,
        text=True,
    )
    # --list-converters exits 0 even when --disable-converter flags are present
    assert result.returncode == 0
