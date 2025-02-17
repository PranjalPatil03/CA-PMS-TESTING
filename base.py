import CommonFunctions as cf 
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
driver = cf.InitializeChromeDriver()
wait = WebDriverWait(driver, 20)
def sequences(sheet_name, row, index, status_df):
    df= status_df[sheet_name]

    if(sheet_name == 'AddKPI'):
        df = status_df[sheet_name]
        add_kpi(row, index, wait, status_df, df)
    elif(sheet_name == 'EditKPI'):
        df = status_df[sheet_name]
        Kpi_Edit(row, index, wait, driver, status_df, df)
    elif(sheet_name == 'DeleteKPI'):
        df = status_df[sheet_name]
        Kpi_Delete(row, index, wait, driver, status_df, df)
    elif(sheet_name == 'AddKPIAction'):
        df = status_df[sheet_name]
        Kpi_Action(row, index, wait, driver, status_df, df)
    elif(sheet_name == 'AddKPIComments'):
        df = status_df[sheet_name]
        Kpi_Comments(row, index, wait, driver, status_df, df)
    elif(sheet_name == 'AddComments'):
        df= status_df[sheet_name]
        add_comments(row, index, wait, status_df, df)
    elif(sheet_name == 'EditKPIAction'):
        df = status_df[sheet_name]
        EditKPIAction(row, index, wait, driver, status_df, df)
    elif(sheet_name == 'DeleteKPIAction'):
        df = status_df[sheet_name]
        DeleteKPIAction(row, index, wait, driver, status_df, df)
    elif(sheet_name == 'EditKPIComments'):
        df = status_df[sheet_name]
        EditKPIComments(row, index, wait, driver, status_df, df)
    elif(sheet_name == 'DeleteKPIComments'):
        df = status_df[sheet_name]
        DeleteKPIComments(row, index, wait, driver, status_df, df)
    else:
        print("No Action Performed")

# Load the Excel file and initialize status_df
excel_file_path = "C:\\Users\\Circular\\Desktop\\test_data_1.xlsx"
status_df = pd.read_excel(excel_file_path, sheet_name=None, dtype=str)

# Process each row in the 'Login' sheet
login_df = status_df['Login']
current_username = None

for index, row in login_df.iterrows():
    username = row['username']
    password = row['password']
    action = str(row['Action'])
    
    # Login logic
    if current_username != username:
        if current_username:
            logout(wait)
        login(driver, username, password, row)
        current_username = username   
    # Call the appropriate sequence
    sequences('DeleteKPIComments', row, index, status_df)

# Write all sheets to a new Excel file
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
new_excel_file_path = f"C:\\Users\\Circular\\Desktop\\test_data_updated{timestamp}.xlsx"
with pd.ExcelWriter(new_excel_file_path, engine='xlsxwriter') as writer:
    for sheet_name, df in status_df.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Updated Excel saved at: {new_excel_file_path}")
driver.quit()

