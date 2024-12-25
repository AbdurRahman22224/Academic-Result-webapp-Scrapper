from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from selenium.webdriver.chrome.options import Options

def download_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure headless mode for servers
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Explicit Chrome binary path

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    return driver


# Function to generate roll number based on inputs
def generate_roll_number(branch, year, course, i):
    formatted_number = f"{i:03}"  # Format the number to always have 3 digits
    return f"{year}{course}{branch[:3].upper()}{formatted_number}"

# Scraping function to get SGPA and CGPA
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
    
