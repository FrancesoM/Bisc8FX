# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 20:34:20 2021

@author: francesco.maio
"""


import numpy as np
import serial
import time
import os
import sys
import re
from scipy import signal
import os
import struct

import matplotlib.pyplot as plt

data_adc_regexp = re.compile(r"\d+\n")
save_path = "raw_data"

def read_all(port, chunk_size=50):
    """Read all characters on the serial port and return them."""
    if not port.timeout:
        raise TypeError('Port needs to have a timeout set!')

    read_buffer = b''

    while True:
        # Read in chunks. Each chunk will wait as long as specified by
        # timeout. Increase chunk_size to fail quicker
        byte_chunk = port.read(size=chunk_size)
        read_buffer += byte_chunk
        if not len(byte_chunk) == chunk_size:
            break

    return read_buffer

def writep(ser):
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.set_buffer_size(rx_size = 500000, tx_size = 200)
    packet = bytearray()
    packet.append(0x61)
    packet.append(0xA)
    ser.write(packet)
    packet = bytearray()
    packet.append(0x00)
    return read_all(ser,100)

#precision = int(input("Enter data precision 1: 8bit, 2: 16bit: "))
try:
    #tout = int(input("Enter timeout, if empty it's 1 sec': "))
    tout = 1
except:
    tout = 1   





fromSerial =[]


#find the last data file and increase number
l = list(filter(lambda s:  "txt" in s and "data" in s, os.listdir()))
numbers = list(map(lambda x: int(re.search(r"\d+",x).group(0)),l))
numbers.sort()
next_number = numbers[-1] + 1 

t2 = 0
t1 = 0

datarr=[]
run=1

fs = 41810

plt.ion()



with serial.Serial('COM5',baudrate=115200,timeout=7) as ser:  # open serial port
    print(ser.name)         # check which port was really used
    

    
    time.sleep(.1)
    ser.flushInput()
    ser.flush()
    
    #manual flush
    #while(len(ser.read(100000000))!=0): 
    #    print("Flushing....")
        
    while(run):
             
            
        analyze_data=1
        #ser.timeout = 5
        #ser.write_timeout = 0.5
        while(analyze_data):
            
            
            action = input("""What to do?:\n
                           'r' to receive new data (ADC only)\n
                           'p' to receive new data (AXI Monitor)\n
                           's' to save the data\n
                           'q' to quit \n
                           """)
        
            if action=="p":
                
                rec = writep(ser)
                
                #uncomment if using two receive buffers
                #n_shorts = len(rec)//2
                #len_vectors = n_shorts//2
                
                #uncomment if using one receive buffer
                rec = rec[:-3]
                n_shorts = len(rec)//2
                N= n_shorts//2
                
                # > little endian
                # {n_shorts} number of 2bytes received
                # H unsigned short, h signed short
                axis_tdata1 = struct.unpack("<{}h".format(N),rec[0:n_shorts])[2:-2]
                axis_tdata2 = struct.unpack("<{}H".format(N),rec[n_shorts:2*n_shorts])[2:-2]
                
                debug=""
                n="\n"
                average = np.average(axis_tdata1)
                debug+="Average = {}".format(average) + n
                debug+="Max = {}".format(np.max(axis_tdata1))+n
                gain = 150
                offset = 1660 # those two numbers are from C program
                adc = average/gain + offset 
                debug+="Original estimate from ADC = {}".format(adc)+n
                print(debug)

                f_interest = 25000 #Hz
                
                N_trim = len(axis_tdata1)
                T = N_trim/fs
                freq = np.arange(N_trim)/T
                
                n_oneside = N_trim//2
                f_oneside = freq[:n_oneside]
                
                figure, ( (ax1,ax2),(ax3,ax4) ) = plt.subplots(2, 2)
                ax1.plot(axis_tdata1)  
                ax3.plot(axis_tdata2)
                
                X1_n = np.fft.fft(axis_tdata1 - np.mean(axis_tdata1))
                X2_n = np.fft.fft(axis_tdata2 - np.mean(axis_tdata2))
                
                
                ax2.semilogx(f_oneside,abs(X1_n[:n_oneside])/N_trim)
                ax4.semilogx(f_oneside,abs(X2_n[:n_oneside])/N_trim)
                
                analyze_data=0
                
                data_to_save = [axis_tdata1 ,axis_tdata2]
                save_path = "debug_data"
                
                plt.draw()
                plt.pause(0.2)
                
            elif action=="r":
                
                #send command to read
                rec = writep(ser)
                
                n_shorts = len(rec)//2
                #format is:
                # > little endian
                # {n_shorts} number of 2bytes received
                # H unsigned short
                data = struct.unpack("<{}H".format(n_shorts),rec)
                x_n = [float(i>>4) for i in data]
                
                """
                x_n = []
                for d in all_data:
                    match = data_adc_regexp.search(d)
                    if match != None:
                        x_n.append(float(match.group(1)))
                """
                
                x_n = x_n[20:]
                
                               
                #since the noise is way below fsample, we can reduce it digitally
                #remove power supply noise
                #bp, ap = signal.iirnotch(50, 30, fs)
                #x_n_noACnoise = signal.filtfilt(bp, ap, x_n)
                x_n_noACnoise = x_n
                
                print("Average background: {}".format(np.mean(x_n_noACnoise)))
                
                X_n = np.fft.fft(x_n_noACnoise - np.mean(x_n_noACnoise))
                freq = np.fft.fftfreq(len(x_n_noACnoise))*fs
                
                f_interest = 15000 #Hz
                df = fs/len(X_n)
                
                max_point = int(f_interest/df)
                
                print("Len FFT {}".format(len(X_n)))
                
                #print(reads)
                print("Read {} data".format(len(x_n_noACnoise)))
                

                
                analyze_data=0
                datarr = []
                
                figure, (ax1, ax2, ax3) = plt.subplots(3, 1)
                
                dt = 1000/fs #ms
                tmax1 = dt*len(x_n_noACnoise)
                tmax2 = dt*len(x_n_noACnoise[0:300])
                
                t = np.array(range(len(x_n_noACnoise)))*dt
                
                l1, = ax1.plot(t[0:300],x_n_noACnoise[0:300])
                ax1.set_label("ms")
                l2, = ax2.plot(t,x_n_noACnoise)
                ax2.set_label("ms")
                l3, = ax3.semilogx(freq[0:max_point],abs(X_n[0:max_point])/len(X_n))
                plt.draw()
                plt.pause(0.2)
                
                data_to_save = [x_n_noACnoise]
                save_path = "raw_data"
                          
                
            
            elif action=="s":
                
                print("saving..")
                for DATA in data_to_save:
                    name = input("Insert the name: ")
                    if len(name)!=0:
                        
                        #name = "data{}.txt".format(next_number)
                        #next_number+=1
                    
                    
                        with open(os.path.join(save_path,name),"w") as fdata:
                        
                            for x in DATA:
                                fdata.write(str(int(x)))
                                fdata.write("\n")
                    else:
                        print("Not saving..")
                    
                print("..done")
    
    
            else:
                analyze_data=0
                run=0
                
                    

plt.show()