#a higher level program to input lock_in time constants


import time
def get_user_input(prompt, default):
    user_input = input(f"{prompt} (default {default}): ")
    return int(user_input) if user_input else default

def get_confirmation(prompt):
    while True:
        confirmation = input(f"{prompt} (yes/no): ").strip().lower()
        if confirmation in ['yes', 'no']:
            return confirmation == 'yes'
        print("Please answer with 'yes' or 'no'.")

def step_time(slope_per_octave,tau_lockin):
    default_slope = slope_per_octave
    default_tau_lockin = tau_lockin
    step_time = 0
    use_defaults = get_confirmation("Do you want to use the default slope/octave (24dB) and time average (30ms) for the lock-in analyzer?")
    if use_defaults:
        slope_set = default_slope
        tau_avg = default_tau_lockin
        step_time = 10*tau_avg
    else:
        slope_set = get_user_input("Enter the new slope/octave (dB)", default_slope)
        tau_avg = get_user_input("Enter the new time constant in milliseconds", default_tau_lockin)
        if slope_set == 6:
            step_time = 5*tau_avg
        elif slope_set == 12:
            step_time = 7*tau_avg
        elif slope_set == 18:
            step_time = 9*tau_avg
        else:
            raise ValueError("Unsupported slope per octave value. Supported values are 6, 12, 18 and 24.")
    
    time.sleep(1)

    print(f"your step time is: {step_time} ms")   
    return step_time