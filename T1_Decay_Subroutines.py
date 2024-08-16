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
import os
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD
from datetime import datetime, timedelta
import time
import numpy as np

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


def create_fig4_teachingpaper_pulse_sequence(tau_ref_ns,tau_laser_ns,tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,ps: PulseStreamer):
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
    
 
    pulse_patt_decay_laser= create_fig_4_laser_pattern_array_rounded_to_8_ns_version_2(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeats,1)

    seq.setDigital(1,pulse_patt_decay_laser) 
    
    # Set channel 2 as the microwave pulse sequence (pulse duration in nanoseconds)
    pulse_patt_decay_mw = create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeats,1)
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

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_ref=")
    #print(pulse_patt_ref)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_decay=")
    #print(pulse_patt_decay)
    #print("---------------------------------------------------")
    #print(pulse_patt_decay)
    seq.setDigital(channel_number_pulse, pulse_patt_decay)

    return seq



def create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,number_of_cycles,ps: PulseStreamer):
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
    #print("create_fig4_teachingpaper_pulse_sequence_repeated: Creating sequence for mw_pulse_length_ns=",mw_pulse_length_ns)
    
    #************* SQUAREWAVE FIRST*******************
    
    # pulse_patt = [(100, 0), (200, 1), (80, 0), (300, 1), (60, 0)]

    square_wave_half_cycle_ns=tau_ref_ns

    pulse_patt_ref = generate_alternating_pairs(square_wave_half_cycle_ns,2*number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("create_fig4_teachingpaper_pulse_sequence_repeated: pulse_patt_ref sum=",sum_first_elements(pulse_patt_ref)/1e9)

    #print("---------------------------------------------------")
    #print("pulse_patt_ref=")
    #print(pulse_patt_ref)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    # n_repeats is 250 if fixed mw pulse
    # But under variable microwave pulse, ???
    #*********** THEN PULSE CYCLE LASER***********************
    pulse_patt_laser = create_fig_4_laser_pattern_array_rounded_to_8_ns_version_2(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeats,number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("create_fig4_teachingpaper_pulse_sequence_repeated: pulse_patt_laser sum=",sum_first_elements(pulse_patt_laser)/1e9)
    #print(pulse_patt_laser)
    seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)
    
    #*********** THEN PULSE CYCLE MW***********************

    
    pulse_patt_mw = create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeats,number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("create_fig4_teachingpaper_pulse_sequence_repeated: pulse_patt_mw sum=",sum_first_elements(pulse_patt_mw)/1e9)
    #print(pulse_patt_mw)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_mw_pulse, pulse_patt_mw)

    return seq



def create_fig5_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
                                                    tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    n_repeats,number_of_cycles,ps):

    # Creates pattern in fig 5 of teaching paper
    # ps is the pulsestreamer object
    # xxx tau_mw_ns=mw_pulse_length_ns

    # Create sequence object 
    seq = ps.createSequence()
    
    #************* SQUAREWAVE FIRST*******************
    square_wave_half_cycle_ns=tau_ref_ns
    pulse_patt_ref = generate_alternating_pairs(square_wave_half_cycle_ns,2*number_of_cycles)
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    #*********** THEN PULSE CYCLE LASER***********************
    pulse_patt_laser = create_fig_5_laser_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    n_repeats,number_of_cycles)
    seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)

    #*********** THEN PULSE CYCLE MW X***********************
    pulse_patt_mw_X = create_fig_5_mw_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    n_repeats,number_of_cycles)

    seq.setDigital(channel_number_mw_pulse, pulse_patt_mw_X)

        # abc

    #*********** THEN PULSE CYCLE MW Y***********************
    pulse_patt_mw_Y = create_fig_5_mw_Y_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    n_repeats,number_of_cycles)

    seq.setDigital(channel_number_mw_phaseshifted_pulse, pulse_patt_mw_Y)

    return seq

def create_fig6_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
                                                    tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    N_CPMG,
                                                    n_repeats,number_of_cycles,ps):

    # Creates pattern in fig 5 of teaching paper
    # ps is the pulsestreamer object
    # xxx tau_mw_ns=mw_pulse_length_ns

    # Create sequence object 
    seq = ps.createSequence()
    
    #************* SQUAREWAVE FIRST*******************
    square_wave_half_cycle_ns=tau_ref_ns
    pulse_patt_ref = generate_alternating_pairs(square_wave_half_cycle_ns,2*number_of_cycles)
    seq.setDigital(channel_number_ref, pulse_patt_ref)

    # abc
    #*********** THEN PULSE CYCLE LASER***********************
    pulse_patt_laser = create_fig_6_laser_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    N_CPMG,
                                                    n_repeats,number_of_cycles)
    seq.setDigital(channel_number_laser_pulse, pulse_patt_laser)

    #*********** THEN PULSE CYCLE MW X***********************
    pulse_patt_mw_X = create_fig_6_mw_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    N_CPMG,
                                                    n_repeats,number_of_cycles)

    seq.setDigital(channel_number_mw_pulse, pulse_patt_mw_X)


    #*********** THEN PULSE CYCLE MW Y***********************
    pulse_patt_mw_Y = create_fig_6_mw_Y_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    N_CPMG,
                                                    n_repeats,number_of_cycles)

    seq.setDigital(channel_number_mw_phaseshifted_pulse, pulse_patt_mw_Y)

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

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_ref=")
    #print(pulse_patt_ref)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    pulse_patt_decay = create_pattern_array_rounded_to_8_ns_different_init_and_readout_pulsewidth(tau_ref_ns, tau_i_ns,tau_readout_ns, tau_delay_ns, number_of_cycles)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_decay=")
    #print(pulse_patt_decay)
    #print("---------------------------------------------------")
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

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_ref=")
    #print(pulse_patt_ref)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    pulse_patt_decay = create_pattern_array__no_init_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_decay=")
    #print(pulse_patt_decay)
    #print("---------------------------------------------------")
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

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_ref=")
    #print(pulse_patt_ref)
    #print("---------------------------------------------------")
    seq.setDigital(channel_number_ref, pulse_patt_ref)


    
    #*********** THEN PULSE CYCLE
    

    #pulse_patt_decay = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    
    #pulse_patt_decay = create_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    pulse_patt_decay = create_pattern_array__no_init_rounded_to_8_ns(tau_ref_ns, tau_i_ns, tau_delay_ns, number_of_cycles)
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("pulse_patt_decay sum=",sum_first_elements(pulse_patt_decay))
    #print("pulse_patt_decay sum divided by 8 ns=",sum_first_elements(pulse_patt_decay)/8)
    
    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

    #print("---------------------------------------------------")
    #print("tau_delay_ns=",tau_delay_ns)
    #print("pulse_patt_decay=")
    #print(pulse_patt_decay)
    #print("---------------------------------------------------")
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



