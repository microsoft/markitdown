#!/usr/bin/env python3 -m pytest
"""Tests that PDF conversion is resilient to malformed form XObjects.

Some PDFs contain a form XObject whose ``/BBox`` is not the four-number
rectangle required by the spec. This used to make the underlying PDF backend
raise ``ValueError: not enough values to unpack (expected 4, got 2)`` and abort
the whole conversion. The converter should skip the malformed page and still
recover the text from the other pages.
"""

import io

from markitdown import MarkItDown


def _pdf_with_invalid_form_bbox() -> bytes:
    """Build a two-page PDF whose second page has a form XObject /BBox [0 0].

    The first page holds the text "Hello from markitdown"; the second invokes a
    form XObject with a malformed (two-number) /BBox. Built in-memory so the test
    stays self-contained and free of line-ending conversion on a committed PDF.
    """
    form_stream = b"q Q"
    text_stream = b"BT /F1 12 Tf 50 100 Td (Hello from markitdown) Tj ET"
    objs = [
        b"<</Type/Catalog/Pages 2 0 R>>",
        b"<</Type/Pages/Kids[3 0 R 4 0 R]/Count 2>>",
        b"<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]"
        b"/Resources<</Font<</F1 7 0 R>>>>/Contents 5 0 R>>",
        b"<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]"
        b"/Resources<</XObject<</Fm0 6 0 R>>>>/Contents 8 0 R>>",
        b"<</Length %d>>\nstream\n%s\nendstream" % (len(text_stream), text_stream),
        b"<</Type/XObject/Subtype/Form/FormType 1/BBox [0 0]/Resources<<>>"
        b"/Length %d>>\nstream\n%s\nendstream" % (len(form_stream), form_stream),
        b"<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>",
        b"<</Length 7>>\nstream\n/Fm0 Do\nendstream",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for i, obj in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (i, obj)
    startxref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer<</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF" % (
        len(objs) + 1,
        startxref,
    )
    return out


def test_invalid_form_bbox_does_not_crash():
    """A page with an invalid form /BBox must not abort the whole document."""
    pdf_bytes = io.BytesIO(_pdf_with_invalid_form_bbox())

    result = MarkItDown().convert_stream(pdf_bytes, file_extension=".pdf")

    # The good first page is recovered even though the second page is malformed.
    assert result.text_content is not None
    assert "Hello from markitdown" in result.text_content
    # A skipped page must not leak a raw Python traceback into the output.
    assert "Traceback" not in result.text_content
