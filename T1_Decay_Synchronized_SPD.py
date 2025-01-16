# Program name T1_Decay_Synchronized_SPD_JNRS.py
# 01/08/2025
# Author Minghao + Peter Burke + Noe
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.
#----------------INSTRUCTIONS------------------------------------
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
#Figure configuration
fig_mode=4  # 2 for pulsed ODMR, 3 for figure 3 , 4 for figure 4, 5 for figure 5, 6 for figure 6
#Pulse Blaster channel definition
channel_number_laser_pulse=1 # laser
channel_number_mw_pulse=2 #MW
channel_number_gate_pulse=4 #SPD gate

tau_laser_ns=5e-6*1e9 # laser pulse width
count_delay_s=3 # Delay for count reading

#Pulsed ODMR 
start_frequency = 2500 #in MHz
stop_frequency = 3200 #in MHz
step_size = int(1) # specing between each frequency point in MHz
step_time = int(3000) #in milliseconds
step_time_s = float(step_time/1000) #in seconds
freq_num= [i * 1e3 for i in range(start_frequency, stop_frequency, step_size)]


# Fig 3 only
# Fig 3 will vary delay between laser init and laser readout pulse between delay_start_s and delay_stop_s and measure the LIA at each point.
delay_start_s=0.1e-3
delay_stop_s=5e-3
delay_number_of_points=50

# Fig 4 only:
# Fig 4 will vary mw pulse length from mw_pulse_length_start_ns to mw_pulse_length_stop_ns and measure LIA at each point
mw_pulse_length_start_ns=10
mw_pulse_length_stop_ns=2000
mw_pulse_length_number_of_points=100

#--------------------- INITIALIZE PULSEBLASTER-------------------------
PB_IPADDRESS= '169.254.8.2'

ps = PulseStreamer(PB_IPADDRESS)
print(f"PulseStreamer initialized: {ps}")
#--------------------- DOWNLOADED PULSES STREAM TO PULSESTREAMER-------------------------
tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)

#T1 measurement
tau_delay_lengths_ns = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)*1e9
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

if(fig_mode==2):
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
    print(f"Unique filename: {step_time_s}")
    pulse_patt_laser = [(tau_laser_ns_rounded, 1),(tau_laser_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_laser_ns_rounded, 0)]
    pulse_patt_mw = [(tau_laser_ns_rounded, 0),(tau_laser_ns_rounded, 1), (tau_laser_ns_rounded, 0), (tau_laser_ns_rounded, 0)]
    pulse_patt_SPD_gate = [(tau_laser_ns_rounded, 0),(tau_laser_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_laser_ns_rounded, 0)]
    seq = ps.createSequence()
    seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)
    seq.setDigital(channel_number_mw_pulse, pulse_patt_mw)
    seq.setDigital(channel_number_gate_pulse, pulse_patt_SPD_gate)
    ps.stream(seq)

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
i=0

if(fig_mode==2):
    columns = ['frequency', 'SPD count']
    with nidaqmx.Task() as task:
        channel = task.ci_channels.add_ci_count_edges_chan(
            "Dev1/ctr0",
            edge=Edge.RISING,
            initial_count=0,
            count_direction=CountDirection.COUNT_UP,
        )
        channel.ci_count_edges_term = "/Dev1/PFI8"
        print("Continuously pollingFig2. Press Ctrl+C to stop.")
        try:
            synth.write("sweep_single",True)
            while True:
                edge_counts = 0
                current_frequency = synth.read("frequency") 
                task.start()
                time.sleep(step_time_s)
                edge_counts = task.read()
                task.stop()
                print(current_frequency,edge_counts)
                pairs.append((current_frequency*1e3,edge_counts))
                x=abs(edge_counts)
                print(i,int(current_frequency*1e3),f"{x:.3f}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
                print(current_frequency*1e3,abs(edge_counts))
                i=i+1
                if current_frequency >=freq_num[-1]:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            task.stop()
            print(f"\nAcquired {edge_counts:n} total counts.")


if(fig_mode==3):
    columns = ['tau delay', 'SPD count']
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
                time.sleep(count_delay_s)
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
    columns = ['tau delay', 'SPD count']
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
                time.sleep(count_delay_s)
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
plt.scatter(df[df.columns[0]], df[df.columns[1]], color='blue', marker='o', label='Data Points')
plt.plot(df[df.columns[0]], df[df.columns[1]], color='blue', label='Data Points')
plt.title(f'{df.columns[0]} vs {df.columns[1]}')
plt.xlabel(df.columns[0])
plt.ylabel(df.columns[1])
plt.grid(True)
plt.legend()
plt.tight_layout()

# Display the plot
plt.show()
















