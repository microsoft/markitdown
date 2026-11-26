"""Regenerate the PDF link fixtures with ReportLab."""

from pathlib import Path

from reportlab.pdfbase.pdfdoc import PDFArray
from reportlab.pdfgen.canvas import Canvas

FIXTURES = Path(__file__).resolve().parent


def add_link(pdf, x, y, label, url):
    width = pdf.stringWidth(label, "Helvetica", 12)
    pdf.linkURL(url, (x, y - 3, x + width, y + 10))


def main():
    pdf = Canvas(str(FIXTURES / "pdf_links_plain.pdf"), invariant=True)
    pdf.drawString(72, 720, "Unlinked: Read more.")
    pdf.drawString(72, 696, "First: Read more.")
    pdf.drawString(72, 672, "Second: Read more.")
    pdf.drawString(72, 648, "Keep  these  spaces.")

    # Annotation order need not match reading order.
    for y, prefix, path in [(672, "Second: ", "second"), (696, "First: ", "first")]:
        x = 72 + pdf.stringWidth(prefix, "Helvetica", 12)
        add_link(pdf, x, y, "Read more", f"https://example.org/{path}")
    pdf.save()

    pdf = Canvas(str(FIXTURES / "pdf_links_mixed.pdf"), invariant=True)
    pdf.drawString(72, 720, "Read more about the schedule.")
    add_link(pdf, 72, 720, "Read more", "https://example.org/schedule")
    pdf.showPage()

    for y, cells in [
        (720, ("Document", "Link", "Revision")),
        (696, ("Index", "Read more", "2026")),
    ]:
        for x, cell in zip((72, 220, 368), cells):
            pdf.drawString(x, y, cell)
    add_link(pdf, 220, 696, "Read more", "https://example.org/index")
    pdf.showPage()

    pdf.drawString(72, 720, "Left middle Right")
    left_end = 72 + pdf.stringWidth("Left", "Helvetica", 12)
    right_start = 72 + pdf.stringWidth("Left middle ", "Helvetica", 12)
    right_end = 72 + pdf.stringWidth("Left middle Right", "Helvetica", 12)
    points = []
    for start, end in [(72, left_end), (right_start, right_end)]:
        points.extend([start, 717, end, 717, end, 730, start, 730])
    pdf.linkURL(
        "https://example.org/both",
        (72, 717, right_end, 730),
        QuadPoints=PDFArray(points),
    )
    pdf.save()

    pdf = Canvas(str(FIXTURES / "pdf_links_rotated.pdf"), invariant=True)
    pdf.setPageRotation(90)
    pdf.translate(72, 100)
    pdf.rotate(90)
    pdf.drawString(0, 0, "Open guide")
    pdf.drawString(0, -24, "Report ] draft")
    for y, label, url in [
        (0, "Open guide", "https://example.org/guide"),
        (-24, "Report ] draft", "https://example.org/v2)draft"),
    ]:
        width = pdf.stringWidth(label, "Helvetica", 12)
        pdf.linkURL(url, (0, y - 3, width, y + 10), relative=True)
    pdf.showPage()
    pdf._doc.Pages.pages[0].MediaBox = PDFArray([40, 40, 240, 340])
    pdf.save()


if __name__ == "__main__":
    main()
