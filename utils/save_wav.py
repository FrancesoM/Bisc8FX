# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 09:29:16 2021

@author: francesco.maio
"""

import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from scipy import signal
import os

path_in = "raw_data"
path_out = "wav_files"
name = "more"

data = []
with open(os.path.join(path_in,name)) as fd:
    lines = fd.read().split("\n")
    for l in lines:
        if len(l) > 0:
            data.append(float(l))
            
for i in range(0):
    data += data        
    
xn = np.array(data) - np.mean(data)

#remove hf noise
b, a = signal.butter(3, 0.05)

#remove power supply noise
bp, ap = signal.iirnotch(50, 30, 41810)

#wzi = signal.lfilter_zi(b, a)
#z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

#z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

y = xn
#y = signal.filtfilt(b, a, xn)
#y = signal.filtfilt(bp,ap,y)

plt.subplot(211)
plt.plot(xn[:500],'r',y[:500],'b')

plt.subplot(212)
plt.plot(xn,'r',y,'b')
plt.show()

print("average sample data: {}".format(np.average(data)))

scaled = np.int16(y/np.max(np.abs(y)) * 32767)
write(os.path.join(path_out,name+".wav"), 41810, scaled)
