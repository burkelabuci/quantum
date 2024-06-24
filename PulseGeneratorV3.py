# Program name PulseGeneratorV1.py
# 6/21/2024
# Author Minghao
# chop current of wire
# Generates a series of digital pulses frequency f on digital channel # Chan


# This program creates Ch2 output waveform of Pulseblaster model 8/2
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

f = 0.5 # fequency of the pulsewidth
t1 = 1/f # pulse width ; default 5e-6
#t2 = 2e-3 # time between pulses ; default 30e-3
chan = 2 # channel output of pulseblaster ; default 1


t1_ns = t1*1E9
#t2_ns = t2*1E9


# Define your delayed time range:


#create pulse sequence,

# Create Pulse Streamer object by entering the IP address of the hardware
#ps = PulseStreamer('169.254.8.2')
ps = PulseStreamer(PB_IPADDRESS)


# Create sequence object 
seq = ps.createSequence()

# Set Analog channel 1 
#seq.setDigital(0, [(t1_ns,1),(t2_ns-t1_ns,0)])
 
#seq.setDigital(0,[(1e6,1),(1e6,0)])
seq.setDigital(chan,[(t1_ns,1),(t1_ns,0)])


# Stream sequence once

ps.stream(seq)

ps.forceFinal()