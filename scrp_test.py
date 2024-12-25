from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time, json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def download_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('http://202.168.87.90/StudentPortal/Login.aspx')
    time.sleep(1)

    return driver


# s = Service(r"C:\Users\abdur\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=s, options=options)

driver = download_selenium()
user_name = '2022UGPI001'
pass_word = 1
lst = []
dict_res = {}

# Forget Password
link2 = driver.find_element(by=By.XPATH, value='//*[@id="lblforgetpass"]')
link2.click()
time.sleep(1.5)

user_input = driver.find_element(by=By.XPATH, value='//*[@id="txt_username"]')
user_input.send_keys(user_name)
time.sleep(0.2)

user_input = driver.find_element(by=By.XPATH, value='//*[@id="txtnewpass"]')
user_input.send_keys(pass_word)
time.sleep(0.2)

user_input = driver.find_element(by=By.XPATH, value='//*[@id="txtConfirmpass"]')
user_input.send_keys(pass_word)
time.sleep(0.2)

user_input = driver.find_element(by=By.XPATH, value='//*[@id="btnSubmit"]')
user_input.send_keys(Keys.ENTER)
time.sleep(1)

# Handle the alert that appears after password reset
try:
    alert = Alert(driver)
    alert.accept()  # Accept the alert (click "OK")
    print("Alert handled")
except:
    print("No alert found")

# Login
# driver.get('http://202.168.87.90/StudentPortal/Login.aspx')
# time.sleep(1)
user_input = driver.find_element(by=By.XPATH, value='//*[@id="txt_username"]')
user_input.send_keys(user_name)
time.sleep(0.2)

user_input = driver.find_element(by=By.XPATH, value='//*[@id="txt_password"]')
user_input.send_keys(pass_word)
time.sleep(0.2)

user_input = driver.find_element(by=By.XPATH, value='//*[@id="btnSubmit"]')
user_input.send_keys(Keys.ENTER)
time.sleep(0.5)

dropdown_element = driver.find_element(By.XPATH, value = '//*[@id="ddlSemester"]')  
dropdown = Select(dropdown_element)
total_options = dropdown.options
value_to_select = 5

try:
    # Try to select the option by value
    # dropdown.select_by_value(value_to_select)
    dropdown.select_by_visible_text('V')
    # dropdown.select_by_index(3)
    user_input = driver.find_element(by=By.XPATH, value='//*[@id="btnimgShowResult"]')
    user_input.send_keys(Keys.ENTER)
    time.sleep(0.5)

    name = driver.find_element(By.ID, "lblStudentName").text
    sgpa = driver.find_element(By.ID, "lblSPI").text

# dropdown.select_by_index(3)
except:
    sgpa = "Not Found"


print(f"Roll_no: {user_name} SGPA: {sgpa}")
dict_res[user_name] = [name, sgpa]
lst.append(dict_res)
# Close the browser
driver.quit()

file_path = 'results.json'

# Dump the lst into the JSON file
with open(file_path, 'w') as json_file:
    json.dump(lst, json_file, indent=4)

print(f"Data has been saved to {file_path}")
