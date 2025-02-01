import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define paths
current_directory = Path(__file__).resolve().parent
chrome_binary_path = current_directory / 'chrome-win64' / 'chrome.exe'
webdriver_path = current_directory / 'chromedriver-win64' / 'chromedriver.exe'  # Path to your chromedriver
excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data.xlsx"  # Path to your Excel file
new_excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_updated.xlsx"  # New file to avoid overwriting

# Initialize the Chrome driver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = str(chrome_binary_path)

service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the data from Excel file
df = pd.read_excel(excel_file_path)

# Ensure the Status column is of type object (string) to avoid dtype issues
if 'Status' not in df.columns:
    df['Status'] = ''
else:
    df['Status'] = df['Status'].astype(str)

# Define the URL to test
url = 'https://pms-ui-dev-centralindia.azurewebsites.net/#/login?returnUrl=%2Fhome'

# Iterate through each row of data in the Excel file
for index, row in df.iterrows():
    try:
        time.sleep(5)
        driver.get('https://pms-ui-dev-centralindia.azurewebsites.net/#/login?returnUrl=%2Fhome')
        time.sleep(5)
        
        # Find username and password fields and fill them in
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username'))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'password'))
        )

        username = str(row['username'])
        password = str(row['password'])
    
        username_field.send_keys(username)
        password_field.send_keys(password)
    
        # Click on the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
        )
        login_button.click()

        # Wait for a few seconds to allow the page to respond
        time.sleep(3)

        # Check if the invalid username or password toast message appears
        try:
            toast_message_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'p-toast-detail')]"))
            )
            toast_message_text = toast_message_element.text

            # Check if it's the "Invalid Username or Password" message
            if "Invalid Username or Password" in toast_message_text:
                print(f"Test failed for {username}: {toast_message_text}")
                df.at[index, 'Status'] = 'Wrong Credentials'  # Mark as Wrong Credentials in the Excel
                
                # Reload the page to retry
                driver.refresh()
                time.sleep(5)  # Wait for the page to reload before proceeding
                continue  # Skip to the next iteration if credentials are invalid
                
        except Exception as e:
            # No toast message found, assuming login success
            print(f"No invalid message for {username}. Proceeding with logout.")
        
        # If no failure message, assume login is successful
        print(f"Test passed for {username}")
        df.at[index, 'Status'] = 'Pass'  # Mark as Pass in the Excel
        
        # Click the logout button after successful login
        try:
            logout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@ptooltip='Logout']"))
            )
            logout_button.click()
            print(f"Logout button clicked for {username}")
        except Exception as e:
            print(f"An error occurred while trying to click the logout button for {username}: {e}")
        
    except Exception as e:
        print(f"An error occurred for {row['username']}: {e}")
        df.at[index, 'Status'] = 'Fail'  # Mark as Fail in case of exception

# Save the updated DataFrame back to a new Excel file
df.to_excel(new_excel_file_path, index=False)

# Close the driver after the loop is done
driver.quit()
