from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from CommonFunctions import Click_Goal_Setting

def Kpi_Delete(row, index, wait, driver, status_df, df):
    
    try:
        
        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'DeleteKPI'
        df1 = df    
        if 'status' not in df.columns:
            df1['status'] = None
        kpi_row = df1.iloc[index]
        print("Entering Edit KPI Function")
        KPI_ID = str(kpi_row['KPI ID'])
        KPI_ID = KPI_ID.split(",")
        Click_Goal_Setting(driver, wait)
        for kpi_id in KPI_ID:
            kpi_id_text = str(int(float(kpi_id))).strip()  # Convert KPI ID to consistent format
            print(f"Looking for KPI ID: {kpi_id_text}")
            
            # Locate the table kpi_rows
            rows = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//table[@role='table' and contains(@class, 'p-datatable-table')]/tbody/tr")
                )
            )
            
            # Iterate through the rows to find the correct KPI ID
            for row in rows:
                kpi_column_value = row.find_element(By.XPATH, "./td[3]").text.strip()  # Assuming KPI ID is in column 3
                print(f"Found KPI ID in row: {kpi_column_value}")
                
                if kpi_column_value == kpi_id_text:
                    print(f"KPI ID {kpi_id_text} matched. Clicking Delete button.")
                    
                    # Wait until the Delete button is clickable
                    delete_button = row.find_element(By.XPATH, "./td[12]//button[contains(@icon, 'pi-trash')]")
                    # Ensure the button is clickable
                    wait.until(EC.element_to_be_clickable(delete_button))
                    # Click the Delete button
                    delete_button.click()
                    print("Clicked on the Delete button.")
                    
                    # Optionally handle confirmation popup if needed
                    confirm_button = row.find_element(By.XPATH, "//p-confirmdialog//button[2]")
                    wait.until(EC.element_to_be_clickable(confirm_button))
                    confirm_button.click()
                    print("Confirmed the deletion.")
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
            
        df1.loc[index, 'status'] = f"KPI ID {kpi_id_text} not found in the table."
        print(f"KPI ID {kpi_id_text} not found in the table.")
        return
    except Exception as e:
        print(f"Error: {e}")
        df1.loc[index, 'status'] = f"KPI ID {kpi_id_text} not found in the table."