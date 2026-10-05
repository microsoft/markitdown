import io
import sys

from openpyxl import Workbook

from markitdown import MarkItDown, StreamInfo
from markitdown.__main__ import main


def _workbook_with_hidden_sheets() -> bytes:
    workbook = Workbook()
    visible_sheet = workbook.active
    visible_sheet.title = "Visible"
    visible_sheet.append(["Visible value"])

    hidden_sheet = workbook.create_sheet("Hidden")
    hidden_sheet.append(["Hidden value"])
    hidden_sheet.sheet_state = "hidden"

    very_hidden_sheet = workbook.create_sheet("Very hidden")
    very_hidden_sheet.append(["Very hidden value"])
    very_hidden_sheet.sheet_state = "veryHidden"

    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    return stream.getvalue()


def _convert_with_hidden_sheets(**kwargs: bool) -> str:
    return MarkItDown().convert(
        io.BytesIO(_workbook_with_hidden_sheets()),
        stream_info=StreamInfo(extension=".xlsx"),
        **kwargs,
    ).markdown


def test_hidden_sheets_are_excluded_by_default() -> None:
    markdown = _convert_with_hidden_sheets()

    assert "## Visible" in markdown
    assert "Visible value" in markdown
    assert "## Hidden" not in markdown
    assert "Hidden value" not in markdown
    assert "## Very hidden" not in markdown
    assert "Very hidden value" not in markdown


def test_hidden_sheets_can_be_included() -> None:
    markdown = _convert_with_hidden_sheets(include_hidden_sheets=True)

    assert "## Visible" in markdown
    assert "## Hidden" in markdown
    assert "Hidden value" in markdown
    assert "## Very hidden" in markdown
    assert "Very hidden value" in markdown


def test_hidden_sheets_can_be_included_from_cli(tmp_path, monkeypatch, capsys) -> None:
    workbook_path = tmp_path / "sheets.xlsx"
    workbook_path.write_bytes(_workbook_with_hidden_sheets())
    monkeypatch.setattr(
        sys,
        "argv",
        ["markitdown", "--include-hidden-sheets", str(workbook_path)],
    )

    main()

    markdown = capsys.readouterr().out
    assert "## Hidden" in markdown
    assert "Hidden value" in markdown
    assert "## Very hidden" in markdown
    assert "Very hidden value" in markdown
