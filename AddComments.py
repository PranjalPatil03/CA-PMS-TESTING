from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import CommonFunctions as cf
from CommonFunctions import Click_Goal_Setting

def add_comments(row, index, wait, status_df, df):
        try:
            excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
            sheet_name = 'AddKPIAction'
           # df2 = pd.read_excel(excel_file_path, sheet_name=sheet_name) 
           # kpi_row = df2.iloc[index]
            df1 = df 
            if 'status' not in df.columns:
                df1['status'] = None
            driver = cf.InitializeChromeDriver
            Click_Goal_Setting(driver, wait)
           
            kpi_row = df1.iloc[index]
            # Click on Add Comments
            try:
                add_comments_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Add Comments']"))
                )
                add_comments_button.click()
                time.sleep(1)  # Wait for comments section to load


                # Input Comments from Excel sheet
                comment_field = wait.until(
                    EC.presence_of_element_located((By.ID, 'comment'))
                )
                comment_value = str(kpi_row['Comments'])  # Assuming Comments column exists
                comment_field.send_keys(comment_value)
            

                # Click Save button
                save_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-button') and .//span[text()='Save']]"))
                )
                save_button.click()
            except Exception as e:
                 print(f" Unable to save the comment{e}")
            try:
                # Wait for the toast messages container to load
                toast_message_elements = wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "p-toast-message-text"))
                )
                print(toast_message_elements)
                # Iterate through each toast message
                for toast_element in toast_message_elements:
                    # Get the type of message (e.g., Warning or Success)
                    summary_element = toast_element.find_element(By.CLASS_NAME, "p-toast-summary")
                    message_type = summary_element.text.strip()

                    # Get the detailed message
                    detail_element = toast_element.find_element(By.CLASS_NAME, "p-toast-detail")
                    detail_message = detail_element.text.strip()
                if message_type == "Warning":
                    print(f"Warning: {detail_message}")
                    df1.loc[index, 'status'] = detail_message
                    # Wait for the Cancel button to be visible
                    cancel_button = wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//span[@class='p-button-label' and text()='Cancel']"))
                    )
                    # Click the Cancel button
                    cancel_button.click()
                    print("Cancel button clicked successfully.")
                elif message_type == "Success":
                    print(f"Success: {detail_message}")
                    df1.loc[index, 'status'] = detail_message
                else:
                    print(f"Unhandled message type: {message_type} with message: {detail_message}")
                    df1.loc[index, 'status'] = detail_message
                    # Wait for the Cancel button to be visible
                    cancel_button = wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//span[@class='p-button-label' and text()='Cancel']"))
                    )
                    # Click the Cancel button
                    cancel_button.click()
                    print("Cancel button clicked successfully.")

            except Exception as e:
                df1.loc[index, 'status'] = e
                print(f"An error occurred: {e}")

            #df1.loc[index, 'status'] = toast_message
        
            time.sleep(1) 

      
        
        except Exception as e:
              print(f"Error : {e}")
    

