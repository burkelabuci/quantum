# Program name NVT1DecayPulseVersion1.py
# 6/12/2024
# Author Minghao
# From reference paper:
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.

# This program creates Ch0 and Ch1 output waveform of Pulseblaster model 8/2 as Fig 3 of reference
# at IP address PB_IPADDRESS

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

tau_ref = 15e-3 # reference time in seconds ; default 15e-3
tau_i = 5e-6 # pulse time in seconds (initialize, readout) ; default 5e-6
tau_delay = 4.2e-3 # delay between initialize and readout in seconds; default 1e-3



# Define your delayed time range:


#create pulse sequence,

# Create Pulse Streamer object by entering the IP address of the hardware
#ps = PulseStreamer('169.254.8.2')
ps = PulseStreamer(PB_IPADDRESS)


# Create sequence object 
seq = ps.createSequence()


# Set channel 0 as refrence (pulse duration in nanoseconds)
seq.setDigital(0, [((tau_ref)*1E9,1),((tau_ref)*1E9,0)])

#seq.setAnalog(0, [((tau_ref)*1E9,0.5),((tau_ref)*1E9,0)])
# Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
seq.setDigital(1, [((tau_i)*1E9, 1), ((tau_ref-tau_i)*1E9, 0),((tau_i)*1E9, 1),((tau_delay)*1E9,0),((tau_i)*1E9, 1), ((tau_ref-tau_i)*1E9, 0)])
 

# Stream sequence once

ps.stream(seq,10000)

