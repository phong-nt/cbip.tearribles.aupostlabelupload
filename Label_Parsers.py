from PyPDF2 import PdfReader
import re

class AuPost_99():
    def __init__(self, pdf_path):
        self.reader = PdfReader(pdf_path)
        self.page = self.reader.pages[0]
        self.text = self.page.extract_text().strip()
        self.readable = bool(len(self.text))
        self.awb_pattern = r"AP Article Id: [0-9]{23}"
        if self.readable:
            self.awb_found = bool(len(re.findall(pattern=self.awb_pattern, string=self.text)))
            if self.awb_found:
                self.awb = re.search(pattern=self.awb_pattern, string=self.text).group(0)
            else:
                self.awb = ""


page1 = AuPost_99(r"C:\Users\nguye\Downloads\Bella + Canvas Jersey Tee - Size L  Mens AU.pdf")

print(page1.readable)
