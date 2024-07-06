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


def T1_Decay_parameters(t_ref,t_i,t_delay_start,t_delay_end,step_time,num_points):
    
    default_tau_ref = t_ref
    default_tau_i = t_i
    default_tau_delay_start = t_delay_start
    default_tau_delay_end = t_delay_end
    default_step_time = step_time
    default_num_points = num_points

    #To confirm 
    user_default = get_confirmation("Do you want to use the default tau_ref (15ms), initialization pulse (1 microseond), and the default delay time (from 0.1ms to 5 ms)?")
    
    if user_default:
        tau_ref = default_tau_ref 
        tau_i = default_tau_i
        tau_delay_start = default_tau_delay_start
        tau_delay_end = default_tau_delay_end 
        step_time = default_step_time
        num_points = default_num_points


    else:
        tau_ref = get_user_input("Enter tau_ref (reference time in seconds)", 15e-3)
        tau_i = get_user_input("Enter tau_i (pulse time in seconds)", 1e-6)
        tau_delay_start = get_user_input("Enter tau_delay_start (beginning of loop)", 0.1e-3)
        tau_delay_end = get_user_input("Enter tau_delay_end (end of loop)", 5e-3)
        step_time = get_user_input("Enter time_between_points (time in seconds between each data point)", 0.3)
        num_points = int(get_user_input("Enter num_loop_points (number of loop points)", 100))
        
    print("\nSummary of your input:")
    print(f"tau_ref: {tau_ref} s")
    time.sleep(1)
    print(f"tau_i: {tau_i} s")
    time.sleep(1)
    print(f"tau_delay_start: {tau_delay_start} s")
    time.sleep(1)
    print(f"tau_delay_end: {tau_delay_end} s")
    time.sleep(1)
    print(f"time_between_points: step_time s")
    time.sleep(1)
    print(f"num_loop_points: {num_points}")
    
    return tau_ref,tau_i,tau_delay_start,tau_delay_end,step_time,num_points






