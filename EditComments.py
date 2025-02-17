from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from CommonFunctions import Click_Goal_Setting

def EditComments(row, index, wait, driver, status_df, df):
    username = row['username']
    employee = row['employee']
    if username != employee:
        print("Fill the goal setting form of own")
        subordinate_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@icon, 'pi-envelope')]")))
        subordinate_button.click()
        table_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@id='pn_id_162-table']/tbody/tr")))
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
                driver.execute_script("arguments[0].click();", eye_button)
    elif username == employee:    
        print("Manager's Account")
        print("Select the employee name and perform the Action")
    
    try:
        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'EditComments'
        df1 = df    
        matching_kpi_rows = df1[
        (df1['Username'] == username) &
        (df1['Employee'] == employee)
        ] 
        if 'status' not in df.columns:
            df1['status'] = None
        # kpi_row = df1.iloc[index]
        if matching_kpi_rows.empty:
            print(f"No matching KPI rows found for Username: {username}, Employee: {employee}")
            return
        print(f"Found {len(matching_kpi_rows)} matching KPI rows for Username: {username}, Employee: {employee}")

        for idx, kpi_row in matching_kpi_rows.iterrows():
            try:
                table = driver.find_element(By.ID, "pn_id_45-table")
                driver.execute_script("arguments[0].scrollIntoView(true);", table)
                rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@id='commentsTable']/tbody/tr")))
                # driver.execute_script("arguments[0].scrollIntoView(true);", rows)
                e_comment = str(kpi_row['e-Comment']).strip()
                e_name = str(kpi_row['e-Name']).strip()
                # Convert Excel date to match the table format
                e_date_raw = kpi_row['e-Date']
                if isinstance(e_date_raw, pd.Timestamp):  # If it's a pandas Timestamp
                    e_date = e_date_raw.strftime('%d-%b-%Y')  # Convert to "14-Feb-2025"
                else:  
                    # If it's a string, try to parse and reformat
                    e_date = datetime.strptime(str(e_date_raw), "%Y-%m-%d %H:%M:%S").strftime('%d-%b-%Y')
                print(f"Looking for: Comment='{e_comment}', Name='{e_name}', Date='{e_date}'") 
            # Iterate through the rows to find the correct KPI ID
                for row in rows:  # Loop through table rows
                    try:
                        # Extract table data
                        table_comment = row.find_element(By.XPATH, "./td[1]").text.strip()
                        table_name = row.find_element(By.XPATH, "./td[2]").text.strip().replace("pi-user", "").strip()
                        table_date = row.find_element(By.XPATH, "./td[3]").text.strip()

                        print(f"Found in table: Comment='{table_comment}', Name='{table_name}', Date='{table_date}'")
                        # Compare with Excel values
                        if table_comment == e_comment and table_name == e_name and table_date == e_date:
                            print("Match found! Clicking Edit button.")
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
                            time.sleep(0.5)
                            edit_button = row.find_element(By.XPATH, ".//button[contains(@icon, 'pi-pencil')]")
                            driver.execute_script("arguments[0].click();", edit_button)  # Use JS click
                            time.sleep(1)  # Wait for action
                           
                    except Exception as e:
                        print(f" {e}")
                    
            except Exception as e:
                print(f"Error processing KPI row: {e}")
                df1.loc[idx, 'status'] = 'Error during processing'   
                try:
                    # Wait for the toast message container to appear
                    toast_message_elements = wait.until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "p-toast-message-text"))
                    )

                    for toast in toast_message_elements:
                        # Extract the summary (type of message) and detail (message content)
                        toast_summary = toast.find_element(By.CLASS_NAME, "p-toast-summary").text
                        toast_detail = toast.find_element(By.CLASS_NAME, "p-toast-detail").text

                        # Check the type of message and print the corresponding detail
                        if "Warning" in toast_summary:
                            print(f"Warning Message: {toast_detail}")
                            df1.loc[index, 'status'] = toast_detail
                            print("clicking on exit button") 
                            exit_button_css = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                            )
                            exit_button_css.click()
                            print("Clicked on exit button") 
                            return 
                        elif "Success" in toast_summary:
                            print(f"Success Message: {toast_detail}")
                            df1.loc[index, 'status'] = toast_detail
                            print("clicking on exit button") 
                            exit_button_css = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                            )
                            exit_button_css.click()
                            print("Clicked on exit button") 
                            return 
                        else:
                            print(f"Other Message Type: {toast_summary} - Detail: {toast_detail}")
                            df1.loc[index, 'status'] = toast_detail
                            print("clicking on exit button") 
                            exit_button_css = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                            )
                            exit_button_css.click()
                            print("Clicked on exit button")
                            return
                    
                except Exception as e:
                    print(f"Exception {e}")      
    except Exception as e:
        print(f"Error: {e}")
        df1.loc[index, 'status'] = f" i don't know"

    finally :
        # Reflect changes in status_df
        status_df['EditComments'] = df
        return