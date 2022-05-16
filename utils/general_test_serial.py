# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 21:02:11 2021

@author: francesco.maio
"""
import serial
with serial.Serial("COM5",115200) as ser:

    ser.close()
    ser.open()
    ser.write(b'a')
    print(ser.read_until("\n"))
    ser.close()