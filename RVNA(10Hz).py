# -*- coding: utf-8 -*-
"""
Updated on 11/14/2021
Fixed Connection bug

Before running the code:
    1. Make sure RVNA software is running
    2. Go to system -> Network setup -> turn on socket interface
    3. make sure socket server is 5025
    
"""

import visa    #PyVisa is required along with NIVisa
from time import sleep
from time import perf_counter
import time
import os
import sys
import csv

def Acquisition():
    rm = visa.ResourceManager()
    #Connect to a Socket on the local machine at 5025
    #Use the IP address of a remote machine to connect to it instead
    try:
        CMT = rm.open_resource('TCPIP0::localhost::5025::SOCKET')
    except:
        print("Failure to connect to VNA!")
        print("Make sure RVNA software is running")
        print("Go to system -> Network setup -> Interface state ON")
        print("make sure socket server is 5025")
    #The VNA ends each line with this. Reads will time out without this
    CMT.read_termination='\n'
    #Set a really long timeout period for slow sweeps(ms)
    CMT.timeout = 10000


    ###########################################
    ###########################################
    ######try stuff here#######################
    ###########################################
    ###########################################


        
    # trigger source bus and create list
    CMT.write("TRIG:SOUR BUS\n")
    CMT.query("*OPC?\n")
    trace = []
    cycle_time_array = []


    # initialize parameters
    filename = input('enter filename: ')
    frequency = input('enter frequency: ')
    frames = input('enter total number of sweeps: ')
    frames = int(frames)
    period = 1/int(frequency) #period in s

    #Acquire data and store them in place

    for i in range(0,frames):
        t0 = time.perf_counter()
        
        # single trigger
        CMT.write("TRIG:SING\n")
        CMT.query("*OPC?\n")
        
        # capture data from trace 1, response is string
        s11_data = CMT.query("CALC1:DATA:FDATa?")
        # split the response string according to commas
        s11_data = s11_data.split(",")
        # get rid of the imag data which are all 0's for log mag measurement
        s11_data = s11_data[::2]
        # convert measurement data from strings into float numbers
        s11_data = [float(s) for s in s11_data]
        trace.append(s11_data)
        while (time.perf_counter()-t0) < period:
            pass
        cycle_time = time.perf_counter()-t0
        print(time.perf_counter()-t0)
        cycle_time_array.append(cycle_time * 1000) #s
        #cycle_time_array.append(cycle_time * 1000) # ms 

    #Write trace data to csv
    for data in trace:
        with open(filename+'.csv', 'a+', newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(data)
                stream.close()

    #Write time data to another csv
    #print(cycle_time_array)
    with open(filename+'_timestamp.csv', 'a+', newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(cycle_time_array)
                stream.close()



    CMT.close() 
    rm.close()
    print('done!')

while True:
    Acquisition()
