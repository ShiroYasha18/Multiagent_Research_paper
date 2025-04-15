import os
import requests
from urllib.parse import urlparse

class DatasetExtractionAgent:
    def extract_dataset(self, paper_link):
        try:
            # Create downloads directory if it doesn't exist
            downloads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
            os.makedirs(downloads_dir, exist_ok=True)

            # Generate unique filename from URL
            filename = os.path.join(downloads_dir, 
                                  f"{urlparse(paper_link).path.split('/')[-1]}.pdf")

            # Download with proper headers and timeout
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            }
            response = requests.get(paper_link, headers=headers, timeout=30)
            response.raise_for_status()

            # Verify content type
            if 'application/pdf' not in response.headers.get('content-type', '').lower():
                raise ValueError("Downloaded content is not a PDF")

            # Save file with proper error handling
            with open(filename, 'wb') as f:
                f.write(response.content)

            return self._extract_data_from_pdf(filename)
        except Exception as e:
            print(f"Error downloading paper: {e}")
            return None

    def _extract_data_from_pdf(self, pdf_path):
        try:
            # Add your PDF data extraction logic here
            return {"sample_data": "Extracted data would go here"}
        except Exception as e:
            print(f"Error extracting data from PDF: {e}")
            return None

    def clean_dataset(self, dataset):
        if dataset is None:
            return {"status": "No data available"}
        # Add your dataset cleaning logic here
        return dataset