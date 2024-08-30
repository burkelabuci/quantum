# Program name T1_Decay.py
# 6/14/2024
# Author Minghao + Peter Burke
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.
# 6/14/2024 Peter debugging Minghao's bug
# Deletes Initialization pulses for demo purposes

# This program creates Ch0 and Ch1 output waveform of Pulseblaster model 8/2 as Fig 3 of reference
# at IP address PB_IPADDRESS

#----------------INSTRUCTIONS------------------------------------
#To generate Fig 3 of teaching paper:

#1. Set up optics to get ODMR to make sure everything is working right.
#2. Set up pulse blaster and photocurrent to lock in. The scale of lock in may need to be adjusted for T1.
#3. Run:
#T1_Decay_Synchronized.py

# This generates every single pulse and downloads it to the pulseblaser.
# The delay gets larger every number_of_cycles, so you vary the delay.
# But the sequence is one giant sequence precomputed.
#The parameters need to be adjusted as needed:

# fig_mode=3 for figure 3.
# tau_ref_ns=2.5e-3*1e9 # 15 ms fig 3, 2.5 ms fig 4.
# number_of_cycles=33 # default 33 for fig 3 33 hz; sets how long each pulse pattern is for a given delay; 200 for Fig 4
# Since the reference rate is 33 Hz, the pulseblaster will create 33 cycles for each delay, giving one second to take the data.
# If you want longer per delay point, increase 33 cycles. E.g. 330 Hz will give 10 seconds of time for each delay point.

# Uncomment one of these three:
#do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
#do_it_all_no_init(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
#do_it_all_different_init_and_readout_pulsewidth(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_readout_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
# Keep the Rabi lines commented out

# the no init creates a readout pulse with no initialization pulse, so should be independent of tdelay.
# in the teaching paper the init and readout pulse are both 5 microseconds, but you can have different readout pulse width if you want
#----------------INSTRUCTIONS------------------------------------
#To generate Fig 4b,c,d of teaching paper:

# This is just ODMR where the lockin output is measured as you step the frequency.
# The program Chopped_ODMR_SRS_DS345.py can be used to do this sweep.
# You just have to adjust the frequency range, step, and time per point.
# To set the pulsing sequence up as in Fig 4a, you need to download the correct pulse sequence into the pulseblaster and set it to run indefinitely.
# Do this with:
# callpulseblasterhelperfunctions.py
# That calls :
# create_fig4_teachingpaper_pulse_sequence(tau_ref_ns,tau_laser_ns,tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,ps)
# You have to input the parameters tau_ref_ns,tau_laser_ns,tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats
# Note there is a function version in T1_Decay_Subroutines.py called
# def chopped_odmr_srs_ds345(start_frequency=2670, stop_frequency=2690, step_size=1, step_time=1000, base_folder=r"C:\Users\BurkeLab\Desktop\072624"):
# It does not plot, just saves the file.

#----------------INSTRUCTIONS------------------------------------
#To generate Fig 4e of teaching paper: (Rabi oscillations)

#1. Set up optics to get ODMR to make sure everything is working right.
#2. Set up pulse blaster and photocurrent to lock in. The scale of lock in may need to be adjusted for T1.
#3. Run:
#T1_Decay_Synchronized.py

# This generates every single pulse and downloads it to the pulseblaser.
# But for each delay, it downloads a new pulse sequence. (Sadly the memory is too small to download the pulses for all delays)
#The parameters need to be adjusted as needed:

# fig_mode=4 for figure 4.
# tau_ref_ns=2.5e-3*1e9 # 15 ms fig 3, 2.5 ms fig 4.
# number_of_cycles=200 # default 33 for fig 3 33 hz; sets how long each pulse pattern is for a given delay; 200 for Fig 4
# Since the reference rate is 200 Hz, the pulseblaster will create 200 cycles for each delay, giving one second to take the data.
# If you want longer per delay point, increase 200 cycles. E.g. 2000 Hz will give 10 seconds of time for each delay point.

# Comment out :
#do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
#do_it_all_no_init(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
#do_it_all_different_init_and_readout_pulsewidth(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_readout_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
# (The Rabi function tried to download one giant sequence but it was too big for the pulseblaster brain to handle)

# Uncommment:
# sequences=rabi_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,number_of_cycles,ps)
# This generates a 1d array of sequences, each one for a different delay.



#----------------INSTRUCTIONS------------------------------------
#To generate Fig 5 of teaching paper: (Hahn echo)

