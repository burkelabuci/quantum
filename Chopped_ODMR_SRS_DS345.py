# Program name Chopped_ODMR_SRS_DS345.py

# 6/27/2024
# Author Minghao
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.


# This code sweep the microwave frequency from start_frequency to stop_frequency
# then extract the voltage reading from Labjack T7, , then plot frequencies (HZ) vs Labjack Voltage (v)
# Compared with the program named Signal Generator ODMR V2, this program will plot the frequencies in Hz instead of MHz

 

#import libraries
import threading
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
from datetime import datetime, timedelta
import time
from datetime import datetime
import os
from main import *
from SR830lockin_settings_achieve import query_lockin_parameters, write_parameters_to_file
from Burkelab_Filenaming import create_folder_and_generate_filename_lockin,create_folder_and_generate_filename_csv
import pyvisa
#____________________________________________________________________________________________________________________________________________________
lockin_parameters_text_name = create_folder_and_generate_filename_lockin()  # Generate unique filename with name SR830_lockinmmddyy


plotname = create_folder_and_generate_filename_csv()# Generate unique filename with name mm/dd/yy (eg. 070324)

#___________________________________________________________________________________________________________________________________________________________
#Parameters for the microwave:
start_frequency = 2400   #in MHz
stop_frequency = 3200 #in MHz

step_size = int(1) # specing between each frequency point in MHz
step_time = int(300) #in milliseconds
loopAmount= stop_frequency-start_frequency #how many points to sweep


#arrays that will be used for plot
frequencies= []



print("\n \t \t Qubit initialization Process; ODMR Single Plot \n \n")

print("\t \t Initializing Systems \n \n")

#______________________________________________________________________________________________________________
#connect to GPIB
os.add_dll_directory("C:/Program Files/Keysight/IO Libraries Suite/bin")
os.add_dll_directory("C:/Program Files (x86)/Keysight/IO Libraries Suite/bin")
rm = pyvisa.ResourceManager("C:/Windows/System32/visa32.dll")

#connect the GPIB with the PC
lockin = rm.open_resource('GPIB0::8::INSTR')
#_____________________________________________________________________________________________________

print("GPIB connected, querying lockin parameters")
# Query the Lock-In parameters
parameters = query_lockin_parameters()


#____________________________________________________________________________________________________
#Microwave VCO initialization
synth = SynthHD("COM3")
print("\t \t Set microwave Parameters \n \n")

# Define the frequency array in Hz
frequencies = [i * 1e6 for i in range(start_frequency, stop_frequency, step_size)]

synth.write("sweep_freq_low", start_frequency)

print("Starting sweeping")


synth.write("sweep_freq_high",stop_frequency)
print("Frequency high set")

synth.write("sweep_freq_step",step_size)
print("Frequency step set")

synth.write("sweep_time_step", step_time)
print("Frequency time set")

# Get the current time
current_time = datetime.now()
print("Current time:", current_time.strftime("%Y-%m-%d %H:%M:%S"))


number_of_elements = len(frequencies)
print("Number of elements in frequencies:", number_of_elements)
time_to_complete_seconds=number_of_elements*step_time*1e-3
completion_time = current_time + timedelta(seconds=time_to_complete_seconds)
print("Estimated completion time:", completion_time.strftime("%Y-%m-%d %H:%M:%S"))
print("Starting collecting")



#define intensity array
intensities= []

# Microwave sweep function
def microwave_sweep():
    # Sweep once the microwave frequencies
    synth.write("sweep_single", True)
    print("Microwave single sweep started")

#loop over and read the signal from the Labjack T7 and append the value to the intensity array
read_steptime= step_time/1000

def read_lockin_display():
    j = 0
    while True:
        try:
            # Query the CH1 display value from the Lock-In Amplifier
            ch1_display_value = lockin.query('OUTR? 1').strip()
            
            # Convert the display value to a float and append to intensities
            intensities.append(float(ch1_display_value))
            
            time.sleep(read_steptime)
            
            # Check if the loop should terminate
            if loopAmount != "infinite":
                j += 1
                if j >= loopAmount:
                    break
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            break
# Create threads
microwave_thread = threading.Thread(target=microwave_sweep)
lockin_thread = threading.Thread(target=read_lockin_display)

# Start threads
microwave_thread.start()
lockin_thread.start()

# Wait for both threads to complete
microwave_thread.join()
lockin_thread.join()


#save the data ie, frequency and intensity as a csv file
saved_dict= {
    "frequencies (Hz)": frequencies,
    "Lockin reading (A)": intensities
}

df= pd.DataFrame(saved_dict)
csv_filepath = plotname  # using plotname as the CSV filename
df.to_csv(csv_filepath, sep="\t")  # save CSV without index

print(f'Data file has been saved to {plotname}')

# Write the settings to the text file
write_parameters_to_file(lockin_parameters_text_name, parameters)

print(f'Lockin parameters have been saved to {lockin_parameters_text_name}')

# Return the microwave to the start frequency
print("Returning microwave to the start frequency...")
synth.write("frequency",start_frequency)
print("Microwave frequency reset complete.")

# Plot and save figure
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.plot(frequencies, intensities, color='blue', marker='o', linestyle='-', label='ODMR Data Line')
plt.title('Lockin Reading vs RF Frequency')
plt.xlabel("Microwave Frequency (Hz)")
plt.ylabel("Lockin Reading (A)")

# Display the plot
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
