import json
import subprocess
import sys
from pathlib import Path

from reportlab.pdfgen import canvas
import jsonschema


def _make_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path))
    c.drawString(100, 700, "Hi")
    c.save()


def test_cli_emits_sidecar(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"
    _make_pdf(pdf_path)
    subprocess.run(
        [sys.executable, "-m", "markitdown", str(pdf_path), "--emit-bbox"],
        check=True,
        cwd=tmp_path,
    )
    sidecar = pdf_path.with_suffix(".bbox.json")
    assert sidecar.exists()
    schema = json.load(open(Path(__file__).parent / "schema.json"))
    jsonschema.validate(instance=json.load(open(sidecar)), schema=schema)
