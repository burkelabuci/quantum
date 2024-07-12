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
import keyboard
import time 
from T1_Decay_Subroutines import *


# Parameters
PB_IPADDRESS= '169.254.8.2'

ps = PulseStreamer(PB_IPADDRESS)

# Create sequence object 
#seq = ps.createSequence()
seqdelay=createsquarewavesequence(0,15e-3,6,ps)
tau_ref_ns=15e-3*1e9
tau_i_ns=1e-3*1e9
tau_delay_ns=2e-3*1e9
number_of_cycles=33
square_wave_half_cycle_s=15e-3

seqdelay=createt1decaysequence(1,  tau_ref_ns,tau_i_ns,tau_delay_ns ,number_of_cycles,ps)

seqref=createsquarewavesequence(0,square_wave_half_cycle_s,number_of_cycles,ps)

channel_number_ref=0
channel_number_pulse=1
seqtotal=create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_delay_ns,number_of_cycles,ps)


# Create an array of sequence objects
#sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]
delay_start_s=1e-3
delay_stop_s=3.14e-3
delay_number_of_points=10


# Generate non-integer delays
delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)

# Create sequences using the non-integer delays
sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]

# old one has integer value of delays
#sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]

# Add all the sequences together
result_sequence = sum(sequences[1:], sequences[0])
ps.stream(result_sequence,1)  # runs forever , but returns program


#ps.stream(sequences[2])  # runs forever , but returns program



