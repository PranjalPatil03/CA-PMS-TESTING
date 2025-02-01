import time
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


# Define paths
current_directory = Path(__file__).resolve().parent
chrome_binary_path = current_directory / 'chrome-win64' / 'chrome.exe'
webdriver_path = current_directory / 'chromedriver-win64' / 'chromedriver.exe'
excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data.xlsx"
new_excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_updated.xlsx"

# Initialize the Chrome driver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = str(chrome_binary_path)

service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the data from Excel file
df = pd.read_excel(excel_file_path)

# Ensure the Status column is available
if 'Status' not in df.columns:
    df['Status'] = ''

# Define the URL to test
url = 'https://pms-ui-dev-centralindia.azurewebsites.net/#/login?returnUrl=%2Fhome'

for index, row in df.iterrows():
    try:
        driver.get(url)
        time.sleep(5)

        username_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'username'))
        )
        password_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'password'))
        )
        
        username = row['username']
        if isinstance(username, float):
            username = str(int(username))
        password = str(row['password'])
        username_field.send_keys(username)
        time.sleep(2)
        password_field.send_keys(password)
        time.sleep(2)

        login_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
        )
        login_button.click()
        time.sleep(5)  # Wait for login

        goal_setting_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'layout-menuitem-text') and text()='Goal Setting']"))
        )
        goal_setting_button.click()
        time.sleep(3)  # Wait for the Goal Setting page to load

        # choose_button_xpath = "//span[@class='p-button-label']"
        choose_button_xpath = "//span[@class='p-ripple p-element p-button p-component p-fileupload-choose']"
        upload_button_xpath = "//div[@class='ng-star-inserted']//p-button[1]//button[1]"
        
        for index, row in df.iterrows():
            file_path = row['File_path']  # Get the file path from the 'File_path' column

            try:
        # Find and click the "Choose" button
                
                choose_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, choose_button_xpath)))
                choose_button.click()

        # Use the file input dialog to send the file path
                time.sleep(1)  # Add a slight delay to ensure file input opens
                file_input = driver.find_element(By.XPATH,"//input[@type='file']")  # Locate the file input field
                file_input.send_keys(file_path)  # Upload the file using the path from Excel
        
        # Wait for the file to be selected
                time.sleep(2)
        
        # Click the upload button
                upload_button = driver.find_element(By.XPATH, upload_button_xpath)
                upload_button.click()
        
        # Wait for the upload to complete
                time.sleep(3)
        
                print(f"File '{file_path}' uploaded successfully.")
        
            except Exception as e:
                print(f"Failed to upload file '{file_path}': {e}") 
            df.at[index, 'Status'] = 'Success'
    except Exception as e:
        df.at[index, 'Status'] = 'Failed'
# Save updated Excel file with Status column
df.to_excel(new_excel_file_path, index=False)

# Close the driver
driver.quit()
              



