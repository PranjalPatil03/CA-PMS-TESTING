# ImportAll
# def ImportAll():
import pyautogui
import time
import os
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import numpy as np
import math
from selenium.common.exceptions import TimeoutException
import KPIADD as ak 
from openpyxl import Workbook



def InitializeChromeDriver():
    
    print("Hello, I am initializing Chrome driver")
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    webdriver_path = os.path.join(base_dir, 'chromedriver-win64', 'chromedriver.exe')
    chrome_binary_path = os.path.join(base_dir, 'chrome-win64', 'chrome.exe')
    current_directory = Path(__file__).resolve().parent
    chrome_binary_path = current_directory / 'chrome-win64' / 'chrome.exe'
    webdriver_path = current_directory / 'chromedriver-win64' / 'chromedriver.exe'
    excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
    new_excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_updated.xlsx"
    
    chrome_options = Options()
    chrome_options.binary_location = str(chrome_binary_path)
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    #wait = WebDriverWait(driver, 15)
    # Press Windows Key + Up Arrow
    pyautogui.hotkey('win', 'up')
    return driver
    


def login(driver, username, password, row):
    excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
    sheet_name = 'Login'
    # Load the sheet data into a DataFrame
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    url = 'https://testpms.mahyco.com/'
    driver.get(url)
    time.sleep(3)

    username_field = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'username')))
    password_field = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'password')))
    
    username_field.clear()
    username = str(row['username'])
    if isinstance(username, float) and math.isnan(username):
        username = "default_username"  
    else:
        username = str(int(username))
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
    login_button.click()
    print("login successfully")
    print("clicking on Goal setting")
    time.sleep(3)

def logout(wait):
    try:
       
       button = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'pi pi-fw pi-user')]")))
       button.click()
        # Locate the logout button using the 'pi pi-power-off' class and click it
       logout_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'pi pi-sign-out')]"))
        )
       logout_button.click()
       print("logout successfully")
       time.sleep(3)  # Add some wait time to ensure the action is completed
    except Exception as e:
        print(f"unable to logout{e}")      
        return
        

def Click_Goal_Setting(driver, wait):
    try:
         # Click on the "Goal Setting" button
           goal_setting_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'layout-menuitem-text') and text()='Goal Setting']")))
    
           goal_setting_button.click()
           time.sleep(2)  # Wait for the Goal Setting page to load
           print("Clicked on goal setting")
    except Exception as e:
        print(f"exception as {e}")
def click_cancel_button(driver):
    try:
        cancel_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@icon, 'pi pi-times')]")))
        cancel_button.click()
        print("Clicked on cancel successfully")
        time.sleep(2)
    except selenium.common.exceptions.TimeoutException:
        print("unable to click on cancel button")
        return


def click_submit_button(driver, wait):
    
    try:
        Click_Goal_Setting(driver, wait)
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-button') and text()='Submit']"))
        )
        submit_button.click()
        print("submit button clicked")
        
        try:
            # Wait for the toast message to appear
            toast_message = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p-toast-detail')]"))
            )

            # Extract the message text
            message_text = toast_message.text
            print(f"Extracted Message: {message_text}")
        except Exception as e:
            print(f'Exception occur {e}')


    except selenium.common.exceptions.TimeoutException:
        driver.refresh()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Add KPI']")))
        print("Unable to click on submit button")
        time.sleep(3)
    try:
        # Click Yes button
        yes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='p-button-label' and text()='Yes']"))
        )
        yes_button.click()
        print("Clicked on Yes button")
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred while clicking on yes button: {e}")
    

    