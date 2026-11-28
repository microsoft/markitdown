"""Spreadsheet conversion, compatibility repairs, and image hooks."""

import inspect
import io
import zipfile
from pathlib import Path
from typing import Any, BinaryIO, Callable, Optional
from unittest.mock import Mock
from xml.etree import ElementTree as ET

import openpyxl
import pytest
from PIL import Image
from bs4 import BeautifulSoup
from defusedxml.common import EntitiesForbidden
from openpyxl.drawing.image import Image as SheetImage
from openpyxl.drawing.spreadsheet_drawing import (
    AbsoluteAnchor,
    AnchorMarker,
    OneCellAnchor,
    TwoCellAnchor,
)

from markitdown import MarkItDown, MissingDependencyException, StreamInfo
from markitdown.converter_utils import _xlsx_images
from markitdown.converters import XlsConverter, XlsxConverter, _xlsx_converter

# Image hooks

_INFO = StreamInfo(extension=".xlsx")


def _png(color: str) -> bytes:
    stream = io.BytesIO()
    Image.new("RGB", (2, 2), color).save(stream, "PNG")
    return stream.getvalue()


_RED, _BLUE = _png("red"), _png("blue")


def _workbook(*, images: bool = True) -> bytes:
    workbook = openpyxl.Workbook()
    first = workbook.active
    first.title = "Second"
    first.append(["Header_one", None])
    first.append(["<native> & *value*", 12])
    last = workbook.create_sheet("First")
    last.append(["Other"])
    last.append(["End"])
    if images:
        for data, anchor in (
            (_RED, OneCellAnchor(_from=AnchorMarker(col=26, row=2))),
            (
                _BLUE,
                TwoCellAnchor(
                    _from=AnchorMarker(col=2, row=4), to=AnchorMarker(col=4, row=7)
                ),
            ),
            (_RED, AbsoluteAnchor()),
        ):
            image = SheetImage(io.BytesIO(data))
            image.anchor = anchor
            first.add_image(image)
        last.add_image(SheetImage(io.BytesIO(_BLUE)), "Z10")
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def _rewrite(data: bytes, change: Callable[[str, bytes], bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(data)) as source:
        with zipfile.ZipFile(output, "w") as target:
            for entry in source.infolist():
                target.writestr(entry, change(entry.filename, source.read(entry)))
    return output.getvalue()


class _ImageConverter(XlsxConverter):
    def __init__(self, render: Callable[..., Optional[str]]):
        super().__init__()
        self.render = render

    def _image_to_html(
        self, image_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any
    ) -> Optional[str]:
        return self.render(image_stream, stream_info, **kwargs)


def _convert(converter: XlsxConverter, data: bytes, **kwargs: Any) -> str:
    return converter.convert(io.BytesIO(data), _INFO, **kwargs).markdown


def test_image_hook_keeps_native_public_signature_and_acceptance() -> None:
    assert list(inspect.signature(XlsxConverter.convert).parameters) == [
        "self",
        "file_stream",
        "stream_info",
        "kwargs",
    ]
    assert list(inspect.signature(XlsxConverter.__init__).parameters) == ["self"]
    assert _ImageConverter.convert is XlsxConverter.convert
    converter = XlsxConverter()
    assert converter.accepts(io.BytesIO(), StreamInfo(extension=".XLSX"))
    assert converter.accepts(
        io.BytesIO(),
        StreamInfo(
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
    assert not converter.accepts(io.BytesIO(), StreamInfo(extension=".xls"))


def test_hook_receives_original_images_metadata_options_and_legacy_anchor_order() -> (
    None
):
    seen = []
    streams = []
    service = object()

    def render(stream: BinaryIO, info: StreamInfo, **kwargs: Any) -> str:
        assert stream.seekable() and stream.tell() == 0
        image = stream.read()
        stream.seek(0)
        assert stream.read() == image
        seen.append((image, info, kwargs))
        streams.append(stream)
        return f"<p><strong>image_{len(seen)}</strong></p>"

    class InheritedImages(_ImageConverter):
        pass

    source = io.BytesIO(_workbook())
    original = source.getvalue()
    source.seek(7)
    info = StreamInfo(
        extension=".xlsx",
        filename="parent.xlsx",
        local_path="/parent.xlsx",
        url="https://example.test/parent.xlsx",
    )
    result = InheritedImages(render).convert(
        source,
        info,
        ocr_service=service,
        heading_style="atx",
        escape_underscores=False,
        filename="parent-option.xlsx",
        url="https://example.test/option.xlsx",
    )

    # Preserve openpyxl's absolute, one-cell, two-cell traversal, not ZIP order.
    assert [(data, metadata) for data, metadata, _ in seen] == [
        (
            _RED,
            StreamInfo(extension=".png", mimetype="image/png", filename="image3.png"),
        ),
        (
            _RED,
            StreamInfo(extension=".png", mimetype="image/png", filename="image1.png"),
        ),
        (
            _BLUE,
            StreamInfo(extension=".png", mimetype="image/png", filename="image2.png"),
        ),
        (
            _BLUE,
            StreamInfo(extension=".png", mimetype="image/png", filename="image4.png"),
        ),
    ]
    assert all(options["ocr_service"] is service for _, _, options in seen)
    assert all(options["filename"] == "parent-option.xlsx" for _, _, options in seen)
    expected_order = [
        "## Second",
        "| <native> & \\*value\\* | 12 |",
        "### Images in this sheet:",
        "**image_1**",
        "**image_2**",
        "**image_3**",
        "## First",
        "| End |",
        "**image_4**",
    ]
    offsets = [result.markdown.index(text) for text in expected_order]
    assert offsets == sorted(offsets)
    assert "Image at " not in result.markdown
    assert all(stream.closed for stream in streams)
    assert not source.closed and source.getvalue() == original


@pytest.mark.parametrize(
    ("template", "expected"),
    [
        ("<strong>{}</strong>", "**one**\n\n**two**\n\n**three**"),
        ("{}", "one\n\ntwo\n\nthree"),
        ("{}<br>line", "one  \nline\n\ntwo  \nline\n\nthree  \nline"),
        (
            "<p>{}</p><p>paragraph</p>",
            "one\n\nparagraph\n\ntwo\n\nparagraph\n\nthree\n\nparagraph",
        ),
    ],
)
def test_image_fragments_are_separate_valid_blocks(
    monkeypatch: pytest.MonkeyPatch, template: str, expected: str
) -> None:
    render = Mock(
        side_effect=[template.format(text) for text in ("one", "two", "three", "four")]
    )
    converter = _ImageConverter(render)
    convert_html = Mock(wraps=converter._html_converter.convert_string)
    monkeypatch.setattr(converter._html_converter, "convert_string", convert_html)

    result = _convert(converter, _workbook())

    assert f"### Images in this sheet:\n\n{expected}\n\n## First\n" in result
    soup = BeautifulSoup(convert_html.call_args_list[1].args[0], "html.parser")
    assert [tag.name for tag in soup.find_all(recursive=False)] == [
        "h3",
        "div",
        "div",
        "div",
    ]
    assert not soup.select("p div")


@pytest.mark.parametrize("fragment", [None, "", " \n\t"])
def test_declining_hook_is_exactly_native(fragment: Optional[str]) -> None:
    data = _workbook()
    options = {"escape_underscores": False, "heading_style": "underlined"}
    assert _convert(_ImageConverter(Mock(return_value=fragment)), data, **options) == (
        _convert(XlsxConverter(), data, **options)
    )


def test_default_converter_does_not_parse_images_or_change_native_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        _xlsx_images, "_XlsxImages", Mock(side_effect=AssertionError("extra parsing"))
    )
    reader = Mock(wraps=_xlsx_converter.pd.read_excel)
    monkeypatch.setattr(_xlsx_converter.pd, "read_excel", reader)

    class NativeSubclass(XlsxConverter):
        pass

    expected = (
        "## Second\n"
        "| Header\\_one | Unnamed: 1 |\n"
        "| --- | --- |\n"
        "| <native> & \\*value\\* | 12 |\n\n"
        "## First\n| Other |\n| --- |\n| End |"
    )
    for converter in (XlsxConverter(), NativeSubclass()):
        assert _convert(converter, _workbook()) == expected
    assert reader.call_count == 2


def test_image_hook_uses_repaired_package_and_repair_stream_is_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = _rewrite(
        _workbook(),
        lambda name, content: (
            content.replace(b"<sheetView ", b'<sheetView showZeroes="0" ', 1)
            if name == "xl/worksheets/sheet1.xml"
            else content
        ),
    )
    repaired_streams = []
    original_repair = _xlsx_converter._repair_sheetview_show_zeroes

    def repair(*args: Any) -> io.BytesIO:
        stream = original_repair(*args)
        repaired_streams.append(stream)
        return stream

    original_images = _xlsx_images._XlsxImages

    def images(stream: BinaryIO):
        assert stream is repaired_streams[-1]
        with zipfile.ZipFile(stream) as archive:
            sheet = archive.read("xl/worksheets/sheet1.xml")
            assert b'showZeros="0"' in sheet and b"showZeroes" not in sheet
        return original_images(stream)

    monkeypatch.setattr(_xlsx_converter, "_repair_sheetview_show_zeroes", repair)
    monkeypatch.setattr(_xlsx_images, "_XlsxImages", images)
    render = Mock(return_value="<p>recognized</p>")
    result = _convert(_ImageConverter(render), data)
    assert result.count("recognized") == 4
    assert render.call_count == 4
    assert all(stream.closed for stream in repaired_streams)


@pytest.mark.parametrize(
    ("fragment", "error"),
    [
        (17, TypeError),
        (b"<p>bytes</p>", TypeError),
        ("<!doctype html><p>text</p>", ValueError),
        ("<html><body>text</body></html>", ValueError),
        ("<head><title>title</title></head>", ValueError),
    ],
)
def test_invalid_hook_results_are_rejected(
    fragment: Any, error: type[Exception]
) -> None:
    with pytest.raises(error, match="_image_to_html must return"):
        _convert(_ImageConverter(Mock(return_value=fragment)), _workbook())


def test_hook_failure_closes_image_stream_and_remains_visible() -> None:
    streams = []
    error = RuntimeError("image failure")

    def render(stream: BinaryIO, *args: Any, **kwargs: Any) -> str:
        streams.append(stream)
        raise error

    source = io.BytesIO(_workbook())
    with pytest.raises(RuntimeError) as caught:
        _ImageConverter(render).convert(source, _INFO)
    assert caught.value is error
    assert streams and all(stream.closed for stream in streams)
    assert not source.closed


def test_native_table_failure_is_not_silently_skipped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = TypeError("not the repairable error")
    monkeypatch.setattr(_xlsx_converter.pd, "read_excel", Mock(side_effect=error))
    render = Mock(return_value="<p>recognized</p>")
    with pytest.raises(TypeError) as caught:
        _convert(_ImageConverter(render), _workbook())
    assert caught.value is error
    render.assert_not_called()


def test_package_relationships_preserve_unusual_image_names_types_and_bytes() -> None:
    data = _workbook()
    svg = b'<svg xmlns="http://www.w3.org/2000/svg"><text>vector</text></svg>'
    output = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(data)) as source:
        with zipfile.ZipFile(output, "w") as target:
            for entry in source.infolist():
                content = source.read(entry)
                name = entry.filename
                if name == "xl/media/image1.png":
                    name, content = "xl/media/vector image.SVG", svg
                elif name.endswith(".rels"):
                    content = content.replace(
                        b"/xl/media/image1.png", b"../media/vector%20image.SVG"
                    )
                elif name == "[Content_Types].xml":
                    content = content.replace(
                        b"</Types>",
                        b'<Override PartName="/xl/media/vector%20image.SVG" '
                        b'ContentType="image/svg+xml"/></Types>',
                    )
                target.writestr(name, content)
    render = Mock(return_value="<p>recognized</p>")

    result = _convert(_ImageConverter(render), output.getvalue())

    assert result.count("recognized") == 4
    assert render.call_args_list[1].args[1] == StreamInfo(
        mimetype="image/svg+xml", extension=".svg", filename="vector image.SVG"
    )
    # The read-only table reader ignores drawings, including vector images.
    captured = []

    def capture(stream, info, **kwargs):
        captured.append(stream.read())
        return None

    _convert(_ImageConverter(capture), output.getvalue())
    assert captured == [_RED, svg, _BLUE, _BLUE]


def test_repeated_relationships_and_grouped_images_are_not_dropped() -> None:
    def group(name: str, content: bytes) -> bytes:
        if name != "xl/drawings/drawing1.xml":
            return content
        root = ET.fromstring(content)
        ns = _xlsx_images._NS
        anchor = root.find("xdr:oneCellAnchor", ns)
        assert anchor is not None
        picture = anchor.find("xdr:pic", ns)
        assert picture is not None
        anchor.remove(picture)
        group = ET.SubElement(anchor, "{" + ns["xdr"] + "}grpSp")
        nonvisual = ET.SubElement(group, "{" + ns["xdr"] + "}nvGrpSpPr")
        ET.SubElement(
            nonvisual, "{" + ns["xdr"] + "}cNvPr", {"id": "20", "name": "Group"}
        )
        ET.SubElement(nonvisual, "{" + ns["xdr"] + "}cNvGrpSpPr")
        ET.SubElement(group, "{" + ns["xdr"] + "}grpSpPr")
        group.append(picture)
        duplicate = ET.fromstring(ET.tostring(picture))
        properties = duplicate.find("xdr:nvPicPr/xdr:cNvPr", ns)
        assert properties is not None
        properties.set("id", "21")
        group.append(duplicate)
        return ET.tostring(root)

    captured = []

    def render(stream, info, **kwargs):
        captured.append(stream.read())
        return "<p>recognized</p>"

    result = _convert(_ImageConverter(render), _rewrite(_workbook(), group))
    assert captured == [_RED, _RED, _RED, _BLUE, _BLUE]
    assert "Image at " not in result
    assert result.count("recognized") == 5


def test_malformed_image_reference_does_not_become_silent_native_fallback() -> None:
    def missing_reference(name: str, content: bytes) -> bytes:
        if name != "xl/drawings/drawing1.xml":
            return content
        return content.replace(b'embed="rId1"', b'embed="missing"')

    with pytest.raises(KeyError):
        _convert(
            _ImageConverter(Mock(return_value="<p>recognized</p>")),
            _rewrite(_workbook(), missing_reference),
        )


def test_embedded_drawing_entities_are_rejected() -> None:
    def entity(name: str, content: bytes) -> bytes:
        if name != "xl/drawings/drawing1.xml":
            return content
        return b'<!DOCTYPE wsDr [<!ENTITY label "not expanded">]>' + content.replace(
            b'name="Image 1"', b'name="&label;"'
        )

    render = Mock(return_value="<p>recognized</p>")
    with pytest.raises(EntitiesForbidden):
        _convert(_ImageConverter(render), _rewrite(_workbook(), entity))
    render.assert_not_called()


def test_missing_dependencies_and_legacy_xls_stay_separate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = (Path(__file__).parent / "test_files" / "test.xls").read_bytes()
    legacy = XlsConverter()
    expected = legacy.convert(io.BytesIO(data), StreamInfo(extension=".xls")).markdown
    dependency = ImportError("openpyxl unavailable")
    monkeypatch.setattr(
        _xlsx_converter, "_xlsx_dependency_exc_info", (ImportError, dependency, None)
    )
    with pytest.raises(MissingDependencyException, match=r"\[xlsx\]"):
        XlsxConverter().convert(io.BytesIO(), _INFO)
    assert not hasattr(legacy, "_image_to_html")
    assert legacy.accepts(io.BytesIO(), StreamInfo(extension=".XLS"))
    assert (
        legacy.convert(io.BytesIO(data), StreamInfo(extension=".xls")).markdown
        == expected
    )


# Conversion regressions


def test_xlsx_legacy_show_zeroes_sheetview(tmp_path) -> None:
    from openpyxl import Workbook

    base_path = tmp_path / "base.xlsx"
    xlsx_path = tmp_path / "legacy_show_zeroes.xlsx"

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Data"
    sheet["A1"] = "hello"
    sheet["B1"] = "world"
    # A cell whose text is byte-identical to the malformed attribute. openpyxl stores it
    # as an inline string, so it lands in the very worksheet part that gets repaired.
    sheet["A2"] = ' showZeroes="0" '
    workbook.save(base_path)

    with zipfile.ZipFile(base_path) as source:
        with zipfile.ZipFile(xlsx_path, "w", zipfile.ZIP_DEFLATED) as target:
            for item in source.infolist():
                data = source.read(item.filename)
                if item.filename == "xl/worksheets/sheet1.xml":
                    data = data.replace(
                        b"<sheetView ", b'<sheetView showZeroes="0" ', 1
                    )
                    # Guard the fixture: the sheet view attribute and the cell text must
                    # both live here, or this test stops exercising the repair.
                    assert data.count(b'showZeroes="0"') == 2
                target.writestr(item, data)

    result = MarkItDown().convert(str(xlsx_path))

    assert "## Data" in result.markdown
    assert "hello" in result.markdown
    assert "world" in result.markdown

    # The repair must not reach into the worksheet's data: the cell keeps its text ...
    assert 'showZeroes="0"' in result.markdown
    # ... and no part of the document was silently renamed on the way through.
    assert "showZeros" not in result.markdown


def test_xlsx_show_zeroes_rename_is_scoped_to_sheet_view_tags() -> None:
    from markitdown.converters._xlsx_converter import _rename_show_zeroes_attribute

    worksheet_xml = (
        b"<worksheet><sheetViews>"
        b'<sheetView showZeroes="0" workbookViewId="0"/>'
        b'<sheetView\n\tshowZeroes="1"\ttabSelected="1"/>'
        b"</sheetViews>"
        # openpyxl ignores custom sheet views entirely, so they need no repair
        b'<customSheetViews><customSheetView showZeroes="0"/></customSheetViews>'
        b'<sheetData><row r="1">'
        b'<c r="A1" t="inlineStr"><is><t xml:space="preserve"> showZeroes="0" '
        b"</t></is></c>"
        b'<c r="B1"><f>IF(A1=" showZeroes=","x","y")</f><v>y</v></c>'
        b"</row></sheetData></worksheet>"
    )

    repaired = _rename_show_zeroes_attribute(worksheet_xml)

    # Every <sheetView> start tag is repaired, whatever separates its attributes ...
    assert repaired.count(b"showZeros=") == 2
    assert b'<sheetView showZeros="0" workbookViewId="0"/>' in repaired
    assert b'<sheetView\n\tshowZeros="1"\ttabSelected="1"/>' in repaired

    # ... and nothing outside those start tags is rewritten.
    assert b'<t xml:space="preserve"> showZeroes="0" </t>' in repaired
    assert b'<f>IF(A1=" showZeroes=","x","y")</f>' in repaired
    assert b'<customSheetView showZeroes="0"/>' in repaired


# Currency formatting


@pytest.mark.parametrize(
    ("fmt", "expected"),
    [
        ("$#,##0.00", "$"),
        ("£#,##0.00", "£"),
        ("€#,##0.00", "€"),
        ("[$USD-409]#,##0.00", "USD"),
        ("[$€-407]#,##0", "€"),
        ("[$-409]#,##0", None),  # locale-only block, no currency symbol
        ("[Red]$#,##0;[Red]-$#,##0", "$"),  # color code stripped before scan
        ("0.00%", None),
        ("General", None),
        ("@", None),
        ("", None),
        # ── Quoted-literal edge cases ─────────────────────────────────────────
        # Single-symbol quoted literal: IS a recognised currency prefix in Excel.
        ('"$"#,##0.00', "$"),
        ('"£"#,##0', "£"),
        # Multi-character quoted literal containing $: display text, not currency.
        ('"$10 off"#,##0', None),
        ('"price: $"#,##0', None),
        # Quoted text before a bare currency symbol: bare symbol still recognised.
        ('"USD "$#,##0', "$"),
        # Unclosed quoted literal (malformed format): safe fallback.
        ('"hello[>=0]$0;0', None),
        ('"unclosed$', None),
    ],
)
def test_extract_currency_prefix(fmt: str, expected: "Optional[str]") -> None:
    assert _xlsx_converter._extract_currency_prefix(fmt) == expected


@pytest.mark.parametrize(
    ("fmt", "value", "expected"),
    [
        # Single section — returned unchanged regardless of value
        ("$#,##0.00", 42, "$#,##0.00"),
        ("$#,##0.00", -1, "$#,##0.00"),
        # 2 sections: positive/zero → section 0, negative → section 1
        ("0;[Red]$0", 42, "0"),           # positive: section 0, no $
        ("0;[Red]$0", 0, "0"),            # zero:     section 0, no $
        ("0;[Red]$0", -42, "[Red]$0"),    # negative: section 1, has $
        # 3 sections: positive → 0, negative → 1, zero → 2
        ("$#,##0;[Red]$#,##0;0", 1, "$#,##0"),
        ("$#,##0;[Red]$#,##0;0", -1, "[Red]$#,##0"),
        ("$#,##0;[Red]$#,##0;0", 0, "0"),
        # 4 sections: text → section 3
        ('$#,##0;[Red]$#,##0;0;"n/a"', "hello", '"n/a"'),
        # ── Conditional operators ────────────────────────────────────────────
        # Item 1: all five comparison operators
        ("[>100]$0;0",   150, "$0"),      # >  : above threshold
        ("[>100]$0;0",    50, "0"),       # >  : below threshold
        ("[>=100]$0;0", 100, "$0"),       # >= : at threshold
        ("[>=100]$0;0",  99, "0"),        # >= : one below threshold
        ("[<0]$0;0",     -5, "$0"),       # <  : below threshold
        ("[<0]$0;0",      5, "0"),        # <  : above threshold
        ("[<=0]$0;0",     0, "$0"),       # <= : at threshold
        ("[<=0]$0;0",     1, "0"),        # <= : one above threshold
        ("[=0]$0;0",      0, "$0"),       # =  : exact match
        ("[=0]$0;0",      1, "0"),        # =  : no match
        # Item 2: decimal and negative thresholds
        ("[>=1.5]$0;0",  2.5, "$0"),
        ("[>=1.5]$0;0",  1.0, "0"),
        ("[>-10]$0;0",   -5, "$0"),
        ("[>-10]$0;0",  -15, "0"),
        # Item 3: multiple conditions evaluated in declaration order
        ("[>=100]$0;[>=50]€0;0", 150, "$0"),   # first condition wins
        ("[>=100]$0;[>=50]€0;0",  75, "€0"),   # first fails, second wins
        ("[>=100]$0;[>=50]€0;0",  25, "0"),    # both fail, catch-all
        # Item 4: unconditional third section is the catch-all
        ("[>=100]$0;[<0]€0;$0",  42, "$0"),    # neither condition, catch-all $
        # Item 5: no prefix when no condition matches and no catch-all
        ("[>=100]$0;[<0]$0",     42, ""),
        # Item 6: color code BEFORE the condition bracket
        ("[Red][>=100]$0;0",    150, "[Red]$0"),  # condition matches; [Red] kept
        ("[Red][>=100]$0;0",     42, "0"),         # condition fails; catch-all
        # Condition after color — condition bracket removed, color bracket kept
        ("[Blue][<0]$0;0",       -5, "[Blue]$0"),
        ("[Blue][<0]$0;0",        5, "0"),
        # ── Edge-case regressions ────────────────────────────────────────────
        # Issue 1: decimal threshold without a leading digit (e.g. .5 not 0.5)
        ("[>=.5]$0;0",  0.7, "$0"),   # above .5: condition matches
        ("[>=.5]$0;0",  0.3, "0"),    # below .5: catch-all
        ("[<.5]$0;0",   0.3, "$0"),   # below .5: condition matches
        ("[<.5]$0;0",   0.7, "0"),    # above .5: catch-all
        # Issue 2: scientific-notation threshold
        ("[>=1E3]$0;0", 1500, "$0"),  # above 1000: condition matches
        ("[>=1E3]$0;0",  500, "0"),   # below 1000: catch-all
        ("[>=1.5e2]$0;0", 200, "$0"), # above 150: condition matches
        ("[>=1.5e2]$0;0",  50, "0"),  # below 150: catch-all
        # Issue 3: condition-like bracket inside a quoted literal — NOT a condition;
        # the format must be treated as sign-based and the section returned intact.
        ('"val[>=0]";0',  42, '"val[>=0]"'),  # positive → section 0, no stripping
        ('"val[>=0]";0',  -5, "0"),            # negative → section 1
    ],
)
def test_select_format_section(fmt: str, value: object, expected: str) -> None:
    assert _xlsx_converter._select_format_section(fmt, value) == expected


def test_currency_section_selection_no_prefix_for_positive_value() -> None:
    """Positive value with format 0;[Red]$0 must NOT receive a $ prefix.

    Regression for the bug where _extract_currency_prefix searched the entire
    format string instead of only the section that applies to the cell's value.
    Excel applies the negative section to the absolute value, so -100 → $100,
    not $-100.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "Amount"
    ws["A2"] = 42         # positive → first section "0", no currency
    ws["A2"].number_format = "0;[Red]$0"
    ws["A3"] = -100       # negative → second section "[Red]$0", has currency
    ws["A3"].number_format = "0;[Red]$0"
    stream = io.BytesIO()
    wb.save(stream)
    wb.close()

    result = _convert(XlsxConverter(), stream.getvalue())

    assert "42" in result           # positive value appears as a plain number
    assert "$42" not in result      # must NOT be prefixed — $ belongs to negative section
    assert "$100" in result         # negative value: prefix applied to absolute value
    assert "$-100" not in result    # Excel shows absolute value, no minus sign


def test_currency_conditional_section_selection() -> None:
    """Conditional format [>=100]$0;0: only values meeting the condition get $.

    Regression for the bug where returning the full format string caused
    _extract_currency_prefix to find $ in a section that did not apply.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "Amount"
    ws["A2"] = 42         # 42 < 100: catch-all "0" applies, no $
    ws["A2"].number_format = "[>=100]$0;0"
    ws["A3"] = 150        # 150 >= 100: "$0" applies, has $
    ws["A3"].number_format = "[>=100]$0;0"
    stream = io.BytesIO()
    wb.save(stream)
    wb.close()

    result = _convert(XlsxConverter(), stream.getvalue())

    assert "$42" not in result   # below threshold: must NOT be prefixed
    assert "42" in result        # value still appears
    assert "$150" in result      # above threshold: must be prefixed


def test_currency_dollar_in_quoted_display_text() -> None:
    """Dollar sign inside a multi-char quoted literal is display text, not a prefix.

    Format '"$10 off"#,##0' uses "$10 off" as a quoted display string.  The $
    is part of the label, not a currency code, so the cell must not be prefixed.
    Regression: _extract_currency_prefix previously scanned raw format strings and
    returned '$' for any '$' it found, regardless of quoting.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "Note"
    ws["A2"] = 42
    ws["A2"].number_format = '"$10 off"#,##0'  # dollar is display text only
    ws["A3"] = 1199
    ws["A3"].number_format = "$#,##0.00"       # real currency format
    stream = io.BytesIO()
    wb.save(stream)
    wb.close()

    result = _convert(XlsxConverter(), stream.getvalue())

    assert "$42" not in result   # display-text dollar must NOT produce a prefix
    assert "42" in result        # value still present
    assert "$1199" in result     # real currency cell keeps its prefix


def test_currency_single_symbol_quoted_prefix() -> None:
    """A single-symbol quoted literal such as "$" is a valid Excel currency prefix.

    Excel generates formats like "$"#,##0.00 in some currency styles; the
    quoted dollar sign is intentional and must be recognised as a prefix.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "Price"
    ws["A2"] = 42
    ws["A2"].number_format = '"$"#,##0.00'
    ws["A3"] = 999
    ws["A3"].number_format = '"£"#,##0'
    stream = io.BytesIO()
    wb.save(stream)
    wb.close()

    result = _convert(XlsxConverter(), stream.getvalue())

    assert "$42" in result    # single-char quoted dollar recognised as prefix
    assert "£999" in result   # single-char quoted pound recognised as prefix


def _currency_workbook() -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prices"
    ws["A1"] = "Item"
    ws["B1"] = "USD"
    ws["C1"] = "GBP"
    ws["D1"] = "Rate"
    ws["A2"] = "Widget"
    ws["B2"] = 1199
    ws["B2"].number_format = "$#,##0.00"
    ws["C2"] = 950
    ws["C2"].number_format = "£#,##0.00"
    ws["D2"] = 0.08
    ws["D2"].number_format = "0.00%"  # not a currency format
    ws["A3"] = "Gadget"
    ws["B3"] = 5995
    ws["B3"].number_format = "$#,##0.00"
    ws["C3"] = 4750
    ws["C3"].number_format = "£#,##0.00"
    ws["D3"] = 0.05
    ws["D3"].number_format = "0.00%"
    stream = io.BytesIO()
    wb.save(stream)
    wb.close()
    return stream.getvalue()


def test_currency_symbols_preserved_in_xlsx_output() -> None:
    result = _convert(XlsxConverter(), _currency_workbook())
    assert "$1199" in result
    assert "£950" in result
    assert "$5995" in result
    assert "£4750" in result
    # Percentage cells retain their raw numeric value without a currency prefix
    assert "$0.08" not in result
    assert "£0.08" not in result


def test_currency_duplicate_column_names() -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "Item"
    ws["B1"] = "Price"
    ws["C1"] = "Price"  # duplicate header; pandas renames it "Price.1"
    ws["A2"] = "Widget"
    ws["B2"] = 1199
    ws["B2"].number_format = "$#,##0.00"
    ws["C2"] = 950
    ws["C2"].number_format = "£#,##0.00"
    stream = io.BytesIO()
    wb.save(stream)
    wb.close()

    result = _convert(XlsxConverter(), stream.getvalue())

    # Each column must receive its own symbol, not the other's
    assert "$1199" in result   # first  "Price"   column → $
    assert "£950" in result    # second "Price.1" column → £
    assert "£1199" not in result  # first column must not receive £
    assert "$950" not in result   # second column must not receive $


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
