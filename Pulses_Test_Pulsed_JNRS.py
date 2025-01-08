

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

tau_ref = 5e-6 # reference time in seconds ; default 15e-3
tau_ref_ns = tau_ref*1e9 # reference time in seconds ; default 15e-3



# Create sequence object 
seq = ps.createSequence()

# Set channel 0 as refrence (pulse duration in nanoseconds)
#seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0),(tau_ref_ns, 1),(tau_ref_ns, 0)])
#seq.setDigital(1, [(tau_ref_ns, 1), (tau_ref_ns, 0), (tau_ref_ns, 1), (tau_ref_ns, 0)])       #Laser
#seq.setDigital(2, [(tau_ref_ns, 0), (tau_ref_ns, 1), (tau_ref_ns, 0), (tau_ref_ns, 1)])       #MW
#seq.setDigital(4, [(tau_ref_ns, 0), (tau_ref_ns, 0), (tau_ref_ns, 1), (tau_ref_ns, 0)])       #SDP gate

seq.setDigital(1, [(tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1)])       #Laser
seq.setDigital(2, [(tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1)])       #MW
seq.setDigital(4, [(tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1)])       #SDP gate


# Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0)])

ps.stream(seq*8)  # runs forever , but returns program