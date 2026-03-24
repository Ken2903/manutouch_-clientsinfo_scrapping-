from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # suppress console noise
driver = webdriver.Chrome()
url = "https://www.manutouch.com.hk/"
driver.get(url)
time.sleep(3)

# login page
login_button = driver.find_element(By.XPATH, "//button[text()='繼續登入']")
login_button.click()
time.sleep(8)

# enter username and password
url_new = "https://api.emmprd.asia.manulife.com/ext/nest-connect-gatewayd/interaction/p7A9rArksMogGXpNoCAwp&lang=zh-hant"
driver.get(url_new)


username = driver.find_element(By.ID, "user")
password = driver.find_element(By.ID, "password")
username.clear()
password.clear()
username.send_keys("")  # enter username
password.send_keys("")  # enter password
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
submit_button.click()
time.sleep(2)

# second login page
login_button2 = driver.find_element(By.ID, "radio1")
login_button2.click()
send_button = driver.find_element(By.XPATH, "//button[text()='發送']")
send_button.click()
time.sleep(35)

# main page 
driver.get(url + "home/customer/customer-search?from=root")
time.sleep(25)

data=[]
x= 0 
# search customer
def search_customer(): 
    global data
    global x
    search= driver.find_elements(By.XPATH, "//*[@class = 'table-row-rwnZRQ']")
    for s in search:
        print(f"page{x}")
        print(s.text)
        data.append(s.text)
        x += 1

search_customer() # first page data
# next page
page_count = 0
for i in range(2, 47):
    try:
        xpath = f"//li[contains(@class, 'mdr-pagination-item') and text()={i}]"
        
        # Wait until the pagination button is clickable
        next_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        
        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        next_button.click()
        
        page_count += 1
        time.sleep(5)  # Allow page to load fully
        search_customer()

    except Exception as e:
        print(f"Failed to click li[{i}]: {e}")
        break

# storing data to csv
df = pd.DataFrame(data, columns=["customer_info"])
df.to_csv("manulife_customer_info.csv", index=False, encoding="utf-8-sig")
driver.quit()

