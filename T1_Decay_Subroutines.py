# T1_Decay_Subroutines.py
# Subroutines to set pulse sequences for T1 decay of NV center measurement.
# Peter Burke 7/3/2024
# Reference paper:
# From reference paper: (aka "teaching paper")
# Sewani, Vikas K., Hyma H. Vallabhapurapu, Yang Yang, Hannes R. Firgau, Chris Adambukulam, 
# Brett C. Johnson, Jarryd J. Pla, and Arne Laucht. 
# "Coherent control of NV− centers in diamond in a quantum teaching lab." American Journal of Physics 88, no. 12 (2020): 1156-1169.
# 6/14/2024 Peter debugging Minghao's bug
# Deletes Initialization pulses for demo purposes

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from labjack import ljm
from pulsestreamer import PulseStreamer
import keyboard
import time 


def square_number(num):
    """
    This function takes a numeric input and returns its square.
    """
    return num * num




def create_fig3_teachingpaper_pulse_sequence(tau_ref_ns,tau_i_ns,tau_delay_ns,ps: PulseStreamer):
    # Creates patter in fig 3 of teaching paper
    # ps is the pulsestreamer object
    # duration is how long the stream runs for in seconds

    #print("****************************************************************")
    #print("Start inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("tau_ref_ns,tau_i_ns,tau_delay_ns=")
    #print(tau_ref_ns,tau_i_ns,tau_delay_ns)




    # Create sequence object 
    seq = ps.createSequence()


    # Set channel 0 as refrence (pulse duration in nanoseconds)
    seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0)])

    # Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
    seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])

 
    ps.stream(seq)  # runs forever , but returns program

    #print("Done inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("****************************************************************")



    return




