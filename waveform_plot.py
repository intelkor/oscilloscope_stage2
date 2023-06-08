#!python3
# *********************************************************
# Author: Tiancheng Xiong
# Date: May 31, 2023
# Purpose: read the data from oscilloscope and then plot the waveform
# Notice: None
# *********************************************************
# Import modules.
# ---------------------------------------------------------
import pyvisa as visa
import struct
import matplotlib.pyplot as plt


import tkinter as tk
from tkinter import messagebox

global scope

def initialize(obj):
    global scope
    scope = obj
    # # Clear status.
    # do_command("*CLS")
    # # Get and display the device's *IDN? string.
    # idn_string = do_query_string("*IDN?")
    # print("Identification string: '%s'" % idn_string)
    # # Load the default setup.
    # do_command("*RST")
    


# =========================================================
#  read_and_plot(): read the data from osciloscope and plot it
# =========================================================
def read_and_plot(download = False, source="CHANnel1", csv_path = "waveform_data.csv",  waveform_path = "waveform.png",debug = False):
    global scope

    # Download waveform data.
    # --------------------------------------------------------
    # Get the waveform type.
    qresult = do_query_string(":WAVeform:TYPE?")
    if debug:
        print("Waveform type: %s" % qresult)
    # Get the number of waveform points.
    qresult = do_query_string(":WAVeform:POINts?")
    if debug:
        print("Waveform points: %s" % qresult)
    # Set the waveform source.
    do_command(f":WAVeform:SOURce {source}")
    qresult = do_query_string(":WAVeform:SOURce?")
    if debug:
        print("Waveform source: %s" % qresult)
    # Choose the format of the data returned:
    do_command(":WAVeform:FORMat BYTE")
    if debug:
        print("Waveform format: %s" % do_query_string(":WAVeform:FORMat?"))
    # Display the waveform settings from preamble:
    wav_form_dict = {
        0: "ASCii",
        1: "BYTE",
        2: "WORD",
        3: "LONG",
        4: "LONGLONG",
    }
    acq_type_dict = {
        1: "RAW",
        2: "AVERage",
        3: "VHIStogram",
        4: "HHIStogram",
        6: "INTerpolate",
        10: "PDETect",
    }
    acq_mode_dict = {
        0: "RTIMe",
        1: "ETIMe",
        3: "PDETect",
    }
    coupling_dict = {
        0: "AC",
        1: "DC",
        2: "DCFIFTY",
        3: "LFREJECT",
    }
    units_dict = {
        0: "UNKNOWN",
        1: "VOLT",
        2: "SECOND",
        3: "CONSTANT",
        4: "AMP",
        5: "DECIBEL",
    }


    preamble_string = do_query_string(":WAVeform:PREamble?")
    ( wav_form, acq_type, wfmpts, avgcnt, x_increment, x_origin, x_reference, y_increment, y_origin, y_reference, coupling,
x_display_range, x_display_origin, y_display_range,
y_display_origin, date, time, frame_model, acq_mode,
completion, x_units, y_units, max_bw_limit, min_bw_limit
) = preamble_string.split(",")
    if debug:
        print("Waveform format: %s" % wav_form_dict[int(wav_form)])
        print("Acquire type: %s" % acq_type_dict[int(acq_type)])
        print("Waveform points desired: %s" % wfmpts)
        print("Waveform average count: %s" % avgcnt)
        print("Waveform X increment: %s" % x_increment)
        print("Waveform X origin: %s" % x_origin)
        print("Waveform X reference: %s" % x_reference) # Always 0.
        print("Waveform Y increment: %s" % y_increment)
        print("Waveform Y origin: %s" % y_origin)
        print("Waveform Y reference: %s" % y_reference) # Always 0.
        print("Coupling: %s" % coupling_dict[int(coupling)])
        print("Waveform X display range: %s" % x_display_range)
        print("Waveform X display origin: %s" % x_display_origin)
        print("Waveform Y display range: %s" % y_display_range)
        print("Waveform Y display origin: %s" % y_display_origin)
        print("Date: %s" % date)
        print("Time: %s" % time)
        print("Frame model #: %s" % frame_model)
        print("Acquire mode: %s" % acq_mode_dict[int(acq_mode)])
        print("Completion pct: %s" % completion)
        print("Waveform X units: %s" % units_dict[int(x_units)])
        print("Waveform Y units: %s" % units_dict[int(y_units)])
        print("Max BW limit: %s" % max_bw_limit)
        print("Min BW limit: %s" % min_bw_limit)
    # Get numeric values for later calculations.
    x_increment = do_query_number(":WAVeform:XINCrement?")
    x_origin = do_query_number(":WAVeform:XORigin?")
    y_increment = do_query_number(":WAVeform:YINCrement?")
    y_origin = do_query_number(":WAVeform:YORigin?")
    # Get the waveform data.
    do_command(":WAVeform:STReaming OFF")
    # rawData = do_query_ieee_block(":WAVeform:DATA?")

    rawData = scope.query_binary_values(":WAVeform:DATA?", datatype = 's', container = bytes)

    # Unpack signed byte data.
    values = struct.unpack("%db" % len(rawData), rawData)
    print("Number of data values: %d" % len(values))

    time = []
    volt = []
    for i in range(0, len(values) - 1):
        time_val = x_origin + (i * x_increment)
        voltage = (values[i] * y_increment) + y_origin
        time.append(time_val)
        volt.append(voltage)


    # Save waveform data values to CSV file.
    if download:
        f = open(csv_path, "w")
        for i in range(0, len(values) - 1):
            time_val = x_origin + (i * x_increment)
            voltage = (values[i] * y_increment) + y_origin
            f.write("%E, %f\n" % (time_val, voltage))
        f.close()
        print("Waveform format BYTE data written to waveform_data.csv.")


    # graph part
    plt.plot(time, volt)
    plt.title(f"{source}")
    plt.xlabel('Time(s)')
    plt.ylabel('Voltage(V)')
    plt.minorticks_on()
    if download:
        plt.savefig(waveform_path)
    
    plt.show()




    # Save the plot to PC
    # scope.write('')

    # screenshot

    file_path = 'testimage.png'
    image_format = 'PNG'
    scope.write(f':DISK:SAVE:IMAGe "{file_path}", {image_format}')
    # scope.write(":DISK:SAVE:IMAGe \"C:/Temp/Temp.png\"")




