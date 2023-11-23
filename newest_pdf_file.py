import glob
import os

downloads_folder_path = os.path.join(os.environ['USERPROFILE'], "Downloads")


pdf_files = glob.glob(os.path.join(downloads_folder_path,"*.pdf"))
pdf_files.sort(key=os.path.getctime)
pdf_files.reverse()