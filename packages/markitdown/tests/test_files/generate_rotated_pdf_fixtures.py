from pathlib import Path

from reportlab.pdfgen import canvas


FIXTURES = Path(__file__).resolve().parent


def draw_rotated_text(pdf: canvas.Canvas, direction: str) -> None:
    pdf.drawString(50, 750, "Rotation example")
    pdf.saveState()
    pdf.translate(250, 400)
    pdf.rotate(90 if direction == "btt" else -90)
    pdf.drawString(0, 0, "Projected Population Kharif Rice")
    pdf.restoreState()


def main() -> None:
    for direction in ("btt", "ttb"):
        pdf = canvas.Canvas(
            str(FIXTURES / f"rotated_plain_{direction}.pdf"), invariant=True
        )
        draw_rotated_text(pdf, direction)
        pdf.save()

    pdf = canvas.Canvas(str(FIXTURES / "rotated_mixed.pdf"), invariant=True)
    draw_rotated_text(pdf, "btt")
    pdf.showPage()
    pdf.drawString(50, 780, "Inventory")
    for y, row in zip(
        (750, 730, 710),
        (
            ("Column A", "Column B", "Column C"),
            ("Alpha", "100", "kg"),
            ("Beta", "200", "lb"),
        ),
    ):
        for x, value in zip((50, 250, 450), row):
            pdf.drawString(x, y, value)
    pdf.showPage()
    draw_rotated_text(pdf, "btt")
    pdf.save()

    pdf = canvas.Canvas(str(FIXTURES / "rotated_empty.pdf"), invariant=True)
    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    main()
