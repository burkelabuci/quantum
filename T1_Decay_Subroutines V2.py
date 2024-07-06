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

from pulsestreamer import PulseStreamer
import keyboard
import time 

def get_user_input(prompt, default):
    user_input = input(f"{prompt} (default {default}): ")
    return float(user_input) if user_input else default

def get_confirmation(prompt):
    while True:
        confirmation = input(f"{prompt} (yes/no): ").strip().lower()
        if confirmation in ['yes', 'no']:
            return confirmation == 'yes'
        print("Please answer with 'yes' or 'no'.")

def create_fig3_teachingpaper_pulse_sequence(tau_ref_ns,tau_i_ns,tau_delay_ns,ps: PulseStreamer):
    # Creates patter in fig 3 of teaching paper
    # ps is the pulsestreamer object
    # duration is how long the stream runs for in seconds

    #print("****************************************************************")
    #print("Start inside of create_fig3_teachingpaper_pulse_sequence ")
    #print("tau_ref_ns,tau_i_ns,tau_delay_ns=")
    #print(tau_ref_ns,tau_i_ns,tau_delay_ns)
    default_tau_ref = 15e-3
    default_tau_i = 1e-6
    default_tau_delay_start = 0.1e-3
    default_tau_delay_end = 5e-3
    default_tau_ref_ns = default_tau_ref*1e9
    default_tau_i_ns = default_tau_i *1e9
    default_tau_delay_start_ns = default_tau_delay_start*1e9
    default_tau_delay_end_ns = default_tau_delay_end*1e9
    
    # Create sequence object 
    seq = ps.createSequence()
    
    
    user_default = get_confirmation("Do you want to use the default tau_ref (15ms), initialization pulse (1 microseond), and the default delay time (from 0.1ms to 5 ms)?")
    if user_default:
        tau_ref_ns = default_tau_ref_ns
        tau_i_ns = default_tau_i_ns
        tau_delay_start_ns = default_tau_delay_start_ns
        tau_delay_end_ns= default_tau_delay_end_ns
    else:
        tau_ref = get_user_input("Enter tau_ref (reference time in seconds)", 15e-3)
        tau_i = get_user_input("Enter tau_i (pulse time in seconds)", 1e-6)
        tau_delay_start = get_user_input("Enter tau_delay_start (beginning of loop)", 0.1e-3)
        tau_delay_end = get_user_input("Enter tau_delay_end (end of loop)", 5e-3)
        tau_ref_ns = tau_ref*1e9
        tau_i_ns = tau_i*1e9
        tau_delay_start_ns = tau_delay_start*1e9
        tau_delay_end_ns = tau_delay_end*1e9


    print("\nSummary of your input:")
    print(f"tau_ref: {tau_ref} s, tau_ref_ns: {tau_ref_ns} ns")
    print(f"tau_i: {tau_i} s, tau_i_ns: {tau_i_ns} ns")
    print(f"tau_delay: {tau_delay} s, tau_delay_ns: {tau_delay_ns} ns")
    print(f"tau_delay_start: {tau_delay_start} s")
    print(f"tau_delay_end: {tau_delay_end} s")
    print(f"num_loop_points: {num_loop_points}")
    print(f"time_between_points: {time_between_points} s")


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




