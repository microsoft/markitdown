import json
import shutil
import urllib.request
from pathlib import Path

import pytest

from markitdown import MarkItDown

DOC_BASE = "https://raw.githubusercontent.com/docling-project/docling/main/tests/data_scanned"
PDF_URL = f"{DOC_BASE}/ocr_test.pdf"
MD_URL = f"{DOC_BASE}/groundtruth/docling_v2/ocr_test.md"
JSON_URL = f"{DOC_BASE}/groundtruth/docling_v2/ocr_test.json"


def _fetch(url: str, dest: Path) -> None:
    dest.write_bytes(urllib.request.urlopen(url).read())


@pytest.mark.skipif(shutil.which("tesseract") is None, reason="tesseract not installed")
def test_docling_ocr_pdf(tmp_path: Path) -> None:
    pdfplumber = pytest.importorskip("pdfplumber")
    pytesseract = pytest.importorskip("pytesseract")
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        pytest.skip("tesseract not installed")

    pdf_path = tmp_path / "ocr_test.pdf"
    md_path = tmp_path / "ocr_test.md"
    json_path = tmp_path / "ocr_test.json"

    _fetch(PDF_URL, pdf_path)
    _fetch(MD_URL, md_path)
    _fetch(JSON_URL, json_path)

    md = MarkItDown()
    result = md.convert_local(pdf_path, emit_bbox=True)

    assert result.bbox is not None
    # normalize whitespace since OCR may insert newlines
    got_md = " ".join(result.markdown.split())
    expect_md = " ".join(md_path.read_text().split())
    assert got_md == expect_md

    gt = json.loads(json_path.read_text())
    page_info = next(iter(gt["pages"].values()))
    width = page_info["size"]["width"]
    height = page_info["size"]["height"]
    bbox_gt = gt["texts"][0]["prov"][0]["bbox"]
    x1, y_top, x2, y_bottom = (
        bbox_gt["l"],
        bbox_gt["t"],
        bbox_gt["r"],
        bbox_gt["b"],
    )
    y1 = height - y_top
    y2 = height - y_bottom
    line = result.bbox.lines[0]
    page_dims = result.bbox.pages[line.page - 1]
    scale_x = page_dims.width / width
    scale_y = page_dims.height / height
    expected_abs = [x1 * scale_x, y1 * scale_y, x2 * scale_x, y2 * scale_y]
    # top-left corner should be close to groundtruth when scaled
    for got, exp in zip(line.bbox_abs[:2], expected_abs[:2]):
        assert got == pytest.approx(exp, abs=20.0)

    # width should roughly match after scaling
    got_width = line.bbox_abs[2] - line.bbox_abs[0]
    exp_width = expected_abs[2] - expected_abs[0]
    assert got_width == pytest.approx(exp_width, abs=20.0)

    # normalized coordinates should be in range
    for v in line.bbox_norm:
        assert 0 <= v <= 1
