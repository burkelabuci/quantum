# Program name Chopped_ODMR_SRS_DS345 v5.py

# 7/8/2024
# Author Minghao
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.


# This code sweep the microwave frequency from start_frequency to stop_frequency
# then extract the voltage reading from Labjack T7, , then plot frequencies (HZ) vs Labjack Voltage (v)
#This new program implement the higher level programs in main.py. Basically, it inputs start/stop frequencies of the microwave, time constant of the lock-in analyzer,
#and converts into proper step time in ms of the microwave.  In addition, the  microwave is programmed to warm up for 10 seconds before sweeping frequencies,
# and to return to start frequency after making the plot.


#___________________________________________________________________ 

#import libraries
import threading
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
import time
from datetime import datetime
import os
from main import *
from SR830lockin_settings_achieve import query_lockin_parameters, write_parameters_to_file
from Burkelab_Filenaming import create_folder_and_generate_filename_lockin,create_folder_and_generate_filename_csv
import pyvisa
#__________________________________________________________________________

lockin_parameters_text_name = create_folder_and_generate_filename_lockin()  # Generate unique filename with name SR830_lockinmmddyy


plotname = create_folder_and_generate_filename_csv()# Generate unique filename with name mm/dd/yy (eg. 070324)

#_____________________________________________________________________

#Parameters for the microwave:
#the program will ask if defult start and stop frequecies will be used

default_startfrequency = 2500 
default_stopfrequency = 3200
start_frequency,stop_frequency = default_freq(default_startfrequency,default_stopfrequency)
loopAmount= stop_frequency-start_frequency #how many points to sweep
step_size = int(1) # specing between each frequency point in MHz

#_____________________________________________________________________________

#parameters for the lock_in analyzer to adjust the step time of the microwave in milliseconds

default_slope = 24 #default slope in db/Octave
default_tau_lockin = 30 #defult lock_in time constant in milliseconds_
rf_step_time = wait_time(default_slope,default_tau_lockin) #input microwave step time in milliseconds


#_______________________________________________________________________________

#arrays that will be used for plot
frequencies= []

time.sleep(1) #wait for 1 second

print(f"Data file successully created: {plotname}")

time.sleep(1) #wait for 1 second

print("\n \t \t Qubit initialization Process; ODMR Single Plot \n \n")

time.sleep(1) #wait for 1 second

print("\t \t Initializing Systems \n \n")

#____________________________________________________________________________
#connect to GPIB
os.add_dll_directory("C:/Program Files/Keysight/IO Libraries Suite/bin")
os.add_dll_directory("C:/Program Files (x86)/Keysight/IO Libraries Suite/bin")
rm = pyvisa.ResourceManager("C:/Windows/System32/visa32.dll")

#connect the GPIB with the PC
lockin = rm.open_resource('GPIB0::8::INSTR')

# Query the Lock-In parameters
parameters = query_lockin_parameters()

# Write the settings to the text file
write_parameters_to_file(lockin_parameters_text_name, parameters)
#______________________________________________________________________



#Microwave VCO initialization
synth = SynthHD("COM3")
print("\t \t Set Parameters \n \n")

# Define the frequency array in Hz
frequencies = np.arange(start_frequency, stop_frequency, step_size) * 1e6

synth.write("sweep_freq_low", start_frequency)

print("Starting sweeping")


synth.write("sweep_freq_high",stop_frequency)
print("Frequency high set")

synth.write("sweep_freq_step",step_size)
print("Frequency step set")

synth.write("sweep_time_step", rf_step_time)
print("Frequency time set")

# Warm up the microwave for 30 seconds
print("Warming up the microwave for 10 seconds...")
time.sleep(10)

print("Warm-up complete. Starting sweep...")


#define intensity array
intensities= []

# Microwave sweep function
def microwave_sweep():
    # Sweep once the microwave frequencies
    synth.write("sweep_single", True)
    print("Microwave sweep started")


#_____________________________________________________________________________________________


#loop over and read the signal from the Labjack T7 and append the value to the intensity array
read_steptime= rf_step_time/1000

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
#______________________________________________________________________
#save the data ie, frequency and intensity as a csv file
saved_dict= {
    "frequencies (Hz)": frequencies,
    "Lockin Reading (A)": intensities
}

df= pd.DataFrame(saved_dict)
csv_filepath = plotname  # using plotname as the CSV filename
df.to_csv(csv_filepath, sep=",")  # save CSV without index

# Get the lock-in parameters and prepare them for adding to the DataFrame
parameters = write_parameters_to_file(plotname, parameters)

#_________________________________________________________________________
# Plot and save figure
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.scatter(frequencies, intensities,color='blue', marker='o', label='ODMR Data Points')
plt.title('Lockin Reading  vs RF Frequency')
plt.xlabel("Microwave Frequency (Hz)")
plt.ylabel("lockin reading (A)")

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