# configure parameters below that pertain to fig 5
# fig_mode=5 for figure 5.
# uncomment  sequences=Hahn_many_sequences(...
# 
#----------------INSTRUCTIONS------------------------------------
#To generate Fig 6 of teaching paper: (CPMG )

# configure parameters below that pertain to fig 6
# fig_mode=6 for figure 6.
# uncomment  sequences=CPMG_many_sequences(...
# 

#---------------------------------------------------------------

import threading
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from labjack import ljm
from pulsestreamer import *
import keyboard
import time 
import sys
from windfreak import SynthHD, synth_hd
from datetime import datetime
import os
import csv
from main import *
from T1_Decay_Subroutines import *
from SR830lockin_settings_achieve import query_lockin_parameters, write_parameters_to_file
from Burkelab_Filenaming import create_folder_and_generate_filename_lockin,create_folder_and_generate_filename_csv
import pyvisa


lockin_parameters_text_name = create_folder_and_generate_filename_lockin()  # Generate unique filename with name SR830_lockinmmddyy


plotname = create_folder_and_generate_filename_csv()# Generate unique filename with name mm/dd/yy (eg. 070324)



#--------------------- PARAMETERS-------------------------

# for both fig 3 and fig 4 and fig 5 and 6
fig_mode=3 # 3 for figure 3 , 4 for figure 4, 5 for figure 5, 6 for figure 6
channel_number_ref=0
channel_number_pulse=1
channel_number_laser_pulse=1 # same thing as channel_number_pulse
channel_number_mw_pulse=2
channel_number_mw_phaseshifted_pulse=3

tau_ref_ns=15e-3*1e9 # 15 ms fig 3, 2.5 ms fig 4. and 5 and 6
number_of_cycles=33 # number of reference cycles for each data point
# default 33 for fig 3 33 hz; sets how long each pulse pattern is for a given delay; 200 for Fig 4, 5
# for fig 4 200 Hz default, so want 200 cycles if 1 second between each point
step_time=number_of_cycles*2*tau_ref_ns*1e-9 # in seconds, how long each data point has pulses going
step_time_microseconds=step_time*1e6

# Fig 3 only
tau_i_ns=5e-6*1e9 # laser initialization pulse width
#tau_readout_ns=tau_i_ns # laser readout pulse width
tau_readout_ns=5e-6*1e9 # laser readout pulse width
# Fig 3 will vary delay between laser init and laser readout pulse between delay_start_s and delay_stop_s and measure the LIA at each point.
delay_start_s=3e-3
delay_stop_s=0.01e-3
delay_number_of_points=100


# for Fig 4, 5, 6
tau_laser_ns=5e-6*1e9 # laser pulse width, fig 4, 5
n_repeats=200 # number of times pattern repeated within a cycle; suggest 200 fig 4, 100 fig 5
rabi_and_hahn_delay_s=2 # delay after setting new microwave pulse time to reading LIA output; can be 2 seconds for fig 4

# Fig 4 only:
tau_padding_ns=1e-6*1e9 # not used for now
tau_padding_before_mw_ns=1000e-9*1e9 # time between end of laser pulse and start of mw pulse (fig 4)
tau_padding_after_mw_ns=1000e-9*1e9 # time between end of mw pulse and start of laser pulse (fig 4)
tau_mw_ns=5e-6*1e9 # not used
# Fig 4 will vary mw pulse length from mw_pulse_length_start_ns to mw_pulse_length_stop_ns and measure LIA at each point
mw_pulse_length_start_ns=10e-9*1e9
mw_pulse_length_stop_ns=250e-9*1e9
mw_pulse_length_number_of_points=100

# Fig 5, 6 only:
tau_mw_X_pi_over_2_ns=50e-9*1e9 # pi/2 pulse X length (fig 5)
tau_mw_X_pi_ns=2*tau_mw_X_pi_over_2_ns # pi pulse X length (fig 5)
tau_mw_Y_pi_ns=tau_mw_X_pi_ns # pi/2 pulse Y length (fig 5)
tau_padding_before_mw_pi_over_2_ns=1000e-9*1e9 # time between end of laser pulse and start of first mw X pi/2 pulse (fig 5)
tau_padding_after_mw_pi_over_2_ns=1000e-9*1e9 # time between end  of second mw X pi/2 pulse and start of next laser pulse (fig 5)
# Fig 5,6 will vary T_delay between mw_T_delay_length_start_ns and mw_T_delay_length_stop_ns and measure LIA at each point
mw_T_delay_length_start_ns=100e-9*1e9
mw_T_delay_length_stop_ns=500e-9*1e9
mw_T_delay_length_number_of_points=3
mw_T_delay_delay_s=2 # delay after setting new microwave pulse time to reading LIA output

