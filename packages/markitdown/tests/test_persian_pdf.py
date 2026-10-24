"""Public API acceptance tests. See test_files/persian/README.md."""

import hashlib
import json
import unicodedata
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from markitdown import MarkItDown, StreamInfo
from markitdown.converters._pdf_layout import (
    _lines,
    _logical_line,
    extract_ordered_content,
)

from .report_persian_pdf import (
    ROOT,
    BUNDLE,
    case_pdf,
    expected,
    body,
    CASES,
    EXPECTED,
    evaluate,
    distance,
    order_accuracy,
    table_rows,
)


@pytest.fixture(scope="module")
def converter():
    return MarkItDown()


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_persian_pdf(case, converter):
    actual = converter.convert_stream(
        case_pdf(case), stream_info=StreamInfo(extension=".pdf")
    ).markdown
    metrics = evaluate(case, actual)
    assert metrics["pass"], f"{case['id']}: {metrics}\nActual: {actual!r}"


def test_fixture_integrity():
    hashes = json.loads((ROOT / "sha256.json").read_text(encoding="utf-8"))
    for name, digest in hashes.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    assert [c["page"] for c in CASES] == list(range(1, len(CASES) + 1))
    import pypdfium2

    with pypdfium2.PdfDocument(BUNDLE) as pdf:
        assert len(pdf) == len(CASES)
    assert len(CASES) >= 15
    assert len({c["id"] for c in CASES}) == len(CASES)
    assert set(EXPECTED) == {c["id"] for c in CASES}


def test_metrics_detect_reordering_and_flattening():
    assert distance("می‌روم", "میروم") == 1
    assert distance("ی", "ي") == 1
    assert order_accuracy(["one", "two"], "two one") == 0
    assert order_accuracy(["one", "two"], "one") == 0
    assert table_rows("name code value\npolymer PE-101 25") == []
    assert table_rows("| a | b |\n| :--- | ---: |\n| c | d |") == [
        ["a", "b"],
        ["c", "d"],
    ]


# Glyph-level reconstruction and fallback regressions


def glyph(text, x, baseline=700, size=14, font_shift=0):
    return dict(
        text=text,
        x0=x,
        x1=x + (0 if text == "َ" else 7),
        top=800 - baseline + font_shift,
        bottom=814 - baseline + font_shift,
        size=size,
        upright=True,
        matrix=(1, 0, 0, 1, x, baseline),
    )


def painted(text):
    # Each item is one glyph mapping; multi-codepoint items are indivisible.
    chars = []
    x = 0
    for value in text:
        chars.append(glyph(value, x))
        if not all(unicodedata.combining(c) for c in value):
            x += 7
    return chars


@pytest.mark.parametrize(
    ("visual", "logical"),
    [
        (list(".مالس"), "سلام."),
        (["م", "لا", "َ", "س"], "سَلام"),
        (list(".تسا A-17 هسانش"), "شناسه A-17 است."),
        (list(".تسا DOC-2026 هسانش"), "شناسه DOC-2026 است."),
        (list(".تسا Python 3.12 نابز"), "زبان Python 3.12 است."),
        (
            list(".تسا https://example.org/a-12 هسانش"),
            "شناسه https://example.org/a-12 است.",
        ),
        (list(".تسا test@example.org یناشن"), "نشانی test@example.org است."),
        (list(".تسا ۱۴۰۵/۰۷/۳۰ خیرات"), "تاریخ ۱۴۰۵/۰۷/۳۰ است."),
        (list(".تسا )x + 3 = 9( هطبار"), "رابطه (x + 3 = 9) است."),
        (list(".تسا g/mL 2.5 رادقم"), "مقدار 2.5 g/mL است."),
        (
            list(".تسا https://example.org/g/mL 12 دک"),
            "کد https://example.org/g/mL 12 است.",
        ),
        (list("Use مالس in DOC-17."), "Use سلام in DOC-17."),
        (list("0123456789"), "0123456789"),
        (list("LTR (A-17) 3.75 mg/L"), "LTR (A-17) 3.75 mg/L"),
    ],
)
def test_directional_glyph_runs(visual, logical):
    assert _logical_line(painted(visual)) == logical


def test_logical_paint_order_is_not_reversed_twice():
    chars = [glyph(char, 140 - i * 7) for i, char in enumerate("می‌روم")]
    assert _logical_line(_lines(chars)[0].chars) == "می‌روم"


