from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import CommonFunctions as cf
def add_comments(row, row_index, wait, driver, status_df, df):
    username = row['username']
    employee = row['employee']
    if username != employee:
        print("Fill the goal setting form of own")
        subordinate_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@icon, 'pi-envelope')]")))
        subordinate_button.click()
        table_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@id='pn_id_160-table']/tbody/tr")))
        for row in table_rows:
            try:
                employee_id = row.find_element(By.XPATH, "./td[3]").text.strip()
                if not employee_id:
                    employee_id = row.find_element(By.XPATH, "./td[3]").get_attribute("textContent").strip()
                    print(f" {employee_id}")
                if not employee_id:
                    employee_id = driver.execute_script("return arguments[0].innerText;", row.find_element(By.XPATH, "./td[3]")).strip()
                    print(f"{employee_id}")
            except Exception as e:
                print(f"Error fetching Employee ID: {e}")
            if employee_id == employee:
                print("matching row found") 
                eye_button = row.find_element(By.XPATH, "./td[7]/button")
                print("Displayed:", eye_button.is_displayed())
                print("Enabled:", eye_button.is_enabled())
                #eye_button = row.find_element(By.XPATH, "./td[7]//button[contains(@class, 'pi-eye')]")
                #eye_button.click()
                # eye_button = row.find_element(By.XPATH, "./td[last()]/button")
                # driver.execute_script("arguments[0].scrollIntoView(true);", eye_button)
                # # Use JavaScript click as fallback
                # driver.execute_script("arguments[0].click();", eye_button)
                driver.execute_script("arguments[0].click();", eye_button)
    else:
        print("Manager's Account")
        print("Select the employee name and perform the Action")


    try:
        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'AddComments'
        df1 = df
        matching_kpi_rows = df1[
            (df1['Username'] == username) &
            (df1['Employee'] == employee)
            
        ]
        if 'status' not in df.columns:
            df1['status'] = None
        if matching_kpi_rows.empty:
            print(f"No matching KPI rows found for Username: {username}, Employee: {employee}")
            return

        print(f"Found {len(matching_kpi_rows)} matching KPI rows for Username: {username}, Employee: {employee}")
                # Click on Add Comments
        try:
            for idx, kpi_row in matching_kpi_rows.iterrows():
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
                        time.sleep(3)
                    if message_type == "Warning":
                        print(f"Warning: {detail_message}")
                        df1.loc[idx, 'status'] = detail_message
                        # Wait for the Cancel button to be visible
                        cancel_button = wait.until(
                            EC.visibility_of_element_located((By.XPATH, "//span[@class='p-button-label' and text()='Cancel']"))
                        )
                        # Click the Cancel button
                        cancel_button.click()
                        print("Cancel button clicked successfully.")
                    elif message_type == "Success":
                        print(f"Success: {detail_message}")
                        df1.loc[idx, 'status'] = detail_message
                    else:
                        print(f"Unhandled message type: {message_type} with message: {detail_message}")
                        df1.loc[idx, 'status'] = detail_message
                        # Wait for the Cancel button to be visible
                        cancel_button = wait.until(
                            EC.visibility_of_element_located((By.XPATH, "//span[@class='p-button-label' and text()='Cancel']"))
                        )
                        # Click the Cancel button
                        cancel_button.click()
                        print("Cancel button clicked successfully.")

                except Exception as e:
                    df1.loc[idx, 'status'] = e
                    print(f"An error occurred: {e}")
        except Exception as e:
                print(f" Unable to save the comment{e}")
       

        #df1.loc[index, 'status'] = toast_message
    
        time.sleep(1)
                
    except Exception as e:
        print(f"Error : {e}")
    finally :
        # Reflect changes in status_df
        status_df['AddComments'] = df
        return


