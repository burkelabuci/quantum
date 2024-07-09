

# main .py
#these are the higher level programs to be used for NV- center ODMR experiment



#libraries
from operations import square_number
import time
from datetime import datetime
import os
#____________________________________________________________________________

#prorgams to ask for inputs
def get_user_input(prompt, default):
    user_input = input(f"{prompt} (default {default}): ")
    return int(user_input) if user_input else default

def get_confirmation(prompt):
    while True:
        confirmation = input(f"{prompt} (yes/no): ").strip().lower()
        if confirmation in ['yes', 'no']:
            return confirmation == 'yes'
        print("Please answer with 'yes' or 'no'.")
#_______________________________________________________________________


#programs to create a folder and generate the name of the file following Burke lab rule
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
#______________________________________________________________________________________

#program to confirm the start and stop microwave frequencies
def default_freq(f1,f2):
    default_start_frequency = f1
    default_stop_frequency = f2
    start_frequency = 0
    stop_frequency = 0
    
    use_defaults = get_confirmation("Do you want to use this frequency range (default as 2800MHz to 3000MHz)?")

    if use_defaults:
        start_frequency = default_start_frequency
        stop_frequency = default_stop_frequency
    else:
        # Get user inputs
        start_frequency = get_user_input("Enter the new start frequency in MHz", default_start_frequency)
        stop_frequency = get_user_input("Enter the new stop frequency in MHz", default_stop_frequency)


    print("\nSummary of your input:")
    time.sleep(1)
    print(f"start frequency: {start_frequency} MHz, stop frequency: {stop_frequency} MHz")
    time.sleep(1)
    print(f"loop amount: {stop_frequency-start_frequency} points")
    
    return start_frequency,stop_frequency
#_______________________________________________________________________

#program to confirm the time constant and slope of the lock-in analyzer and automatically convert to proper step time in ms of the microwave
def step_time(slope_per_octave,tau_lockin):
    default_slope = slope_per_octave
    default_tau_lockin = tau_lockin
    step_time = 0
    use_defaults = get_confirmation("Do you want to use the default slope/octave (24dB) and time average (30ms) for the lock-in analyzer?")
    if use_defaults:
        slope_set = default_slope
        tau_avg = default_tau_lockin
        step_time = 10*tau_avg
    else:
        slope_set = get_user_input("Enter the new slope/octave (dB)", default_slope)
        tau_avg = get_user_input("Enter the new time constant in milliseconds", default_tau_lockin)
        if slope_set == 6:
            step_time = 5*tau_avg
        elif slope_set == 12:
            step_time = 7*tau_avg
        elif slope_set == 18:
            step_time = 9*tau_avg
        elif slope_set == 24:
            step_time = 10*tau_avg
        else:
            raise ValueError("Unsupported slope per octave value. Supported values are 6, 12, 18 and 24.")
    
    time.sleep(1)

    print(f"your step time is: {step_time} ms")   
    return step_time
