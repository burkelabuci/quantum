# Program name Burkelab_Filenaming.py
# 7/29/2024
# Author Minghao Jiang


#This program is a subroutine that automatically generates a folder on a default path, and save the file following the Burkelab policy (mm/dd/yy xxxxx)


import os
from datetime import datetime


default_path = r"C:\Users\BurkeLab\Desktop"
def create_folder_and_generate_filename(base_path=default_path):
    # Get today's date in mmddyy format
    today_date = datetime.now().strftime("%m%d%y")
    
    # Construct the folder path
    folder_path = os.path.join(base_path, today_date)
    
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Find existing files in folder_path
    existing_files = os.listdir(folder_path)
    
    # Get current date components
    now = datetime.now()
    month = now.strftime('%m')  # Month as 2 digits (e.g., 06)
    day = now.strftime('%d')    # Day as 2 digits (e.g., 17)
    year = now.strftime('%y')   # Year as 2 digits (e.g., 24)
    
    # Initialize file_number
    file_number = 1
    
    # Iterate through existing files to find the next available file_number
    while True:
        filename = f"{month}{day}{year}{file_number:04d}.csv"
        if filename not in existing_files:
            break
        file_number += 1
    
    # Return the full path of the next available filename
    filepath = os.path.join(folder_path, filename)
    print(f"Dear user, data will be saved in: {filepath}")
    return filepath