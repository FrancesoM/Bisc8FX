# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 15:32:36 2021

@author: francesco.maio
"""


import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from scipy import signal
import os

path_in = "raw_data"
path_out = "mod_data"
name = "hls_no_notch"

process = False


data = []
with open(os.path.join(path_in,name)) as fd:
    lines = fd.read().split("\n")
    for l in lines:
        if len(l) > 0:
            if process:
                data.append(( float(l) - 1774)*10  +1774 )
                
            else:
                val = int(float(l))
                adc_val = val<<4
                data.append(adc_val)
                
if process:
    name = name+"_processed"
else:
    name = name+"_adc"                
    
with open(os.path.join(path_out,name),"w") as fd:
    for i in data:
        fd.write(str(int(i))+",")
    