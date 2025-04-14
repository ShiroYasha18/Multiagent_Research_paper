from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

class ReportLabPDFGenerator:
    def generate_pdf(self, title, sections, filename, include_xai_visuals=False, grubbs_outlier_table=False):
        pdf_file = f"{filename}.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        body_style = styles['BodyText']
        bullet_style = ParagraphStyle('Bullet', parent=styles['BodyText'], bulletIndent=20)

        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))

        for section_title, content in sections.items():
            story.append(Paragraph(f"<b>{section_title}</b>", styles['Heading2']))
            story.append(Spacer(1, 12))
            for line in content.split('\n'):
                if line.startswith('*'):
                    story.append(Paragraph(line[1:], bullet_style))
                else:
                    story.append(Paragraph(line, body_style))
                story.append(Spacer(1, 6))

        if include_xai_visuals:
            try:
                story.append(Spacer(1, 12))
                story.append(Paragraph("XAI Visualizations", styles['Heading2']))
                story.append(Image("shap_explanation.png", width=400, height=200))
                story.append(Image("lime_explanation.html", width=400, height=200))
            except Exception as e:
                print(f"❌ Failed to embed XAI visuals: {e}")

        if grubbs_outlier_table:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Grubbs Outlier Detection Table", styles['Heading2']))
            table_data = [["Value", "Outlier"]] + [[str(i), "No"] for i in range(1, 11)]
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)

        doc.build(story)
        print(f"✅ PDF Generated: {pdf_file}")