import CommonFunctions as cf
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import selenium.common.exceptions
from datetime import datetime
from selenium.webdriver.common.keys import Keys

def add_kpi(row, row_index, wait, status_df, df):
    from CommonFunctions import Click_Goal_Setting
    excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
    sheet_name = 'AddKPI'
    # Load the sheet data into a DataFrame
    import pandas as pd
    from CommonFunctions import InitializeChromeDriver
    df1 = df
     # Instead of overwriting the entire 'status' column, ensure only the specific row is updated
    if 'status' not in df.columns:
        df1['status'] = None
    try:
        driver = cf.InitializeChromeDriver
        # Navigate to Goal Setting page
        Click_Goal_Setting(driver, wait)
        # Wait until 'Add KPI' button is clickable
        add_kpi_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Add KPI']")))
        add_kpi_button.click()
        print('clicked on add kpi')
       
        try:
        # Fill in the fields from the row data (Aspect, Objective, KPI, Weightage, Target, Target Date)           
            kpi_row = df1.iloc[row_index]
            try:
                aspect_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'aspect')))
                aspect_dropdown.click()
                print("clicked on Aspect dropdwon")
                aspect_value = str(kpi_row['Aspect'])
                aspect_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[@role='option']//span[text()='{aspect_value}']"))
                ) 
                aspect_option.click()
                print("Aspect selected")
               
            except Exception as e :
                print(f"exception {e}")
            try:
                # Fill Objective
                objective_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'objective')))
                objective_dropdown.click()
                print("clicked on Objective dropdwon")
               
                objective_value = str(kpi_row['Objective'])
                objective_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[@role='option']//span[text()='{objective_value}']"))
                )
                objective_option.click()
                print("object selected")
                
            except:
                print('unable to click on objevctive or objective is empty')
                objective_dropdown.click()

            # Fill KPI
            try:
                # free_text_input = driver.find_elements(By.XPATH, "//input[@placeholder='Enter Free Text Kpi']")
                # if free_text_input:
                #     free_text_kpi_button = wait.until(
                #         EC.element_to_be_clickable((By.XPATH, "//i[@class='pi pi-pencil cursor-pointer mt-2 text-sm']"))
                #     )
                #     free_text_kpi_button.click()
                #     print("Free text KPI button clicked")
                #     kpi_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'KPI')))
                #     kpi_dropdown.click()
                #     print("clicked on KPI dropdwon")
                    
                #     kpi_value = str(row['KPI'])
                #     # try:
                #     kpi_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[@role='option']//span[text()='{kpi_value}']"))
                #     )
                #     kpi_option.click()
                    
                # else:
                #     print("test")

                kpi_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'KPI')))
                kpi_dropdown.click()
                print("clicked on KPI dropdwon")
                
                kpi_value = str(kpi_row['KPI'])
                # try:
                kpi_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[@role='option']//span[text()='{kpi_value}']"))
                )
                kpi_option.click()
                
                print("KPI selected")
               
            except Exception as e:

                # If KPI is not found in the dropdown, enter it as free text
                print(f" KPI '{e}' not found in dropdown. Switching to free text entry.")
                kpi_dropdown.click()
                # Click the 'free text KPI' button (pencil icon)
                # free_text_kpi_button = wait.until(
                #     EC.element_to_be_clickable((By.XPATH, "//i[@class='pi pi-pencil cursor-pointer mt-2 text-sm']"))
                # )
                # free_text_kpi_button.click()
                # print("Free text KPI button clicked")
                # time.sleep(2)

                # # Find the text input field and input the KPI value from the Excel sheet
                # free_text_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
                # free_text_input.clear()
                # free_text_input.send_keys(kpi_value)
                # print(f"Entered KPI '{kpi_value}' as free text.")
                # time.sleep(2)
                # try:
                #     uom_value = str(kpi_row['UoM'])  # Get UoM value from the Excel sheet
                #     uom_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@id='uom']")))
                #     uom_dropdown.click()
                  
                    
                #     # Select the UoM from the dropdown list based on the value in the sheet
                #     uom_option = wait.until(
                #         EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[@role='option']//span[text()='{uom_value}']"))
                #     )
                #     uom_option.click()
                #     print(f"UoM '{uom_value}' selected from dropdown.")
                 

                # except Exception as e:
                #     print(f"UoM '{uom_value}' not found in dropdown.{e} Ensure it's present in the sheet.")

            try:
                weightage_field = wait.until(
                    EC.visibility_of_element_located((By.ID, "weightage"))
                )
                weightage_field.click()
                #weightage_field.clear()
                weightage_field.send_keys(int(kpi_row['Weightage']))
               
            except Exception as e:
                print(f"Unable to add weightage{e}")
            try:
                target_field = wait.until(
                    EC.visibility_of_element_located((By.ID, 'target'))
                )
                if target_field.is_enabled():
                    target_field.clear()
                    target_field.send_keys(str(kpi_row['Target']))
                    print("Target field filled.")
                else:
                    print("Target field is disabled, skipping.")
                time.sleep(1)
            except Exception as e:
                print(f"unable to add Target{e}")
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
                
                target_date_field.click()
                print("clicked on target date field")
                target_date_field.send_keys(Keys.CONTROL + "a")
                target_date_field.send_keys(Keys.BACK_SPACE)
                target_date_field.send_keys(formatted_date)
               
            except Exception as e:
                print(f"unable to add Target Date{e}")
            try:
                # Click Save button
                save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']")))
                save_button.click()
                print("clicked on Save button")


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
                        print(message_type)
                        # Get the detailed message
                        detail_element = toast_element.find_element(By.CLASS_NAME, "p-toast-detail")
                        detail_message = detail_element.text.strip()
                        print(detail_message)
                    if message_type == "Warning":
                        print(f"Warning: {detail_message}")
                        df1.loc[row_index, 'status'] = detail_message
                        try:
                            cancel_button = wait.until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(@icon, 'pi pi-times')]"))
                            )
                            cancel_button.click()
                            print("Clicked on cancel successfully")
                        
                        except Exception as e:
                            print(f"unable to click on cancel button{e}")
                    elif message_type == "Success" :
                        print(f"Success: {detail_message}")
                        df1.loc[row_index, 'status'] = detail_message
                    else:
                        df1.loc[row_index, 'status'] = detail_message
                        print(detail_message)
                        try:
                            cancel_button = wait.until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(@icon, 'pi pi-times')]"))
                            )
                            cancel_button.click()
                            print("Clicked on cancel successfully")
                        
                        except Exception as e:
                            print(f"unable to click on cancel button{e}")
                except Exception as e:
                    print(f"exception {e}")          
            except Exception as e:
                print(f"Unable to click on Save button{e}")
            #df1.loc[row_index, 'status'] = " p "

        except Exception as e:
            print({e})
            df.loc[row_index, 'status'] = f"Error: {str(e)}"
           
    except Exception as e:
        print(f"unable to click on Add KPI button {e}")
        df1.loc[row_index, 'status'] = "Unable to click on Add KPI Button"

    finally :
          # Reflect changes in status_df
        status_df['AddKPI'] = df
        return