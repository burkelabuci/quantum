# Variable width pulse
# Peter Burke 7/11/2024
# Assisted by Minghao
# Reference paper:
# From reference paper: (aka "teaching paper")
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.


# This program creates a reference square wave (ch0)
# and on ch1 a pulse at the same frequency as the reference square wave with adjustable pulse width.

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

tau_ref = 15e-3 # reference time in seconds ; default igor15e-3 # Square wave half cycle
tau_pulse_width = 15e-3 # pulse time in seconds (initialize, readout) ; default 5e-6

tau_ref_ns=tau_ref*1E9
tau_pulse_width_ns=tau_pulse_width*1E9

# Create sequence object 
seq = ps.createSequence()

# Set channel 0 as refrence (pulse duration in nanoseconds)
seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0)])

# Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0)])

seq.setDigital(1,[(tau_pulse_width_ns, 1), (tau_ref_ns - tau_pulse_width_ns, 0)])
ps.stream(seq)  # runs forever , but returns program