def rabi_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_start_ns,mw_pulse_length_stop_ns,mw_pulse_length_number_of_points,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,number_of_cycles,ps):
         

    #mw_pulse_length_start_ns=0
    #mw_pulse_length_stop_ns=3e-6*1e-9
    #mw_pulse_length_number_of_points=10

    # As fig 4 teaching paper
    # Generate non-integer microwave pulse times
    mw_pulse_lengths_ns = np.linspace(mw_pulse_length_start_ns, mw_pulse_length_stop_ns, mw_pulse_length_number_of_points)
    mw_pulse_lengths_ns = np.round(mw_pulse_lengths_ns).astype(int)
    print("rabi_many_sequences: mw_pulse_lengths_ns=")
    print(mw_pulse_lengths_ns)




    # Apply the rounding function to each delay
    #rounded_delays = np.array([round_to_nearest_8ns(delay) for delay in delays])
    #print("rounded_delays=")
    #print(rounded_delays)

    # Create sequences using the non-integer delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref, channel_number_pulse, tau_ref_ns, tau_i_ns, delay*1e9, number_of_cycles, ps) for delay in delays]


    sequences= [create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,number_of_cycles,ps)for mw_pulse_length_ns in mw_pulse_lengths_ns]


    # old one has integer value of delays
    #sequences = [create_fig3_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_pulse,tau_ref_ns,tau_i_ns,delay*1e-3*1e9,number_of_cycles,ps) for delay in range(1, 11)]

    # Add all the sequences together
    result_sequence = sum(sequences[1:], sequences[0])
    #ps.stream(result_sequence)  # runs forever , but returns program
    return sequences


def Hahn_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
                        tau_ref_ns,tau_laser_ns,
                        tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                        mw_T_delay_length_start_ns,mw_T_delay_length_stop_ns,mw_T_delay_length_number_of_points,
                        tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                        n_repeats,number_of_cycles,ps):
    
    
    
    
    # Fig 5 of teaching paper         
    # Generate non-integer delays
    mw_T_delay_lengths_ns =  np.linspace(mw_T_delay_length_start_ns, mw_T_delay_length_stop_ns, mw_T_delay_length_number_of_points)
    mw_T_delay_lengths_ns = np.round(mw_T_delay_lengths_ns).astype(int)
    print("T1_Decay_Synchronized.py: mw_T_delay_lengths_ns=")
    print(mw_T_delay_lengths_ns)


    #sequences= [create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,number_of_cycles,ps)for mw_pulse_length_ns in mw_pulse_lengths_ns]

    sequences= [create_fig5_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
                                                                tau_ref_ns,tau_laser_ns,
                                                                tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                                mw_T_delay_length_ns,
                                                                tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                                n_repeats,number_of_cycles,ps)
                for mw_T_delay_length_ns in mw_T_delay_lengths_ns]

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


def CPMG_many_sequences(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
                        tau_ref_ns,tau_laser_ns,
                        tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                        mw_T_delay_length_start_ns,mw_T_delay_length_stop_ns,mw_T_delay_length_number_of_points,
                        tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                        N_CPMG,
                        n_repeats,number_of_cycles,ps):
    
    
    
    
    # Fig 5 of teaching paper         
    # Generate non-integer delays
    mw_T_delay_lengths_ns =  np.linspace(mw_T_delay_length_start_ns, mw_T_delay_length_stop_ns, mw_T_delay_length_number_of_points)
    mw_T_delay_lengths_ns = np.round(mw_T_delay_lengths_ns).astype(int)
    print("T1_Decay_Synchronized.py: mw_T_delay_lengths_ns=")
    print(mw_T_delay_lengths_ns)


    #sequences= [create_fig4_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,tau_ref_ns,tau_laser_ns,mw_pulse_length_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns,n_repeats,number_of_cycles,ps)for mw_pulse_length_ns in mw_pulse_lengths_ns]

    sequences= [create_fig6_teachingpaper_pulse_sequence_repeated(channel_number_ref,channel_number_laser_pulse,channel_number_mw_pulse,channel_number_mw_phaseshifted_pulse,
                                                                tau_ref_ns,tau_laser_ns,
                                                                tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                                mw_T_delay_length_ns,
                                                                tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                                N_CPMG,
                                                                n_repeats,number_of_cycles,ps)
                for mw_T_delay_length_ns in mw_T_delay_lengths_ns]

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

def create_fig_4_laser_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeat,n):

    #round_to_nearest_8ns(value)
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
    tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
    #tau_padding_ns_rounded=round_to_nearest_8ns(tau_padding_ns)
    tau_padding_before_ns_rounded=round_to_nearest_8ns(tau_padding_before_mw_ns)
    tau_padding_after_ns_rounded=round_to_nearest_8ns(tau_padding_after_mw_ns)
    
    
    
    
    pattern_1_subunit = [
        (tau_laser_ns_rounded, 1), 
        ((tau_padding_before_ns_rounded+tau_mw_ns_rounded+tau_padding_after_ns_rounded), 0)
    ]
    # there is still a large 0 here
    # if pattern_1_end_time_ns<0 print error, too many repeats!
    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns_rounded+tau_mw_ns_rounded+tau_padding_before_ns_rounded+tau_padding_after_ns_rounded)
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")

    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]

    pattern_1=pattern_1_subunit*n_repeat + pattern_1_end
    
    pattern_2_subunit = [
        (tau_laser_ns_rounded, 1), 
        (tau_mw_ns_rounded+tau_padding_before_ns_rounded+tau_padding_after_ns_rounded, 0)
    ]

    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeat + pattern_2_end
    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * n

    return pattern_array

