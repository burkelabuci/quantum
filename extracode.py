
# EXTRA::::

# Create sequence object 
seq = ps.createSequence()

# Set channel 0 as refrence (pulse duration in nanoseconds)
seq.setDigital(0, [(tau_ref_ns, 1), (tau_ref_ns, 0)])

# Set channel 1 as the laser pulse sequence (pulse duration in nanoseconds)
seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),((tau_i_ns), 1),((tau_delay_ns),0),((tau_i_ns), 1), ((tau_ref_ns-2*tau_i_ns-tau_delay_ns), 0)])

#DELETE THE Intialization
#seq.setDigital(1, [ (tau_ref_ns, 0),((tau_i_ns+tau_delay_ns),0),(tau_i_ns,1),((tau_ref_ns-2*tau_i_ns-tau_delay_ns),0)])
# DELETE READ PULSE
#seq.setDigital(1, [(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0),(tau_i_ns, 1), ((tau_ref_ns-tau_i_ns), 0)])

# Stream sequence once
#ps.stream(seq)
ps.stream(seq) # 10,000 reps = 2*tau_ref *10,000 seconds = 300 seconds = 5 mins



