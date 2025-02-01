import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # For handling Enter key in Select2
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import logging
import time
 
# Set up logging
logging.basicConfig(filename='form_filling_errors.log', level=logging.ERROR)
 
# File paths
current_directory = Path(__file__).resolve().parent
webdriver_path = current_directory / 'chromedriver-win64' / 'chromedriver.exe'
chrome_binary_path = current_directory / 'chrome-win64' / 'chrome.exe'
 
# Setup Chrome options
chrome_options = Options()
chrome_options.binary_location = str(chrome_binary_path)
chrome_options.add_argument('--no-sandbox')  # Disable sandbox
chrome_options.add_argument('--disable-dev-shm-usage')  # Prevent memory issues
chrome_options.add_argument('--disable-extensions')  # Disable Chrome extensions
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
 
service = Service(str(webdriver_path))
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
 
driver.get('https://pms-ui-dev-centralindia.azurewebsites.net/#/login?returnUrl=%2Fhome')
time.sleep(5)
username_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')
username_field.send_keys('99999999')
password_field.send_keys('password')
login_button = driver.find_element(By.CLASS_NAME, 'p-button')
login_button.click()
time.sleep(5)
 
try:
    goal_setting_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#/goal-setting']")))
    goal_setting_button.click()
    time.sleep(5)
    print("Clicked on Goal Setting button.")
    # click on manage template button
    manage_templates_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Manage Templates']/parent::a")))
    manage_templates_button.click()
    # Click on Template
    template_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#/template']")))
    template_button.click()
    print("Clicked on Template button.")
    


    print("Clicked on Manage Templates button.")
    time.sleep(5)
except Exception as e:
    logging.error("Error clicking Goal Setting button: %s", e)

driver.quit()
 
 