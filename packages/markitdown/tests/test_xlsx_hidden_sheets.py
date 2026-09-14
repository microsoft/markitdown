import io
import zipfile

import pytest
from openpyxl import Workbook

from markitdown import MarkItDown


def _workbook(*, legacy_sheet_view=False, invalid_hidden_cell=False):
    workbook = Workbook()
    workbook.remove(workbook.active)
    for title, state, value in [
        ("Summary", "visible", "public summary"),
        ("Hidden", "hidden", "hidden details"),
        ("VeryHidden", "veryHidden", "very hidden details"),
        ("Appendix", "visible", "public appendix"),
    ]:
        sheet = workbook.create_sheet(title)
        sheet.sheet_state = state
        sheet.append(["Value"])
        sheet.append([value])

    original = io.BytesIO()
    workbook.save(original)
    workbook.close()
    result = io.BytesIO()
    with zipfile.ZipFile(original) as source:
        with zipfile.ZipFile(result, "w") as target:
            for item in source.infolist():
                data = source.read(item.filename)
                if legacy_sheet_view and item.filename == "xl/worksheets/sheet1.xml":
                    assert b"<sheetView " in data
                    data = data.replace(
                        b"<sheetView ", b'<sheetView showZeroes="0" ', 1
                    )
                if invalid_hidden_cell and item.filename == "xl/worksheets/sheet2.xml":
                    original_cell = (
                        b'<c r="A2" t="inlineStr"><is><t>hidden details</t></is></c>'
                    )
                    assert original_cell in data
                    data = data.replace(
                        original_cell, b'<c r="A2" t="n"><v>not-a-number</v></c>'
                    )
                target.writestr(item, data)
    result.seek(0)
    return result


@pytest.mark.parametrize("legacy_sheet_view", [False, True])
def test_exclude_hidden_sheets_preserves_visible_sheet_order(legacy_sheet_view):
    stream = _workbook(legacy_sheet_view=legacy_sheet_view)
    result = MarkItDown().convert_stream(
        stream, file_extension=".xlsx", include_hidden_sheets=False
    )

    assert "hidden details" not in result.markdown
    assert "## Hidden" not in result.markdown
    assert "## VeryHidden" not in result.markdown
    assert "public summary" in result.markdown
    assert "public appendix" in result.markdown
    assert result.markdown.index("## Summary") < result.markdown.index("## Appendix")
    assert not stream.closed


@pytest.mark.parametrize("options", [{}, {"include_hidden_sheets": True}])
def test_hidden_sheets_are_included_by_default(options):
    result = MarkItDown().convert_stream(_workbook(), file_extension=".xlsx", **options)

    headings = ["## Summary", "## Hidden", "## VeryHidden", "## Appendix"]
    positions = [result.markdown.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert "hidden details" in result.markdown
    assert "very hidden details" in result.markdown


def test_excluded_hidden_cells_are_not_parsed():
    result = MarkItDown().convert_stream(
        _workbook(invalid_hidden_cell=True),
        file_extension=".xlsx",
        include_hidden_sheets=False,
    )

    assert "public summary" in result.markdown
    assert "public appendix" in result.markdown
    assert "hidden details" not in result.markdown
