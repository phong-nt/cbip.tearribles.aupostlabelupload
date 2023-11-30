import anchanto
import sys


driver = anchanto.driver
print(anchanto.login_page)
# driver.get(anchanto.login_page)


for i in range(1, len(sys.argv)):
    driver.get(r"https://ewms.anchanto.com/orders/bulk/order_status_tracker")
    anchanto.try_clear(driver, '//textarea[@name="order_numbers"]')
    anchanto.try_input(driver, '//textarea[@name="order_numbers"]', sys.argv[i])
    anchanto.try_click(driver, '//input[@value="Submit"]')
    anchanto.try_click(driver, f'//table/tbody/tr/td/a[contains(text(), "{sys.argv[i]}")]')
    tracking = anchanto.try_gettxt(driver, '//div/label[contains(text(), "Tracking")]/following-sibling::label/a/label[1]')
    driver.get(f"https://ewms.anchanto.com/orders/modify_order?order_number={tracking}")


