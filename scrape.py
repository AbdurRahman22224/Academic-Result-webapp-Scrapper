from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

def download_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # Ensure headless mode for servers
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.binary_location = "/usr/bin/google-chrome"  # Explicit Chrome binary path

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    return driver


# Function to generate roll number based on inputs
def generate_roll_number(branch, year, course, i):
    formatted_number = f"{i:03}"  # Format the number to always have 3 digits
    return f"{year}{course}{branch[:3].upper()}{formatted_number}"

def scrape_results(driver, user_name, sem):
    driver.get('http://202.168.87.90/StudentPortal/Login.aspx')
    time.sleep(1.3)
    # Forget Password
    link2 = driver.find_element(by=By.XPATH, value='//*[@id="lblforgetpass"]')
    link2.click()
    time.sleep(0.5)

    user_input = driver.find_element(by=By.XPATH, value='//*[@id="txt_username"]')
    user_input.clear() 
    user_input.send_keys(user_name)
    time.sleep(1)

    pass_word = '1'  # Password
    # user_input = driver.find_element(by=By.XPATH, value='//*[@id="txtnewpass"]')
    #txtnewpass
    user_input = driver.find_element(By.CSS_SELECTOR, '#txtnewpass')
    user_input.send_keys(pass_word)
    time.sleep(0.5)

    user_input = driver.find_element(by=By.XPATH, value='//*[@id="txtConfirmpass"]')
    user_input.send_keys(pass_word)
    time.sleep(0.2)

    user_input = driver.find_element(by=By.XPATH, value='//*[@id="btnSubmit"]')
    user_input.send_keys(Keys.ENTER)
    time.sleep(0.8)

    # Handle alert
    
    # Handle the alert that appears after password reset
    try:
        alert = Alert(driver) 
        # alert = driver.switch_to.alert
        alert_text = alert.text  # Get the text of the alert to decide the action
        if "Server UnAvailable" in alert_text:
            alert.accept()  # Accept the alert to dismiss it
            return None, None, None # Skip this iteration and move to the next roll number
        
        else:
            print(alert_text, 'in else')
            alert.accept() 
    except:
        print("No alert found")


    # Login
    user_input = driver.find_element(by=By.XPATH, value='//*[@id="txt_username"]')
    user_input.send_keys(user_name)
    time.sleep(0.2)

    user_input = driver.find_element(by=By.XPATH, value='//*[@id="txt_password"]')
    user_input.send_keys(pass_word)
    time.sleep(0.2)

    user_input = driver.find_element(by=By.XPATH, value='//*[@id="btnSubmit"]')
    user_input.send_keys(Keys.ENTER)
    time.sleep(0.5)
    dropdown_element = driver.find_element(By.XPATH, value='//*[@id="ddlSemester"]')

    try:
        # Select Semester
        dropdown = Select(dropdown_element)
        # dropdown.select_by_index(sem)
        dropdown.select_by_visible_text(sem)  
        time.sleep(0.2)

        user_input = driver.find_element(by=By.XPATH, value='//*[@id="btnimgShowResult"]')
        user_input.send_keys(Keys.ENTER)
        time.sleep(0.5)
    
        name = driver.find_element(By.ID, "lblStudentName").text
        sgpa = driver.find_element(By.ID, "lblSPI").text
        cgpa = driver.find_element(By.ID, "lblCPI").text 
        return name, sgpa, cgpa
    
    except:
        return None, None, None
    # 8th 
# //*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[2]/td[2]
# //*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]
# //*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[4]/td[2]

# 6th
# //*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[2]/td[2]  //*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[2]/td[8] //*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[8]
     
def genrate_subjects(driver): 
    subjects = []
    i = 2  # Adjust index if needed
    while True:
        try:
            xpath = f'//*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[{i}]/td[2]'
            element = driver.find_element("xpath", xpath)
            print("Subject found:", repr(element.text.strip()))
            subjects.append(element.text.strip()) 
            i += 1
        except Exception as e:
            print("Subject element not found. Reason:", e)
            break  # Exit loop when no more subjects
    return subjects

  


# def genrate_subjects(driver):
#     try:
#         # Try finding the first subject using relative XPath
    
#         xpath = '//*[@id="PnlShowResult"]/table/tbody/tr[4]/td/table/tbody/tr[]/td[2]'
#         element = driver.find_element(By.XPATH, xpath)
#         print("Subject found:", repr(element.text.strip()))
#         return element.text.strip()
#     except Exception as e:
#         print("Subject element not found. Reason:", e)
#         return None

