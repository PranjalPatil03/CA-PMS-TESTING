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



def DeleteKPIComments(row, index, wait, driver, status_df, df):
    try:
        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'DeleteKPIComments'
        df1 = df    
        if 'status' not in df.columns:
            df1['status'] = None
        kpi_row = df1.iloc[index]
        KPI_IDS = str(kpi_row['KPI ID'])
        print("enter in try block")
        print(KPI_IDS)
        KPI_IDS = KPI_IDS.split(",")
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
            third_column = row.find_element(By.XPATH, "./td[3]")
            third_column_value = third_column.text
            print(third_column_value)

            if third_column_value == kpi_id_text:
                print(f"KPI ID {kpi_id_text} found")
                # Once the correct row is found, locate the button in the 9th column and click it
                comment_button = row.find_element(By.XPATH, "./td[10]/button/span[1]")
                comment_button.click()
                time.sleep(1)
                print("Clicked on Comment_button")
                kpi_found = True
                break
        if not kpi_found:
            print(f"No row found with KPI ID {kpi_id_text}. Exiting.")
            df1.loc[index, 'status'] = 'KPI not Found in the Table.'
            return
        # Excel date strings
        excel_name = kpi_row['e-Name']
        excel_date = kpi_row['e-Date']
        excel_comment = kpi_row['e-Comment']

        print(f"Looking for matching row with values: Name = {excel_name}, Date = {excel_date}, Comment = {excel_comment}")
        # Wait for the comment list to load
        comment_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//app-comment-list"))
        )
        # Locate individual comment items within the list
        comments = comment_list.find_elements(By.XPATH, ".//div[contains(@class, 'comment-item')]")
       
        for comment in comments:
            # Extract values from the table
            name_value = comment.find_element(By.XPATH, ".//span[contains(@class, 'comment-author')]").text.strip()
            print(f"{name_value}")
            date_value = comment.find_element(By.XPATH, ".//span[contains(@class, 'comment-date')]").text.strip()
            comment_value = comment.find_element(By.XPATH, ".//div[contains(@class, 'comment-text')]").text.strip()
            print(f"{date_value} { comment_value}")
             # Parse dates from Excel and table
            excel_date_parsed = datetime.strptime(str(excel_date), "%Y-%m-%d %H:%M:%S").date()
            print(f" excel_start_date_prased{excel_date_parsed}")
            try:
                table_date_parsed = datetime.strptime(date_value, "%d-%b-%Y").date()
            except ValueError as e:
                print(f"Error parsing table dates: {e}. Start Date: '{date_value}'")
                

            # Compare values
            if (
                name_value == excel_name and

                excel_date_parsed == table_date_parsed and
                comment_value == excel_comment
            ):
                print("Matching row found.")

                try:
                    # Locate and click the Edit button in the last column
                    delete_button = comment.find_element(By.CSS_SELECTOR, ".pi-trash")
                    time.sleep(1)
                    delete_button.click()
                except Exception as e:
                    print(f"Unable to click on Delete Button {e}")
                try:
                    # Locate the checkicon element inside the button (if this is the "Yes" button)
                    yes_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Yes')]/parent::button"))
                    )
                    # Click on the button
                    yes_button.click()
                except Exception as e:
                    print(f" Unable to click on Yes button. {e}")            
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
                    print("clicking on exit button") 
                    exit_button_css = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                    )
                    exit_button_css.click()
                    print("Clicked on exit button")
                    return
        # If no matching row is found
        print("No matching row found in the table.")
        df1.loc[index, 'status'] = "Provided comment is not found in comments"
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