import nidaqmx
from nidaqmx.constants import AcquisitionType, CountDirection, Edge
import numpy as np
import sys

# Initialize an array to store the counts
intensities = []
#Parameters for the microwave:
start_frequency = 2820 #in MHz
stop_frequency = 2920 #in MHz

step_size = int(1) # specing between each frequency point in MHz
step_time = int(300) #in milliseconds
step_time_s = float(step_time/1000) #in seconds
sampling_rate = 1/step_time_s #sampling rate for counter in Hz
loopAmount= stop_frequency-start_frequency #how many points to sweep

with nidaqmx.Task() as task:
    channel = task.ci_channels.add_ci_count_edges_chan(
        "Dev1/ctr0",
        edge=Edge.RISING,
        initial_count=0,
        count_direction=CountDirection.COUNT_UP,
    )
    task.timing.cfg_samp_clk_timing(
        1000, source="/Dev1/PFI9", sample_mode=AcquisitionType.CONTINUOUS
    )
    channel.ci_count_edges_term = "/Dev1/PFI8"
    print(step_time_s)
    print(sampling_rate)
    print("Start counting. Press Ctrl+C to stop.")
    task.start()

#loop over and read the signal from the Labjack T7 and append the value to the intensity array
    j=0
    while True:
        try:
            edge_counts = task.read(number_of_samples_per_channel=1)
            intensities.append(edge_counts[0])
            if loopAmount != "infinite":
                j=j+1
                print(j,edge_counts[0])
            if j>= loopAmount:
                break
        except KeyboardInterrupt:
            pass
        finally:
            task.stop()
            
print(intensities)
print(len(intensities))

