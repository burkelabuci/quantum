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
#seqdelay=createsquarewavesequence(0,15e-3,6,ps)
tau_ref_ns=15e-3*1e9
tau_i_ns=0.1e-3*1e9
tau_delay_ns=2e-3*1e9
number_of_cycles=33
channel_number_ref=0
channel_number_pulse=1
delay_start_s=0.1e-3
delay_stop_s=3e-3
delay_number_of_points=10



do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps)




