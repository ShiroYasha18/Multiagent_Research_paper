from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

class ReportLabPDFGenerator:
    def __init__(self):
        pass

    def generate_pdf(self, title, sections, filename, images=None):
        pdf_path = f"{filename}.pdf"
        self.pdf = canvas.Canvas(pdf_path, pagesize=letter)
        self.pdf.setTitle(title)
        
        y_position = 750
        
        # Add title
        self.pdf.setFont("Helvetica-Bold", 16)
        self.pdf.drawString(100, y_position, title)
        y_position -= 30
        
        # Add content from sections
        for section_title, content in sections.items():
            if y_position < 100:
                self.pdf.showPage()
                y_position = 750
            
            self.pdf.setFont("Helvetica-Bold", 14)
            self.pdf.drawString(50, y_position, section_title)
            y_position -= 20
            
            self.pdf.setFont("Helvetica", 10)
            
            # Convert content to string if it's a list
            if isinstance(content, list):
                content = "\n".join(str(item) for item in content)
            elif not isinstance(content, str):
                content = str(content)
            
            content_lines = self._wrap_text(content, 80)
            for line in content_lines:
                if y_position < 50:
                    self.pdf.showPage()
                    y_position = 750
                self.pdf.drawString(50, y_position, line)
                y_position -= 15
            
            y_position -= 20
        
        # Add images if provided
        if images:
            for img_path in images:
                if os.path.exists(img_path):
                    self.pdf.showPage()
                    
                    img_name = os.path.basename(img_path).split('.')[0]
                    self.pdf.setFont("Helvetica-Bold", 12)
                    self.pdf.drawString(100, 750, f"Visualization: {img_name}")
                    
                    try:
                        img = ImageReader(img_path)
                        img_width, img_height = img.getSize()
                        aspect = img_height / float(img_width)
                        
                        display_width = 400
                        display_height = display_width * aspect
                        
                        x_pos = (letter[0] - display_width) / 2
                        y_pos = 700 - display_height
                        
                        self.pdf.drawImage(img_path, x_pos, y_pos, 
                                         width=display_width, 
                                         height=display_height)
                        
                        self.pdf.setFont("Helvetica", 10)
                        self.pdf.drawString(100, y_pos - 30, 
                            "Explainable AI visualization showing feature importance and model interpretability.")
                    except Exception as e:
                        self.pdf.drawString(100, 700, f"Error displaying image: {str(e)}")
        
        self.pdf.save()
        return pdf_path
    
    def _wrap_text(self, text, width):
        """Wrap text to fit within specified width."""
        if not isinstance(text, str):
            text = str(text)
            
        lines = []
        for paragraph in text.split('\n'):
            if len(paragraph) <= width:
                lines.append(paragraph)
                continue
            
            current_line = ""
            for word in paragraph.split(' '):
                if len(current_line) + len(word) + 1 <= width:
                    current_line += " " + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
        
        return lines