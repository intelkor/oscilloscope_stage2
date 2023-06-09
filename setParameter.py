#!python3
# *********************************************************
# Author: Tiancheng Xiong
# Date: June 5, 2023
# Purpose: set parameters for oscilloscope
# Notice:
# *********************************************************
# Import modules.
# ---------------------------------------------------------
import pyvisa as visa
import sys
import pandas as pd
import tkinter as tk
from tkinter import *

global scope

def initialize(obj):
    global scope
    # # Clear status.
    # do_command("*CLS")
    # # Get and display the device's *IDN? string.
    # idn_string = do_query_string("*IDN?")
    # print("Identification string: '%s'" % idn_string)
    # # Load the default setup.
    # do_command("*RST")
    scope = obj

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



# -------main logic----------------

global source

# frontend part
def auto_scale_click():
    # call auto scale function
    autoScle()


def channel_control_select(selection):
    global source
    # source = "CHANnel1"   # default
    if selection == "channel 1":
        source = "CHANnel1"
    elif selection == "channel 2":
        source = "CHANnel2"
    elif selection == "channel 3":
        source = "CHANnel3"
    else:
        source = "CHANnel4"

    choose_channel(source)
    print(selection)


def impedance_control_select(selection):
    choice = "DC"
    if selection == "DC coupling, 1 MΩ impedance":
        choice = "DC"
    elif selection == "DC coupling, 50Ω impedance":
        choice = "DC50"
    elif selection == "AC coupling, 1 MΩ impedance":
        choice = "AC"
    else:
        choice = "LFR2"

    impedance_select(choice)

def trigger_slope_select(selection):
    mode = "rise"
    if selection == "rise":
        mode = "POS"
    elif selection == "fall":
        mode = "NEG"
    else:
        mode = "EITH"
    choose_trigger_slope(mode)



# points acquiring control
def points_acquire_control():
    value = entry_points.get()
    print(value)
    points_acquire(value)

def auto_clicked_control():
    points_auto_clicked()

# sample rate group

def sample_rate_control():
    value = entry_sample_rate.get()
    print(value)
    sample_rate(value)

def rate_auto_clicked():
    sample_auto_clicked()




########################## backend part ############################
def autoScle():
    global scope
    scope.write(":AUToscale")

def choose_channel(source = "CHANnel1"):
    pass
    # scope.write(f":CHANnel:SELECT 2")


def average_on_off(val = "off"):
    global scope
    if val == "on":
        scope.write( ":ACQuire:AVERage ON")
    else:
        scope.write( ":ACQuire:AVERage OFF")


def impedance_select(choice):
    global scope
    global source
    print(source)
    scope.write(f":{source}:INPut {choice}")


# POS, NEG, EITH
def choose_trigger_slope(mode="POS"):
    global scope
    scope.write(f":TRIGGER:EDGE:SLOPE {mode}")
    #maybe have an error handling

# points acquiring control
def points_acquire(num = 10000003):
    global scope
    scope.write(f":ACQuire:POINts:ANALog {num}")

def points_auto_clicked():
    global scope
    scope.write(":ACQuire:POINts:ANALog AUTO")



# sample rate group
def sample_rate(num = 250E+6):
    global scope
    scope.write(f":ACQuire:SRATe:ANALog {num}")

def sample_auto_clicked():
    global scope
    scope.write(":ACQuire:SRATe:ANALog:AUTO ON")


# vertical scaling (100 to 1300) mv
def vertical_scaling(value):
    global source
    global scope
    scope.write(f":{source}:SCALe {value}E-3")

# vertical offset (0 to 1000) mv
def vertical_offset(value):
    global source
    global scope
    scope.write(f"{source}:OFFSet {value}E-3")


def horizontal_scaling(value):
    global source
    global scope
    scope.write(f":TIMebase:SCALe {value}E-06")


def horizontal_offset(value):
    global source
    global scope
    scope.write(f":TIMebase:POSition {value}E-6")



# -------ending-----------------





# =========================================================
# Main program:
# =========================================================
# rm = visa.ResourceManager()
# scope = rm.open_resource("USB0::0x0957::0x9009::MY53120106::0::INSTR")
# scope.timeout = 20000



# # GUI: pop out a ugly window
# window = tk.Tk()
# window.geometry("500x500")
# window.title("Oscilloscope Setting Window")
# label = tk.Label(window, text="Setting Parameter")
# label.pack(anchor = W)
# button = tk.Button(window, text="autoscale", command=auto_scale_click)
# button.pack(anchor = W)


# # Channel selection
# selected_option = StringVar(window)
# selected_option.set("channel 1")
# label = Label(window, text="Choose a channel:")
# label.pack(anchor = W)
# options = ["channel 1", "channel 2", "channel 3", "channel 4"]
# drop_down = OptionMenu(window, selected_option, *options, command = channel_control_select)
# drop_down.pack(anchor = W)
# drop_down.config(width=20)


# # set the input of impedance
# selected_option = StringVar(window)
# selected_option.set("50 Ohm")
# label = Label(window, text="Choose a value of impedance:")
# label.pack(anchor = W)
# options = ["DC coupling, 1 MΩ impedance", "DC coupling, 50Ω impedance", "AC coupling, 1 MΩ impedance", "AC 1 MΩ input impedance"]
# drop_down = OptionMenu(window, selected_option, *options, command = impedance_control_select)
# drop_down.pack(anchor = W)
# drop_down.config(width=20)


# # trigger slope selection
# selected_option2 = StringVar(window)
# selected_option2.set("rise")
# label = Label(window, text="Choose a slope:")
# label.pack(anchor = W)
# options = ["rise", "fall", "Either"]
# drop_down = OptionMenu(window, selected_option2, *options, command = trigger_slope_select)
# drop_down.pack(anchor = W)
# drop_down.config(width=20)


# # set the number of points
# label = tk.Label(window, text="Enter the number of acquired points")
# label.pack(side=LEFT)
# entry_points = tk.Entry(window)
# entry_points.pack(side=LEFT)
# points_submitted_btn_1 = tk.Button(window, text="Submitted", command=points_acquire_control)
# points_submitted_btn_1.pack(side=LEFT)
# points_auto_btn_1 = tk.Button(window, text="Automatic", command=points_auto_clicked)
# points_auto_btn_1.pack(side=LEFT)


# # set the sampling rate
# label = tk.Label(window, text="Enter the sampling rate")
# label.pack(side=LEFT)
# entry_sample_rate = tk.Entry(window)
# entry_sample_rate.pack(side=LEFT)
# points_submitted_btn_2 = tk.Button(window, text="Submitted", command=sample_rate_control)
# points_submitted_btn_2.pack(side=LEFT)
# points_auto_btn_2 = tk.Button(window, text="Automatic", command=rate_auto_clicked)
# points_auto_btn_2.pack(side=LEFT)




# window.mainloop()
# scope.close()
# print("End of program.")
# sys.exit()




