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


def draw_cell_text(pdf, lines, left, bottom, right, top, direction):
    pdf.saveState()
    if direction == "btt":
        pdf.translate(left + 12, bottom + 5)
        pdf.rotate(90)
    else:
        pdf.translate(right - 12, top - 5)
        pdf.rotate(-90)
    text = pdf.beginText()
    text.setFont("Helvetica", 9)
    text.setLeading(12)
    for line in lines:
        text.textLine(line)
    pdf.drawText(text)
    pdf.restoreState()


def draw_ruled_tables(pdf, direction):
    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, 760, "Before the first table")
    columns = [50, 78, 160, 205, 250, 295, 340, 385, 430, 475, 520, 565]
    for x in columns:
        top = 560 if x in (385, 430, 520) else 700
        bottom = 450 if x == 78 else 430
        pdf.line(x, bottom, x, top)
    for y in (700, 510, 490, 470, 450, 430):
        pdf.line(50, y, 565, y)
    pdf.line(340, 560, 565, 560)
    pdf.drawString(52, 680, "No.")
    draw_cell_text(pdf, ["Index"], 50, 510, 78, 650, direction)
    pdf.drawString(80, 680, "District")
    headers = [
        ["Projected Population", "for 2012-13", "(In lakhs)"],
        ["Adult", "Equivalent to 88%", "(In lakhs)"],
        ["Total Consumption", "requirement", "(In Lakh tonnes)"],
        ["Total Requirement", "Including seeds", "and feeds"],
    ]
    for index, lines in enumerate(headers, 2):
        draw_cell_text(
            pdf, lines, columns[index], 510, columns[index + 1], 700, direction
        )
    pdf.drawString(342, 680, "Production (Rice)")
    pdf.drawString(477, 680, "Surplus/Deficit")
    for index, label in enumerate(("Kharif", "Rabi", "Total", "Rice", "Paddy"), 6):
        draw_cell_text(
            pdf, [label], columns[index], 510, columns[index + 1], 560, direction
        )
    rows = [
        "1 Alpha 23.65 20.81 3.04 3.47 2.78 0.86 3.64 0.17 0.25".split(),
        "2 Beta 15.34 13.50 1.97 2.25 3.50 0.05 3.55 1.30 1.94".split(),
        ["TOTAL", ""] + "38.99 34.31 5.01 5.72 6.28 0.91 7.19 1.47 2.19".split(),
    ]
    for y, row in zip((496, 456, 436), rows):
        for x, value in zip(columns, row):
            pdf.drawString(x + 2, y, value)
    pdf.drawString(50, 370, "Between the tables")
    for x in (50, 150, 250):
        pdf.line(x, 220, x, 260)
    for y in (220, 240, 260):
        pdf.line(50, y, 250, y)
    for x, y, value in [
        (52, 246, "Name | code"),
        (152, 246, "Amount"),
        (52, 226, "<total>"),
        (152, 226, "3.47"),
    ]:
        pdf.drawString(x, y, value)
    pdf.drawString(50, 180, "After the second table")


def main() -> None:
    for direction in ("btt", "ttb"):
        pdf = canvas.Canvas(
            str(FIXTURES / f"rotated_plain_{direction}.pdf"), invariant=True
        )
        draw_rotated_text(pdf, direction)
        pdf.save()

        pdf = canvas.Canvas(
            str(FIXTURES / f"rotated_ruled_{direction}.pdf"), invariant=True
        )
        draw_ruled_tables(pdf, direction)
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
