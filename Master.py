import CommonFunctions as cf 
from CommonFunctions import Click_Goal_Setting
from CommonFunctions import login
from CommonFunctions import click_submit_button
import KPIADD as ak 
from KPIADD import add_kpi
from KPIEDIT import Kpi_Edit
from KPIDELETE import Kpi_Delete
from KPIActionADD import Kpi_Action
from KPICommentsADD import Kpi_Comments
from AddComments import add_comments
from EditKPIAction import EditKPIAction
from DeleteKPIAction import DeleteKPIAction
from EditKPIComments import EditKPIComments
from DeleteKPIComments import DeleteKPIComments
from EditComments import EditComments
from DeleteComments import DeleteComments
import time
import os
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import numpy as np
import math
from selenium.common.exceptions import TimeoutException
from CommonFunctions import logout

# Dictionary to map sheet names to functions
action_map = {
    'AddKPI': add_kpi,
    'EditKPI': Kpi_Edit,
    'DeleteKPI': Kpi_Delete,
    'AddKPIAction': Kpi_Action,
    'AddKPIComments': Kpi_Comments,
    'AddComments': add_comments,
    'EditKPIAction': EditKPIAction,
    'DeleteKPIAction': DeleteKPIAction,
    'EditKPIComments': EditKPIComments,
    'DeleteKPIComments': DeleteKPIComments,
    'EditComments' : EditComments,
    'DeleteComments' : DeleteComments
}

# Function to execute sequences dynamically
def sequences(sheet_name, row, index, status_df, driver, wait):
    df = status_df.get(sheet_name)
    
    if sheet_name in action_map:
        action_map[sheet_name](row, index, wait, driver, status_df, df)
    else:
        print(f"No action performed for {sheet_name}")


# Load the Excel file and initialize status_df
def processSheets(excel_file_path, new_excel_file_path, url):
    driver = cf.InitializeChromeDriver()
    wait = WebDriverWait(driver, 20)
    # excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
    status_df = pd.read_excel(excel_file_path, sheet_name=None, dtype=str)

    # Process each row in the 'Login' sheet
    login_df = status_df['Login']
    current_username = None

    for index, row in login_df.iterrows():
        username = row['username']
        password = row['password']
        employee = row['employee']
        action = str(row['Action'])
        
        # Login logic
        if current_username != username:
            if current_username:
                logout(wait)
            login(driver, username, password, row, url)
            current_username = username
            # driver = cf.InitializeChromeDriver
            # Navigate to Goal Setting page
            Click_Goal_Setting(driver, wait)  
            
        # Call the appropriate sequence function based on the action column
        if action and action in action_map:
            sequences(action, row, index, status_df, driver, wait)

    # Write all sheets to a new Excel file
    # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # new_excel_file_path = f"C:\\Users\\Circular\\Desktop\\test_data_updated{timestamp}.xlsx"
    # Dictionary to store updated sheets
    updated_sheets = {}

    # Loop through each sheet in status_df
    for sheet_name, df in status_df.items():
        # Condition to check for updates (Modify based on your column names)
        if 'Status' in df.columns and df['Status'].notna().any():  # Example: If 'Status' column has non-null values
            updated_sheets[sheet_name] = df

    # Write only the updated sheets to the new Excel file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"Test_data_status{timestamp}.xlsx"
    if updated_sheets:  # Ensure there's something to write
        error_file_path = os.path.join(new_excel_file_path, filename)
        with pd.ExcelWriter(error_file_path, engine='xlsxwriter') as writer:
            for sheet_name, df in updated_sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    driver.quit()
    return error_file_path
    print(f"Updated Excel saved at: {error_file_path}")
    

