# Program name labjackstatistics.py
# 7/11/2024
# Author Peter Burke
# This program measures the voltage from the labjack every t_wait seconds for num_readings times then saves to file.

 

#import libraries
from labjack import ljm
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windfreak import SynthHD, synth_hd
import time
import csv
import csv
import pandas as pd
from main import *
#__________________________________________________________________________

base_path = r"C:\Users\BurkeLab\Desktop" # Specify the path where you want to create a data folder

base_folder = create_date_folder(base_path) #create a folder with name mm/dd/yy (eg. 070324) where you want to save your data

plotname = generate_unique_filename(base_folder)# Generate unique filename with name mm/dd/yy (eg. 070324)
#***************************************************************************************
#Parameters:
t_wait =10 # wait time between points in seconds
num_readings=100 # total # of readings

t_each= 100 #milliseconds Minghao what is this ??????

#***************************************************************************************
# Create filename
#Define the name of data
#plotname= str(input("Enter the name of the data following BurkeLab Rules MMDDYYNNN(example names: 0617240001 do not use special characters or spaces)"))


print(f"Data file successully created: {plotname}")
#***************************************************************************************
# Initialize labjack




handle = ljm.openS("ANY", "ANY")
 

#AIN#_NEGATIVE_CH: Specifies the negative channel to be used for each positive channel. 199=Default=> Single-Ended.
#AIN#_RANGE: The range/span of each analog input. Write the highest expected input voltage. For T7, the default is -10V to 10V
#AIN#_RESOLUTION_INDEX: The resolution index for command-response and AIN-EF readings. A larger resolution index generally results in lower noise and longer sample times.
#Default value of 0 corresponds to an index of 8 (T7) 
#AIN#_SETTLING_US: Settling time for command-response and AIN-EF readings. For T-7: Auto. Max is 50000 (microseconds).

names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX", "AIN0_SETTLING_US",
             "AIN1_NEGATIVE_CH", "AIN1_RANGE", "AIN1_RESOLUTION_INDEX", "AIN1_SETTLING_US"]

#Default values
aValues = [199, 10.0, 0, 0, 199, 10.0, 0, 0]
num_Frames= len(names)

ljm.eWriteNames(handle, num_Frames, names, aValues)


numFrames = 2
names = ["AIN0", "DAC0"]
intervalHandle = 1



lbj_steptime = t_each*1000 # labjack step time in microseconds
ljm.startInterval(intervalHandle, lbj_steptime)




#***************************************************************************************
# Read loop:

# Initialize a 2D array to store the reading number and callme return value
readings = []

# Call the function num_readings times with a wait time of t_wait between each call
for i in range(num_readings):

    # read labjack:
    reading_value = abs(ljm.eReadNames(handle, numFrames, names)[0])
    print(i,reading_value)
    ljm.waitForNextInterval(intervalHandle)
    
    readings.append(reading_value)  # Store reading number and callme return value
    time.sleep(t_wait)


# Optional: Convert the readings list to a numpy array for further processing
import numpy as np
readings_array = np.array(readings)


# Print the readings array
print("Readings Array:", readings_array)

# Calculate the average (mean) of the readings
average_reading = np.mean(readings_array)
print("Average Reading:", average_reading)

# Calculate the standard deviation of the readings
std_deviation = np.std(readings_array)
print("Standard Deviation:", std_deviation)


#***************************************************************************************
# plot readings:

# Plot the readings
plt.figure(figsize=(10, 6))
plt.plot(readings_array, marker='o', linestyle='-', color='b', label='Readings')
plt.axhline(y=average_reading, color='r', linestyle='--', label=f'Average: {average_reading:.2f}')
plt.fill_between(range(len(readings_array)), 
                 average_reading - std_deviation, 
                 average_reading + std_deviation, 
                 color='gray', alpha=0.2, label=f'Std Dev: {std_deviation:.2e}')



# make y axis start at zero
# Set y-axis limits to ensure the actual value display
#plt.ylim(min(0, np.min(readings_array) - std_deviation), np.max(readings_array) + std_deviation)

# Add labels and title
plt.xlabel('Index')
plt.ylabel('Reading Value')
plt.title('Readings Plot with Average and Standard Deviation')
plt.legend()

# Show the plot
plt.show()


#***************************************************************************************
# Save to file
# Specify the filename for the CSV file
columns = ['point_number', 'labjack reading']
# Open the file in 'w' mode with newline='' to prevent extra newline characters
with open(plotname, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)
        
    # Write header row
    csvwriter.writerow(columns)   
        
    # Write each value in readings as a row in the CSV file with an index
    for i, value in enumerate(readings):
        csvwriter.writerow([i+1, value])  # index starts from 1

# Create a DataFrame with 'point_number' as index and 'labjack reading' as column
df = pd.DataFrame({'labjack reading': readings}, index=pd.RangeIndex(start=1, stop=len(readings)+1, name='point_number'))

# Save DataFrame to CSV (excluding index)
df.to_csv(plotname, index=False)

print(f'Data successfully saved to {plotname}')

#********************CHATGPTSAVETOFILE**********************





