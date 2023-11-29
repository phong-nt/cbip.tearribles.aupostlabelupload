from PyPDF2 import PdfReader
import re
from prettytable import PrettyTable

class AuPost_99():
    def __init__(self, pdf_path):
        self.reader = PdfReader(pdf_path)
        self.length = len(self.reader.pages)
        self.page = list([i for i in self.reader.pages])
        self.text = list([i.extract_text().strip() for i in self.page])
        self.readable = list([bool(len(i)) for i in self.text])
        awb_pattern = r"AP Article Id: [0-9]{23}"
        self.awb_found = list([False] * self.length)
        self.awb = list([None]* self.length)
        self.is_Tearribles_shipment = list([False]*self.length)
        self.ref = list([None] * self.length)

        for i in range(self.length):
            if self.readable[i]:
                self.awb_found[i] = bool(len(re.findall(pattern=awb_pattern, string=self.text[i])))
            if self.awb_found[i]:
                self.awb[i] = (re.search(pattern=awb_pattern, string=self.text[i]).group(0)).replace("AP Article Id: ", "")
            if bool(len(re.findall("Tearribles", self.text[i]))):
                self.is_Tearribles_shipment[i] = True
            if self.is_Tearribles_shipment[i]:
                self.ref[i] = ((re.search(pattern="Ref: AU[0-9]{4}", string=self.text[i])).group(0)).replace("Ref: ", "")

            
        
        
    def info(self):
        info_table = PrettyTable(["Index", "Readable", "Ref", "AWB"])
        for i in range(self.length):
            info_table.add_row([i, self.readable[i], self.ref[i], self.awb[i]])

        print(info_table)       



# demo
path = r"C:\Users\nguye\Downloads\4ecc3a56-ad43-4eb5-b978-b3c161bdc3bc.pdf"
label = AuPost_99(path)

label.info()