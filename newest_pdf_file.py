import glob
import os

download_folder = "C:\\Users\\nguye\\Downloads\\"

list_of_files = glob.glob(download_folder+"*")
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)