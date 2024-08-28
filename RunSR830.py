# Program name RunSR830.py
# 8/26/2024
# Author Minghao Jiang
#This Python script queries and logs settings from an SR830 DSP Lock-In Amplifier. It:

#1. Initializes the GPIB connection.
#2. Generates a unique filename for the settings file.
#3. Retrieves Lock-In parameters (e.g., sensitivity, time constant).
#4. Writes these parameters to a text file.
#5. Queries and prints the CH1 display value.

#_________________________________________________________________________________________________
from SR830lockin_settings_achieve import query_lockin_parameters, write_parameters_to_file

from Burkelab_Filenaming import create_folder_and_generate_filename_lockin

import os
from datetime import datetime
import pyvisa
#__________________________________________________________________________________________________

#connect to GPIB
os.add_dll_directory("C:/Program Files/Keysight/IO Libraries Suite/bin")
os.add_dll_directory("C:/Program Files (x86)/Keysight/IO Libraries Suite/bin")
rm = pyvisa.ResourceManager("C:/Windows/System32/visa32.dll")

#connect the GPIB with the PC
lockin = rm.open_resource('GPIB0::8::INSTR')
#___________________________________________________________________________________________________


lockin_parameters_text_name = create_folder_and_generate_filename_lockin()  # Generate unique filename with name SR830_lockinmmddyy

# Query the Lock-In parameters
parameters = query_lockin_parameters()

# Write the settings to the text file
write_parameters_to_file(lockin_parameters_text_name, parameters)

# Query the CH1 display value
ch1_display_value = lockin.query('OUTR? 1').strip()

# Print the result
print(f"CH1 Display Value: {ch1_display_value}")
