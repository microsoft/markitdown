import io
import subprocess
import sys

import pytest
from openpyxl import Workbook


@pytest.mark.parametrize("stdin", [False, True])
@pytest.mark.parametrize("exclude", [False, True])
def test_cli_hidden_xlsx_sheets(tmp_path, stdin, exclude):
    workbook = Workbook()
    workbook.remove(workbook.active)
    for title, state, text in [
        ("Summary", "visible", "public summary"),
        ("Hidden", "hidden", "hidden sentinel"),
        ("Private", "veryHidden", "veryHidden sentinel"),
        ("Appendix", "visible", "public appendix"),
    ]:
        sheet = workbook.create_sheet(title)
        sheet.sheet_state = state
        sheet.append(["Value"])
        sheet.append([text])
    stream = io.BytesIO()
    workbook.save(stream)
    workbook.close()
    command = [sys.executable, "-m", "markitdown"]
    if exclude:
        command.append("--exclude-hidden-sheets")
    if stdin:
        command.extend(["-x", "xlsx"])
    else:
        path = tmp_path / "sheets.xlsx"
        path.write_bytes(stream.getvalue())
        command.append(str(path))
    result = subprocess.run(
        command, input=stream.getvalue() if stdin else None, capture_output=True
    )
    assert result.returncode == 0, result.stderr.decode()
    output = result.stdout.decode()
    assert "public summary" in output
    assert "public appendix" in output
    assert output.index("## Summary") < output.index("## Appendix")
    assert ("hidden sentinel" in output) is not exclude
    assert ("veryHidden sentinel" in output) is not exclude
