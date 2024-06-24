# Program name resonance heat.py
# 6/19/2024
# Author Minghao
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.


# This code initiate the microwave at frequency of f1
# and then switch to the frequency of f2
# then extract 2 data points of voltage reading from Labjack T7,  then plot data point index vs Labjack Voltage (v)
#for the schemetic, refrence to page 47 of Minghao's lab Log book.
 

#import libraries
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
import time


#Parameters for the microwave:
f1 = 2870 #in MHz
f2 = 3100 #in MHz
step_size = f2-f1
step_time = int(1000) #in milliseconds
loopAmount= 2

#arrays that will be used for plot
frequencies= []

#Define the name of data
plotname= str(input("Enter the name of the data following BurkeLab Rules MMDDYYNNN(example names: 0617240001 do not use special characters or spaces)"))



print("\n \t \t Qubit initialization Process; ODMR Single Plot \n \n")

print("\t \t Initializing Systems \n \n")

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

#define the frequency array
frequencies= []
for i in range(f1, f2+1, step_size):
    frequencies.append(i)

synth.write("sweep_freq_low", f1)

print("Starting sweeping")


synth.write("sweep_freq_high",f2)
print("Frequency high set")

synth.write("sweep_freq_step",step_size)
print("Frequency step set")

synth.write("sweep_time_step", step_time)
print("Frequency time set")

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
    "frequencies": frequencies,
    "Labjack voltage": intensities
}

df= pd.DataFrame(saved_dict)
df.to_csv(str("C:\\Users\\BurkeLab\\Desktop\\NV-center\\10xAverageplots\\"+plotname + ".csv"), "\t")


#make a plot and save it
plottitle= str("C:\\Users\\BurkeLab\\Desktop\\NV-center\\10xAverageplots\\"+ plotname)


plt.plot(frequencies, intensities,"o")
plt.xlabel("Microwave Frequency (MHz)")
plt.ylabel("Labjack Voltage (V)")

plt.savefig(plottitle)
plt.show()