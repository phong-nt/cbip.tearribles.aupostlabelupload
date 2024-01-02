from PyPDF2 import PdfReader, PdfWriter
# import re
# import glob
import os
import time
from datetime import date
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# experiment with colored console output
from colorama import just_fix_windows_console, Fore, Style
just_fix_windows_console()

print(f"{Style.BRIGHT}Tearribles label processor by Nguyen Tien Phong\n\n\n{Style.RESET_ALL}")

#get the downloads folder
download_folder_path = os.path.join(os.environ['USERPROFILE'], "Downloads")
print(f"Looking into Downloads folder at {Fore.CYAN}{download_folder_path}{Style.RESET_ALL}\n")
# create a sub-folder for today's orders

def create_sub_folder(under):
    today = date.today()
    prefix = "Tearribles_"
    serial = today.strftime("%y")+today.strftime("%m")+today.strftime("%d")
    try:
        print(f"Creating subfolder {Fore.CYAN}{prefix}{serial}{Style.RESET_ALL}")
        os.mkdir(os.path.join(under, prefix+serial))
    except:
        print(f"{Fore.YELLOW}The folder is already there.{Style.RESET_ALL}")
    
    return f"{prefix}{serial}"



# list all pdf files in the folder (last saved first)
def list_of_pdfs(folder_path):
    import glob
    import os

    full_path = os.path.join(folder_path, "*.pdf")
    pdf_files = glob.glob(full_path)
    pdf_files.sort(key=os.path.getctime)
    pdf_files.reverse()
    
    return pdf_files


list_pdfs = list_of_pdfs(download_folder_path)

# look into each file, if there is "Ref: AU[0-9]{4}" then True, else False
def is_Tearribles_label(filepath):
    import re
    
    ref_found = 0
    readable = True
    ref = False
    try:
        reader = PdfReader(filepath)
        first_page = reader.pages[0]
        first_page_text = first_page.extract_text()
        ref_found = len(re.findall("Ref: AU[0-9]{4}", first_page_text))
    except:
        readable = False
        # print(f"{Fore.LIGHTRED_EX}File not readable.{Style.RESET_ALL}")
    if ref_found >= 1:
        ref = True
    else:
        ref = False
    return ref, readable

# iterate through the list, detecting Tearribles label    
last_pdf = ""
for i in list_pdfs:
    short_i = i.replace(download_folder_path+"\\", "")
    print(f"\t{Style.DIM}Inspecting{Style.RESET_ALL} {Style.BRIGHT}{short_i: <70}{Style.RESET_ALL}", end=" ")
    ref_i, readable_i = is_Tearribles_label(i)
    if ref_i and readable_i:
        last_pdf = i
        print(f"{Fore.GREEN}Label found!\n{Style.RESET_ALL}")
        break
    if readable_i:
        print(f"{Style.DIM}Not a Tearribles label.{Style.RESET_ALL}")
    else:
        print(f"{Style.DIM}{Fore.LIGHTRED_EX}Can't see what's inside.{Style.RESET_ALL}")
        
if last_pdf == "":
    print(f"\n{Style.BRIGHT}{Fore.RED}None of the labels is valid. This is pointless.\n{Style.RESET_ALL}")
    sys.exit()
else:
    today_folder = create_sub_folder(under=download_folder_path)
    


print(f"\nReading {Fore.CYAN}{last_pdf}{Style.RESET_ALL}.")
# reader = PdfReader(f"{last_pdf}")

# extract text from pages to a list
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    output = []
    for i in range(len(reader.pages)):
        page_i = reader.pages[i]
        page_i_text = page_i.extract_text()
        output.append(page_i_text.strip())
    
    return output

all_text = extract_text_from_pdf(f"{last_pdf}")

# length of the all_text list is also number of pages
print(f"The selected file has {Fore.YELLOW}{len(all_text)}{Style.RESET_ALL} page(s)\n")


