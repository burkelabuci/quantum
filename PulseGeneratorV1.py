# Program name PulseGeneratorV1.py
# 6/14/2024
# Author Minghao
# Professor Burke tutorial
# Generates a series of pulses of width t1, amplitude A1, delay t2, on channel # Chan


# This program Ch0 Analog output waveform of Pulseblaster model 8/2 as Fig 3 of reference
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


t1 = 1e-3 # pulse width ; default 5e-6
t2 = 30e-3 # time between pulses ; default 30e-3
A1 = 0.1 # pulse height in Volts; default 0.1 V ; max is xyz V
chan = 1 # channel output of pulseblaster ; default 1


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

# Set Analog channel 1 
seq.setAnalog(0, [((tau_ref)*1E9,1),((tau_ref)*1E9,0)])
 

# Stream sequence once

ps.stream(seq,10000)

ps.F