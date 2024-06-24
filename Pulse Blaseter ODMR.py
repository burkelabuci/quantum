# Program name Pulse Blaster ODMR.py
# 6/17/2024
# Author Minghao
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.


# This code use the pulse blaster instead of the signal generator to modulate the LDC 202C laser diode controller with frequency f
# sweep the microwave frequency from start_frequency to stop_frequency
# then extract the voltage reading from Labjack T7, , then plot frequencies (MHZ) vs Labjack Voltage (v)
#for the schemetic, refrence to page 47 of Minghao's lab Log book.


#import libraries
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
from pulsestreamer import PulseStreamer
import time


#Parameters:

#for the microwave
start_frequency = 2800 #in MHz 
stop_frequency = 3000 #in MHz  
step_size = int(1)
step_time = int(10) #in milliseconds
loopAmount= stop_frequency- start_frequency

#for the pulse streamer 8/2
f = 1000 # in Hz
tau = 1/f # in seconds
tau_ns = tau*1E9 # in nanoseconds
PB_IPADDRESS= '169.254.8.2' #ip address of the pulse streamer 8/2
ch = 1 #channel used for pulse blaster default digital output


#Define the name of data
plotname= str(input("Enter the name of the data following BurkeLab Rules MMDDYYNNN(example names: 0617240001 do not use special characters or spaces)"))


print("\n \t \t Qubit initialization Process; ODMR Single Plot \n \n")

print("\t \t Initializing Systems \n \n")

print("\t \t Pulse Blaster is on \n \n")


# Create Pulse Streamer object by entering the IP address of the hardware
ps = PulseStreamer(PB_IPADDRESS)


# Create sequence object 
seq = ps.createSequence()

# Set channel 0 as refrence (pulse duration in nanoseconds)
seq.setDigital(ch, [(tau_ns, 1), (tau_ns, 0)])


#stream the sequence
ps.stream(seq) # 10,000 reps = 2*tau_ref *10,000 seconds = 300 seconds = 5 mins

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
for i in range(start_frequency, stop_frequency, step_size):
    frequencies.append(i)

synth.write("sweep_freq_low", start_frequency)

print("Starting sweeping")


synth.write("sweep_freq_high",stop_frequency)
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




saved_dict= {
    "frequencies": frequencies,
    "Labjack voltage": intensities
}


df= pd.DataFrame(saved_dict)
df.to_csv(str("C:\\Users\\BurkeLab\\Desktop\\NV-center\\10xAverageplots\\"+plotname + ".csv"), "\t")

plottitle= str("C:\\Users\\BurkeLab\\Desktop\\NV-center\\10xAverageplots\\"+ plotname)


plt.plot(frequencies, intensities)
plt.xlabel("Microwave Frequency (MHz)")
plt.ylabel("Labjack Voltage (V)")

plt.savefig(plottitle)
plt.show()


ps.forceFinal()