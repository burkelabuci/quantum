# ODMRvsTauMicrowave.py
# Peter Burke 7/26/2024
# Measures ODMR at different microwave pulse times
# Saves one file for each microwave pulse time



#----------------INSTRUCTIONS------------------------------------
#To generate Fig 4b,c,d of teaching paper:
# Set up parameters, pay attention to:
# tau_ref_ns=2.5e-3*1e9 # 15 ms fig 3, 2.5 ms fig 4.
# number_of_cycles=200 # default 33 for fig 3 33 hz; sets how long each pulse pattern is for a given delay; 200 for Fig 4
# Since the reference rate is 200 Hz, the pulseblaster will create 200 cycles for each delay, giving one second to take the data.
# If you want longer per delay point, increase 200 cycles. E.g. 2000 Hz will give 10 seconds of time for each delay point.

# This calls create_fig4_teachingpaper_pulse_sequence(tau_ref_ns, tau_laser_ns, tau_mw_ns, tau_padding_before_mw_ns, tau_padding_after_mw_ns, n_repeats, ps)
# for each tau_mw_ns
# Then calls chopped_odmr_srs_ds345(
#    start_frequency=2600,
#    stop_frequency=3100,
#    step_size=1,
#    step_time=300,
#    base_folder=r"C:\Users\BurkeLab\Desktop\072624"
#    )

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from labjack import ljm
from pulsestreamer import PulseStreamer
from pulsestreamer import *
import keyboard
import time 
from T1_Decay_Subroutines import *
from T1_Decay_parameters import *
import numpy as np

# Parameters
PB_IPADDRESS= '169.254.8.2'

ps = PulseStreamer(PB_IPADDRESS)

ps.setTrigger(TriggerStart.SOFTWARE)



#--------------------- PARAMETERS-------------------------
tau_ref_ns=2.5e-3*1e9 # 15 ms for fig 3, 2.5 ms for fig 4
tau_i_ns=5e-6*1e9 # laser initialization/readout pulse width
number_of_cycles=200 # default 33 fig 3, 200 fig 4; sets how long each pulse pattern is for a given delay
channel_number_ref=0
channel_number_pulse=1
delay_start_s=100e-6
delay_stop_s=1e-6
delay_number_of_points=100
step_time=number_of_cycles*2*tau_ref_ns*1e-9 # in seconds
step_time_microseconds=step_time*1e6
tau_delay_ns=1e-3*1e9

# for Fig 4
tau_laser_ns=5e-6*1e9
tau_mw_ns=1e-6*1e9
tau_padding_ns=1e-6*1e9
n_repeats=200 # 250  but with padding must be less
tau_padding_before_mw_ns=1000e-9*1e9
tau_padding_after_mw_ns=1000e-9*1e9


# Parameters for chopped ODMR:
start_frequency = 2400 #in MHz
stop_frequency = 3200 #in MHz
step_size = int(1) # specing between each frequency point in MHz
step_time = int(300) #in milliseconds
base_folder = r"C:\Users\BurkeLab\Desktop\082324" # Specify the base folder where you want to save the files





# Parameters for tau_mw_ns values
tau_mw_ns_start = 10e-9 * 1e9  # Start value for tau_mw_ns
tau_mw_ns_stop = 250e-9 * 1e9  # Stop value for tau_mw_ns
tau_mw_ns_points = 20  # Number of points for tau_mw_ns

# Calculate tau_mw_ns values
tau_mw_ns_values = np.linspace(tau_mw_ns_start, tau_mw_ns_stop, tau_mw_ns_points)
tau_mw_ns_values = np.round(tau_mw_ns_values).astype(int)
print(tau_mw_ns_values)



pulse_blaster_settle_time=1 # seconds to wait after new pulse blaster time



for tau_mw_ns in tau_mw_ns_values:
    #current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print(f"Current time: {current_time}")
    #print("calling this function")
    #print(f"tau_ref_ns: {tau_ref_ns}")
    #print(f"tau_laser_ns: {tau_laser_ns}")
    #print(f"tau_mw_ns: {tau_mw_ns}")
    #print(f"tau_padding_before_mw_ns: {tau_padding_before_mw_ns}")
    #print(f"tau_padding_after_mw_ns: {tau_padding_after_mw_ns}")
    #print(f"n_repeats: {n_repeats}")

    print("Starting sweep for tau_mw_ns=",tau_mw_ns)
    create_fig4_teachingpaper_pulse_sequence(tau_ref_ns, tau_laser_ns, tau_mw_ns, tau_padding_before_mw_ns, tau_padding_after_mw_ns, n_repeats, ps)

    #print("starting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    ps.startNow()
    time.sleep(pulse_blaster_settle_time)  # Adding delay to ensure pulse streamer completes its sequence before the next iteration
    chopped_odmr_srs_ds345(start_frequency, stop_frequency, step_size, step_time, base_folder)

    #chopped_odmr_srs_ds345(start_frequency=2670, stop_frequency=2690, step_size=1, step_time=1000, base_folder=r"C:\Users\BurkeLab\Desktop\072624")
    #chopped_odmr_srs_ds345(2670, 2690, 1, 1000, "C:\Users\BurkeLab\Desktop\072624")