def test_coincident_joiner_retains_unicode_position():
    chars = painted(["م", "و", "ر", "‌", "ی", "م"])
    chars[4]["x0"] = 21
    chars[4]["x1"] = 28
    chars[5]["x0"] = 28
    chars[5]["x1"] = 35
    chars[3]["x0"] = 21.004
    chars[3]["x1"] = 21
    assert _logical_line(_lines(chars)[0].chars) == "می‌روم"


def test_font_metrics_do_not_split_baseline():
    chars = [glyph("P", 0, font_shift=-6), glyph("3", 7), glyph("ت", 14)]
    assert len(_lines(chars)) == 1
    assert _logical_line(_lines(chars)[0].chars) == "تP3"


def test_geometry_inserts_missing_spaces():
    chars = painted(list("تسا"))
    chars += [glyph("A-17", 40)]
    chars += [glyph(c, 70 + i * 7) for i, c in enumerate("هسانش")]
    assert _logical_line(chars) == "شناسه A-17 است"


@pytest.mark.parametrize("rotated", [True, False])
def test_unsupported_orientation_and_empty_page_defer(rotated):
    chars = painted(list("مالس")) if rotated else []
    if rotated:
        chars[0]["matrix"] = (0, 1, -1, 0, 0, 700)
    assert extract_ordered_content(SimpleNamespace(chars=chars)) is None


def test_ruled_ltr_table_is_not_reinterpreted_as_columns():
    chars = [
        glyph("left", 10),
        glyph("right", 400),
        glyph("bottom", 10, 650),
        glyph("value", 400, 650),
    ]
    page = SimpleNamespace(chars=chars, width=600, edges=[object()])
    assert extract_ordered_content(page) is None


def test_spanning_heading_defers_ltr_column_guess():
    chars = [
        glyph("Title", 200, 750),
        glyph("left", 10),
        glyph("right", 400),
        glyph("bottom", 10, 650),
        glyph("value", 400, 650),
    ]
    assert (
        extract_ordered_content(SimpleNamespace(chars=chars, width=600, edges=[]))
        is None
    )


def test_pdfminer_fallback_remains_available():
    from markitdown.converters import _pdf_converter

    with patch.object(
        _pdf_converter.pdfplumber, "open", side_effect=ValueError("bad layout")
    ):
        actual = (
            MarkItDown()
            .convert_stream(
                case_pdf(next(c for c in CASES if c["id"] == "ltr_sentence")),
                stream_info=StreamInfo(extension=".pdf"),
            )
            .markdown
        )
    assert actual.strip() == "The identifier DOC-2026-A15 uses Python 3.12."


def test_page_cache_is_closed_when_layout_reconstruction_fails(monkeypatch):
    from markitdown.converters import _pdf_converter

    closed = []
    original_close = _pdf_converter.pdfplumber.page.Page.close

    def close(page):
        closed.append(page.page_number)
        return original_close(page)

    def fail(page):
        raise ValueError("invalid glyph layout")

    monkeypatch.setattr(_pdf_converter.pdfplumber.page.Page, "close", close)
    monkeypatch.setattr(_pdf_converter, "extract_ordered_content", fail)
    actual = (
        MarkItDown()
        .convert_stream(
            case_pdf(next(c for c in CASES if c["id"] == "ltr_sentence")),
            stream_info=StreamInfo(extension=".pdf"),
        )
        .markdown
    )
    assert actual.strip() == "The identifier DOC-2026-A15 uses Python 3.12."
    assert 1 in closed


def test_complete_persian_bundle(converter):
    # Exercise page boundaries and the mixed plain/RTL/table extraction path as
    # well as isolated pages. This expected document is built from authored
    # ground truth, never from extraction results.
    pages = []
    for case in CASES:
        truth = expected(case)
        if isinstance(truth, list):
            rows = ["| " + " | ".join(truth[0]) + " |"]
            rows.append("| " + " | ".join("---" for _ in truth[0]) + " |")
            rows.extend("| " + " | ".join(row) + " |" for row in truth[1:])
            truth = "\n".join(rows)
        pages.append(truth)
    assert body(converter.convert(str(BUNDLE)).markdown) == "\n\n".join(pages)