# Fig 6 only:
N_CPMG=4 # number of CPMG refocusing pulses

#--------------------- INITIALIZE PULSEBLASTER-------------------------
PB_IPADDRESS= '169.254.8.2'

ps = PulseStreamer(PB_IPADDRESS)


#ps.setTrigger(TriggerStart.SOFTWARE)


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


ljm.startInterval(intervalHandle, int(step_time_microseconds))

#______________________________________________
#connect to GPIB
os.add_dll_directory("C:/Program Files/Keysight/IO Libraries Suite/bin")
os.add_dll_directory("C:/Program Files (x86)/Keysight/IO Libraries Suite/bin")
rm = pyvisa.ResourceManager("C:/Windows/System32/visa32.dll")

#connect the GPIB with the PC
lockin = rm.open_resource('GPIB0::8::INSTR')

# Query the Lock-In parameters
parameters = query_lockin_parameters()


#--------------------- DOWNLOADED PULSES STREAM TO PULSESTREAMER-------------------------




print("T1_Decay_Synchronized.py: calling function with these parameters:")
print(f"T1_Decay_Synchronized.py: channel_number_ref: {channel_number_ref}")
print(f"T1_Decay_Synchronized.py: channel_number_pulse: {channel_number_pulse}")
print(f"T1_Decay_Synchronized.py: tau_ref_ns: {tau_ref_ns}")
print(f"T1_Decay_Synchronized.py: tau_i_ns: {tau_i_ns}")
print(f"T1_Decay_Synchronized.py: tau_readout_ns: {tau_readout_ns}")
print(f"T1_Decay_Synchronized.py: number_of_cycles: {number_of_cycles}")
print(f"T1_Decay_Synchronized.py: (fig 3 only) delay_start_s: {delay_start_s}")
print(f"T1_Decay_Synchronized.py: (fig 3 only) delay_stop_s: {delay_stop_s}")
print(f"T1_Decay_Synchronized.py: (fig 3 only) delay_number_of_points: {delay_number_of_points}")
print(f"T1_Decay_Synchronized.py: (fig 4 only) mw_pulse_length_start_ns: {mw_pulse_length_start_ns}")
print(f"T1_Decay_Synchronized.py: (fig 4 only) mw_pulse_length_stop_ns: {mw_pulse_length_stop_ns}")
print(f"T1_Decay_Synchronized.py: (fig 4 only) mw_pulse_length_number_of_points: {mw_pulse_length_number_of_points}")



#do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)


