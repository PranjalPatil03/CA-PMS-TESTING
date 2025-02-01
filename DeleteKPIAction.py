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



def DeleteKPIAction(row, index, wait, driver, status_df, df):
    try:
        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'AddKPIAction'
        df1 = df    
        if 'status' not in df.columns:
            df1['status'] = None
        kpi_row = df1.iloc[index]
        KPI_IDS = str(kpi_row['KPI ID'])
        print("enter in try block")
        #kpi_ids_from_excel = KPI_IDS.split(",")
        print(KPI_IDS)
        KPI_IDS = KPI_IDS.split(",")
    #     print(f"Error while clicking on button: {e}")  
        #for kpi_id in KPI_IDS:
             # Convert to float first, then to int to handle decimal strings like '5979.0'
        kpi_id_text = str(int(float(kpi_row['KPI ID']))).strip()
    # Locate the table body rows
        print(kpi_id_text)
        time.sleep(2)

        print("Table found")
        # time.sleep(4)
        # rows = table.find_elements(By.TAG_NAME, "tr")
        # print(f"Number of rows found: {len(rows)}")
        Click_Goal_Setting(driver, wait)
        rows = WebDriverWait(driver,20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@role='table' and contains(@class, 'p-datatable-table')]/tbody/tr"))
        )
        #  print(rows)
        kpi_found = False
        # Loop through the rows to find the one with 5952 in the 3rd column
        for row in rows:
            try:
                third_column = row.find_element(By.XPATH, "./td[3]")
                third_column_value = third_column.text
                print(third_column_value)

                if third_column_value == kpi_id_text:
                    print(f"KPI ID {kpi_id_text} found")
                    # Once the correct row is found, locate the button in the 9th column and click it
                    action_button = row.find_element(By.XPATH, "./td[9]/button/span[1]")
                    action_button.click()
                    print("Clicked on Action_button")
                    kpi_found = True
                    break
            except Exception as e:
                print(f"Exception{e}")
                
        if not kpi_found:
            print(f"No row found with KPI ID {kpi_id_text}. Exiting.")
            df1.loc[index, 'status'] = 'KPI not Found in the Table.'
            return
        # Excel date strings
        excel_action = kpi_row['e-Actions']
        excel_start_date = kpi_row['e-StartDate']
        excel_end_date = kpi_row['e-EndDate']

        print(f"Looking for matching row with values: Action = {excel_action}, StartDate = {excel_start_date}, EndDate = {excel_end_date}")
        # Locate the specific table using the id
        table = wait.until(
            EC.presence_of_element_located((By.ID,"kpiActionsTable"))
        )
        # print(f"{table} is the table........................................................")
        # Locate rows within the table
        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        print(rows)
    
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
              
                try:
                    # Wait for the delete button to be present
                    delete_button = row.find_element(By.XPATH, "./td[6]//button[contains(@icon, 'pi pi-trash')]")
                    # Click the delete button
                    delete_button.click()
                    print("Delete button clicked.")
                except Exception as e:  
                    print(f"Exception{e}")
                try:
                    # Use XPath to locate the parent button containing <checkicon>
                    yes_button = driver.find_element(By.XPATH, "//checkicon[contains(@class, 'p-element')]/parent::button")

                    # Click the 'Yes' button
                    yes_button.click()

                    print("Successfully clicked on the 'Yes' button.")
                except Exception as e:
                    print(f"An error occurred, while clicking on yes button: {e}")
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
                    print(f"Unable to capture Toast message {e}")

           
        print("Action, StartDate, EndDate Does not matched with excel column")
        df1.loc[index, 'status'] = "Action, StartDate, EndDate Does not matched with excel column"
        print("clicking on exit button") 
        exit_button_css = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
        )
        exit_button_css.click()
        print("Clicked on exit button")
        return
    except Exception as e:
        print(f"Exception {e}")           