from fpdf import FPDF

class PaperGenerator:
    def __init__(self, title):
        self.pdf = FPDF()
        self.title = title

    def add_section(self, heading, content):
        """Adds a section to the research paper."""
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, heading, ln=True, align="L")
        self.pdf.set_font("Arial", "", 12)
        self.pdf.multi_cell(0, 10, content)
        self.pdf.ln(5)

    def generate_paper(self, hypothesis, literature_review, experiment_design, data_analysis):
        """Generates a structured PDF research paper."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, self.title, ln=True, align="C")
        self.pdf.ln(10)

        # Add sections
        self.add_section("Abstract", f"This paper explores {self.title} based on AI-driven insights.")
        self.add_section("1. Hypothesis", hypothesis)
        self.add_section("2. Literature Review", literature_review)
        self.add_section("3. Experiment Design", experiment_design)
        self.add_section("4. Data Analysis", data_analysis)
        self.add_section("5. Conclusion", "Findings suggest further investigation is needed in this area.")

        # Save PDF
        file_name = f"{self.title.replace(' ', '_')}.pdf"
        self.pdf.output(file_name)
        return file_name