do_it_all_no_init(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
#do_it_all_different_init_and_readout_pulsewidth(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_readout_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)

#rabi(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_ns,n_repeats,number_of_cycles,ps)

#sequences=rabi_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,number_of_cycles,ps)


#sequences=Hahn_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
#                              tau_ref_ns,tau_laser_ns,
#                              tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
#                              mw_T_delay_length_start_ns,mw_T_delay_length_stop_ns,mw_T_delay_length_number_of_points,
#                              tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
#                              n_repeats,number_of_cycles,ps)

#sequences=CPMG_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
#                              tau_ref_ns,tau_laser_ns,
#                              tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
#                              mw_T_delay_length_start_ns,mw_T_delay_length_stop_ns,mw_T_delay_length_number_of_points,
#                              tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
#                              N_CPMG,
#                              n_repeats,number_of_cycles,ps)

#print("T1_Decay_Synchronized.py:  -----------------------------")
print("T1_Decay_Synchronized.py: sequences created")
#print("T1_Decay_Synchronized.py:  -----------------------------")


#--------------LOOP SETUP----------------------------



# Initialize the data array
# Initialize an empty list to store the pairs (i, i^2)
pairs = []


# Define column names
columns = ['tau delay', 'lockin reading']

# parameters for loop:
loopAmount=delay_number_of_points

if(fig_mode==3):
    
# copy of time delay array
# Generate non-integer delays
    delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
#print(delays)

if(fig_mode==4):
    
# copy of time delay array
# Generate non-integer delays
    #delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
    delays = np.linspace(mw_pulse_length_start_ns, mw_pulse_length_stop_ns, mw_pulse_length_number_of_points)
    delays = np.round(delays).astype(int)
    print("T1_Decay_Synchronized.py: mw_pulse_lengths_ns=")
    print(delays)
#loop over and read the signal from the Labjack T7 and append the value to the intensity array



if(fig_mode==5):
    
# copy of time delay array
# Generate non-integer delays
    #delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
    delays = np.linspace(mw_T_delay_length_start_ns, mw_T_delay_length_stop_ns, mw_T_delay_length_number_of_points)
    delays = np.round(delays).astype(int)
    print("T1_Decay_Synchronized.py: mw_pulse_lengths_ns=")
    print(delays)
#loop over and read the signal from the Labjack T7 and append the value to the intensity array


if(fig_mode==6): # same as fig 5, varies tdelay
    
# copy of time delay array
# Generate non-integer delays
    #delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
    delays = np.linspace(mw_T_delay_length_start_ns, mw_T_delay_length_stop_ns, mw_T_delay_length_number_of_points)
    delays = np.round(delays).astype(int)
    print("T1_Decay_Synchronized.py: mw_pulse_lengths_ns=")
    print(delays)
#loop over and read the signal from the Labjack T7 and append the value to the intensity array
#--------------LOOP START----------------------------

# Count down from 10
if(fig_mode==3):
    print("Countdown....")
    for i in range(10, 0, -1):
        print(i)
        time.sleep(1)
    print("BLASTOFF!")

print("starting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


if(fig_mode==3):
    ps.startNow()
    for tau in delays:
        try:
            # Query the CH1 display value from the Lock-In Amplifier
            ch1_display_value = lockin.query('OUTR? 1').strip()
            
            print(tau, float(ch1_display_value))
            # Convert the display value to a float and append to pairs
            pairs.append((tau, float(ch1_display_value)))
            
            time.sleep(step_time)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            break  

    
                    

num_points=len(delays)
i=0
#if(fig_mode==4):
if fig_mode == 4 or fig_mode == 5 or fig_mode == 6: # both loops are same code
    # Get the current time
    current_time = datetime.now()
    print("Current time:", current_time.strftime("%Y-%m-%d %H:%M:%S"))
    time_to_complete_seconds=(step_time+rabi_and_hahn_delay_s)*mw_pulse_length_number_of_points
    # Convert total time to minutes and seconds
    minutes, seconds = divmod(time_to_complete_seconds, 60)
    print(f"Estimated time to complete: {int(minutes)} minutes and {int(seconds)} seconds")
    completion_time = current_time + timedelta(seconds=time_to_complete_seconds)
    print("Estimated completion time:", completion_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Starting collecting")

    print("Point, Tau(ns), result, time")
    for sequence, tau in zip(sequences, delays):
    # Your code here
        #print(f"Sequence: {sequence}, Tau: {tau}")

        #print("Tau, Current Time:",tau, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #print(sequence)
        ps.stream(sequence)
        ps.startNow()
        #print("starting at",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(rabi_and_hahn_delay_s)
        results = ljm.eReadNames(handle, numFrames, names)
        pairs.append((1e-9*tau,abs(results[0])))  # Append the tuple to the list
        x=abs(results[0])
        print(i,int(tau),f"{x:.3f}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
        #print(tau,abs(results[0]))
        i=i+1
        ljm.waitForNextInterval(intervalHandle)

    
#--------------------- DISPLAY DATA AND SAVE TO FILE-------------------------

#print(pairs)  # Print the list of tuples


# Open the file in 'w' mode with newline='' to prevent extra newline characters
with open(plotname, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)   
# Write each pair (i, i^2) as a row in the CSV file
    for pair in pairs:
        csvwriter.writerow(pair)

# Create a DataFrame
df = pd.DataFrame(pairs, columns=columns)


# Save DataFrame to CSV
csv_filepath = plotname  # using plotname as the CSV filename
df.to_csv(csv_filepath, sep="\t")  # save CSV without index

print(f'Data file has been saved to {plotname}')

# Write the settings to the text file
write_parameters_to_file(lockin_parameters_text_name, parameters)

print(f'Lockin parameters have been saved to {lockin_parameters_text_name}')

# Plotting
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.scatter(df['tau delay'], df['lockin reading'], color='blue', marker='o', label='Data Points')
plt.title('Lockin Reading  vs Tau Delay')
plt.xlabel('Tau Delay')
plt.ylabel('Lockin Reading')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
















