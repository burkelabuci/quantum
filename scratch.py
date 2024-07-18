# scratch code temporary 
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

#--------------------- PARAMETERS-------------------------
tau_ref_ns=15e-3*1e9
tau_i_ns=5e-6*1e9 # laser initialization/readout pulse width
number_of_cycles=330 # default 33; sets how long each pulse pattern is for a given delay
channel_number_ref=0
channel_number_pulse=1
delay_start_s=3e-3
delay_stop_s=0.01e-3
delay_number_of_points=100
step_time=number_of_cycles*2*tau_ref_ns*1e-9 # in seconds
step_time_microseconds=step_time*1e6

#--------------------- SCRATCH CODE-------------------------

do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)
#do_it_all_no_init(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)

do_it_all_different_init_and_readout_pulsewidth(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_readout_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps):

    # tau_readout_ns is the readout pulse width
    # tau_i_ns is the intitialization pulse width
    
    

    # Create sequences using the non-integer delays
    sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]



def create_fig3_teachingpaper_pulse_sequence_repeated_different_init_and_readout_pulsewidth(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_delay_ns,number_of_cycles,ps: PulseStreamer):
    # Creates patter in fig 3 of teaching paper
    # ps is the pulsestreamer object
    # duration is how long the stream runs for in seconds

 pulse_patt_decay = create_fig3_teachingpaper_pulse_sequence_repeated_different_init_and_readout_pulsewidth(tau_ref_ns, tau_i_ns,tau_readout_ns, tau_delay_ns, number_of_cycles)
    

    pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    create_pattern_array_rounded_to_8_ns_different_init_and_readout_pulsewidth
    
    
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    create_fig3_teachingpaper_pulse_sequence
    pulse_patt_decay = create_fig3_teachingpaper_pulse_sequence_different_init_and_readout_pulsewidth(tau_ref_ns, tau_i_ns,tau_readout_ns, tau_delay_ns, number_of_cycles)
    
    
    create_pattern_array_rounded_to_8_ns
    
    
    
    



rabi(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_ns,n_repeats,ps)

def create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_delay_ns,number_of_cycles,ps: PulseStreamer):