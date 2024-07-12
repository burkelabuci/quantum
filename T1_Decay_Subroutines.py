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




def createsquarewavesequence(channel_number,square_wave_half_cycle_s,number_of_cycles,ps: PulseStreamer):
    # create a sequence that is a square wave
    # input is square wave half cycle in seconds
    # input is number of cycles in the sequence
    # channel_number is the channel number (default 0)
    # return is a sequence in pulseblaster format
    # reference : https://www.swabianinstruments.com/static/documentation/PulseStreamer/sections/api-doc.html

    #print("****************************************************************")

    #square_wave_half_cycle_s=15e-3 # temporarily hard code
    #number_of_cycles=100# temporarily hard code
    square_wave_half_cycle_ns=square_wave_half_cycle_s*1e9 # convert to ns

    # Create sequence object 
    seq = ps.createSequence()

    # pulse_patt = [(100, 0), (200, 1), (80, 0), (300, 1), (60, 0)]

    pulse_patt = generate_alternating_pairs(square_wave_half_cycle_ns,2*number_of_cycles)
    print(pulse_patt)
    seq.setDigital(channel_number, pulse_patt)

    
    return seq




 

    #print("Done inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("****************************************************************")



    return




def createt1decaysequence(channel_number,  tau_ref_ns,tau_i_ns,tau_delay_ns ,number_of_cycles,ps: PulseStreamer):

    # Creates patter in fig 3 of teaching paper
    # ps is the pulsestreamer object
    # duration is how long the stream runs for in seconds
    # return is a sequence in pulseblaster format
    # reference : https://www.swabianinstruments.com/static/documentation/PulseStreamer/sections/api-doc.html



    # Create sequence object 
    seq = ps.createSequence()

    # pulse_patt = [(100, 0), (200, 1), (80, 0), (300, 1), (60, 0)]


    pulse_patt = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    print(pulse_patt)
    seq.setDigital(channel_number, pulse_patt)

    return seq




 

    #print("Done inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("****************************************************************")



    return




def create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_delay_ns,number_of_cycles,ps: PulseStreamer):
    # Creates patter in fig 3 of teaching paper
    # ps is the pulsestreamer object
    # duration is how long the stream runs for in seconds

    #print("****************************************************************")
    #print("Start inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("tau_ref_ns,tau_i_ns,tau_delay_ns=")
    #print(tau_ref_ns,tau_i_ns,tau_delay_ns)
    
    

    # Create sequence object 
    seq = ps.createSequence()
    
    #************* SQUAREWAVE FIRST*******************
    
    square_wave_half_cycle_ns=tau_ref_ns

    # pulse_patt = [(100, 0), (200, 1), (80, 0), (300, 1), (60, 0)]

    pulse_patt_ref = generate_alternating_pairs(square_wave_half_cycle_ns,2*number_of_cycles)
    print(pulse_patt_ref)
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    print(pulse_patt_decay)
    seq.setDigital(channel_number_pulse, pulse_patt_decay)

    return seq

def do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps):


    # Generate non-integer delays
    delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
    print(delays)

    # Create sequences using the non-integer delays
    sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]

    # old one has integer value of delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]

    # Add all the sequences together
    result_sequence = sum(sequences[1:], sequences[0])
    ps.stream(result_sequence)  # runs forever , but returns program

def generate_alternating_pairs(x_value, num_pairs):
    # Peter Burke 7/12/2024
    # Chatgpt to created alternating pairs
    # Example of calling the function
    #x_value = 5
    #num_pairs = 10
    #pairs = generate_alternating_pairs(x_value, num_pairs)
    #print(pairs)

    """
    Generates a list of (x, y) pairs where y alternates between 0 and 1.
    
    Parameters:
        x_value (int or float): The constant x value for each pair.
        num_pairs (int): The number of pairs to generate.
    
    Returns:
        list of tuples: The generated (x, y) pairs.
    """
    #return [(x_value, i % 2) for i in range(num_pairs)]
    return [(x_value,1- i % 2) for i in range(num_pairs)]


def create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, n):
    pattern = [
        (tau_i_ns, 1), 
        ((tau_ref_ns - tau_i_ns), 0), 
        (tau_i_ns, 1), 
        (tau_delay_ns, 0), 
        (tau_i_ns, 1), 
        ((tau_ref_ns - 2 * tau_i_ns - tau_delay_ns), 0)
    ]
    
    pattern_array = pattern * n
    return pattern_array