from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def try_input(driver, xpath, content):
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(content)


def try_click(driver, xpath):
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def try_gettxt(driver, xpath):
    elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath))).text
    return elem

login_page = r"https://ewms.anchanto.com/login"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

email_box_path = '//div[@class="form-group"]/input[@id="user_email"]'
passw_box_path = '//div[@class="form-group"]/input[@id="user_password"]'
login_btn_path = '//div[@class="form-group"]/input[@name="commit"]'

print(f"Entering {login_page}")
driver.get(login_page)

print("Trying to login:", end=" ")
try_input(driver, email_box_path, 'phong.nguyen@cbiplogistics.com')
try_input(driver, passw_box_path, 'Cbip@1994')
try_click(driver, login_btn_path)

alert_div_path = '//div[@class="result"]/div[1]'
alert = driver.find_element(By.XPATH, alert_div_path).text
print(alert)

welcm_mes_path = '//ul[@class="nav ace-nav"]/li[6]/a[@class="dropdown-toggle"]'
print(try_gettxt(driver, welcm_mes_path))