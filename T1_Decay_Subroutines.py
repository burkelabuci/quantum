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

    # STILL Need to round to 8 ns...
    # Set channel 0 as refrence (pulse duration in nanoseconds)
    seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0)])

    # Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
    # Fix 8 ns rounding:
#    seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
    pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, 1)
    seq.setDigital(1,pulse_patt_decay) 
    

 
    ps.stream(seq)  # runs forever , but returns program

    #print("Done inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("****************************************************************")



    return


def create_fig4_teachingpaper_pulse_sequence(tau_ref_ns,tau_laser_ns,tau_mw_ns,tau_padding_ns,n_repeats,ps: PulseStreamer):
    # Creates patter in fig 4 of teaching paper
    # ps is the pulsestreamer object
    # n_repeats is how long many repeats per cycle


    # Create sequence object 
    seq = ps.createSequence()

    # STILL Need to round to 8 ns...
    # Set channel 0 as refrence (pulse duration in nanoseconds)
    seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0)])

    # Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
    # Fix 8 ns rounding:
#    seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
    pulse_patt_decay_laser = create_fig_4_laser_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_ns, n_repeats,1)
    seq.setDigital(1,pulse_patt_decay_laser) 
    
    # Set channel 2 as the microwave pulse sequence (pulse duration in nanoseconds)
    pulse_patt_decay_mw = create_fig_4_mw_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_ns, n_repeats,1)
    seq.setDigital(2,pulse_patt_decay_mw) 
 
    ps.stream(seq)  # runs forever , but returns program

    #print("Done inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("****************************************************************")



    return

def create_fig3_teachingpaper_pulse_sequence_different_init_and_readout_pulsewidth(tau_ref_ns,tau_i_ns,tau_readout_ns,tau_delay_ns,ps: PulseStreamer):
    # Creates patter in fig 3 of teaching paper
    # ps is the pulsestreamer object
    # duration is how long the stream runs for in seconds
    # tau_readout_ns is the readout pulse width
    # tau_i_ns is the intitialization pulse width
    #print("****************************************************************")
    #print("Start inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("tau_ref_ns,tau_i_ns,tau_delay_ns=")
    #print(tau_ref_ns,tau_i_ns,tau_delay_ns)



    # Create sequence object 
    seq = ps.createSequence()

    # STILL Need to round to 8 ns...
    # Set channel 0 as refrence (pulse duration in nanoseconds)
    seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0)])

    # Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
    # Fix 8 ns rounding:
#    seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, 1)
    pulse_patt_decay = create_pattern_array_rounded_to_8_ns_different_init_and_readout_pulsewidth(tau_ref_ns, tau_i_ns,tau_readout_ns, tau_delay_ns, 1)
    
    seq.setDigital(1,pulse_patt_decay) 
    

 
    ps.stream(seq)  # runs forever , but returns program

    #print("Done inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("****************************************************************")



    return

def create_fig3_teachingpaper_pulse_sequence_no_init_pulse(tau_ref_ns,tau_i_ns,tau_delay_ns,ps: PulseStreamer):
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
    #seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])
    pulse_patt_decay = create_pattern_array__no_init_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, 1)
    seq.setDigital(1,pulse_patt_decay) 
    
 
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
    # Note: Internally, the Pulse Streamer hardware is always splitting the sequence data into 8 nanosecond long chunks. 

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
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_ref sum=",sum_first_elements(pulse_patt_ref))
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_ref=")
    print(pulse_patt_ref)
    print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_decay=")
    print(pulse_patt_decay)
    print("---------------------------------------------------")
    #print(pulse_patt_decay)
    seq.setDigital(channel_number_pulse, pulse_patt_decay)

    return seq



