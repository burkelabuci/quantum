# Program name noise.py
# 6/19/2024
# Author Minghao
#This program is used to study noise

#testing
# test number 2
# test number 3

# This code sit the microwave frequency at sit_frequency
# then extract the 10000 data points of voltage reading from Labjack T7 in a time period of t_collect,  then plot data point index vs Labjack Voltage (units)
#for the schemetic, refrence to page 47 of Minghao's lab Log book.
 
#git test
#import libraries
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
import time


#Parameters:
sit_frequency = 2873 #in MHz
num = 300 #number of data points collected
t_each= 100 #milliseconds
t_collect = t_each * num # time used to collect data in seconds
# to do: Change the code. Use t_each, num as entry. Calculate t_collect=t_each * num.



#Define the name of data
plotname= str(input("Enter the name of the data following BurkeLab Rules MMDDYYNNN(example names: 0617240001 do not use special characters or spaces)"))

numlist = []

for i in range(1,num+1):
    numlist.append(i)


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


synth.write("frequency", sit_frequency)

print("microwave initiated")


print("Starting collecting")


lbj_steptime = t_each*1000 # labjack step time in microseconds
ljm.startInterval(intervalHandle, lbj_steptime)

#define intensity array
intensities= []
#loop over and read the signal from the Labjack T7 and append the value to the intensity array
j=0
while True:
    try:
        results = ljm.eReadNames(handle, numFrames, names)
        intensities.append(abs(results[0]))
        ljm.waitForNextInterval(intervalHandle)
        if j != "infinite":
            j=j+1
            if j>= num:
                break
    except KeyboardInterrupt:
        break
    except Exception:
        print(sys.exc_info()[1])
        break



#save the data ie, frequency and intensity as a csv file
saved_dict= {
    "data point index": numlist,
    "Labjack voltage": intensities
}

df= pd.DataFrame(saved_dict)
df.to_csv(str("C:\\Users\\BurkeLab\\Desktop\\NV-center\\062124\\"+plotname + ".csv"), "\t")


#make a plot and save it
plottitle= str("C:\\Users\\BurkeLab\\Desktop\\NV-center\\062124\\"+ plotname)


plt.plot(numlist, intensities)
plt.xlabel("data point index")
plt.ylabel("Labjack Voltage (mV)")

plt.savefig(plottitle)
plt.show()
