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

def default_freq(f1,f2):
    default_start_frequency = f1
    default_stop_frequency = f2
    default_loop_amount = default_stop_frequency-default_start_frequency

    use_defaults = get_confirmation("Do you want to use this frequency range (default as 2800MHz to 3000MHz)?")

    if use_defaults:
        start_frequency = default_start_frequency
        stop_frequency = default_stop_frequency
    else:
        # Get user inputs
        start_frequency = get_user_input("Enter the new start frequency in MHz", default_start_frequency)
        stop_frequency = get_user_input("Enter the new stop frequency in MHz", default_stop_frequency)


    print("\nSummary of your input:")
    time.sleep(1)
    print(f"start frequency: {start_frequency} MHz, stop frequency: {stop_frequency} MHz")
    time.sleep(1)
    print(f"loop amount: {stop_frequency-start_frequency} points")
    
    return [start_frequency,stop_frequency]
    
