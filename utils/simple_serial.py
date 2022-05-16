# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 21:42:19 2021

@author: francesco.maio
"""

import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial('COM5',baudrate=115200,timeout=1)

ser.isOpen()

print ('Enter your commands below.\r\nInsert "exit" to leave the application.')

usrinput=1
while 1 :
    # get keyboard input
    usrinput = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(usrinput)
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print(">>" + out ) 