def create_fig_4_laser_pattern_array_rounded_to_8_ns_version_2(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeat,n):

    #round_to_nearest_8ns(value)
    # only round the total wavetime to 8 ns, not each individual component
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
    tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
    #tau_padding_ns_rounded=round_to_nearest_8ns(tau_padding_ns)
    tau_padding_before_ns_rounded=round_to_nearest_8ns(tau_padding_before_mw_ns)
    tau_padding_after_ns_rounded=round_to_nearest_8ns(tau_padding_after_mw_ns)
    tau_mw_ns_int=int(tau_mw_ns)
    
    
    # Internally, the Pulse Streamer hardware is always splitting the sequence data into 8 nanosecond long chunks. When a sequence is shorter than 8 ns or its length is not an exact multiple of 8 ns the extra time will be padded to complete the last chunk. You can observe the effects of such padding if you try to stream a short pulse repetitively.
    #https://www.swabianinstruments.com/static/documentation/PulseStreamer/sections/api-doc.html
    
    # PJB 8/14/2024 We will only use tau_ref_ns_rounded since this will ensure each cycle is 8 ns multiples. The white space at the end will assure this.
    # Anyways, Tref is usually  2.5 ms or 15 ms, so an 8 ns round will not matter.


    pattern_1_subunit = [
        (tau_laser_ns, 1), 
        ((tau_padding_before_mw_ns+tau_mw_ns_int+tau_padding_after_mw_ns), 0)
    ]
    # there is still a large 0 here
    # if pattern_1_end_time_ns<0 print error, too many repeats!
    pattern_1_end_time_ns=tau_ref_ns-n_repeat*(tau_laser_ns+tau_mw_ns_int+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")

    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]

    pattern_1=pattern_1_subunit*n_repeat + pattern_1_end
    
    pattern_2_subunit = [
        (tau_laser_ns, 1), 
        ((tau_padding_before_mw_ns+tau_mw_ns_int+tau_padding_after_mw_ns), 0)
    ]

    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeat + pattern_2_end
    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * n
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_laser_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print(f"tau_mw_ns = {tau_mw_ns}")
        print(f"tau_padding_before_mw_ns = {tau_padding_before_mw_ns}")
        print(f"tau_padding_after_mw_ns = {tau_padding_after_mw_ns}")
        print(f"n_repeat = {n_repeat}")
        print(f"n = {n}")
    return pattern_array


