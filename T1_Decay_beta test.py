

# Program name T1_Decay.py
# 7/6/2024
# Author Minghao
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.
# 6/14/2024 Peter debugging Minghao's bug
# Deletes Initialization pulses for demo purposes

# This program creates Ch0 and Ch1 output waveform of Pulseblaster model 8/2 as Fig 3 of reference
# at IP address PB_IPADDRESS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from labjack import ljm
from pulsestreamer import PulseStreamer
import keyboard
import time 
import sys
from windfreak import SynthHD, synth_hd
from datetime import datetime
import os
import csv


from T1_Decay_Subroutines import *
from T1_Decay_parameters import *
from main import *
#___________________________________________________________

base_path = r"C:\Users\BurkeLab\Desktop" # Specify the path where you want to create a data folder

base_folder = create_date_folder(base_path) #create a folder with name mm/dd/yy (eg. 070324) where you want to save your data

filename = generate_unique_filename(base_folder)# Generate unique filename with name mm/dd/yy (eg. 070324)









#_____________________________________________________________
# Parameters
PB_IPADDRESS= '169.254.8.2'


default_tau_ref = 15e-3 # reference time in seconds ; default 15e-3
#tau_ref = 15e-3 # reference time in seconds ; default 15e-3
default_tau_i = 1e-6 # pulse time in seconds (initialize, readout) ; default 5e-6
default_tau_delay_start=0.1e-3 # beginning of loop
default_tau_delay_end= 5e-3 # beginning of loop
default_num_points=100 # of loop points
default_step_time = 0.3 # time in seconds between each data point

tau_ref,tau_i,tau_delay_start,tau_delay_end,step_time,num_points = T1_Decay_parameters(default_tau_ref,default_tau_i,default_tau_delay_start,default_tau_delay_end,default_step_time,default_num_points)

tau_ref_ns=tau_ref*1E9
tau_i_ns=tau_i*1E9


# Create Pulse Streamer object by entering the IP address of the hardware
#ps = PulseStreamer('169.254.8.2')
ps = PulseStreamer(PB_IPADDRESS)

#print("calling create_fig3_teachingpaper_pulse_sequence ")
#create_fig3_teachingpaper_pulse_sequence(tau_ref_ns,tau_i_ns,tau_delay_ns,ps) # call for 10 seconds
#print(" create_fig3_teachingpaper_pulse_sequence returned ")

#--------------------- INITIALIZE LABJACK-------------------------

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



#-------------------------------------------------------------


# Calculate the step size
step_size = (tau_delay_end - tau_delay_start) / (num_points - 1)

# Initialize the loop
tau_delays = [tau_delay_start + i * step_size for i in range(num_points)]


# Initialize the data array
pairs = []

# Define column names
columns = ['tau delay', 'labjack reading']

# Loop through the calculated tau_delays
for tau in tau_delays:
    # Your code here
    print(f"calling create_fig3_teachingpaper_pulse_sequence with tau_delay= ,{tau*1e3} ms")
    create_fig3_teachingpaper_pulse_sequence(tau_ref_ns,tau_i_ns,tau/1e-9,ps)
    time.sleep(step_time)  # Delay for time_between_points seconds
    # read and print labjack voltage:
    try:
        results = ljm.eReadNames(handle, numFrames, names)
        print("labjack voltage reading =",abs(results[0]))
    except KeyboardInterrupt:
        break
    except Exception:
        print(sys.exc_info()[1])
        break
    pairs.append((tau,abs(results[0])))  # Append the tuple to the list


print(pairs)  # Print the list of tuples


# Open the file in 'w' mode with newline='' to prevent extra newline characters
with open(filename, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)   
# Write each pair (i, i^2) as a row in the CSV file
    for pair in pairs:
        csvwriter.writerow(pair)

# Create a DataFrame
df = pd.DataFrame(pairs, columns=columns)


# Save DataFrame to CSV
df.to_csv(filename,sep="\t")
time.sleep(1)
print(f'T1_Decay data successfully saved to {filename}')

# Plotting
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.scatter(df['tau delay'], df['labjack reading'], color='blue', marker='o', label='Data Points')
plt.title('Labjack Reading  vs Tau Delay')
plt.xlabel('Tau Delay')
plt.ylabel('Labjack Reading')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()














