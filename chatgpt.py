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

def main():
    # Example input values
    tau_ref_ns = 100  # Replace with actual value
    tau_i_ns = 2     # Replace with actual value
    tau_delay_ns = 30 # Replace with actual value
    n = 3             # Number of copies
    
    # Create the pattern array
    pattern_array = create_pattern_array(tau_ref_ns, tau_i_ns, tau_delay_ns, n)
    
    # Print the result with brackets around the entire output
    print("Pattern Array:")
    print("[" + ", ".join(f"({x}, {y})" for x, y in pattern_array) + "]")

if __name__ == "__main__":
    main()
