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
default_tau_ref = 15e-3 # reference time in seconds ; default 15e-3
#tau_ref = 15e-3 # reference time in seconds ; default 15e-3
default_tau_i = 1e-6 # pulse time in seconds (initialize, readout) ; default 5e-6
default_cycles=330 #number of cycles of sequences created
default_tau_delay_start=0.1e-3 # beginning of loop
default_tau_delay_end= 3e-3 # beginning of loop
default_delay_num_points = 10 #number of points collected

#ask for inputs for parameters above
tau_ref,tau_i,delay_start_s,delay_end_s,cycle,num_points = T1_Decay_Synchronized_parameters(default_tau_ref,default_tau_i,default_tau_delay_start,default_tau_delay_end,default_cycles,default_delay_num_points)

#convert into nano seconds
tau_ref_ns=tau_ref*1e9
tau_i_ns=tau_i*1e9

channel_number_ref=0 
channel_number_pulse=1
step_time=cycle*2*tau_ref_ns*1e-9 # in seconds
step_time_microseconds=step_time*1e6


do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,cycle,delay_start_s,delay_end_s,num_points,ps)




for i in range(1, 11):
    print(i)
    time.sleep(1)

print("starting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
ps.startNow()





