# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 13:34:58 2021

@author: francesco.maio
"""

import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from scipy import signal
import os
import math

import datetime

path_in = "debug_data"
path_out = "wav_files"
name = "one_intro"
name2 = None
out_name = name

do_ac_filter=0
do_filter=1
do_saturate=0
built_in_filter=0

do_write = 1

fs = 41810

data = []
with open(os.path.join(path_in,name)) as fd:
    lines = fd.read().split("\n")
    for l in lines:
        if len(l) > 0:
            data.append(float(l))

    
y = np.array(data) 

amplitude = 0.5*abs(max(y)-min(y))
#y = np.array([ ( np.sign(y_i) )*(1 - np.exp( - 100*(1/amplitude)*abs(y_i) ) ) for y_i in y  ])*amplitude
y = np.array([ ( math.atan(y_i/2000) ) for y_i in y  ])*amplitude

out_name += "_saturated_"