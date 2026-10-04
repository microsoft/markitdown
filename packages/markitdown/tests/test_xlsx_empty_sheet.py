import io

from openpyxl import Workbook

from markitdown import MarkItDown, StreamInfo


def _xlsx_bytes(workbook: Workbook) -> bytes:
    buf = io.BytesIO()
    workbook.save(buf)
    return buf.getvalue()


def test_completely_empty_sheet_is_skipped() -> None:
    """A sheet with no columns must not emit malformed table syntax."""
    workbook = Workbook()
    workbook.active.title = "HasData"
    workbook.active["A1"] = "col"
    workbook.active["A2"] = "v"
    workbook.create_sheet("CompletelyEmpty")

    result = MarkItDown().convert_stream(
        io.BytesIO(_xlsx_bytes(workbook)),
        stream_info=StreamInfo(extension=".xlsx"),
    )

    assert "## HasData" in result.markdown
    assert "| col |" in result.markdown
    assert "| v |" in result.markdown
    assert "CompletelyEmpty" not in result.markdown
    assert "|\n|  |" not in result.markdown


def test_header_only_sheet_keeps_empty_table() -> None:
    """A sheet with a header row but no data already produces a valid table."""
    workbook = Workbook()
    workbook.active.title = "HeaderOnly"
    workbook.active["A1"] = "col"

    result = MarkItDown().convert_stream(
        io.BytesIO(_xlsx_bytes(workbook)),
        stream_info=StreamInfo(extension=".xlsx"),
    )

    assert "## HeaderOnly" in result.markdown
    assert "| col |" in result.markdown
    assert "| --- |" in result.markdown


def test_single_completely_empty_workbook_emits_nothing() -> None:
    workbook = Workbook()
    workbook.active.title = "Empty"

    result = MarkItDown().convert_stream(
        io.BytesIO(_xlsx_bytes(workbook)),
        stream_info=StreamInfo(extension=".xlsx"),
    )

    assert result.markdown.strip() == ""
    assert "|" not in result.markdown


def test_empty_sheet_with_image_keeps_the_image() -> None:
    """Skipping an empty sheet's table must not drop images anchored on it."""
    from typing import Any, BinaryIO, Optional

    from openpyxl.drawing.image import Image as SheetImage
    from PIL import Image

    from markitdown.converters import XlsxConverter

    class ImageConverter(XlsxConverter):
        def _image_to_html(
            self, image_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any
        ) -> Optional[str]:
            return "<p>sheet image</p>"

    png = io.BytesIO()
    Image.new("RGB", (2, 2), "red").save(png, "PNG")
    workbook = Workbook()
    workbook.active.title = "HasData"
    workbook.active["A1"] = "col"
    workbook.create_sheet("OnlyAnImage").add_image(
        SheetImage(io.BytesIO(png.getvalue())), "B2"
    )
    workbook.create_sheet("CompletelyEmpty")

    markdown = (
        ImageConverter()
        .convert(io.BytesIO(_xlsx_bytes(workbook)), StreamInfo(extension=".xlsx"))
        .markdown
    )

    assert "## OnlyAnImage" in markdown
    assert "sheet image" in markdown.split("## OnlyAnImage", 1)[1]
    assert "## CompletelyEmpty" not in markdown
    assert "|  |" not in markdown
