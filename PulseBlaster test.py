# PulseBlaster test.py
# Minghao Jiang 7/9/2024
# Reference paper:
# From reference paper: (aka "teaching paper")
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.
# This program produces Fig 3 on the teaching paper.
# This program will need you to hard code the laser parameters tau_ref, tau_i, and tau_delay. It is usually used as a program to test if the pulseblaster
# is working properly. If you wanna get data for T1_decay, go to the file T1_Decay.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from labjack import ljm
from pulsestreamer import PulseStreamer
import keyboard
import time 


# Parameters
PB_IPADDRESS= '169.254.8.2'

ps = PulseStreamer(PB_IPADDRESS)

tau_ref = 15e-3 # reference time in seconds ; default 15e-3
#tau_ref = 15e-3 # reference time in seconds ; default 15e-3
tau_i = 1e-6 # pulse time in seconds (initialize, readout) ; default 5e-6
tau_delay =1e-3 # delay between initialize and readout in seconds; default 1e-3

tau_ref_ns=tau_ref*1E9
tau_i_ns=tau_i*1E9
tau_delay_ns=tau_delay*1E9

# Create sequence object 
seq = ps.createSequence()

# Set channel 0 as refrence (pulse duration in nanoseconds)
seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0)])

# Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0)])
 
ps.stream(seq)  # runs forever , but returns program



