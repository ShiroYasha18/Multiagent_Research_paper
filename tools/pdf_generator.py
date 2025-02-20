import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(results, filename="research_report.pdf"):
    """Creates a structured PDF report with final research findings."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Start position for text

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y_position, "AI Research Report")
    y_position -= 30

    c.setFont("Helvetica", 12)

    for section, content in results.items():
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, section)
        y_position -= 20

        c.setFont("Helvetica", 12)
        wrapped_text = textwrap.wrap(content, width=90)  # ✅ Dynamically wrap text

        for line in wrapped_text:
            c.drawString(50, y_position, line)
            y_position -= 15
            if y_position < 50:  # If the page is full, create a new page
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50

        y_position -= 20  # Space before the next section

    c.save()
    print(f"📄 Research report saved as: {filename}")
