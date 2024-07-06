# Program name Chopped_ODMR_SRS_DS345 v5.py

# 7/5/2024
# Author Minghao
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.


# This code sweep the microwave frequency from start_frequency to stop_frequency
# then extract the voltage reading from Labjack T7, , then plot frequencies (HZ) vs Labjack Voltage (v)


#___________________________________________________________________ 

#import libraries
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
from RF_frequency import *
from Lock_in import *
#__________________________________________________________________________

base_path = r"C:\Users\BurkeLab\Desktop" # Specify the path where you want to create a data folder

base_folder = create_date_folder(base_path) #create a folder with name mm/dd/yy (eg. 070324) where you want to save your data

plotname = generate_unique_filename(base_folder)# Generate unique filename with name mm/dd/yy (eg. 070324)

#_____________________________________________________________________

#Parameters for the microwave:
#the program will ask if defult start and stop frequecies will be used

default_startfrequency = 2800 
default_stopfrequency = 3000
start_frequency,stop_frequency = default_freq(default_startfrequency,default_stopfrequency)
loopAmount= stop_frequency-start_frequency #how many points to sweep
step_size = int(1) # specing between each frequency point in MHz

#_____________________________________________________________________________

#parameters for the lock_in analyzer to adjust the step time of the microwave in milliseconds

default_slope = 24 #default slope in db/Octave
default_tau_lockin = 30 #defult lock_in time constant in milliseconds_
rf_step_time = step_time(default_slope,default_tau_lockin) #input microwave step time in milliseconds


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

print("Starting collecting")


#define intensity array
intensities= []

#sweep once the microwave frequencies
#for sweep continuously:
#synth.write("sweep_cont",True)
synth.write("sweep_single",True)
print("Actual sweep once true")


#_____________________________________________________________________________________________


#loop over and read the signal from the Labjack T7 and append the value to the intensity array
revised_steptime= rf_step_time*1000
ljm.startInterval(intervalHandle, revised_steptime)
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


#______________________________________________________________________
#save the data ie, frequency and intensity as a csv file
saved_dict= {
    "frequencies (Hz)": frequencies,
    "Labjack voltage (V)": intensities
}

df= pd.DataFrame(saved_dict)
csv_filepath = plotname  # using plotname as the CSV filename
df.to_csv(csv_filepath, sep="\t")  # save CSV without index


#_________________________________________________________________________
# Plot and save figure
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.scatter(frequencies, intensities,color='blue', marker='o', label='Data Points')
plt.title('Labjack Reading  vs RF Frequency')
plt.xlabel("Microwave Frequency (Hz)")
plt.ylabel("labjack voltage (V)")

# Display the plot
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
