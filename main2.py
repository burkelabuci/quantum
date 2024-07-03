def get_user_input(prompt, default):
    user_input = input(f"{prompt} (default {default}): ")
    return float(user_input) if user_input else default

def get_confirmation(prompt):
    while True:
        confirmation = input(f"{prompt} (yes/no): ").strip().lower()
        if confirmation in ['yes', 'no']:
            return confirmation == 'yes'
        print("Please answer with 'yes' or 'no'.")

tau_ref = get_user_input("Enter tau_ref (reference time in seconds)", 15e-3)
tau_i = get_user_input("Enter tau_i (pulse time in seconds)", 1e-6)
tau_delay = get_user_input("Enter tau_delay (delay between initialize and readout in seconds)", 1e-3)

tau_ref_ns = tau_ref * 1E9
tau_i_ns = tau_i * 1E9
tau_delay_ns = tau_delay * 1E9

tau_delay_start = get_user_input("Enter tau_delay_start (beginning of loop)", 0.1e-3)
tau_delay_end = get_user_input("Enter tau_delay_end (end of loop)", 0.1e-3)
num_loop_points = int(get_user_input("Enter num_loop_points (number of loop points)", 100))
time_between_points = get_user_input("Enter time_between_points (time in seconds between each data point)", 0.3)

print("\nSummary of your input:")
print(f"tau_ref: {tau_ref} s, tau_ref_ns: {tau_ref_ns} ns")
print(f"tau_i: {tau_i} s, tau_i_ns: {tau_i_ns} ns")
print(f"tau_delay: {tau_delay} s, tau_delay_ns: {tau_delay_ns} ns")
print(f"tau_delay_start: {tau_delay_start} s")
print(f"tau_delay_end: {tau_delay_end} s")
print(f"num_loop_points: {num_loop_points}")
print(f"time_between_points: {time_between_points} s")

if get_confirmation("Is this information correct?"):
    print("Input confirmed. Proceeding with the values.")
else:
    print("Please run the script again to input correct values.")