def    create_fig_5_laser_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    n_repeats,number_of_cycles):


    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)


    tau_laser_off_time_subunit= tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns+mw_T_delay_length_ns+tau_mw_X_pi_ns+mw_T_delay_length_ns+tau_mw_Y_pi_ns+tau_padding_after_mw_pi_over_2_ns
    # off time of laser before it is on again

    pattern_1_subunit = [
        (tau_laser_ns, 1), 
        ((tau_laser_off_time_subunit), 0)
    ]
    # there is still a large 0 here
    # if pattern_1_end_time_ns<0 print error, too many repeats!
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*(
        tau_laser_ns+tau_laser_off_time_subunit
        )
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")

    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]

    pattern_1=pattern_1_subunit*n_repeats + pattern_1_end
    
    pattern_2_subunit = [
        (tau_laser_ns, 1), 
        ((tau_laser_off_time_subunit), 0)
    ]

    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeats + pattern_2_end
    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_laser_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("create_fig_5_laser_pattern_array: Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print(f"n_repeat = {n_repeats}")
        print(f"number_of_cycles = {number_of_cycles}")
    return pattern_array


def  create_fig_5_mw_pattern_array(tau_ref_ns,tau_laser_ns,
                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                    mw_T_delay_length_ns,
                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                    n_repeats,number_of_cycles):

    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)
    
    pattern_1_subunit = [
        (tau_laser_ns+tau_padding_before_mw_pi_over_2_ns, 0), 
        (tau_mw_X_pi_over_2_ns, 1),
        (mw_T_delay_length_ns,0),
        (tau_mw_X_pi_ns, 1),
        (mw_T_delay_length_ns,0),
        (tau_mw_X_pi_over_2_ns, 1),
        (tau_padding_after_mw_pi_over_2_ns,0)
    ]
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    print("create_fig_5_mw_pattern_array:total_time=",total_time)
   
           
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeats+pattern_1_end # this may not be a multiple of 8 ns:

    pattern_1_total_time = sum(pair[0] for pair in pattern_1)
    print("create_fig_5_mw_pattern_array:pattern_1_total_time=",pattern_1_total_time)
    
    # Now do second half of pattern (all MW off)
    
    tau_laser_off_time_subunit= tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns+mw_T_delay_length_ns+tau_mw_X_pi_ns+tau_mw_Y_pi_ns+tau_padding_after_mw_pi_over_2_ns
    # off time of laser before it is on again

    pattern_2_subunit = [
        (tau_laser_ns+tau_laser_off_time_subunit, 0)
    ]

    total_time = sum(pair[0] for pair in pattern_2_subunit)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern_2_subunit + [(padding_needed, 0)]
    
    pattern_2_subunit = adjusted_pattern
    
    
    pattern_2_end = pattern_1_end
    
    pattern_2=[
        (tau_ref_ns,0)
    ]
    # tau_ref off
    

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")


    #print(f"Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("#################### create_fig_4_mw_pattern_array_rounded_to_8_ns")            
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print("####################")            
        pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
        pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
        pattern_1_length_ns = sum(time for time, _ in pattern_1)
        print(f"pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
        
        print(f"pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

        print(f"pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
        print(f"pattern_1_length_ns: {pattern_1_length_ns} ns")
        print("####################")            
        

    


    return pattern_array

def  create_fig_5_mw_Y_pattern_array(tau_ref_ns,tau_laser_ns,
                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                    mw_T_delay_length_ns,
                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                    n_repeats,number_of_cycles):

    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)
    
    pattern_1_subunit = [
        (tau_laser_ns+tau_padding_before_mw_pi_over_2_ns, 0), 
        (tau_mw_X_pi_over_2_ns, 0),
        (mw_T_delay_length_ns,0),
        (tau_mw_Y_pi_ns, 1),
        (mw_T_delay_length_ns,0),
        (tau_mw_X_pi_over_2_ns, 0),
        (tau_padding_after_mw_pi_over_2_ns,0)
    ]
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    print("create_fig_5_mw_pattern_array:total_time=",total_time)
   
           
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeats+pattern_1_end # this may not be a multiple of 8 ns:

    pattern_1_total_time = sum(pair[0] for pair in pattern_1)
    print("create_fig_5_mw_pattern_array:pattern_1_total_time=",pattern_1_total_time)
    
    # Now do second half of pattern (all MW off)
    
    tau_laser_off_time_subunit= tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns+mw_T_delay_length_ns+tau_mw_X_pi_ns+tau_mw_Y_pi_ns+tau_padding_after_mw_pi_over_2_ns
    # off time of laser before it is on again

    pattern_2_subunit = [
        (tau_laser_ns+tau_laser_off_time_subunit, 0)
    ]

    total_time = sum(pair[0] for pair in pattern_2_subunit)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern_2_subunit + [(padding_needed, 0)]
    
    pattern_2_subunit = adjusted_pattern
    
    
    pattern_2_end = pattern_1_end
    
    pattern_2=[
        (tau_ref_ns,0)
    ]
    # tau_ref off
    

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")


    #print(f"Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("#################### create_fig_4_mw_pattern_array_rounded_to_8_ns")            
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print("####################")            
        pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
        pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
        pattern_1_length_ns = sum(time for time, _ in pattern_1)
        print(f"pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
        
        print(f"pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

        print(f"pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
        print(f"pattern_1_length_ns: {pattern_1_length_ns} ns")
        print("####################")            
        

    


    return pattern_array


def    create_fig_6_laser_pattern_arrayold(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    N_CPMG,
                                                    n_repeats,number_of_cycles):


    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)


    tau_laser_off_time_subunit= tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns+mw_T_delay_length_ns+tau_mw_X_pi_ns+mw_T_delay_length_ns+tau_mw_Y_pi_ns+tau_padding_after_mw_pi_over_2_ns
    # off time of laser before it is on again

    pattern_1_subunit = [
        (tau_laser_ns, 1), 
        ((tau_laser_off_time_subunit), 0)
    ]
    # there is still a large 0 here
    # if pattern_1_end_time_ns<0 print error, too many repeats!
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*(
        tau_laser_ns+tau_laser_off_time_subunit
        )
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")

    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]

    pattern_1=pattern_1_subunit*n_repeats + pattern_1_end
    
    pattern_2_subunit = [
        (tau_laser_ns, 1), 
        ((tau_laser_off_time_subunit), 0)
    ]

    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeats + pattern_2_end
    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_laser_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("create_fig_5_laser_pattern_array: Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print(f"n_repeat = {n_repeats}")
        print(f"number_of_cycles = {number_of_cycles}")
    return pattern_array



def    create_fig_6_laser_pattern_array(tau_ref_ns,tau_laser_ns,
                                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                                    mw_T_delay_length_ns,
                                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                                    N_CPMG,
                                                    n_repeats,number_of_cycles):


    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)
    mw_T_delay_length_ns_over_2=int(mw_T_delay_length_ns/2)


   
    pattern_1_subunit_before_CPMG = [
        (tau_laser_ns, 1), 
        (tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns, 0)
    ]
    blank_time_pattern_1_subunit_during_CPMG_single_focus= mw_T_delay_length_ns_over_2 + tau_mw_Y_pi_ns + mw_T_delay_length_ns + tau_mw_Y_pi_ns + mw_T_delay_length_ns_over_2
    pattern_1_subunit_during_CPMG_single_focus = [
        (blank_time_pattern_1_subunit_during_CPMG_single_focus, 0) 
    ]
    pattern_1_subunit_during_CPMG = N_CPMG*pattern_1_subunit_during_CPMG_single_focus
    
    pattern_1_subunit_after_CPMG = [
        (tau_mw_X_pi_over_2_ns, 0),
        (tau_padding_after_mw_pi_over_2_ns,0)
    ]

    pattern_1_subunit = pattern_1_subunit_before_CPMG + pattern_1_subunit_during_CPMG + pattern_1_subunit_after_CPMG
    print("create_fig_6_mw_pattern_array:pattern_1_subunit=")
    print(pattern_1_subunit)
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    print("create_fig_5_mw_pattern_array:total_time=",total_time)
   
           
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeats+pattern_1_end # this may not be a multiple of 8 ns:

    pattern_1_total_time = sum(pair[0] for pair in pattern_1)
    print("create_fig_5_mw_pattern_array:pattern_1_total_time=",pattern_1_total_time)
    



#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    
    pattern = pattern_1 + pattern_1 # second cycle laser pattern is identical to first cycle
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_laser_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("create_fig_5_laser_pattern_array: Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print(f"n_repeat = {n_repeats}")
        print(f"number_of_cycles = {number_of_cycles}")
    return pattern_array




def  create_fig_6_mw_pattern_array(tau_ref_ns,tau_laser_ns,
                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                    mw_T_delay_length_ns,
                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                    N_CPMG,
                                    n_repeats,number_of_cycles):

    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)
    mw_T_delay_length_ns_over_2=int(mw_T_delay_length_ns/2)
    
    pattern_1_subunit_before_CPMG = [
        (tau_laser_ns+tau_padding_before_mw_pi_over_2_ns, 0), 
        (tau_mw_X_pi_over_2_ns, 1)
    ]
    blank_time_pattern_1_subunit_during_CPMG_single_focus= mw_T_delay_length_ns_over_2 + tau_mw_Y_pi_ns + mw_T_delay_length_ns + tau_mw_Y_pi_ns + mw_T_delay_length_ns_over_2
    pattern_1_subunit_during_CPMG_single_focus = [
        (blank_time_pattern_1_subunit_during_CPMG_single_focus, 0) 
    ]
    pattern_1_subunit_during_CPMG = N_CPMG*pattern_1_subunit_during_CPMG_single_focus
    
    pattern_1_subunit_after_CPMG = [
        (tau_mw_X_pi_over_2_ns, 1),
        (tau_padding_after_mw_pi_over_2_ns,0)
    ]

    pattern_1_subunit = pattern_1_subunit_before_CPMG + pattern_1_subunit_during_CPMG + pattern_1_subunit_after_CPMG
    print("create_fig_6_mw_pattern_array:pattern_1_subunit=")
    print(pattern_1_subunit)
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    print("create_fig_5_mw_pattern_array:total_time=",total_time)
   
           
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeats+pattern_1_end # this may not be a multiple of 8 ns:

    pattern_1_total_time = sum(pair[0] for pair in pattern_1)
    print("create_fig_5_mw_pattern_array:pattern_1_total_time=",pattern_1_total_time)
    
    # Now do second half of pattern (all MW off)
    
    tau_laser_off_time_subunit= tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns+mw_T_delay_length_ns+tau_mw_X_pi_ns+tau_mw_Y_pi_ns+tau_padding_after_mw_pi_over_2_ns
    # off time of laser before it is on again

    pattern_2_subunit = [
        (tau_laser_ns+tau_laser_off_time_subunit, 0)
    ]

    total_time = sum(pair[0] for pair in pattern_2_subunit)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern_2_subunit + [(padding_needed, 0)]
    
    pattern_2_subunit = adjusted_pattern
    
    
    pattern_2_end = pattern_1_end
    
    pattern_2=[
        (tau_ref_ns,0)
    ]
    # tau_ref off
    

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")


    #print(f"Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("#################### create_fig_4_mw_pattern_array_rounded_to_8_ns")            
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print("####################")            
        pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
        pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
        pattern_1_length_ns = sum(time for time, _ in pattern_1)
        print(f"pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
        
        print(f"pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

        print(f"pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
        print(f"pattern_1_length_ns: {pattern_1_length_ns} ns")
        print("####################")            
        

    


    return pattern_array



def  create_fig_6_mw_Y_pattern_array(tau_ref_ns,tau_laser_ns,
                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                    mw_T_delay_length_ns,
                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                    N_CPMG,
                                    n_repeats,number_of_cycles):

    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)
    mw_T_delay_length_ns_over_2=int(mw_T_delay_length_ns/2)
    
    pattern_1_subunit_before_CPMG = [
        (tau_laser_ns+tau_padding_before_mw_pi_over_2_ns, 0), 
        (tau_mw_X_pi_over_2_ns, 0)
    ]
    blank_time_pattern_1_subunit_during_CPMG_single_focus= mw_T_delay_length_ns_over_2 + tau_mw_Y_pi_ns + mw_T_delay_length_ns + tau_mw_Y_pi_ns + mw_T_delay_length_ns_over_2
    pattern_1_subunit_during_CPMG_single_focus = [
        (mw_T_delay_length_ns_over_2, 0), 
        (tau_mw_Y_pi_ns, 1), 
        (mw_T_delay_length_ns, 0), 
        (tau_mw_Y_pi_ns, 1), 
        (mw_T_delay_length_ns_over_2, 0) 
    ]
    pattern_1_subunit_during_CPMG = N_CPMG*pattern_1_subunit_during_CPMG_single_focus
    
    pattern_1_subunit_after_CPMG = [
        (tau_mw_X_pi_over_2_ns, 0),
        (tau_padding_after_mw_pi_over_2_ns,0)
    ]

    pattern_1_subunit = pattern_1_subunit_before_CPMG + pattern_1_subunit_during_CPMG + pattern_1_subunit_after_CPMG
    print("create_fig_6_mw_pattern_array:pattern_1_subunit=")
    print(pattern_1_subunit)
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    print("create_fig_5_mw_pattern_array:total_time=",total_time)
   
           
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeats+pattern_1_end # this may not be a multiple of 8 ns:

    pattern_1_total_time = sum(pair[0] for pair in pattern_1)
    print("create_fig_5_mw_pattern_array:pattern_1_total_time=",pattern_1_total_time)
    
    # Now do second half of pattern (all MW off)
    
    tau_laser_off_time_subunit= tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns+mw_T_delay_length_ns+tau_mw_X_pi_ns+tau_mw_Y_pi_ns+tau_padding_after_mw_pi_over_2_ns
    # off time of laser before it is on again

    pattern_2_subunit = [
        (tau_laser_ns+tau_laser_off_time_subunit, 0)
    ]

    total_time = sum(pair[0] for pair in pattern_2_subunit)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern_2_subunit + [(padding_needed, 0)]
    
    pattern_2_subunit = adjusted_pattern
    
    
    pattern_2_end = pattern_1_end
    
    pattern_2=[
        (tau_ref_ns,0)
    ]
    # tau_ref off
    

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")


    #print(f"Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("#################### create_fig_4_mw_pattern_array_rounded_to_8_ns")            
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print("####################")            
        pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
        pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
        pattern_1_length_ns = sum(time for time, _ in pattern_1)
        print(f"pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
        
        print(f"pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

        print(f"pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
        print(f"pattern_1_length_ns: {pattern_1_length_ns} ns")
        print("####################")            
        

    


    return pattern_array


def  create_fig_6_mw_Y_pattern_array_old(tau_ref_ns,tau_laser_ns,
                                    tau_mw_X_pi_over_2_ns,tau_mw_X_pi_ns,tau_mw_Y_pi_ns,
                                    mw_T_delay_length_ns,
                                    tau_padding_before_mw_pi_over_2_ns,tau_padding_after_mw_pi_over_2_ns,
                                    N_CPMG,
                                    n_repeats,number_of_cycles):

    # round all to integers ns so the 8 ns thing goes away hopefully
    tau_mw_X_pi_over_2_ns=int(tau_mw_X_pi_over_2_ns)
    tau_mw_X_pi_ns=int(tau_mw_X_pi_ns)
    tau_mw_Y_pi_ns=int(tau_mw_Y_pi_ns)
    mw_T_delay_length_ns=int(mw_T_delay_length_ns)
    tau_padding_before_mw_pi_over_2_ns=int(tau_padding_before_mw_pi_over_2_ns)
    tau_padding_after_mw_pi_over_2_ns=int(tau_padding_after_mw_pi_over_2_ns)
    
    pattern_1_subunit = [
        (tau_laser_ns+tau_padding_before_mw_pi_over_2_ns, 0), 
        (tau_mw_X_pi_over_2_ns, 0),
        (mw_T_delay_length_ns,0),
        (tau_mw_Y_pi_ns, 1),
        (mw_T_delay_length_ns,0),
        (tau_mw_X_pi_over_2_ns, 0),
        (tau_padding_after_mw_pi_over_2_ns,0)
    ]
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    print("create_fig_5_mw_pattern_array:total_time=",total_time)
   
           
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns-n_repeats*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeats+pattern_1_end # this may not be a multiple of 8 ns:

    pattern_1_total_time = sum(pair[0] for pair in pattern_1)
    print("create_fig_5_mw_pattern_array:pattern_1_total_time=",pattern_1_total_time)
    
    # Now do second half of pattern (all MW off)
    
    tau_laser_off_time_subunit= tau_padding_before_mw_pi_over_2_ns+tau_mw_X_pi_over_2_ns+mw_T_delay_length_ns+tau_mw_X_pi_ns+tau_mw_Y_pi_ns+tau_padding_after_mw_pi_over_2_ns
    # off time of laser before it is on again

    pattern_2_subunit = [
        (tau_laser_ns+tau_laser_off_time_subunit, 0)
    ]

    total_time = sum(pair[0] for pair in pattern_2_subunit)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern_2_subunit + [(padding_needed, 0)]
    
    pattern_2_subunit = adjusted_pattern
    
    
    pattern_2_end = pattern_1_end
    
    pattern_2=[
        (tau_ref_ns,0)
    ]
    # tau_ref off
    

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * number_of_cycles
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")


    #print(f"Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("#################### create_fig_4_mw_pattern_array_rounded_to_8_ns")            
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print("####################")            
        pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
        pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
        pattern_1_length_ns = sum(time for time, _ in pattern_1)
        print(f"pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
        
        print(f"pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

        print(f"pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
        print(f"pattern_1_length_ns: {pattern_1_length_ns} ns")
        print("####################")            
        

    


    return pattern_array

def create_fig_4_mw_pattern_array_rounded_to_8_ns(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeat,n):

    #round_to_nearest_8ns(value)
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
    tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
    #tau_padding_ns_rounded=round_to_nearest_8ns(tau_padding_ns)
    tau_padding_before_ns_rounded=round_to_nearest_8ns(tau_padding_before_mw_ns)
    tau_padding_after_ns_rounded=round_to_nearest_8ns(tau_padding_after_mw_ns)
    
    pattern_1_subunit = [
        (tau_laser_ns_rounded+tau_padding_before_ns_rounded, 0), 
        (tau_mw_ns_rounded, 1),
        (tau_padding_after_ns_rounded,0)
    ]
    
       
    # there is still a large 0 here
    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns_rounded+tau_mw_ns_rounded+tau_padding_before_ns_rounded+tau_padding_after_ns_rounded)
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeat+pattern_1_end
    
    pattern_2_subunit = [
        (tau_laser_ns_rounded+tau_padding_before_ns_rounded, 0), 
        (tau_mw_ns_rounded, 0),
        (tau_padding_after_ns_rounded,0)
    ]
    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeat + pattern_2_end

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * n
    

    return pattern_array

def create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeat,n):


    #round_to_nearest_8ns(value)
    # only round the total wavetime to 8 ns, not each individual component
    
    tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
    tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
    tau_mw_ns_int=int(tau_mw_ns)
    tau_padding_before_ns_rounded=round_to_nearest_8ns(tau_padding_before_mw_ns)
    tau_padding_after_ns_rounded=round_to_nearest_8ns(tau_padding_after_mw_ns)
    
    pattern_1_subunit = [ # maybe this needs to be an integral multiple of 8 ns
        (tau_laser_ns+tau_padding_before_mw_ns, 0), 
        (tau_mw_ns_int, 1),
        (tau_padding_after_mw_ns,0)
    ]
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_subunit xxx: {total_time} ns")
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    #padding_needed=int(padding_needed)
    # Append the required padding to the pattern
    adjusted_pattern = pattern_1_subunit + [(padding_needed, 0)]
    #print("create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: adjusted_pattern =")
    #print(adjusted_pattern)


    pattern_1_subunit = adjusted_pattern
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    
       
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns-n_repeat*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeat+pattern_1_end # this may not be a multiple of 8 ns:
    
    
    pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
    pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
    pattern_1_length_ns = sum(time for time, _ in pattern_1)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: n_repeat: {n_repeat} ")
    
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_length_ns: {pattern_1_length_ns} ns")

    
    
    
    # Internally, the Pulse Streamer hardware is always splitting the sequence data into 8 nanosecond long chunks. When a sequence is shorter than 8 ns or its length is not an exact multiple of 8 ns the extra time will be padded to complete the last chunk. You can observe the effects of such padding if you try to stream a short pulse repetitively.
    #https://www.swabianinstruments.com/static/documentation/PulseStreamer/sections/api-doc.html
    
    # PJB 8/14/2024 We will only use tau_ref_ns_rounded since this will ensure each cycle is 8 ns multiples. The white space at the end will assure this.
    # Anyways, Tref is usually  2.5 ms or 15 ms, so an 8 ns round will not matter.
    
    pattern_2_subunit = [
        (tau_laser_ns+tau_padding_before_mw_ns, 0), 
        (tau_mw_ns_int, 0),
        (tau_padding_after_mw_ns,0)
    ]

    total_time = sum(pair[0] for pair in pattern_2_subunit)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern_2_subunit + [(padding_needed, 0)]
    
    pattern_2_subunit = adjusted_pattern
    
    
    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeat + pattern_2_end

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * n
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    #print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")


    #print(f"Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("#################### create_fig_4_mw_pattern_array_rounded_to_8_ns")            
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print(f"tau_mw_ns = {tau_mw_ns}")
        print(f"tau_mw_ns_rounded_to_10ps = {tau_mw_ns_rounded_to_10ps}")
        print(f"tau_padding_before_mw_ns = {tau_padding_before_mw_ns}")
        print(f"tau_padding_after_mw_ns = {tau_padding_after_mw_ns}")
        print(f"n_repeat = {n_repeat}")
        print(f"n = {n}")
        print("####################")            
        pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
        pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
        pattern_1_length_ns = sum(time for time, _ in pattern_1)
        print(f"pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
        print(f"n_repeat: {n_repeat} ")
        
        print(f"pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

        print(f"pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
        print(f"pattern_1_length_ns: {pattern_1_length_ns} ns")
        print("####################")            
        

    


    return pattern_array

def create_fig_4_mw_pattern_array_rounded_to_8_ns_version_3(tau_ref_ns, tau_laser_ns, tau_mw_ns,tau_padding_before_mw_ns,tau_padding_after_mw_ns, n_repeat,n):

    #round_to_nearest_8ns(value)
    # only round the total wavetime to 8 ns, not each individual component
    # for testing purpsoses only to fix 8 ns bug
    tau_ref_ns_rounded=round_to_nearest_8ns(tau_ref_ns)
    
    
    tau_laser_ns_rounded=round_to_nearest_8ns(tau_laser_ns)
    tau_mw_ns_rounded=round_to_nearest_8ns(tau_mw_ns)
    tau_mw_ps=tau_mw_ns*1000
    tau_mw_ps_rounded_to_10ps=round(tau_mw_ps/10)*10
    tau_mw_ns_rounded_to_10ps=tau_mw_ps_rounded_to_10ps/1000 # need this to get even clean numbers due to finite precision of computer.
    # tau_mw_ns_rounded_to_10ps=tau_mw_ns_rounded # temporary bug test, yes it fixes 8 ns bug, but why???

    #tau_padding_ns_rounded=round_to_nearest_8ns(tau_padding_ns)
    tau_padding_before_ns_rounded=round_to_nearest_8ns(tau_padding_before_mw_ns)
    tau_padding_after_ns_rounded=round_to_nearest_8ns(tau_padding_after_mw_ns)
    
    pattern_1_subunit = [ # maybe this needs to be an integral multiple of 8 ns
        (tau_laser_ns+tau_padding_before_mw_ns, 0), 
        (tau_mw_ns_rounded_to_10ps, 1),
        (tau_padding_after_mw_ns,0)
    ]
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_subunit xxx: {total_time} ns")
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    #padding_needed=int(padding_needed)
    # Append the required padding to the pattern
    adjusted_pattern = pattern_1_subunit + [(padding_needed, 0)]
    print("create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: adjusted_pattern =")
    print(adjusted_pattern)


    pattern_1_subunit = adjusted_pattern
    total_time = sum(pair[0] for pair in pattern_1_subunit)
    
       
    # there is still a large 0 here
#    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*(tau_laser_ns+tau_mw_ns_rounded_to_10ps+tau_padding_before_mw_ns+tau_padding_after_mw_ns)
    pattern_1_end_time_ns=tau_ref_ns_rounded-n_repeat*total_time
    pattern_1_end=[
        (pattern_1_end_time_ns,0)
    ]
    if(pattern_1_end_time_ns<0):
        print("error, too many repeats!")
    
    pattern_1=pattern_1_subunit*n_repeat+pattern_1_end # this may not be a multiple of 8 ns:
    
    
    pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
    pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
    pattern_1_length_ns = sum(time for time, _ in pattern_1)
    print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
    print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: n_repeat: {n_repeat} ")
    
    print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

    print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
    print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2: pattern_1_length_ns: {pattern_1_length_ns} ns")

    
    
    
    # Internally, the Pulse Streamer hardware is always splitting the sequence data into 8 nanosecond long chunks. When a sequence is shorter than 8 ns or its length is not an exact multiple of 8 ns the extra time will be padded to complete the last chunk. You can observe the effects of such padding if you try to stream a short pulse repetitively.
    #https://www.swabianinstruments.com/static/documentation/PulseStreamer/sections/api-doc.html
    
    # PJB 8/14/2024 We will only use tau_ref_ns_rounded since this will ensure each cycle is 8 ns multiples. The white space at the end will assure this.
    # Anyways, Tref is usually  2.5 ms or 15 ms, so an 8 ns round will not matter.
    
    pattern_2_subunit = [
        (tau_laser_ns+tau_padding_before_mw_ns, 0), 
        (tau_mw_ns_rounded_to_10ps, 0),
        (tau_padding_after_mw_ns,0)
    ]

    total_time = sum(pair[0] for pair in pattern_2_subunit)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern_2_subunit + [(padding_needed, 0)]
    
    pattern_2_subunit = adjusted_pattern
    
    
    pattern_2_end = pattern_1_end
    
    pattern_2=pattern_2_subunit*n_repeat + pattern_2_end

    
    pattern = pattern_1 + pattern_2
    
    pattern_array = pattern * n
    # Calculate and print the total length in nanoseconds
    total_length_ns = sum(time for time, _ in pattern_array)
    print(f"create_fig_4_mw_pattern_array_rounded_to_8_ns_version_2 Total sequence length: {total_length_ns} ns")


    #print(f"Total sequence length: {total_length_ns} ns")
    # Check if the total length is a multiple of 8
    if total_length_ns % 8 != 0:
        print("#################### create_fig_4_mw_pattern_array_rounded_to_8_ns")            
        print("Error: Total sequence length is not a multiple of 8 ns")
        print(f"Total sequence length: {total_length_ns} ns")
        print("Function arguments:")
        print(f"tau_ref_ns = {tau_ref_ns}")
        print(f"tau_laser_ns = {tau_laser_ns}")
        print(f"tau_mw_ns = {tau_mw_ns}")
        print(f"tau_mw_ns_rounded_to_10ps = {tau_mw_ns_rounded_to_10ps}")
        print(f"tau_padding_before_mw_ns = {tau_padding_before_mw_ns}")
        print(f"tau_padding_after_mw_ns = {tau_padding_after_mw_ns}")
        print(f"n_repeat = {n_repeat}")
        print(f"n = {n}")
        print("####################")            
        pattern_1_subunit_length_ns = sum(time for time, _ in pattern_1_subunit)
        pattern_1_end_length_ns = sum(time for time, _ in pattern_1_end)
        pattern_1_length_ns = sum(time for time, _ in pattern_1)
        print(f"pattern_1_subunit_length_ns: {pattern_1_subunit_length_ns} ns")
        print(f"n_repeat: {n_repeat} ")
        
        print(f"pattern_1_subunit_length_ns *(n_repeat): {pattern_1_subunit_length_ns*n_repeat} ns")

        print(f"pattern_1_end_length_ns: {pattern_1_end_length_ns} ns")
        print(f"pattern_1_length_ns: {pattern_1_length_ns} ns")
        print("####################")            
        

    # temp create pattern_array 
    pattern_1_subunit = [ # maybe this needs to be an integral multiple of 8 ns
        (2.5e-3*1e9, 1), 
        (2.5e-3*1e9, 0) 
    ]


    pattern_1_subunit = [ # maybe this needs to be an integral multiple of 8 ns
        (5007, 1), 
        (19993, 0)
    ]
    pattern_1b_subunit = [ # maybe this needs to be an integral multiple of 8 ns
        (3204, 1)
    ]

    num_subunits=int(((2.5e-3)/(25000e-9)))
    print("num_subunits = ",num_subunits)
    #pattern_1=pattern_1_subunit*int(((2.5e-3)/(8e-9)))
    pattern_1=pattern_1_subunit*num_subunits
    pattern_2 = [ # maybe this needs to be an integral multiple of 8 ns
        (2.5e-3*1e9, 0) 
    ]
    # 356*7016=2497696
    #pattern_array=((pattern_1_subunit*356+pattern_1b_subunit)+pattern_2)*n
    pattern_array=(pattern_1+pattern_2)*n

    #print(pattern_array)

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



def chopped_odmr_srs_ds345(start_frequency=2670, stop_frequency=2690, step_size=1, step_time=1000, base_folder=r"C:\Users\BurkeLab\Desktop\072624"):
    # Peter Burke 7/26/2024
    # ChatGPT made this function from the python file chopped_odmr_srs_ds345.py
    # Peter Burke modified it
    # Example of how to call the function
    #chopped_odmr_srs_ds345()
    #You can call chopped_odmr_srs_ds345() with your desired parameters, and it will execute the same logic as the original script. If you need to change the parameters like #start_frequency, stop_frequency, etc., you can pass them as arguments to the function.
    def generate_unique_filename(base_folder):
        os.makedirs(base_folder, exist_ok=True)
        now = datetime.now()
        month = now.strftime('%m')
        day = now.strftime('%d')
        year = now.strftime('%y')
        existing_files = os.listdir(base_folder)
        file_number = 1
        while True:
            filename = f"{month}{day}{year}{file_number:04d}"
            if f"{filename}.csv" not in existing_files:
                break
            file_number += 1
        filepath = os.path.join(base_folder, f"{filename}.csv")
        return filepath

    plotname = generate_unique_filename(base_folder)
    print(f"Unique filename: {plotname}")

    #print("\n \t \t Qubit initialization Process; ODMR Single Plot \n \n")
    #print("\t \t Initializing Systems \n \n")

    handle = ljm.openS("ANY", "ANY")

    names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]
    aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
    num_Frames = len(names)
    ljm.eWriteNames(handle, num_Frames, names, aValues)

    numFrames = 2
    names = ["AIN0", "DAC0"]
    intervalHandle = 1

    synth = SynthHD("COM3")
    #print("\t \t Set Parameters \n \n")

    frequencies = [i * 1e6 for i in range(start_frequency, stop_frequency, step_size)]
    synth.write("sweep_freq_low", start_frequency)
    #print("Starting sweeping")
    synth.write("sweep_freq_high", stop_frequency)
    #print("Frequency high set")
    synth.write("sweep_freq_step", step_size)
    #print("Frequency step set")
    synth.write("sweep_time_step", step_time)
    #print("Frequency time set")

    current_time = datetime.now()
    print("Current time:", current_time.strftime("%Y-%m-%d %H:%M:%S"))

    number_of_elements = len(frequencies)
    #print("Number of elements in frequencies:", number_of_elements)
    time_to_complete_seconds = number_of_elements * step_time * 1e-3
    completion_time = current_time + timedelta(seconds=time_to_complete_seconds)
    print("Estimated completion time:", completion_time.strftime("%Y-%m-%d %H:%M:%S"))
    #print("Starting collecting")

    revised_steptime = step_time * 1000
    ljm.startInterval(intervalHandle, revised_steptime)

    intensities = []

    synth.write("sweep_single", True)
    #print("Actual sweep once true")

    j = 0
    while True:
        try:
            results = ljm.eReadNames(handle, numFrames, names)
            intensities.append(abs(results[0]))
            ljm.waitForNextInterval(intervalHandle)
            if stop_frequency - start_frequency != "infinite":
                j += 1
                if j >= stop_frequency - start_frequency:
                    break
        except KeyboardInterrupt:
            break
        except Exception:
            print(sys.exc_info()[1])
            break

    saved_dict = {
        "frequencies (Hz)": frequencies,
        "Labjack voltage (V)": intensities
    }

    df = pd.DataFrame(saved_dict)
    csv_filepath = plotname
    df.to_csv(csv_filepath, sep="\t")

    #plt.plot(frequencies, intensities)
    #plt.xlabel("Microwave Frequency (Hz)")
    #plt.ylabel("labjack voltage (V)")

    #plt.show()
    
    # Release the COM port and close LabJack handle
    synth.close()
    ljm.close(handle)
    print("COM port released and LabJack handle closed.")


