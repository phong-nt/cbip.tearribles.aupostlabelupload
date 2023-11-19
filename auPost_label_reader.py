from PyPDF2 import PdfReader, PdfWriter
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

download_folder_path = "C:\\Users\\nguye\\Downloads\\"
merged_file_name = input("Input PDF file name: ")

print(f"\nReading {download_folder_path}{merged_file_name}.")
reader = PdfReader(f"{download_folder_path}{merged_file_name}")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    output = []
    for i in range(len(reader.pages)):
        page_i = reader.pages[i]
        page_i_text = page_i.extract_text()
        output.append(page_i_text.strip())
    
    return output

all_text = extract_text_from_pdf(f"{download_folder_path}{merged_file_name}")
print(f"The selected file has {len(all_text)} page(s)")


def extract_AWB_from_label_text(text):
    import re
    pattern = "^AP Article Id: [0-9]+"
    extracted_text = re.search(pattern=pattern, string=text).group(0)
    extracted_awb = re.sub("AP Article Id: ", "", extracted_text)
    return extracted_awb

def extract_REF_from_label_text(text):
    import re
    pattern = "Ref: AU[0-9]{4}"
    extracted_text = re.search(pattern=pattern, string=text).group()
    extracted_ref = re.sub("Ref: ", "", extracted_text)
    return extracted_ref





awb = []
ref = []
for i in all_text:
    awb.append(extract_AWB_from_label_text(i))
    ref.append(extract_REF_from_label_text(i))
    print(extract_REF_from_label_text(i)+": "+extract_AWB_from_label_text(i))



def PDF_Splitter(input_file, output_file_name, page_index):
    with open(input_file, "rb") as infile:
        reader = PdfReader(input_file)
        writer = PdfWriter()
        writer.add_page(reader.pages[page_index])

    

    with open(output_file_name, 'wb') as outfile:
        writer.write(outfile)

inputfile = f"{download_folder_path}{merged_file_name}"
outputfile = f"{download_folder_path}{ref[0]}_{awb[0]}.pdf"
index = 0

for i in range(len(all_text)):
    PDF_Splitter(
        input_file=f"{download_folder_path}{merged_file_name}",
        output_file_name=f"{download_folder_path}{ref[i]}_{awb[i]}.pdf",
        page_index=i
    )
print(f"\nSplitted labels are located at {download_folder_path}.")

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

    label_path = download_folder_path+ref[i]+"_"+awb[i]+".pdf"
    print(f"\tStep 3: Uploading label at {label_path}")
    try_input(driver, "//input[@id='order_bucket_order_invoices_attributes_0_data']", label_path)
    time.sleep(1)
    
    print(f"\t-----\n\tModifying order {ref[i]} is complete.\n \n \n")
    try_click(driver, "//input[@value='Update']")
    time.sleep(1)

driver.close()
print(f"Your work is done. {len(awb)} order(s) affected.")