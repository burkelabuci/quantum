

# main .py

from operations import square_number
import time
from datetime import datetime
import os

def create_date_folder(base_path):
    # Get today's date in the desired format
    today_date = datetime.now().strftime("%m%d%y")
    
    # Create the full path for the folder
    folder_path = os.path.join(base_path, today_date)
    
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Dear user, folder created: {folder_path}")
    else:
        print(f"Dear user, folder already exists: {folder_path}, your data will be saved here")
    
    return folder_path

def generate_unique_filename(base_folder):
    # Ensure base_folder exists, create if it doesn't
    os.makedirs(base_folder, exist_ok=True)
    
    # Get current date
    now = datetime.now()
    month = now.strftime('%m')  # Month as 2 digits (e.g., 06)
    day = now.strftime('%d')    # Day as 2 digits (e.g., 17)
    year = now.strftime('%y')   # Year as 2 digits (e.g., 24)
    
    # Find existing files in base_folder
    existing_files = os.listdir(base_folder)
    
    # Initialize file_number
    file_number = 1
    
    # Iterate through existing files to find the next available file_number
    while True:
        filename = f"{month}{day}{year}{file_number:04d}"
        if f"{filename}.csv" not in existing_files:
            break
        file_number += 1
    
    # Return the filepath with the next available file_number
    filepath = os.path.join(base_folder, f"{filename}.csv")
    
    return filepath

def main():
    # Prompt the user to enter a number with a default value of 3
    input_value = input("Please enter a number (default is 3): ")
    
    # Use the default value if the user does not enter anything
    if not input_value:
        number = 3
    else:
        try:
            number = float(input_value)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return
    
    # Confirm the entered value
    confirm = input(f"You entered {number}. Is this correct? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Input not confirmed. Exiting program.")
        return
    
    # Call the function from module.py
    result = square_number(number)
    
    # Print the result
    print(f"The square of {number} is {result}")

if __name__ == "__main__":
    main()
