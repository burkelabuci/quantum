# PulseBlaster test.py
# Peter Burke 7/12/2024
# calls pulse blaster helper functions
# used to debut

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


# Parameters
PB_IPADDRESS= '169.254.8.2'

ps = PulseStreamer(PB_IPADDRESS)

ps.setTrigger(TriggerStart.SOFTWARE)



#--------------------- PARAMETERS-------------------------
tau_ref_ns=2.500000000011e-3*1e9 # 15 ms for fig 3, 2.5 ms for fig 4
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
tau_mw_ns=111.1111111e-9*1e9
tau_padding_ns=1e-6*1e9
n_repeats=175 # 250  but with padding must be less
tau_padding_before_mw_ns=1000e-9*1e9
tau_padding_after_mw_ns=1000e-9*1e9

#create_fig3_teachingpaper_pulse_sequence(tau_ref_ns,tau_i_ns,tau_delay_ns,ps)
#create_fig3_teachingpaper_pulse_sequence_no_init_pulse(tau_ref_ns,tau_i_ns,tau_delay_ns,ps)


print("calling this function")
print(f"tau_ref_ns: {tau_ref_ns}")
print(f"tau_laser_ns: {tau_laser_ns}")
print(f"tau_mw_ns: {tau_mw_ns}")
print(f"tau_padding_before_mw_ns: {tau_padding_before_mw_ns}")
print(f"tau_padding_after_mw_ns: {tau_padding_after_mw_ns}")
print(f"n_repeats: {n_repeats}")


#create_fig4_teachingpaper_pulse_sequence(tau_ref_ns,tau_laser_ns,tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,ps)


create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeats,1)


# Count down from 10
#print("Countdown....")
#for i in range(10, 0, -1):
#    print(i)
#    time.sleep(1)
#print("BLASTOFF!")

#print("starting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#ps.startNow()