def create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_ns,tau_padding_ns,n_repeats,number_of_cycles,ps: PulseStreamer):
    # called by    
    # rabi(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_ns,n_repeats,ps)
    tau_mw_ns=mw_pulse_length_ns


    # called by 
    # rabi(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_ns,n_repeats,ps)


    # Creates patter in fig 4 of teaching paper
    # ps is the pulsestreamer object

    

    # Create sequence object 
    seq = ps.createSequence()
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Creating sequence for mw_pulse_length_ns=",mw_pulse_length_ns)
    
    #************* SQUAREWAVE FIRST*******************
    
    # pulse_patt = [(100, 0), (200, 1), (80, 0), (300, 1), (60, 0)]

    square_wave_half_cycle_ns=tau_ref_ns

    pulse_patt_ref = generate_alternating_pairs(square_wave_half_cycle_ns,2*number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_ref sum=",sum_first_elements(pulse_patt_ref)/1e9)

    #print("---------------------------------------------------")
    #print("pulse_patt_ref=")
    #print(pulse_patt_ref)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    # n_repeats is 250 if fixed mw pulse
    # But under variable microwave pulse, ???
    #*********** THEN PULSE CYCLE LASER***********************
    pulse_patt_laser = create_fig_4_laser_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_ns, n_repeats,number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_laser sum=",sum_first_elements(pulse_patt_laser)/1e9)
    #print(pulse_patt_laser)
    seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)
    
    #*********** THEN PULSE CYCLE MW***********************

    
    pulse_patt_mw = create_fig_4_mw_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_ns, n_repeats,number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_mw sum=",sum_first_elements(pulse_patt_mw)/1e9)
    #print(pulse_patt_mw)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_mw_pulse, pulse_patt_mw)

    return seq


def create_fig3_teachingpaper_pulse_sequence_repeated_different_init_and_readout_pulsewidth(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_readout_ns,tau_delay_ns,number_of_cycles,ps: PulseStreamer):
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
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_ref sum=",sum_first_elements(pulse_patt_ref))
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_ref=")
    print(pulse_patt_ref)
    print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    pulse_patt_decay = create_pattern_array_rounded_to_8_ns_different_init_and_readout_pulsewidth(tau_ref_ns, tau_i_ns,tau_readout_ns, tau_delay_ns, number_of_cycles)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_decay=")
    print(pulse_patt_decay)
    print("---------------------------------------------------")
    #print(pulse_patt_decay)
    seq.setDigital(channel_number_pulse, pulse_patt_decay)

    return seq


def create_fig3_teachingpaper_pulse_sequence_repeated_no_init_pulse(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_delay_ns,number_of_cycles,ps: PulseStreamer):
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
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_ref sum=",sum_first_elements(pulse_patt_ref))
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_ref=")
    print(pulse_patt_ref)
    print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    pulse_patt_decay = create_pattern_array__no_init_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_decay=")
    print(pulse_patt_decay)
    print("---------------------------------------------------")
    #print(pulse_patt_decay)
    seq.setDigital(channel_number_pulse, pulse_patt_decay)

    return seq



def create_fig3_teachingpaper_pulse_sequence_repeated_no_init_pulse(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_delay_ns,number_of_cycles,ps: PulseStreamer):
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
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_ref sum=",sum_first_elements(pulse_patt_ref))
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_ref=")
    print(pulse_patt_ref)
    print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    pulse_patt_decay = create_pattern_array__no_init_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    print("---------------------------------------------------")
    print("tau_delay_ns=",tau_delay_ns)
    print("pulse_patt_decay=")
    print(pulse_patt_decay)
    print("---------------------------------------------------")
    #print(pulse_patt_decay)
    seq.setDigital(channel_number_pulse, pulse_patt_decay)

    return seq


def do_it_all(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps):


    # Generate non-integer delays
    delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
    print("delays=")
    print(delays)

    # Apply the rounding function to each delay
    #rounded_delays = np.array([round_to_nearest_8ns(delay) for delay in delays])
    #print("rounded_delays=")
    #print(rounded_delays)



    # Create sequences using the non-integer delays
    sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]

    # old one has integer value of delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]

    # Add all the sequences together
    result_sequence = sum(sequences[1:], sequences[0])
    ps.stream(result_sequence)  # runs forever , but returns program



