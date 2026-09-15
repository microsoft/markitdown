import io
import zipfile
from typing import Any

from openpyxl import Workbook

from markitdown import StreamInfo
from markitdown_ocr._ocr_service import OCRResult
from markitdown_ocr._xlsx_converter_with_ocr import XlsxConverterWithOCR


class MockOCRService:
    def extract_text(self, image_stream: Any, **kwargs: Any) -> OCRResult:
        return OCRResult(text="", backend_used="mock")


def _legacy_show_zeroes_workbook() -> io.BytesIO:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Data"
    sheet["A1"] = "hello"
    sheet["B1"] = "world"

    base = io.BytesIO()
    workbook.save(base)
    base.seek(0)

    malformed = io.BytesIO()
    with zipfile.ZipFile(base) as source:
        with zipfile.ZipFile(malformed, "w", zipfile.ZIP_DEFLATED) as target:
            for item in source.infolist():
                data = source.read(item.filename)

                if item.filename == "xl/worksheets/sheet1.xml":
                    data = data.replace(
                        b"<sheetView ",
                        b'<sheetView showZeroes="0" ',
                        1,
                    )
                    assert b'<sheetView showZeroes="0"' in data

                target.writestr(item, data)

    malformed.seek(0)
    return malformed


def test_xlsx_ocr_converter_repairs_legacy_show_zeroes() -> None:
    converter = XlsxConverterWithOCR()
    workbook = _legacy_show_zeroes_workbook()

    result = converter.convert(
        workbook,
        StreamInfo(extension=".xlsx"),
        ocr_service=MockOCRService(),
    )

    assert "## Data" in result.markdown
    assert "hello" in result.markdown
    assert "world" in result.markdown
