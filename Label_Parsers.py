from PyPDF2 import PdfReader
import re

class AuPost_99():
    def __init__(self, pdf_path):
        self.reader = PdfReader(pdf_path)
        self.length = len(self.reader.pages)
        self.page = list([i for i in self.reader.pages])
        self.text = list([i.extract_text().strip() for i in self.page])
        self.readable = list([bool(len(i)) for i in self.text])
        awb_pattern = r"AP Article Id: [0-9]{23}"
        self.awb_found = list([None] * self.length)
        self.awb = list([None]* self.length)

        for i in range(self.length):
            if self.readable[i]:
                self.awb_found[i] = bool(len(re.findall(pattern=awb_pattern, string=self.text[i])))
            if self.awb_found[i]:
                self.awb[i] = (re.search(pattern=awb_pattern, string=self.text[i]).group(0)).replace("AP Article Id: ", "")
        
        
    def info(self):
        print(f"\n+-----+-----------+"+"-"*23+"+")
        print("|index", end="|")
        print("is readable", end="|")
        print("AWB".center(23, " "), end="|\n")
        print(f"+-----+-----------+"+"-"*23+"+")
        for i in range(self.length):
            print(f"|{i:5}|{self.readable[i]:11}|{self.awb[i]:23}|")
        print("+-----+-----------+"+"-"*23+"+")        




path = r"C:\Users\nguye\Downloads\4ecc3a56-ad43-4eb5-b978-b3c161bdc3bc.pdf"
label = AuPost_99(path)

label.info()