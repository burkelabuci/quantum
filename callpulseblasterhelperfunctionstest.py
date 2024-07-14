# callpulseblasterhelperfunctionstest.py
# Peter Burke 7/14/2024
# calls pulse blaster helper functions
# but with no pulse blaster hardware
# used to debug

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#from labjack import ljm
#from pulsestreamer import PulseStreamer
#from pulsestreamer import *
import keyboard
import time 
from T1_Decay_Subroutines import *
#from T1_Decay_parameters import *




#--------------------- PARAMETERS-------------------------
tau_ref = 15e-3 # reference time in seconds ; default 15e-3
#tau_ref = 15e-3 # reference time in seconds ; default 15e-3
tau_i = 1e-6 # pulse time in seconds (initialize, readout) ; default 5e-6
number_of_cycles=33 #number of cycles of sequences created
tau_delay_start=0.1e-3 # beginning of loop
tau_delay_end= 3e-3 # beginning of loop
delay_num_points = 10 #number of points collected

#convert into nano seconds
tau_ref_ns=tau_ref*1e9
tau_i_ns=tau_i*1e9

channel_number_ref=0 
channel_number_pulse=1
step_time=number_of_cycles*2*tau_ref_ns*1e-9 # in seconds
step_time_microseconds=step_time*1e6

delay_start_s=10e-6
delay_stop_s=100e-6
delay_number_of_points=10

#do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,cycle,delay_start_s,delay_end_s,num_points,ps)

    #************* SQUAREWAVE FIRST*******************
    
square_wave_half_cycle_ns=tau_ref_ns

# pulse_patt = [(100, 0), (200, 1), (80, 0), (300, 1), (60, 0)]

pulse_patt_ref = generate_alternating_pairs(square_wave_half_cycle_ns,2*number_of_cycles)
print("*************************************************************************************")
print(pulse_patt_ref)
print("*************************************************************************************")

print("sum of alternating pulse_patt_ref=",sum_first_elements(pulse_patt_ref))
should_be = square_wave_half_cycle_ns*2*number_of_cycles
print("should be",should_be)
print("*************************************************************************************")

#print(pulse_patt_ref)
#seq.setDigital(channel_number_ref, pulse_patt_ref)
print("*************************************************************************************")


#*********** THEN PULSE CYCLE

tau_delay_ns=100e-6*1e9
pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)

#print(pulse_patt_decay)
#seq.setDigital(channel_number_pulse, pulse_patt_decay)
print("*************************************************************************************")

print("generating delays")
# Generate non-integer delays
delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
#print(delays)

for delay in delays:
    #print(delay, delay*1e9)
    #print(delay*1e9)
    pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles)







