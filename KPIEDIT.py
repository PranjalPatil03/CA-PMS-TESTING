from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from CommonFunctions import Click_Goal_Setting

def Kpi_Edit(row, index, wait, driver, status_df, df):
    
    try:
        
        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'EditKPI'
        df1 = df 
        if 'status' not in df.columns:
            df1['status'] = None
        kpi_row = df1.iloc[index]
        print("Entering Edit KPI Function")
        KPI_ID = str(kpi_row['KPI ID'])
        KPI_ID = KPI_ID.split(",")
        Click_Goal_Setting(driver, wait)
       # for kpi_id in KPI_ID:
        kpi_id_text = str(int(float(kpi_row['KPI ID']))).strip()  # Convert KPI ID to consistent format
        print(f"Looking for KPI ID: {kpi_id_text}")
        
        # Locate the table kpi_rows
        rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@role='table' and contains(@class, 'p-datatable-table')]/tbody/tr"))
        )
        kpi_found = False   
        # Iterate through the rows to find the correct KPI ID
        for row in rows:
            kpi_column_value = row.find_element(By.XPATH, "./td[3]").text.strip()  # Assuming KPI ID is in column 3
            print(f"Found KPI ID in row: {kpi_column_value}")
            
            if kpi_column_value == kpi_id_text:
                print(f"KPI ID {kpi_id_text} matched. Clicking Edit button.")
                
                # Locate and click the Edit button in column 12
                edit_button = WebDriverWait(row, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "./td[12]//span[@class='p-button-icon pi pi-pencil']"))
                )
                edit_button.click()
                print("Clicked on Edit button.")
                kpi_found = True
                break
        if not kpi_found :
            print(f"No row found with KPI ID {kpi_id_text}. Exiting.")
            df1.loc[index, 'status'] = 'KPI not Found in the Table.' 
            return     
        try:
            uom_value = str(kpi_row['UoM'])  # Get UoM value from the Excel sheet
            uom_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@id='uom']")))
            uom_dropdown.click()
            time.sleep(2)
            uom_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[@role='option']//span[text()='{uom_value}']"))
            )
            uom_option.click()
            print(f"UoM '{uom_value}' selected from dropdown.")
            time.sleep(2)

        except:
            print(f"UoM not found in dropdown. Ensure it's present in the sheet.")

        try:
            weightage_field = wait.until(
                EC.visibility_of_element_located((By.ID, 'weightage'))
            )
            weightage_field.click()
            weightage_field.clear()
            weightage_field.send_keys(Keys.CONTROL + "a")
            weightage_field.send_keys(Keys.BACK_SPACE)
            print(kpi_row['Weightage'])
            weightage_field.send_keys(int(kpi_row['Weightage']))
        except:
            print("Weightage field is enable")
        try:
            target_field = wait.until(
                EC.visibility_of_element_located((By.ID, 'target'))
            )
            if target_field.is_enabled():
                target_field.clear()
                target_value = kpi_row['Target']
                # target_field.send_keys(str(int(float(target_value))))
                target_field.send_keys(int(kpi_row['Target']))
                print("Target field filled.")
            else:
                print("Target field is disabled, skipping.")
            time.sleep(1)
        except Exception as e:
            print(f"Target{e}")
            print("target field filled 01")
        try:
            target_date_field = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox']"))
            )
            print("target date field found")
            target_date_value = kpi_row['Target Date']
                
                # Handle the unconverted data error
            target_date_str = str(target_date_value).split(' ')[0]  # Remove the time part if it exists only date part will show
            formatted_date = datetime.strptime(target_date_str, '%Y-%m-%d').strftime('%d-%m-%Y')
            print("convert date format")
            time.sleep(1)
            target_date_field.click()
            print("clicked on target date field")
            target_date_field.send_keys(Keys.CONTROL + "a")
            target_date_field.send_keys(Keys.BACK_SPACE)
            target_date_field.send_keys(formatted_date)
        except:
            print("target date field is not present")
        # Wait for the Update button to appear and click it
        update_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Update')]"))
        )
        update_button.click()
        print("Clicked on Update button.")
        time.sleep(2)  # Small delay before proceeding to the next KPI ID 
        try:
            # Wait for the toast message container to appear
            toast_message_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "p-toast-message-text"))
            )
            # Extract the summary (type of message) and detail (message content)
            toast_summary = toast_message_element.find_element(By.CLASS_NAME, "p-toast-summary").text
            toast_detail = toast_message_element.find_element(By.CLASS_NAME, "p-toast-detail").text
            print(f"{toast_summary} {toast_detail}")
            # Print the appropriate message based on the summary
            if "Warning" in toast_summary:
                print(f"Warning: {toast_detail}")
                df1.loc[index, 'status'] = toast_detail
                cancel_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-button-outlined') and span[contains(@class, 'pi pi-times')]]"))
                )
                cancel_button.click()
                print("Cancel button clicked successfully.")
            elif "Success" in toast_summary:
                print(f"Success: {toast_detail}")
                df1.loc[index, 'status'] = toast_detail
            else:
                print(f"Other message: {toast_summary} - {toast_detail}")
                df1.loc[index, 'status'] = toast_detail
                cancel_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-button-outlined') and span[contains(@class, 'pi pi-times')]]"))
                )
                cancel_button.click()
                print("Cancel button clicked successfully.")
        except Exception as e:
            print(f"Error while checking toast message: {e}")
        # break  # Move to the next KPI ID once Edit and Update are completed
                
        # else:
        #     print(f"KPI ID {kpi_id_text} not found in the table.")
        #     # df1.loc[index, 'status'] = f"KPI ID {kpi_id_text} not found in the table."

    except Exception as e:
        print(f"Error: {e}")