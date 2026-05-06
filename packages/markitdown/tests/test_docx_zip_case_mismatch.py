"""Regression test for #1812.

Some .docx producers emit zip files where local file header names disagree
with the central-directory names in case only (e.g. ``customXML/item2.xml``
locally, ``customXml/item2.xml`` centrally). Most zip tools accept this,
but Python's :mod:`zipfile` raises ``BadZipFile``. ``pre_process_docx``
must repair the archive before opening so .docx conversion does not crash
on these files.
"""

from __future__ import annotations

import struct
import zipfile
from io import BytesIO

import pytest

from markitdown.converter_utils.docx.pre_process import (
    _fix_zip_name_casing,
    pre_process_docx,
)


_MINIMAL_DOCUMENT_XML = (
    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    b'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    b"<w:body><w:p><w:r><w:t>hello world</w:t></w:r></w:p></w:body>"
    b"</w:document>"
)


def _build_minimal_docx_bytes(local_name_override: dict[str, str] | None = None) -> bytes:
    """Build a minimal .docx zip in memory.

    If ``local_name_override`` is supplied, after writing the archive the
    local file header bytes for the listed entry are patched in place so
    the local name differs from the central-directory name (case only —
    same byte length).
    """
    buf = BytesIO()
    with zipfile.ZipFile(buf, mode="w") as zf:
        zf.writestr("word/document.xml", _MINIMAL_DOCUMENT_XML)
        # An entry whose case will be munged by the override below.
        zf.writestr("customXml/item2.xml", b"<root/>")
    raw = bytearray(buf.getvalue())
    if not local_name_override:
        return bytes(raw)

    # Patch local file headers in place. The central directory remains
    # intact, so opening the resulting bytes with stock zipfile fails — the
    # exact bug we want to reproduce.
    info_offsets: dict[str, int] = {}
    with zipfile.ZipFile(BytesIO(bytes(raw)), mode="r") as zf:
        for info in zf.infolist():
            info_offsets[info.filename] = info.header_offset
    for central_name, replacement_local_name in local_name_override.items():
        offset = info_offsets[central_name]
        # Sanity: the local file header signature must be at this offset.
        assert raw[offset : offset + 4] == b"PK\x03\x04"
        fname_len = struct.unpack_from("<H", raw, offset + 26)[0]
        new_bytes = replacement_local_name.encode("utf-8")
        assert len(new_bytes) == fname_len, (
            "test setup error: replacement name must match the original "
            "byte length so the override is purely a case-flip"
        )
        raw[offset + 30 : offset + 30 + fname_len] = new_bytes
    return bytes(raw)


def test_setup_actually_reproduces_badzipfile():
    """Sanity guard: without the fix, the constructed bytes raise BadZipFile.

    If this test ever passes silently (i.e. zipfile stops validating local-
    vs-central name mismatches), the regression below would also pass for
    the wrong reason and we'd lose coverage of the original bug.
    """
    bad = _build_minimal_docx_bytes(
        local_name_override={"customXml/item2.xml": "customXML/item2.xml"}
    )
    with pytest.raises(zipfile.BadZipFile):
        with zipfile.ZipFile(BytesIO(bad), mode="r") as zf:
            zf.read("customXml/item2.xml")


def test_fix_zip_name_casing_repairs_mismatched_local_header():
    """``_fix_zip_name_casing`` must rewrite local headers to match the
    central directory so the archive becomes openable."""
    bad = _build_minimal_docx_bytes(
        local_name_override={"customXml/item2.xml": "customXML/item2.xml"}
    )
    fixed = _fix_zip_name_casing(BytesIO(bad))
    # After repair the archive opens cleanly and the entry reads back.
    with zipfile.ZipFile(fixed, mode="r") as zf:
        assert zf.read("customXml/item2.xml") == b"<root/>"


def test_fix_zip_name_casing_passes_through_normal_archive():
    """A correctly-formed .docx must not be rewritten — return the same
    stream rewound to the start so callers can keep using it."""
    good = _build_minimal_docx_bytes(local_name_override=None)
    src = BytesIO(good)
    out = _fix_zip_name_casing(src)
    # Either the same object or an equivalent BytesIO; either way the bytes
    # we get back should match the input we started with.
    out.seek(0)
    assert out.read() == good


def test_pre_process_docx_accepts_case_mismatched_archive():
    """End-to-end regression for #1812: ``pre_process_docx`` must not
    raise on a .docx whose local headers differ from the central directory
    in case only, and the resulting archive must still contain the
    pre-processed ``word/document.xml`` payload."""
    bad = _build_minimal_docx_bytes(
        local_name_override={"customXml/item2.xml": "customXML/item2.xml"}
    )
    out = pre_process_docx(BytesIO(bad))
    out.seek(0)
    with zipfile.ZipFile(out, mode="r") as zf:
        # word/document.xml is one of the pre-processed files; it should be
        # present and contain the original body text (no math substitution
        # occurs on this minimal payload).
        body = zf.read("word/document.xml")
        assert b"hello world" in body
        # The previously-mismatched entry survived too.
        assert zf.read("customXml/item2.xml") == b"<root/>"
