import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf(results, filename="research_report.pdf"):
    """Creates a structured PDF report with clear section formatting and readability."""

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 50  # Left margin
    y_position = height - 60  # Start position for text

    # ✅ Title Section
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, y_position, "AI Research Report")
    y_position -= 30

    # ✅ Iterate over sections and format text properly
    for section, content in results.items():
        # ✅ Section Headers
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, section)
        y_position -= 20

        # ✅ Format Content with Proper Line Spacing
        c.setFont("Helvetica", 12)
        paragraphs = content.split("\n\n")  # Split into paragraphs for better spacing

        for paragraph in paragraphs:
            wrapped_lines = textwrap.wrap(paragraph, width=85)  # Wrap long lines

            for line in wrapped_lines:
                c.drawString(margin, y_position, line)
                y_position -= 15  # Line spacing

                # ✅ If the page is full, start a new page
                if y_position < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 50

            y_position -= 10  # Extra space between paragraphs

        y_position -= 20  # Space between sections

    c.save()
    print(f"📄 Research report saved as: {filename}")