# extract awb number using regex
def extract_AWB_from_label_text(text):
    import re
    pattern = "^AP Article Id: [0-9]{23}"
    extracted_text = re.search(pattern=pattern, string=text).group(0)
    extracted_awb = re.sub("AP Article Id: ", "", extracted_text)
    return extracted_awb


# extract order ref using regex
def extract_REF_from_label_text(text):
    import re
    pattern = "Ref: AU[0-9]{4}"
    extracted_text = re.search(pattern=pattern, string=text).group()
    extracted_ref = re.sub("Ref: ", "", extracted_text)
    return extracted_ref


# iterate through the all_text list and execute the above functions
awb = []
ref = []
for i in all_text:
    awb.append(extract_AWB_from_label_text(i))
    ref.append(extract_REF_from_label_text(i))
    print(extract_REF_from_label_text(i)+": "+extract_AWB_from_label_text(i))


# split the pdf by each page
def PDF_Splitter(input_file, output_file_name, page_index):
    with open(input_file, "rb") as infile:
        reader = PdfReader(infile)
        writer = PdfWriter()
        writer.add_page(reader.pages[page_index])

    

    with open(output_file_name, 'wb') as outfile:
        writer.write(outfile)


# execute the splitting
# inputfile = last_pdf
# outputfile = f"{download_folder_path}\\Tearribles\\{ref[0]}_{awb[0]}.pdf"
# index = 0

for i in range(len(all_text)):
    PDF_Splitter(
        input_file=f"{last_pdf}",
        output_file_name=f"{download_folder_path}\\{today_folder}\\{ref[i]}_{awb[i]}.pdf",
        page_index=i
    )
print(f"\nSplitted labels are located at {Fore.CYAN}{download_folder_path}\\{today_folder}{Style.RESET_ALL}")

# setting up Chrome
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

# go to the website
print("\nEntering Anchanto")
driver.get("https://ewms.anchanto.com/login")
print(driver.title)

# credentials
eml = "phong.nguyen@cbiplogistics.com"
pwd = "Cbip@1994"


# define actions
def try_input(driver, element_xpath, value):
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        element.clear()
        element.send_keys(value)
    except:
        time.sleep(1)
        print(f"Trying to input into {element_xpath}")


def try_click(driver, element_xpath):
    import time
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        element.click()
    except:
        time.sleep(1)
        print("Trying again")

def wait_element(driver, element_xpath):
    import time
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        print(element.text)
    except:
        time.sleep(1)
        print("-", end='')

def try_select(driver, element_xpath):
    webdriver


# log in

try_input(driver, "//input[@id='user_email']",    eml)
try_input(driver, "//input[@id='user_password']", pwd)
try_click(driver, "//input[@value='Sign In']")
wait_element(driver, "//li[@class='light-blue']/a[@class='dropdown-toggle']")

print("-----\nBegin uploading information:\n-----")

# execution
for i in range(len(awb)):
    print(ref[i]+":")
    driver.get("https://ewms.anchanto.com/orders/modify_order")
    print(f"\tStep 1: Searching for order {ref[i]}")
    try_input(driver, "//input[@id='order_number']", ref[i])
    try_click(driver, "//button[@id='check-order']")
    time.sleep(1)
    print(f"\tStep 2: Inputting AWB: {awb[i]}")
    try_input(driver, "//input[@name='order_bucket[delivery_ref_no]']", awb[i])
    time.sleep(1)

    label_path = os.path.join(download_folder_path, today_folder, f"{ref[i]}_{awb[i]}.pdf")
    print(f"\tStep 3: Uploading label at {label_path}")
    try_input(driver, "//input[@id='order_bucket_order_invoices_attributes_0_data']", label_path)
    time.sleep(1)
    
    print(f"\t-----\n\tModifying order {ref[i]} is complete.\n \n \n")
    try_click(driver, "//input[@value='Update']")
    time.sleep(1)

driver.close()
print(f"Your work is done. {len(awb)} order(s) affected.")