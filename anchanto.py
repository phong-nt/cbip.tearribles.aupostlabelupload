from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_user_agent import user_agent




def try_input(driver, xpath, content):
    try:
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(content)
    except:
        print(f"Cannot enter {content} into {xpath}")


def try_click(driver, xpath):
    try:
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except:
        print(f"Cannot locate {xpath}")


def try_gettxt(driver, xpath):
    try:
        elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath))).text
        return elem
    except:
        print(f"Cannot locate {xpath}")
        return None


login_page = r"https://ewms.anchanto.com/login"
ua = user_agent("chrome")
chrome_options = Options()
chrome_options.add_argument(f"--user-agent={ua}")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

email_box_path = '//div[@class="form-group"]/input[@id="user_email"]'
passw_box_path = '//div[@class="form-group"]/input[@id="user_password"]'
login_btn_path = '//div[@class="form-group"]/input[@name="commit"]'

driver.get(login_page)
print(f"Opening {driver.current_url}")

print("Trying to login:", end=" ")
try_input(driver, email_box_path, 'phong.nguyen@cbiplogistics.com')
try_input(driver, passw_box_path, 'Cbip@1994')
try_click(driver, login_btn_path)

alert_div_path = '//div[@class="result"]/div[1]'
print(try_gettxt(driver, alert_div_path))

welcm_mes_path = '//ul[@class="nav ace-nav"]/li[6]/a[@class="dropdown-toggle"]'
print(try_gettxt(driver, welcm_mes_path))