def rabi(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_ns,n_repeats,number_of_cycles,ps):
         

    #mw_pulse_length_start_ns=0
    #mw_pulse_length_stop_ns=3e-6*1e-9
    #mw_pulse_length_number_of_points=10

    # As fig 4 teaching paper
    # Generate non-integer microwave pulse times
    mw_pulse_lengths_ns = np.linspace(mw_pulse_length_start_ns, mw_pulse_length_stop_ns, mw_pulse_length_number_of_points)
    print("mw_pulse_lengths_ns=")
    print(mw_pulse_lengths_ns)

    # Apply the rounding function to each delay
    #rounded_delays = np.array([round_to_nearest_8ns(delay) for delay in delays])
    #print("rounded_delays=")
    #print(rounded_delays)

    # Create sequences using the non-integer delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]


    sequences= [create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_ns,tau_padding_ns,n_repeats,number_of_cycles,ps)for mw_pulse_length_ns in mw_pulse_lengths_ns]


    # old one has integer value of delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]

    # Add all the sequences together
    result_sequence = sum(sequences[1:], sequences[0])
    ps.stream(result_sequence)  # runs forever , but returns program



def rabi_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_ns,n_repeats,number_of_cycles,ps):
         

    #mw_pulse_length_start_ns=0
    #mw_pulse_length_stop_ns=3e-6*1e-9
    #mw_pulse_length_number_of_points=10

    # As fig 4 teaching paper
    # Generate non-integer microwave pulse times
    mw_pulse_lengths_ns = np.linspace(mw_pulse_length_start_ns, mw_pulse_length_stop_ns, mw_pulse_length_number_of_points)
    print("mw_pulse_lengths_ns=")
    print(mw_pulse_lengths_ns)

    # Apply the rounding function to each delay
    #rounded_delays = np.array([round_to_nearest_8ns(delay) for delay in delays])
    #print("rounded_delays=")
    #print(rounded_delays)

    # Create sequences using the non-integer delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]


    sequences= [create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_ns,tau_padding_ns,n_repeats,number_of_cycles,ps)for mw_pulse_length_ns in mw_pulse_lengths_ns]


    # old one has integer value of delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]

    # Add all the sequences together
    result_sequence = sum(sequences[1:], sequences[0])
    #ps.stream(result_sequence)  # runs forever , but returns program
    return sequences


def do_it_all_different_init_and_readout_pulsewidth(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,tau_readout_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps):


    # tau_readout_ns is the readout pulse width
    # tau_i_ns is the intitialization pulse width
    # Generate non-integer delays
    delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
    print("delays=")
    print(delays)

    # Apply the rounding function to each delay
    #rounded_delays = np.array([round_to_nearest_8ns(delay) for delay in delays])
    #print("rounded_delays=")
    #print(rounded_delays)



    # Create sequences using the non-integer delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]
    sequences = [create_fig3_teachingpaper_pulse_sequence_repeated_different_init_and_readout_pulsewidth(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns,tau_readout_ns, delay*1e9, number_of_cycles, ps) for delay in delays]


    # old one has integer value of delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]

    # Add all the sequences together
    result_sequence = sum(sequences[1:], sequences[0])
    ps.stream(result_sequence)  # runs forever , but returns program



def do_it_all_no_init(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,number_of_cycles,delay_start_s,delay_stop_s,delay_number_of_points,ps):

    # no intialization pulse
    # Generate non-integer delays
    delays = np.linspace(delay_start_s, delay_stop_s, delay_number_of_points)
    print("delays=")
    print(delays)

    # Apply the rounding function to each delay
    #rounded_delays = np.array([round_to_nearest_8ns(delay) for delay in delays])
    #print("rounded_delays=")
    #print(rounded_delays)



    # Create sequences using the non-integer delays
    sequences = [create_fig3_teachingpaper_pulse_sequence_repeated_no_init_pulse(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]

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

def create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, n):
    #round_to_nearest_8ns(value)
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_i_ns_rounded=round_to_nearest_8ns(tau_i_ns)
    tau_delay_ns_rounded=round_to_nearest_8ns(tau_delay_ns)
    
    pattern = [
        (tau_i_ns_rounded, 1), 
        ((tau_ref_ns_rounded - tau_i_ns_rounded), 0), 
        (tau_i_ns_rounded, 1), 
        (tau_delay_ns_rounded, 0), 
        (tau_i_ns_rounded, 1), 
        ((tau_ref_ns_rounded - 2 * tau_i_ns_rounded - tau_delay_ns_rounded), 0)
    ]
    
    pattern_array = pattern * n
    return pattern_array

