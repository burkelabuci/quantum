

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

tau_ref = 5e-6 # reference time in seconds ; default 15e-3
tau_ref_ns = tau_ref*1e9 # reference time in seconds ; default 15e-3

tau_laser_ns=5e-6*1e9 # laser pulse width, fig 4, 5
tau_padding_ns=1e-6*1e9 # not used for now
tau_padding_before_mw_ns=1000e-9*1e9 # time between end of laser pulse and start of mw pulse (fig 4)
tau_padding_after_mw_ns=1000e-9*1e9 # time between end of mw pulse and start of laser pulse (fig 4)
tau_mw_ns=5e-6*1e9 # not used

channel_number_laser_pulse=1 # same thing as channel_number_pulse
channel_number_mw_pulse=2
channel_number_mw_phaseshifted_pulse=3
channel_number_gating_pulses=4

tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
tau_padding_before_mw_ns_rounded=round_to_nearest_8ns(tau_padding_before_mw_ns)
tau_padding_after_mw_ns_rounded=round_to_nearest_8ns(tau_padding_after_mw_ns)
tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
tau_laser_off_ns_rounded=tau_padding_before_mw_ns_rounded+tau_mw_ns_rounded+tau_padding_after_mw_ns_rounded  

# Create sequence object 
seq = ps.createSequence()

# Set channel 0 as refrence (pulse duration in nanoseconds)
#seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0),(tau_ref_ns, 1),(tau_ref_ns, 0)])
#seq.setDigital(1, [(tau_ref_ns, 1), (tau_ref_ns, 0), (tau_ref_ns, 1), (tau_ref_ns, 0)])       #Laser
#seq.setDigital(2, [(tau_ref_ns, 0), (tau_ref_ns, 1), (tau_ref_ns, 0), (tau_ref_ns, 1)])       #MW
#seq.setDigital(4, [(tau_ref_ns, 0), (tau_ref_ns, 0), (tau_ref_ns, 1), (tau_ref_ns, 0)])       #SDP gate

#seq.setDigital(1, [(tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1)])       #Laser
#seq.setDigital(2, [(tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1)])       #MW
#seq.setDigital(4, [(tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1), (tau_ref_ns, 1)])       #SDP gate




pulse_patt_laser = [(tau_laser_ns_rounded, 1),(tau_laser_off_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_laser_off_ns_rounded, 0)]
pulse_patt_mw = [(tau_laser_ns_rounded, 0),(tau_padding_before_mw_ns_rounded, 0), (tau_mw_ns_rounded, 1), (tau_padding_after_mw_ns_rounded, 0), (tau_laser_ns_rounded, 0), (tau_laser_off_ns_rounded, 0)]
pulse_patt_SPD_gate = [(tau_laser_ns_rounded, 0),(tau_laser_off_ns_rounded, 0), (tau_laser_ns_rounded, 1), (tau_laser_off_ns_rounded, 0)]

seq = ps.createSequence()
seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)
seq.setDigital(channel_number_mw_pulse, pulse_patt_mw)
seq.setDigital(channel_number_gating_pulses, pulse_patt_SPD_gate)
ps.stream(seq)

# Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0)])

ps.stream(seq*8)  # runs forever , but returns program