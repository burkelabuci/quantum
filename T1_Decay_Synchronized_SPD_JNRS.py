# Program name T1_Decay_Synchronized_SPD_JNRS.py
# 01/08/2025
# Author Minghao + Peter Burke + Noe
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.

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
import nidaqmx
from nidaqmx.constants import AcquisitionType, CountDirection, Edge

plotname = create_folder_and_generate_filename_csv()# Generate unique filename with name mm/dd/yy (eg. 070324)


#--------------------- PARAMETERS-------------------------

# for both fig 3 and fig 4 and fig 5 and 6
fig_mode=4 # 3 for figure 3 , 4 for figure 4, 5 for figure 5, 6 for figure 6
channel_number_laser_pulse=1 # same thing as channel_number_pulse
channel_number_mw_pulse=2
channel_number_gate_pulse=4

# Fig 3 only
# Fig 3 will vary delay between laser init and laser readout pulse between delay_start_s and delay_stop_s and measure the LIA at each point.
delay_start_s=0.5e-3
delay_stop_s=5e-3
delay_number_of_points=50


# for Fig 4, 5, 6
tau_laser_ns=5e-6*1e9 # laser pulse width, fig 4, 5
rabi_and_hahn_delay_s=5 # delay after setting new microwave pulse time to reading LIA output; can be 2 seconds for fig 4

# Fig 4 only:
# Fig 4 will vary mw pulse length from mw_pulse_length_start_ns to mw_pulse_length_stop_ns and measure LIA at each point
mw_pulse_length_start_ns=10
mw_pulse_length_stop_ns=3000
mw_pulse_length_number_of_points=50

# Fig 5, 6 only:
tau_mw_X_pi_over_2_ns=50e-9*1e9 # pi/2 pulse X length (fig 5)
tau_mw_X_pi_ns=2*tau_mw_X_pi_over_2_ns # pi pulse X length (fig 5)
tau_mw_Y_pi_ns=tau_mw_X_pi_ns # pi/2 pulse Y length (fig 5)
tau_padding_before_mw_pi_over_2_ns=1000e-9*1e9 # time between end of laser pulse and start of first mw X pi/2 pulse (fig 5)
tau_padding_after_mw_pi_over_2_ns=1000e-9*1e9 # time between end  of second mw X pi/2 pulse and start of next laser pulse (fig 5)
# Fig 5,6 will vary T_delay between mw_T_delay_length_start_ns and mw_T_delay_length_stop_ns and measure LIA at each point
mw_T_delay_length_start_ns=100e-9*1e9
mw_T_delay_length_stop_ns=500e-9*1e9
mw_T_delay_length_number_of_points=20
mw_T_delay_delay_s=2 # delay after setting new microwave pulse time to reading LIA output

# Fig 6 only:
N_CPMG=4 # number of CPMG refocusing pulses

#--------------------- INITIALIZE PULSEBLASTER-------------------------
PB_IPADDRESS= '169.254.8.2'

ps = PulseStreamer(PB_IPADDRESS)
print(f"PulseStreamer initialized: {ps}")


#ps.setTrigger(TriggerStart.SOFTWARE)

#--------------------- DOWNLOADED PULSES STREAM TO PULSESTREAMER-------------------------




print("T1_Decay_Synchronized.py: calling function with these parameters:")
print(f"T1_Decay_Synchronized.py: channel_number_pulse: {channel_number_laser_pulse}")
print(f"T1_Decay_Synchronized.py: tau_i_ns: {tau_laser_ns}")
print(f"T1_Decay_Synchronized.py: (fig 3 only) delay_start_s: {delay_start_s}")
print(f"T1_Decay_Synchronized.py: (fig 3 only) delay_stop_s: {delay_stop_s}")
print(f"T1_Decay_Synchronized.py: (fig 3 only) delay_number_of_points: {delay_number_of_points}")
print(f"T1_Decay_Synchronized.py: (fig 4 only) mw_pulse_length_start_ns: {mw_pulse_length_start_ns}")
print(f"T1_Decay_Synchronized.py: (fig 4 only) mw_pulse_length_stop_ns: {mw_pulse_length_stop_ns}")
print(f"T1_Decay_Synchronized.py: (fig 4 only) mw_pulse_length_number_of_points: {mw_pulse_length_number_of_points}")


tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)

#T1 measurement
tau_delay_lengths_ns = np.linspace(delay_start_s, delay_stop_s,delay_number_of_points)*1e9
tau_delay_lengths_ns = np.round(tau_delay_lengths_ns).astype(int)
print(tau_delay_lengths_ns)
#Rabi Oscillations
mw_pulse_lengths_ns = np.linspace(mw_pulse_length_start_ns, mw_pulse_length_stop_ns, mw_pulse_length_number_of_points)
mw_pulse_lengths_ns = np.round(mw_pulse_lengths_ns).astype(int)
print("rabi_many_sequences: mw_pulse_lengths_ns=")
print(mw_pulse_lengths_ns)

sequences=[]
tau_mw_variable=[]
tau_laser_variable=[]

