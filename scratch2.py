def adjust_pattern_to_multiple_of_8ns(pattern, tau_padding_before_mw_ns, tau_padding_after_mw_ns):
    # Calculate total time in nanoseconds
    total_time = sum(pair[0] for pair in pattern)
    
    # Calculate the amount of padding needed to make total_time a multiple of 8 ns
    padding_needed = (8 - (total_time % 8)) % 8
    
    # Append the required padding to the pattern
    adjusted_pattern = pattern + [(padding_needed, 0)]
    
    return adjusted_pattern

# Define your initial pattern
pattern_1_subunit = [
    (tau_laser_ns + tau_padding_before_mw_ns, 0),
    (tau_mw_ns_rounded_to_10ps, 1),
    (tau_padding_after_mw_ns, 0)
]

# Adjust the pattern
adjusted_pattern = adjust_pattern_to_multiple_of_8ns(pattern_1_subunit, tau_padding_before_mw_ns, tau_padding_after_mw_ns)

print(adjusted_pattern)
