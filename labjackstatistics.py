# Program name labjackstatistics.py
# 7/11/2024
# Author Peter Burke
# This program measures the voltage from the labjack every t_wait seconds for num_readings times then saves to file.

 

#import libraries
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
import time


#***************************************************************************************
#Parameters:
t_wait =0.1 # wait time between points in seconds
num_readings=10 # total # of readings

t_each= 100 #milliseconds Minghao what is this ??????

#***************************************************************************************
# Create filename
#Define the name of data
plotname= str(input("Enter the name of the data following BurkeLab Rules MMDDYYNNN(example names: 0617240001 do not use special characters or spaces)"))



#***************************************************************************************
# Initialize labjack




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



lbj_steptime = t_each*1000 # labjack step time in microseconds
ljm.startInterval(intervalHandle, lbj_steptime)




#***************************************************************************************
# Read loop:

# Initialize a 2D array to store the reading number and callme return value
readings = []

# Call the function num_readings times with a wait time of t_wait between each call
for i in range(num_readings):

    # read labjack:
    reading_value = abs(ljm.eReadNames(handle, numFrames, names)[0])
    ljm.waitForNextInterval(intervalHandle)
    
    readings.append([i + 1, reading_value])  # Store reading number and callme return value
    time.sleep(t_wait)

# Print the readings
for reading in readings:
    print(f"Reading {reading[0]}: {reading[1]}")

# Optional: Convert the readings list to a numpy array for further processing
import numpy as np
readings_array = np.array(readings)
print(readings_array)


#***************************************************************************************



#***************************************************************************************
# Save to file