def wave_dw_btn():
    label.config(text="Test Begin!")
    messagebox.showinfo("Message", "Download the waveform!")
    read_and_plot(download=False)


def img_dw_btn():
    label.config(text="Test Begin!")
    messagebox.showinfo("Message", "Download the screenshot!")
    download_screen_image()



def download_screen_image(path = "screen_image.png"):
    rawData = scope.query_binary_values(":DISPlay:DATA? PNG", datatype='s', container=bytes)
    # result = scope.query_binary_values("%s" % query, datatype='s', container = bytes)
    f = open(path, "wb")
    f.write(rawData)
    f.close()



# =========================================================
# Send a command and check for errors:
# =========================================================
def do_command(command, hide_params=False):
    global scope
    if hide_params:
        (header, data) = command.split(" ", 1)

    scope.write("%s" % command)

# =========================================================
# Send a command and binary values and check for errors:
# =========================================================
def do_command_ieee_block(command, values):
    global scope
    scope.write_binary_values("%s " % command, values, datatype='B')

# =========================================================
# Send a query, check for errors, return string:
# =========================================================
def do_query_string(query):
    global scope
    result = scope.query("%s" % query)
    return result
# =========================================================
# Send a query, check for errors, return floating-point value:
# =========================================================
def do_query_number(query):
    global scope
    results = scope.query("%s" % query)
    return float(results)
# =========================================================
# Send a query, check for errors, return binary values:
# =========================================================
def do_query_ieee_block(query):
    global scope
    result = scope.query_binary_values("%s" % query, datatype='s')
    return result[0]


# =========================================================
# Main program:
# =========================================================
# rm = visa.ResourceManager()
# scope = rm.open_resource("USB0::0x0957::0x9009::MY53120106::0::INSTR")
# # scope.timeout = 20000
# # read_and_plot(download=False)
# # scope.close()
# # print("End of program.")
# # sys.exit()



# # gui part
# window = tk.Tk()

# window.geometry("500x500")
# window.title("Tkinter Example")
# label = tk.Label(window, text="Image Download")
# label.pack()
# button = tk.Button(window, text="Download the waveform!", command=wave_dw_btn)
# button.pack()



# label = tk.Label(window, text="Screenshot Download")
# label.pack()
# button = tk.Button(window, text="Download the Screenshot!", command=img_dw_btn)
# button.pack()


# window.mainloop()

