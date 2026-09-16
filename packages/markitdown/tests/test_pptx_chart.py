#!/usr/bin/env python3 -m pytest
"""A chart the converter cannot read must not cost the whole presentation."""

import io
import zipfile

import pptx
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

from markitdown import MarkItDown, StreamInfo
from markitdown.converters._pptx_converter import PptxConverter


def _build_deck() -> bytes:
    """A deck with a column chart on slide 1 and plain text on slide 2."""
    prs = pptx.Presentation()

    chart_slide = prs.slides.add_slide(prs.slide_layouts[5])
    chart_slide.shapes.title.text = "Quarterly revenue"
    data = CategoryChartData()
    data.categories = ["Q1", "Q2", "Q3"]
    data.add_series("Revenue", (10.0, 20.0, 30.0))
    chart_slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(1),
        Inches(2),
        Inches(6),
        Inches(4),
        data,
    )

    text_slide = prs.slides.add_slide(prs.slide_layouts[1])
    text_slide.shapes.title.text = "Outlook"
    text_slide.placeholders[
        1
    ].text_frame.text = "Everything after the chart lives here."

    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()


def _rewrite_chart_part(deck: bytes, old: bytes, new: bytes) -> io.BytesIO:
    """Return the deck with `old` replaced by `new` inside its chart part."""
    source = zipfile.ZipFile(io.BytesIO(deck))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as target:
        for entry in source.infolist():
            payload = source.read(entry.filename)
            if entry.filename.startswith("ppt/charts/chart"):
                assert old in payload, f"{old!r} not in the chart part"
                payload = payload.replace(old, new)
            target.writestr(entry, payload)
    out.seek(0)
    return out


def _convert(stream: io.BytesIO) -> str:
    return (
        MarkItDown()
        .convert_stream(stream, stream_info=StreamInfo(extension=".pptx"))
        .markdown
    )


def test_a_readable_chart_is_still_a_table() -> None:
    markdown = _convert(io.BytesIO(_build_deck()))

    assert "| Q1 | 10.0 |" in markdown
    assert "Everything after the chart lives here." in markdown


def test_a_non_numeric_point_does_not_lose_the_presentation() -> None:
    """`#N/A` in a numeric cache is what a linked worksheet leaves behind.

    python-pptx parses the cache eagerly, so the whole series raises. The rest
    of the deck has nothing to do with that chart and must survive.
    """
    deck = _rewrite_chart_part(_build_deck(), b"<c:v>20.0</c:v>", b"<c:v>#N/A</c:v>")

    markdown = _convert(deck)

    assert "# Quarterly revenue" in markdown
    assert "Everything after the chart lives here." in markdown
    # Categories and the series name are readable, so the table keeps its shape.
    assert "| Category | Revenue |" in markdown
    assert "| Q1 |" in markdown


def test_an_unreadable_chart_becomes_a_placeholder() -> None:
    """A chart that fails for any other reason reports itself and moves on."""
    deck = _rewrite_chart_part(
        _build_deck(), b'<c:order val="0"/>', b'<c:order val="zero"/>'
    )

    markdown = _convert(deck)

    assert "[unsupported chart]" in markdown
    assert "# Quarterly revenue" in markdown
    assert "Everything after the chart lives here." in markdown


def test_an_unsupported_plot_type_still_becomes_a_placeholder() -> None:
    deck = _rewrite_chart_part(_build_deck(), b"c:barChart", b"c:surface3DChart")

    markdown = _convert(deck)

    assert "[unsupported chart]" in markdown
    assert "Everything after the chart lives here." in markdown


def test_the_chart_converter_never_returns_none() -> None:
    """The caller concatenates the result straight into the document."""

    class _Unreadable:
        @property
        def has_title(self):
            raise ValueError("something the converter has never seen")

    assert PptxConverter()._convert_chart_to_markdown(_Unreadable()) is not None
