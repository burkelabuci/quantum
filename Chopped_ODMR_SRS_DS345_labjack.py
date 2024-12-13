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


#Parameters for the microwave:
start_frequency = 2820 #in MHz
stop_frequency = 2920 #in MHz

step_size = int(1) # specing between each frequency point in MHz
step_time = int(3000) #in milliseconds
loopAmount= stop_frequency-start_frequency #how many points to sweep
plotname = create_folder_and_generate_filename_csv()# Generate unique filename with name mm/dd/yy (eg. 070324)

#arrays that will be used for plot
frequencies= []


print(f"Unique filename: {plotname}")


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
print("\t \tGPIB connected, querying lockin parameters\n \n")
# Query the Lock-In parameters
parameters = query_lockin_parameters()

#open the labjack 
#For Labjack T7 instruction for communication with python, see https://support.labjack.com/docs/python-for-ljm-windows-mac-linux
handle = ljm.openS("ANY", "ANY")
 

#AIN#_NEGATIVE_CH: Specifies the negative channel to be used for each positive channel. 199=Default=> Single-Ended.
#AIN#_RANGE: The range/span of each analog input. Write the highest expected input voltage. For T7, the default is -10V to 10V
#AIN#_RESOLUTION_INDEX: The resolution index for command-response and AIN-EF readings. A larger resolution index generally results in lower noise and longer sample times.
#Default value of 0 corresponds to an index of 8 (T7) 
#AIN#_SETTLING_US: Settling time for command-response and AIN-EF readings. For T-7: Auto. Max is 50000 (microseconds).

names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]

#Default values
aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
num_Frames= len(names)

ljm.eWriteNames(handle, num_Frames, names, aValues)


numFrames = 2
names = ["AIN0", "DAC0"]

intervalHandle = 1



#Microwave VCO initialization
synth = SynthHD("COM3")
print("\t \t Set Parameters \n \n")

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

synth.write("sweep_single", True)
print("Microwave single sweep started")

# Get the current time
current_time = datetime.now()
print("Current time:", current_time.strftime("%Y-%m-%d %H:%M:%S"))


number_of_elements = len(frequencies)
print("Number of elements in frequencies:", number_of_elements)
time_to_complete_seconds=number_of_elements*step_time*1e-3
completion_time = current_time + timedelta(seconds=time_to_complete_seconds)
print("Estimated completion time:", completion_time.strftime("%Y-%m-%d %H:%M:%S"))
print("Starting collecting")

revised_steptime= step_time*1000
ljm.startInterval(intervalHandle, revised_steptime)


#define intensity array
intensities= []

#sweep once the microwave frequencies
#for sweep continuously:
#synth.write("sweep_cont",True)
synth.write("sweep_single",True)
print("Actual sweep once true")

#loop over and read the signal from the Labjack T7 and append the value to the intensity array
j=0
while True:
    try:
        results = ljm.eReadNames(handle, numFrames, names)
        intensities.append(abs(results[0]))
        ljm.waitForNextInterval(intervalHandle)
        if loopAmount != "infinite":
            j=j+1
            if j>= loopAmount:
                break
    except KeyboardInterrupt:
        break
    except Exception:
        print(sys.exc_info()[1])
        break



#save the data ie, frequency and intensity as a csv file
saved_dict= {
    "frequencies (Hz)": frequencies,
    "Labjack voltage (V)": intensities
}

df= pd.DataFrame(saved_dict)
csv_filepath = plotname  # using plotname as the CSV filename
df.to_csv(csv_filepath, sep=",")  # save CSV without index

# Get the lock-in parameters and prepare them for adding to the DataFrame
parameters = write_parameters_to_file(plotname, parameters)

# Convert parameters dictionary to DataFrame
params_df = pd.DataFrame([parameters])

# Concatenate the DataFrame with parameters DataFrame horizontally
df_with_params = pd.concat([df, params_df], axis=1)

# Save the combined DataFrame to CSV
df_with_params.to_csv(csv_filepath , sep=",")  # save CSV with index

print(f'Data file has been saved to {plotname}')

print(f'Lockin parameters have been saved to {plotname}')


# Plot and save figure
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.plot(frequencies, intensities, color='blue', marker='o', linestyle='-', label='ODMR Data Line')
plt.title('Lockin Reading vs RF Frequency')
plt.xlabel("Microwave Frequency (Hz)")
plt.ylabel("Labjack Reading (V)")

# Display the plot
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()

# Return the microwave to the start frequency
print("Returning microwave to the start frequency...")
synth.write("frequency",start_frequency)
print("Microwave frequency reset complete.")