if(fig_mode==3):
    for tau_delay_length_ns in tau_delay_lengths_ns:
        tau_delay_length_ns_rounded=round_to_nearest_8ns(tau_delay_length_ns)
        pulse_patt_laser = [(tau_laser_ns_rounded, 1),(tau_delay_length_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_delay_length_ns_rounded, 0)]
        pulse_patt_SPD_gate = [(tau_laser_ns_rounded, 0),(tau_delay_length_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_delay_length_ns_rounded, 0)]
        print(pulse_patt_laser)
        seq=ps.createSequence()
        seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)
        seq.setDigital(channel_number_gate_pulse, pulse_patt_SPD_gate)
        sequences.append(seq)
        tau_laser_variable.append(tau_delay_length_ns_rounded)
    
if(fig_mode==4):
    for mw_pulse_length_ns in mw_pulse_lengths_ns:
        mw_pulse_length_ns_rounded=round_to_nearest_8ns(mw_pulse_length_ns)
        tau_padding_before_mw_ns_rounded=round_to_nearest_8ns((tau_laser_ns_rounded-mw_pulse_length_ns_rounded)/2)
        tau_padding_after_mw_ns_rounded=tau_padding_before_mw_ns_rounded
        tau_laser_off_ns_rounded=tau_padding_before_mw_ns_rounded+mw_pulse_length_ns_rounded+tau_padding_after_mw_ns_rounded  
        pulse_patt_mw = [(tau_laser_ns_rounded, 0),(tau_padding_before_mw_ns_rounded, 0), (mw_pulse_length_ns_rounded, 1), (tau_padding_after_mw_ns_rounded, 0), (tau_laser_ns_rounded, 0), (tau_laser_off_ns_rounded, 0)]
        pulse_patt_laser = [(tau_laser_ns_rounded, 1),(tau_laser_off_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_laser_off_ns_rounded, 0)]
        #pulse_patt_SPD_gate = [(tau_laser_ns_rounded, 0),(tau_laser_off_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_laser_off_ns_rounded, 0)]
        pulse_patt_SPD_gate=pulse_patt_laser
        print(pulse_patt_mw)
        seq=ps.createSequence()
        seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)
        seq.setDigital(channel_number_mw_pulse, pulse_patt_mw)
        seq.setDigital(channel_number_gate_pulse, pulse_patt_SPD_gate)
        sequences.append(seq)
        tau_mw_variable.append(mw_pulse_length_ns_rounded)

# Initialize the data array
# Initialize an empty list to store the pairs (i, i^2)
pairs = []


# Define column names
columns = ['tau delay', 'labjack reading']
i=0
if(fig_mode==3):
    with nidaqmx.Task() as task:
        channel = task.ci_channels.add_ci_count_edges_chan(
            "Dev1/ctr0",
             edge=Edge.RISING,
             initial_count=0,
             count_direction=CountDirection.COUNT_UP,
         )
        channel.ci_count_edges_term = "/Dev1/PFI8"
        print("Start counting Fig3. Press Ctrl+C to stop.")
        for sequence, tau in zip(sequences, tau_laser_variable):
             try:
                edge_counts = 0
                ps.stream(sequence)
                task.start()
                time.sleep(rabi_and_hahn_delay_s)
                edge_counts = task.read()
                task.stop()
                print(tau,edge_counts)
                pairs.append((tau,edge_counts))
                x=abs(edge_counts)
                print(i,int(tau),f"{x:.3f}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
                print(tau,abs(edge_counts))
                i=i+1
             except KeyboardInterrupt:
                 pass
             finally:
                 task.stop()

if fig_mode == 4 or fig_mode == 5 or fig_mode == 6: # both loops are same code
    with nidaqmx.Task() as task:
        channel = task.ci_channels.add_ci_count_edges_chan(
            "Dev1/ctr0",
            edge=Edge.RISING,
            initial_count=0,
            count_direction=CountDirection.COUNT_UP,
        )
        channel.ci_count_edges_term = "/Dev1/PFI8"
        print("Start counting Fig4. Press Ctrl+C to stop.")
        for sequence, tau in zip(sequences, tau_mw_variable):
            try:
                edge_counts = 0
                ps.stream(sequence)
                task.start()
                time.sleep(rabi_and_hahn_delay_s)
                edge_counts = task.read()
                task.stop()
                print(tau,edge_counts)
                pairs.append((tau,edge_counts))
                x=abs(edge_counts)
                print(i,int(tau),f"{x:.3f}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
                print(tau,abs(edge_counts))
                i=i+1
            except KeyboardInterrupt:
                pass
            finally:
                task.stop()
    
#--------------------- DISPLAY DATA AND SAVE TO FILE-------------------------

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
df.to_csv(csv_filepath, sep=",")  # save CSV without index

print(f'Data file has been saved to {plotname}')

print(f'Lockin parameters have been saved to {plotname}')

# Plotting
plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
plt.scatter(df['tau delay'], df['labjack reading'], color='blue', marker='o', label='Data Points')
plt.plot(df['tau delay'], df['labjack reading'], color='blue', label='Data Points')
plt.title('SPD count  vs Tau Delay')
plt.xlabel('Tau Delay')
plt.ylabel('SPD count')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
















