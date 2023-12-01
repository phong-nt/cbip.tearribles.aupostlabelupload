from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AnchantoWeb:
    LOGIN_PAGE = r"https://ewms.anchanto.com/login"
    global_timeout = 10


    def __init__(self):
        # self.ua = user_agent("chrome")
        # self.ua = ua
        self.options = Options()
        # self.options.add_argument(f"--user-agent={self.ua}")
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=self.options)

    def clear(self, xpath):
        try:
            WebDriverWait(self.driver, AnchantoWeb.global_timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).clear()
            return True
        except:
            print("Clear content failed.")
            return False

    
    def input(self, xpath, content, clear_first=False):
        try:
            if clear_first:
                self.clear(xpath=xpath)
            WebDriverWait(self.driver, AnchantoWeb.global_timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(content)
            return True
        except:
            print("Input content failed.")
            return False
        

    def click(self, xpath):
        try:
            WebDriverWait(self.driver, AnchantoWeb.global_timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            return True
        except:
            print(f"Click to {xpath} failed.")
            return False
        
    
    def bring(self, xpath):
        try:
            msg = WebDriverWait(self.driver, AnchantoWeb.global_timeout).until(EC.visibility_of_element_located((By.XPATH, xpath))).text
            print(msg)
            return True
        except:
            print("Can't read the message.")
            return False
                

    def open_wms(self):
        self.driver.get(AnchantoWeb.LOGIN_PAGE)

    def sign_in(self, username, password):
        if self.driver.current_url == AnchantoWeb.LOGIN_PAGE:
            self.clear("//input[@id='user_email']")
            self.clear("//input[@id='user_password']")
            self.input("//input[@id='user_email']", username)
            self.input("//input[@id='user_password']", password)
            self.click("//input[@name='commit']")
            self.bring("//div[@class='alert alert-warning']")
            self.bring("//ul[@class='nav ace-nav']/li/a[@class='dropdown-toggle']")
        else:
            print("Not a login page.")




# ua = user_agent("chrome")
browser = AnchantoWeb()
browser.open_wms()
browser.sign_in("phong.nguyen@cbiplogistics.com", "Cbip@1994")

