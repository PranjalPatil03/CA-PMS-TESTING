from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import math
from math import isnan 
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import CommonFunctions
from CommonFunctions import Click_Goal_Setting



def EditKPIAction(row, index, wait, driver, status_df, df):
    try:
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


        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'EditKPIAction'
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
        time.sleep(2)
        for idx, kpi_row in matching_kpi_rows.iterrows():
            print("Entering Edit KPI Function")
            kpi_id_text = None
            if pd.notna(kpi_row['KPI ID']):  # Check if KPI ID column is not empty
                kpi_id_text = str(int(float(kpi_row['KPI ID']))).strip()  # Convert KPI ID to consistent format
                print(f"Looking for KPI ID: {kpi_id_text}")
            else:
                print(f"KPI ID is empty for row, now we have to click on KPI Action by it Aspect Objective and KPI.")
            rows = WebDriverWait(driver,20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table[@role='table' and contains(@class, 'p-datatable-table')]/tbody/tr"))
            )
            kpi_found = False
            # Loop through the rows to find the one with 5952 in the 3rd column
            for row in rows:
                try:
                    if kpi_id_text:
                        third_column = row.find_element(By.XPATH, "./td[3]")
                        third_column_value = third_column.text
                        print(third_column_value)
                        if third_column_value == kpi_id_text:
                            print(f"KPI ID {kpi_id_text} found")
                            # Once the correct row is found, locate the button in the 9th column and click it
                            action_button = row.find_element(By.XPATH, "./td[9]/button/span[1]")
                            action_button.click()
                            time.sleep(1)
                            print("Clicked on Action_button")
                            kpi_found = True
                            break
                    else:
                        aspect_value = row.find_element(By.XPATH, ".//td[1]").text.strip()  # 1st column (Aspect)
                        objective_value = row.find_element(By.XPATH, ".//td[2]").text.strip()  # 2nd column (Objective)
                        table_kpi_id_value = row.find_element(By.XPATH, ".//td[4]").text.strip()  # 4th column (KPI ID)

                        expected_aspect = kpi_row['EAspect']
                        expected_objective = kpi_row['EObjective']
                        expected_kpi_id = str(kpi_row['EKPI']).strip()
                        if (aspect_value == expected_aspect and
                                objective_value == expected_objective and
                                table_kpi_id_value == expected_kpi_id):
                            print(f"Matched by Aspect, Objective, and KPI. Clicking KPI Action button.")
                            action_button = row.find_element(By.XPATH, "./td[9]/button/span[1]")
                            action_button.click()
                            time.sleep(1)
                            print("Clicked on Action_button")
                            break
                except Exception as e:
                    print(f"not able to find the column {e}")
            # if not kpi_found:
            #     print(f"No row found with KPI ID {kpi_id_text}. Exiting.")
            #     df1.loc[index, 'status'] = 'KPI not Found in the Table.'
            #     return
            # Excel date strings
            excel_action = kpi_row['e-Actions']
            excel_start_date = kpi_row['e-StartDate']
            excel_end_date = kpi_row['e-EndDate']

            print(f"Looking for matching row with values: Action = {excel_action}, StartDate = {excel_start_date}, EndDate = {excel_end_date}")
            # Locate the specific table using the id
            table = wait.until(
                EC.presence_of_element_located((By.ID, "kpiActionsTable"))
            )
            # Locate rows within the table
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            for row in rows:
                # Extract values from the table
                action_value = row.find_element(By.XPATH, "./td[1]").text.strip()
                print(f"{action_value}")
                start_date_value = row.find_element(By.XPATH, "./td[2]").text.strip()
                end_date_value = row.find_element(By.XPATH, "./td[3]").text.strip()
                print(f"{start_date_value} { end_date_value}")
                # Parse dates from Excel and table
                excel_start_date_parsed = datetime.strptime(str(excel_start_date), "%Y-%m-%d %H:%M:%S").date()
                excel_end_date_parsed = datetime.strptime(str(excel_end_date), "%Y-%m-%d %H:%M:%S").date()
                print(f" excel_start_date_prased{excel_start_date_parsed}, excel_end_date_parsed{excel_end_date_parsed}")
                try:
                    table_start_date_parsed = datetime.strptime(start_date_value, "%d-%m-%Y").date()
                    table_end_date_parsed = datetime.strptime(end_date_value, "%d-%m-%Y").date()
                except ValueError as e:
                    print(f"Error parsing table dates: {e}. Start Date: '{start_date_value}', End Date: '{end_date_value}'")
                    continue

                # Compare values
                if (
                    action_value == excel_action and

                    excel_start_date_parsed == table_start_date_parsed and
                    excel_end_date_parsed == table_end_date_parsed
                    ):
                    print("Matching row found.")                    
                    # Locate and click the Edit button in the last column
                    edit_button = row.find_element(By.XPATH, "./td[last()]//button[span[contains(@class, 'pi-pencil')]]")
                    edit_button.click()
                    try: 
                        # Fill the Action field
                        action_value = kpi_row['KPIAction']

                        # Check if the value is NaN and handle it
                        if pd.isna(action_value) or str(action_value).strip() == '':
                            print("Action field is empty in the sheet. Skipping input or setting a default value.")
                            action_value = ''  # Set a default value or skip input
                        else:
                            action_value = str(action_value).strip()

                        action_input = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//input[@inputid='action']"))
                        )
                        action_input.clear()

                        if action_value:
                            action_input.send_keys(action_value)
                            print(f"Entered Action value: {action_value}")
                        else:
                            print("Action field left empty.")
                    except: 
                        print(" unable to fill the field")
                    # Fill the Status dropdown
                    try:
                        status_dropdown = wait.until(
                            EC.presence_of_element_located((By.ID, 'status'))  # Locate the Status dropdown
                        )
                        status_dropdown.click()
                        print("Clicked on status dropdown")
                        # Get the Status value from the Excel sheets
                        status_value = str(kpi_row['Status'])  # Fetch the status value from the sheet
                        # Locate and click the appropriate option in the dropdown
                        status_option = wait.until(
                            EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[@role='option']//span[text()='{status_value}']"))
                        )
                        status_option.click()
                        print(f"Status '{status_value}' selected")
                    except:
                        print(f"No data found for KPI ID {kpi_id_text} in Excel.")
                        
                    try: 
                        start_date_value = kpi_row['StartDate']
                        print(f"Type of start_date_value: {type(start_date_value)}")
                        print(f"start_date_value: {start_date_value}")
                        # If start_date_value is of type numpy.datetime64, convert it to string
                        if isinstance(start_date_value, (np.datetime64, datetime)):
                            start_date_value = str(start_date_value)
                        # Check the format and handle accordingly
                        if "T" in start_date_value or "00:00:00" in start_date_value:  # It's in ISO format
                            start_date_value = start_date_value.split(' ')[0]
                            start_date_value = datetime.strptime(start_date_value.split('T')[0], "%Y-%m-%d").strftime('%d-%m-%Y')
                        else:  # It's in 'DD-MM-YYYY' format
                            try:
                                start_date_value = datetime.strptime(start_date_value, "%d-%m-%Y").strftime('%d-%m-%Y')
                            except ValueError:
                                print("Date format is incorrect or not recognized.")

                        print(f"Type of start_date_value: {type(start_date_value)}")
                        print(f"Formatted Start Date: {start_date_value}")

                        # Fill the Start Date
                        start_date_input = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//input[@id='startDate']"))
                        )
                        start_date_input.click()
                        # Simulate Ctrl + A to select all text
                        start_date_input.send_keys(Keys.CONTROL, 'a')
                        # Simulate Backspace to delete the selected text
                        start_date_input.send_keys(Keys.BACKSPACE)
                        start_date_input.send_keys(start_date_value)
                        print(f"Filled Start Date with: {start_date_value}")
                    except : 
                        print(f"Unable to fill Start date")
                    try: 
                        end_date_value = kpi_row['EndDate']
                        # End Date processing if needed
                        print(f"Type of end_date_value: {type(end_date_value)}")
                        print(f"end_date_value: {end_date_value}")
                        # Filling end date value
                        if isinstance(end_date_value, (np.datetime64, datetime)):
                            end_date_value = str(end_date_value)
                        # Check the format and handle accordingly
                        if "T" in end_date_value or "00:00:00" in end_date_value:  # It's in ISO format
                            end_date_value = end_date_value.split(' ')[0]
                            end_date_value = datetime.strptime(end_date_value.split('T')[0], "%Y-%m-%d").strftime('%d-%m-%Y')
                        else:  # It's in 'DD-MM-YYYY' format
                            try:
                                end_date_value = datetime.strptime(end_date_value, "%d-%m-%Y").strftime('%d-%m-%Y')
                            except ValueError:
                                print("Date format is incorrect or not recognsized.")

                        print(f"Type of end_date_value: {type(end_date_value)}")
                        print(f"Formatted end Date: {end_date_value}")

                        # Fill the Start Date
                        end_date_input = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//input[@id='endDate']"))
                        )
                        end_date_input.click()
                        # Simulate Ctrl + A to select all text
                        end_date_input.send_keys(Keys.CONTROL, 'a')

                        # Simulate Backspace to delete the selected text
                        end_date_input.send_keys(Keys.BACKSPACE)
                        
                        end_date_input.send_keys(end_date_value)
                        print(f"Filled End Date with: {end_date_value}")
                    except Exception as e:
                        print(f" Unable to fill the End date {e}")
                    try:
                        # Fill the Comments field
                        comments_input = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//textarea[@id='comments']"))
                        )
                        comments_input.clear()
                        comments_input.send_keys(kpi_row['Comments'])
                    except Exception as e:
                        print(f" Unable to fill Comments Input {e}")            
                    try:
                        update_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@icon='pi pi-check']"))
                        )
                        update_button.click()
                        print("Clicked on the Update button.")
                    except Exception as e:
                        print(f"Unable to click on Update button: {e}")
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
                                 
                            elif "Success" in toast_summary:
                                print(f"Success Message: {toast_detail}")
                                df1.loc[index, 'status'] = toast_detail
                                print("clicking on exit button") 
                                exit_button_css = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                                )
                                exit_button_css.click()
                                print("Clicked on exit button") 
                                 
                            else:
                                print(f"Other Message Type: {toast_summary} - Detail: {toast_detail}")
                                df1.loc[index, 'status'] = toast_detail
                                print("clicking on exit button") 
                                exit_button_css = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                                )
                                exit_button_css.click()
                                print("Clicked on exit button")
                                    
                    except Exception as e:
                        try:
                            # Handle other types of error messages
                            generic_message = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'The Start Date cannot be greater than End Date')]"))
                            )
                            print(f"Error: {generic_message.text}")
                            df1.loc[index, 'status'] = generic_message
                            print("clicking on exit button") 
                            exit_button_css = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                            )
                            exit_button_css.click()
                            print("Clicked on exit button")  
                            
                        except Exception as inner_e:
                            print("No message detected or unable to locate message.")
                else:
                    print("No matching row found in the table.")
                    print("clicking on exit button") 
                    exit_button_css = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                    )
                    exit_button_css.click()
                    print("Clicked on exit button") 

        # If no matching row is found
        print("No matching row found in the table.")
        df1.loc[index, 'status'] = "No matching row found"
        print("clicking on exit button") 
        exit_button_css = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
        )
        exit_button_css.click()
        print("Clicked on exit button")  
        return

    except Exception as e:
        print(f"Exception{e}")
        df1.loc[index, 'status'] = "KPI ID Does not found in the table"

    finally:
        # Reflect changes in status_df
        status_df['EditKPIAction'] = df
        return
    
