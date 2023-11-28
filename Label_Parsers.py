import PyPDF2
import re

class AuPost_99(self):
    def __init__(self):
        from PyPDF2 import PdfReader
        import re
        self.reader = PdfReader(self)
        self.page = self.reader.pages[0]
        self.text = self.page.extract_text()
        self.ref = re.search(pattern="^AP Article Id: [0-9]{23}", string=self.text).group(0)