def create_fig_4_laser_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_ns, n_repeat,n):

    #round_to_nearest_8ns(value)
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
    tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
    tau_padding_ns_rounded=round_to_nearest_8ns(tau_padding_ns)
    
    pattern_1_subunit = [
        (tau_laser_ns_rounded, 1), 
        (tau_mw_ns_rounded, 0)
    ]
    
    # there is still a large 0 here
    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns_rounded+tau_mw_ns_rounded)
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]

    pattern_1=pattern_1_subunit*n_repeat + pattern_1_end
    
    pattern_2_subunit = [
        (tau_laser_ns_rounded, 1), 
        (tau_mw_ns_rounded, 0)
    ]
    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeat + pattern_2_end
    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * n
    return pattern_array


def create_fig_4_mw_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_ns, n_repeat,n):

    #round_to_nearest_8ns(value)
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
    tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
    tau_padding_ns_rounded=round_to_nearest_8ns(tau_padding_ns)
    
    pattern_1_subunit = [
        (tau_laser_ns_rounded, 0), 
        (tau_mw_ns_rounded, 1)
    ]
    
       
    # there is still a large 0 here
    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns_rounded+tau_mw_ns_rounded)
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    
    
    pattern_1=pattern_1_subunit*n_repeat+pattern_1_end
    
    pattern_2_subunit = [
        (tau_laser_ns_rounded, 0), 
        (tau_mw_ns_rounded, 0)
    ]
    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeat + pattern_2_end

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * n
    return pattern_array


def create_pattern_array_rounded_to_8_ns_different_init_and_readout_pulsewidth(tau_ref_ns, tau_i_ns, tau_readout_ns,tau_delay_ns, n):
    #round_to_nearest_8ns(value)
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_i_ns_rounded=round_to_nearest_8ns(tau_i_ns)
    tau_delay_ns_rounded=round_to_nearest_8ns(tau_delay_ns)
    tau_readout_ns_rounded=round_to_nearest_8ns(tau_readout_ns)
    
    pattern = [
        (tau_i_ns_rounded, 1), 
        ((tau_ref_ns_rounded - tau_i_ns_rounded), 0), 
        (tau_i_ns_rounded, 1), 
        (tau_delay_ns_rounded, 0), 
        (tau_readout_ns_rounded, 1), 
        ((tau_ref_ns_rounded -  tau_i_ns_rounded -tau_readout_ns_rounded- tau_delay_ns_rounded), 0)
    ]
    
    pattern_array = pattern * n
    return pattern_array

def create_pattern_array__no_init_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, n):
    #round_to_nearest_8ns(value)
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_i_ns_rounded=round_to_nearest_8ns(tau_i_ns)
    tau_delay_ns_rounded=round_to_nearest_8ns(tau_delay_ns)
    

    pattern_no_init = [
        ((tau_ref_ns_rounded+tau_i_ns_rounded+tau_delay_ns_rounded), 0), 
        (tau_i_ns_rounded, 1), 
        (2*tau_ref_ns_rounded - (tau_ref_ns_rounded+tau_i_ns_rounded+tau_delay_ns_rounded+tau_i_ns_rounded), 0)
    ]
    pattern_array = pattern_no_init * n
    return pattern_array

def sum_first_elements(pattern):
    """
    Calculate the sum of all the first elements in a list of pairs.

    Parameters:
    pattern (list of tuples): A list of pairs (tuples) where the first element is a float and the second element is an integer.

    Returns:
    float: The sum of all the first elements of the pairs.
    """
    return sum(pair[0] for pair in pattern)

    # Example usage:
    #example_pattern = [(1000.0, 1), (14999000.0, 0), (1000.0, 1), (100000.0, 0), (1000.0, 1), (14898000.0, 0)]
    #print(sum_first_elements(example_pattern))
    
     
     
     
     
def round_to_nearest_8ns(value_in_ns):
     # Function to round each delay to the nearest multiple of 8 ns
    ns_per_step = 8  # 8 nanoseconds
    return int( round(value_in_ns / ns_per_step) * ns_per_step   )