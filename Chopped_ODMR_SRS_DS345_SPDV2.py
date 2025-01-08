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
import nidaqmx
from nidaqmx.constants import AcquisitionType, CountDirection, Edge
import pyvisa


#Parameters for the microwave:
start_frequency = 2400 #in MHz
stop_frequency = 3200 #in MHz

step_size = int(1) # specing between each frequency point in MHz
step_time = int(300) #in milliseconds
loopAmount= stop_frequency-start_frequency #how many points to sweep
plotname = create_folder_and_generate_filename_csv()# Generate unique filename with name mm/dd/yy (eg. 070324)

#arrays that will be used for plot
frequencies= []

freq_num= [i * 1e6 for i in range(start_frequency, stop_frequency, step_size)]
print(f"Unique filename: {plotname}")


print("\n \t \t Qubit initialization Process; ODMR Single Plot \n \n")

print("\t \t Initializing Systems \n \n")

#______________________________________________________________________________________________________________
#__________________________________________initialize the USB-6453 DAQ Counter__________________________________

#______________________________________________________________________________________________________________

#Microwave VCO initialization
synth = SynthHD("COM3")
print("\t \t Set Parameters \n \n")


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


number_of_elements = len(freq_num)
print("Number of elements in frequencies:", number_of_elements)
time_to_complete_seconds=number_of_elements*step_time*1e-3
completion_time = current_time + timedelta(seconds=time_to_complete_seconds)
print("Estimated completion time:", completion_time.strftime("%Y-%m-%d %H:%M:%S"))
print("Starting collecting")


#define intensity array
intensities= []


synth.write("sweep_single",True)
print("Actual sweep once true")

with nidaqmx.Task() as task:
    channel = task.ci_channels.add_ci_count_edges_chan(
        "Dev1/ctr0",
        edge=Edge.RISING,
        initial_count=0,
        count_direction=CountDirection.COUNT_UP,
    )
    channel.ci_count_edges_term = "/Dev1/PFI8"

    print("Continuously polling. Press Ctrl+C to stop.")
    task.start()
    
#loop over and read the signal from the Labjack T7 and append the value to the intensity array
    j=0
    while True:
        try:
            edge_counts = 0
            current_frequency = synth.read("frequency")
            edge_counts = task.read()
            print(j,current_frequency,edge_counts)
            frequencies.append(current_frequency*1e3)
            intensities.append(edge_counts)
            time.sleep(0.3)
            if loopAmount != "infinite":
                j=j+1
            if j>= loopAmount:
                break
        except KeyboardInterrupt:
            pass
        finally:
            task.stop()


#save the data ie, frequency and intensity as a csv file
saved_dict= {
    "frequencies (Hz)": frequencies,
    "Photon counts (pc)": intensities
}

df= pd.DataFrame(saved_dict)
csv_filepath = plotname  # using plotname as the CSV filename
df.to_csv(csv_filepath, sep=",")  # save CSV without index






print(f'Data file has been saved to {plotname}')

print(f'Lockin parameters have been saved to {plotname}')


# Plot and save figure
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.plot(frequencies, intensities, color='blue', marker='o', linestyle='-', label='ODMR Data Line')
plt.title('Single photon counts vs RF Frequency')
plt.xlabel("Microwave Frequency (Hz)")
plt.ylabel("photon counts(pc)")

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