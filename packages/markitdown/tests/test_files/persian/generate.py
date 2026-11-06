"""Optional fixture authoring tool; never invoked by tests."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).parent


def generate():
    pdf = FPDF(unit="pt", format="A4")
    pdf.set_creation_date(datetime(2026, 1, 1, tzinfo=timezone.utc))
    pdf.set_title("Persian PDF regression cases")
    pdf.set_author("MarkItDown regression fixtures")
    pdf.add_font("Noto", fname=ROOT / "fonts/NotoSansArabic-Regular.ttf")
    pdf.add_font("Latin", fname=ROOT / "fonts/NotoSans-Regular.ttf")
    pdf.set_fallback_fonts(["Latin"])
    cases = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    for page, case in enumerate(cases, 1):
        assert case["page"] == page, "Manifest page order must match the PDF"
        pdf.add_page()
        pdf.set_font("Latin" if case["direction"] == "ltr" else "Noto", size=14)
        pdf.set_text_shaping(True, direction=case["direction"])

        def line(text, x, y, width):
            pdf.set_xy(x, y)
            pdf.cell(width, 30, text, align="R" if case["direction"] == "rtl" else "L")

        if "table" in case:
            for r, row in enumerate(case["table"]):
                for col, text in enumerate(row):
                    x = 370 - 160 * col
                    pdf.rect(x, 70 + r * 40, 160, 40)
                    line(text, x + 5, 75 + r * 40, 150)
        elif case.get("columns"):
            xs = [320, 50] if case["direction"] == "rtl" else [50, 320]
            for i, text in enumerate(case["blocks"]):
                line(text, xs[i // 2], 70 + (i % 2) * 50, 220)
        else:
            for i, text in enumerate(case["blocks"]):
                if case["id"] == "heading":
                    pdf.set_font("Noto", size=20 if i == 0 else 14)
                line(text, 40, 70 + i * 65, 515)
    pdf.output(ROOT / "persian_cases.pdf")
    files = [ROOT / "persian_cases.pdf"] + sorted((ROOT / "fonts").glob("*"))
    (ROOT / "sha256.json").write_text(
        json.dumps(
            {
                str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in files
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    generate()
