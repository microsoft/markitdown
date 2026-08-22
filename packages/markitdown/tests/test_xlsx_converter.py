from pathlib import Path

import pandas as pd

from markitdown import MarkItDown


def test_convert_xlsx_selected_sheet(tmp_path: Path) -> None:
    workbook = tmp_path / "workbook.xlsx"
    with pd.ExcelWriter(workbook, engine="openpyxl") as writer:
        pd.DataFrame({"value": ["first"]}).to_excel(
            writer, sheet_name="First", index=False
        )
        pd.DataFrame({"value": ["second"]}).to_excel(
            writer, sheet_name="Second", index=False
        )

    result = MarkItDown().convert(workbook, sheet_name="Second")

    assert "## Second" in result.markdown
    assert "second" in result.markdown
    assert "## First" not in result.markdown
    assert "first" not in result.markdown


def test_convert_xlsx_defaults_to_all_sheets(tmp_path: Path) -> None:
    workbook = tmp_path / "workbook.xlsx"
    with pd.ExcelWriter(workbook, engine="openpyxl") as writer:
        pd.DataFrame({"value": ["first"]}).to_excel(
            writer, sheet_name="First", index=False
        )
        pd.DataFrame({"value": ["second"]}).to_excel(
            writer, sheet_name="Second", index=False
        )

    result = MarkItDown().convert(workbook)

    assert "## First" in result.markdown
    assert "## Second" in result.markdown
