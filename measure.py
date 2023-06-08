#!python3
# *********************************************************
# Author: Tiancheng Xiong
# Date: June 2, 2023
# Purpose: record some measurements and save them to a csv file
# Notice: bug in getting duty cycle; need to figure out get the min, max and average value; maybe add units for measurement in the future
# *********************************************************
# Import modules.
# ---------------------------------------------------------
import pyvisa as visa
import sys
import pandas as pd

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


# measure specific measurements
# figure out the unit
def measure(source="CHANnel1", path = "output.csv", debug = False):
    global scope
    measList = []
    valueList = []
    # do_command(":MEASure:SOURce CHANnel1")
    # qresult = do_query_string(":MEASure:SOURce?")
    # print("Measure source: %s" % qresult)
    # do_command(":MEASure:FREQuency")
    #
    # do_command(":MEASure:VAMPlitude")
    # qresult = do_query_string(":MEASure:VAMPlitude?")
    # print("Measured vertical amplitude on channel 1: %s" % qresult)

    # Rise time: still need to figure out how to get the min, max and average rise time
    rise_time = do_query_number(f":MEASure:RISetime? {source}")
    measList.append("rise time")
    valueList.append(rise_time)


    # Fall time: still need to figure out how to get the min, max and average fall time
    fall_time = do_query_number(f":MEASure:FALLtime? {source}")
    measList.append("fall time")
    valueList.append(fall_time)


    # Frequency
    frequency = do_query_number(f":MEASure:FREQuency? {source}")
    measList.append("frequency")
    valueList.append(frequency)


    # period
    period = do_query_number(f":MEASure:period? {source}")
    measList.append("period")
    valueList.append(period)


    # amplitude
    amplitude = do_query_number(f":MEASure:period? {source}")
    measList.append("amplitude")
    valueList.append(amplitude)


    # measure the number of positive pulse in the screen
    NumOfPulse = do_query_number(f":MEASure:PPULses? {source}")


    # pulse width
    pulse_width = do_query_number(f":MEASure:PWIDth? {source}")
    measList.append("pulse width")
    valueList.append(pulse_width)


    # BUGGGGGGGGGGGGGGGGG!
    # duty cycle (cycle to cycle duty cycle)
    # duty_cycle = do_query_string(f":MEASure:CTCDutycycle {source}, RISing")
    # scope.write(":ANALyze:AEDGes ON")
    # test = scope.query(":MEASure:CTCDutycycle? CHANnel1,RISing")
    # print(test)
    # print(f"Measured duty cycle on {source}: %s" % duty_cycle)

    if debug:
        print(f"Measured rising time on {source}: %s" % rise_time)
        print(f"Measured falling time on {source}: %s" % fall_time)
        print(f"Measured frequency on {source}: %s" % frequency)
        print(f"Measured period on {source}: %s" % period)
        print(f"Measured amplitude on {source}: %s" % amplitude)
        print(f"Number of positive pulse on {source}: %s" % NumOfPulse)
        print(f"Measured pulse width on {source}: %s" % pulse_width)

    # download the data to csv
    if path:
        df = pd.DataFrame({'Measurement': measList, 'Value': valueList})
        df.to_csv(path, index=False)

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
# scope.timeout = 20000

# # invoke the function
# measure(path="measurement.csv")

# scope.close()
# print("End of program.")
# sys.exit()




