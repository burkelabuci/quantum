import pyvisa 
import os
from datetime import datetime

# Program name SR830lockin_settings_achieve.py
# 8/26/2024
# Author Minghao Jiang
#This Python script interfaces with an SR830 DSP Lock-In Amplifier to query and retrieve its configuration parameters using GPIB communication. 
#It collects settings such as sensitivity, time constant, low pass filter slope, reference mode, input configuration, input shielding grounding,
# coupling, and line notch filter status. The script maps these raw parameter codes to human-readable descriptions using predefined dictionaries. 
# The retrieved settings are then saved to a text file in UTF-8 encoding to ensure proper handling of special characters.
#________________________________________________________________________________________

def query_lockin_parameters():
    os.add_dll_directory("C:/Program Files/Keysight/IO Libraries Suite/bin")
    os.add_dll_directory("C:/Program Files (x86)/Keysight/IO Libraries Suite/bin")
    rm = pyvisa.ResourceManager("C:/Windows/System32/visa32.dll")

#connect the GPIB with the PC
    lockin = rm.open_resource('GPIB0::8::INSTR')
    sensitivity_code = lockin.query('SENS?').strip()
    time_constant = lockin.query('OFLT?').strip()
    slope = lockin.query('OFSL?').strip()
    rmod = lockin.query('RMOD?').strip()
    isrc = lockin.query('ISRC?').strip()
    ignd = lockin.query('IGND?').strip()
    icpl = lockin.query('ICPL?').strip()
    ilin = lockin.query('ILIN?').strip()


    # Sensitivity mapping
    sensitivity_dict = {
    '0': '2 nV/fA',
    '1': '5 nV/fA',
    '2': '10 nV/fA',
    '3': '20 nV/fA',
    '4': '50 nV/fA',
    '5': '100 nV/fA',
    '6': '200 nV/fA',
    '7': '500 nV/fA',
    '8': '1 µV/pA',
    '9': '2 µV/pA',
    '10': '5 µV/pA',
    '11': '10 µV/pA',
    '12': '20 µV/pA',
    '13': '50 µV/pA',
    '14': '100 µV/pA',
    '15': '200 µV/pA',
    '16': '500 µV/pA',
    '17': '1 mV/nA',
    '18': '2 mV/nA',
    '19': '5 mV/nA',
    '20': '10 mV/nA',
    '21': '20 mV/nA',
    '22': '50 mV/nA',
    '23': '100 mV/nA',
    '24': '200 mV/nA',
    '25': '500 mV/nA',
    '26': '1 V/µA'
    }


# Time constant mapping
    time_constant_dict = {
    '0': '10 µs',
    '1': '30 µs',
    '2': '100 µs',
    '3': '300 µs',
    '4': '1 ms',
    '5': '3 ms',
    '6': '10 ms',
    '7': '30 ms',
    '8': '100 ms',
    '9': '300 ms',
    '10': '1 s',
    '11': '3 s',
    '12': '10 s',
    '13': '30 s',
    '14': '100 s',
    '15': '300 s',
    '16': '1 ks',
    '17': '3 ks',
    '18': '10 ks',
    '19': '30 ks'
    }


# Slope mapping
    slope_dict = {
    '0': '6 dB/oct',
    '1': '12 dB/oct',
    '2': '18 dB/oct',
    '3': '24 dB/oct'
    }


# Reference mode mapping
    rmod_dict = {
    '0': 'High Reserve',
    '1': 'Normal',
    '2': 'Low Noise'
    }


# Input configuration mapping
    isrc_dict = {
    '0': 'A',
    '1': 'A-B',
    '2': 'I (1 MΩ)',
    '3': 'I (100 MΩ)'
    }



# Input grounding mapping
    ignd_dict = {
    '0': 'Float',
    '1': 'Ground'
}


# Input coupling mapping
    icpl_dict = {
    '0': 'AC',
    '1': 'DC'
}

# Input line notch filter mapping
    ilin_dict = {
    '0': 'Out (no filters)',
    '1': 'Line notch in',
    '2': '2xLine notch in',
    '3': 'Both notch filters in'
}

    return {
        'Sensitivity': sensitivity_dict.get(sensitivity_code, "Unknown sensitivity"),
        'Time Constant': time_constant_dict.get(time_constant, "Unknown time constant"),
        'Low Pass Filter Slope': slope_dict.get(slope, "Unknown slope"),
        'Reference Mode': rmod_dict.get(rmod, "Unknown reference mode"),
        'Input Configuration': isrc_dict.get(isrc, "Unknown input configuration"),
        'Input Shield Grounding': ignd_dict.get(ignd, "Unknown input grounding"),
        'Input Coupling': icpl_dict.get(icpl, "Unknown input coupling"),
        'Input Line Notch Filter': ilin_dict.get(ilin, "Unknown line notch filter status")
    }

def write_parameters_to_file(filepath, parameters):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write("Settings for SR830 DSP Lock-in Analyzer:\n")
        for key, value in parameters.items():
            file.write(f"{key} Setting: {value}\n")
    return parameters
