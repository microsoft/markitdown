import io
import zipfile
from pathlib import Path

import pytest
from openpyxl import Workbook

from markitdown import MarkItDown

ROWS = [
    ["token", "blank", "amount"],
    ["NA", None, 1],
    ["NULL", None, 2],
    ["None", None, 3],
    ["n/a", None, 4],
    ["nan", "present", 5],
]


@pytest.mark.parametrize("file_format", ["xlsx", "xlsx_legacy", "xls"])
def test_excel_preserves_literal_na_values(file_format):
    if file_format == "xls":
        # The legacy workbook contains ROWS, including real blank cells.
        stream = io.BytesIO(
            Path(__file__)
            .with_name("test_files")
            .joinpath("literal_na.xls")
            .read_bytes()
        )
    else:
        workbook = Workbook()
        workbook.active.title = "Data"
        for row in ROWS:
            workbook.active.append(row)
        stream = io.BytesIO()
        workbook.save(stream)
        stream.seek(0)

        if file_format == "xlsx_legacy":
            repaired_input = io.BytesIO()
            with zipfile.ZipFile(stream) as source:
                with zipfile.ZipFile(repaired_input, "w") as target:
                    for item in source.infolist():
                        data = source.read(item.filename)
                        if item.filename == "xl/worksheets/sheet1.xml":
                            data = data.replace(
                                b"<sheetView ", b'<sheetView showZeroes="0" ', 1
                            )
                        target.writestr(item, data)
            stream = repaired_input
            stream.seek(0)

    result = MarkItDown().convert_stream(
        stream, file_extension=".xls" if file_format == "xls" else ".xlsx"
    )

    assert result.markdown == (
        "## Data\n"
        "| token | blank | amount |\n"
        "| --- | --- | --- |\n"
        "| NA |  | 1 |\n"
        "| NULL |  | 2 |\n"
        "| None |  | 3 |\n"
        "| n/a |  | 4 |\n"
        "| nan | present | 5 |"
    )
