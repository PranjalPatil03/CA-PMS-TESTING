from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from CommonFunctions import Click_Goal_Setting


def Kpi_Comments(row, index, wait, driver, status_df, df):
    try:
        excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
        sheet_name = 'AddKPIComments'
        #df2 = pd.read_excel(excel_file_path, sheet_name=sheet_name) 
        df1 = df 
        if 'status' not in df.columns:
                df1['status'] = None
        kpi_row = df1.iloc[index]
        KPI_IDS = str(kpi_row['KPI ID'])
        print("enter in try block")
        #kpi_ids_from_excel = KPI_IDS.split(",")
        print(KPI_IDS)
        KPI_IDS = KPI_IDS.split(",")
        # Convert to float first, then to int to handle decimal strings like '5979.0'
        kpi_id_text = str(int(float(kpi_row['KPI ID']))).strip()
        # Locate the table body rows
        print(kpi_id_text)
        time.sleep(2)
        print("Table found")

        Click_Goal_Setting(driver, wait)
        rows = WebDriverWait(driver,20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@role='table' and contains(@class, 'p-datatable-table')]/tbody/tr"))
        )
        kpi_found = False
        # Loop through the rows to find the one with KPI ID in the 3rd column
        for row in rows:
            third_column = row.find_element(By.XPATH, "./td[3]")
            third_column_value = third_column.text
            print(third_column_value)

            if third_column_value == kpi_id_text:
                print(f"KPI ID {kpi_id_text} found")
                # Once the correct row is found, locate the button in the 9th column and click it
                comment_button = row.find_element(By.XPATH, "./td[10]//span[@class='p-button-icon pi pi-comments']")
                comment_button.click()
                print("Clicked on comment button")
                kpi_found = True
                break
        if not kpi_found:
            print(f"No row found with KPI ID {kpi_id_text}. Exiting.")
            df1.loc[index, 'status'] = 'KPI not Found in the Table.'
            return
        try:
            # Click the "Add" button to add a new comment
            add_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Add']"))
            )
            add_button.click()
            print(f"Clicked on Add button")

            # Fill in the comment field with the comment value from the row
            comment_value = kpi_row['Comments']
            comment_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//textarea[@id='comment']"))
            )
            comment_field.clear()
            comment_field.send_keys(comment_value)
            print(f"Entered Comment {comment_value}")

            # Click the "Save" button to save the comment
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@label='Save']"))
            )
            save_button.click()
        except Exception as e:
            print(f"unable to save the comment{e}")

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

                # Print the message based on the type
                if message_type == "Warning":
                    print(f"Warning: {detail_message}")
                    df1.loc[index, 'status'] = detail_message
                    # Click Exit button (SVG element)
                    exit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                    )
                    exit_button.click()
                    print("Clicked on Exit button")
                elif message_type == "Success":
                    print(f"Success: {detail_message}")
                    df1.loc[index, 'status'] = detail_message
                    # Click Exit button (SVG element)
                    exit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                    )
                    exit_button.click()
                    print("Clicked on Exit button")
                else:
                    print(f"Unhandled message type: {message_type} with message: {detail_message}")
                    df1.loc[index, 'status'] = detail_message
                    # Click Exit button (SVG element)
                    exit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.p-dialog-header-close-icon.p-icon"))
                    )
                    exit_button.click()
                    print("Clicked on Exit button")

                
        except:
            df1.loc[index, 'status'] = e
            print("unable to click on close button")
            return
        time.sleep(2)
    except Exception as e:
        df1.loc[index, 'status'] = e
        print(f"Error : {e}")





