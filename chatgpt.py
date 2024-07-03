import csv

# Define the filename where you want to save the CSV
filename = 'pairs.csv'

# Define the data pairs
pairs = [(1, 1), (2, 4), (3, 9), (4, 16)]

# Define column headings
headers = ['Number', 'Square']

# Open the file in 'w' mode with newline='' to prevent extra newline characters
with open(filename, 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)
    
    # Write headers to the CSV file
    csvwriter.writerow(headers)
    
    # Write each pair (i, i^2) as a row in the CSV file
    for pair in pairs:
        csvwriter.writerow(pair)

print(f'Pairs saved to {filename}')
