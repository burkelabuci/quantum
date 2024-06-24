#061424 ramp.py
#Minghao
#This code sweep the microwave frequency from f1 to f2 then back down to f1 over and over again.
# The sweep time is given by tsweep

#tsweep = 100e-3 # sweep time in seconds
f1 = 2800 # start frequency in MHz
f2 = 3000 # stop frequency in MHz
step_size = int(float(1))# step size in MHz
step_time= int(1) #milliseconds

revised_steptime= step_time*1000


#import libraries
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
import time




def get_avg(intensities):
    avg = sum(intensities)/len(intensities)
    return avg 

def normalize(intensities):
    max_val = max(intensities)
    norm_vals = []
    for values in intensities:
        newval= values/max_val
        norm_vals.append(newval)
    return norm_vals
    
def average_arrays(arrs):
    nump_arrs= []
    for arrays in arrs:
        nump_arrs.append(np.array(arrays))
    
    avg= sum(nump_arrs)/ len(nump_arrs)
    return avg


print("\n \t \t Qubit initialization Process; ODMR Single Plot \n \n")

print("\t \t Initializing Systems \n \n")

 
handle = ljm.openS("ANY", "ANY")#ljm.openS("ANY", "ANY", "ANY")
#handle = ljm.openS("T4", "ANY", "ANY") 
names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]
aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
num_Frames= len(names)
ljm.eWriteNames(handle, num_Frames, names, aValues)
numFrames = 2
names = ["AIN0", "DAC0"]
intervalHandle = 1

#Microwave VCO initialization
synth = SynthHD("COM3")
print("\t \t Set Parameters \n \n")


#set start and stop frequencies in MHz




loopAmount= f2- f1

frequencies= []


for i in range(f1, f2, step_size):
    frequencies.append(i)

for j in range(0,1000):
    synth.write("power",10)
    synth.write("sweep_freq_low",f1)




    synth.write("sweep_freq_high",f2)


    synth.write("sweep_freq_step",step_size)


    synth.write("sweep_time_step", step_time)



    ljm.startInterval(intervalHandle, revised_steptime)

    synth.write("sweep_single",True)

    j=0
    while True:
        try:
            results = ljm.eReadNames(handle, numFrames, names)
        
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








