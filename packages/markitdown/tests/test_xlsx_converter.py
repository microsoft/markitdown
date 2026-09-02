from pathlib import Path

from openpyxl import Workbook

from markitdown import MarkItDown


def test_xlsx_currency_formats_are_preserved(tmp_path: Path) -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Budget"
    worksheet.append(["Item", "Cost", "Total"])
    worksheet.append(["Breakfast", 12.5, 25])
    worksheet["B2"].number_format = '"$"#,##0.00'
    worksheet["C2"].number_format = '[$€-407]#,##0.00'

    path = tmp_path / "budget.xlsx"
    workbook.save(path)

    result = MarkItDown().convert(path)

    assert "$12.50" in result.markdown
    assert "€25.00" in result.markdown
