import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text

class DatasetExtractionAgent:
    def __init__(self):
        self.supported_formats = ["pdf", "html", "csv"]

    def download_pdf(self, url, filename="downloaded_paper.pdf"):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ PDF Downloaded: {filename}")
            return filename
        else:
            raise Exception("❌ Failed to download PDF")

    def extract_from_pdf(self, pdf_path):
        text = extract_text(pdf_path)
        tables = re.findall(r'\b\d+\.\d*\b', text)
        return pd.DataFrame(tables, columns=["Extracted Values"])

    def extract_from_web(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        data = []
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                data.append(cols)
        return pd.DataFrame(data)

    def extract_dataset(self, source):
        if source.startswith("http"):
            print("🔍 Detecting URL Source...")
            pdf_file = self.download_pdf(source)
            return self.extract_from_pdf(pdf_file)
        elif source.endswith(".pdf"):
            print("🔍 Detecting Local PDF Source...")
            return self.extract_from_pdf(source)
        elif source.endswith(".html") or source.startswith("http"):
            print("🔍 Detecting HTML Source...")
            return self.extract_from_web(source)
        else:
            raise ValueError("Unsupported dataset format")

    def extract_from_pdf_table(self, pdf_path):
        import camelot
        print(f"📄 Extracting Tables from {pdf_path}...")
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
        if len(tables) == 0:
            print("❌ No tables found in PDF.")
            return pd.DataFrame()
        table_df = pd.concat([table.df for table in tables], ignore_index=True)
        return table_df

    def clean_dataset(self, df):
        df.dropna(inplace=True)
        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)
        return df
