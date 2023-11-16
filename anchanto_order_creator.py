from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
anchanto_browser = webdriver.Chrome(options=options)
anchanto_browser.get("https://ewms.anchanto.com/login")
print(anchanto_browser.title)


email = "phong.nguyen@cbiplogistics.com"
password = "Cbip@1994"

def try_inputting(driver, element_xpath, value):
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        element.send_keys(value)
    except:
        time.sleep(1)
        print("Trying again")

def try_click(driver, element_xpath):
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        element.click()
    except:
        time.sleep(1)
        print("Trying again")

def keep_looking_for_element(driver, element_xpath):
    try:
        element = driver.find_element(By.XPATH, element_xpath)
        print(element.text)
    except:
        time.sleep(1)
        print("-", end='')
    
try_inputting(anchanto_browser, "//input[@id='user_email']", email)
try_inputting(anchanto_browser, "//input[@id='user_password']", password)

try_click(anchanto_browser, "//input[@value='Sign In']")
keep_looking_for_element(anchanto_browser, "//li[@class='light-blue']/a[@class='dropdown-toggle']")

anchanto_browser.get("https://ewms.anchanto.com/orders/bulk/order_status_tracker")

order_in_question = str(input("Enter order: "))

try_inputting(anchanto_browser, "//input[@id='order_number']", order_in_question)
try_click(anchanto_browser, "//button[@id='check-order']")



time.sleep(10)
# anchanto_browser.quit()
print("Browser closed.")

