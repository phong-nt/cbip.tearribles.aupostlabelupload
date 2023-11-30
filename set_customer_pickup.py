import anchanto
import time
import sys


driver = anchanto.driver
print(f"Entering {anchanto.login_page}")
anchanto.try_login_anchanto(driver, "phong.nguyen@cbiplogistics.com", "Cbip@1994")


for i in range(1, len(sys.argv)):
    driver.get(r"https://ewms.anchanto.com/orders/bulk/order_status_tracker")
    anchanto.try_clear(driver, '//textarea[@name="order_numbers"]')
    anchanto.try_input(driver, '//textarea[@name="order_numbers"]', sys.argv[i])
    anchanto.try_click(driver, '//input[@value="Submit"]')
    anchanto.try_click(driver, f'//table/tbody/tr/td/a[contains(text(), "{sys.argv[i]}")]')
    tracking = anchanto.try_gettxt(driver, '//div/label[contains(text(), "Tracking")]/following-sibling::label/a/label[1]')
    driver.get(f"https://ewms.anchanto.com/orders/modify_order?order_number={tracking}")
    time.sleep(3)
    anchanto.try_select(driver, '//select[@id="order_bucket_carrier_code"]', 'B1P')
    time.sleep(3)
    # try to click on the checkbox
    #TODO: first check if checkbox is unchecked, if checked then ignore
    anchanto.try_click(driver, '//label[contains(text(), "Is Customer Pickup?")]//preceding-sibling::div/label/input')
    time.sleep(3)
    anchanto.try_click(driver, '//input[@value="Update"]')

    


