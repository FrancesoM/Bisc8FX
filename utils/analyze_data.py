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
import math
import sys
import datetime
import io_helpers
import dsp_helpers


path_in = "raw_data"


fs = 41810

LUT = io_helpers.open_decimal(".","LUT_sat_16b_signed")

check_vitis = 0
check_vivado = 1
#

name2 = "atan_saturation_{}.{}"
name1 = "digital_setup_{}.{}"

#x = io_helpers.data_file(path_in, name1.format( "C_sim" , "dat"  ) , 16, True).open()
#y = io_helpers.data_file(path_in, name1.format( "rtl"   , "mem"  ), 16, True).open()

xname = "monitor0.bin"
yname = "monitor1.bin"

x = io_helpers.data_file(path_in, xname, 16, True).open()
y = io_helpers.data_file(path_in, yname, 16, True).open()

x = x[512:]
y = y[512:]

#io_helpers.listen_wave(x,fs)
#io_helpers.listen_wave(y,fs)

X, txx, Zxx = signal.stft(x, fs, nperseg=2048)
Y, tyy, Zyy   = signal.stft(y, fs, nperseg=2048)

freq = np.fft.fftfreq(len(x))*fs

# Harsh downsample by 4 for displaying purposes


DS_factor =1
F_interest = 0.25 # interested in frequencies from 0 to 25% fsample

# downsample X
xfreq_size = int(X.shape[0]*F_interest)
xtime_size = txx.shape[0]

xfreq_size_ds = xfreq_size//DS_factor 
xtime_size_ds = xtime_size//DS_factor 

Zxx_ds=np.zeros((xfreq_size_ds,xtime_size_ds),dtype=complex)

for f in range(xfreq_size-1):
    for t in range(xtime_size-1):
        if f%DS_factor==0 and t%DS_factor==0:
            Zxx_ds[f//DS_factor,t//DS_factor] = Zxx[f,t]

X_ds   = []
for i in range(xfreq_size_ds):
    X_ds.append(X[i*DS_factor])

txx_ds = []
for i in range(xtime_size_ds):
    txx_ds.append(txx[i*DS_factor])



# downsample Y
yfreq_size = int(Y.shape[0]*F_interest)
ytime_size = tyy.shape[0]

yfreq_size_ds = yfreq_size//DS_factor 
ytime_size_ds = ytime_size//DS_factor 

Zyy_ds=np.zeros((yfreq_size_ds,ytime_size_ds),dtype=complex)

for f in range(yfreq_size-1):
    for t in range(ytime_size-1):
        if f%DS_factor==0 and t%DS_factor==0:
            Zyy_ds[f//DS_factor,t//DS_factor] = Zyy[f,t]

Y_ds   = []
for i in range(yfreq_size_ds):
    Y_ds.append(Y[i*DS_factor])

tyy_ds = []
for i in range(ytime_size_ds):
    tyy_ds.append(tyy[i*DS_factor])

#%%
plt.figure()
plt.subplot(221)
#plt.plot(xn[:500],'r',y[:500],'b')
plt.plot(x)

plt.subplot(222)
#plt.plot(xn,'r',y,'b')
plt.plot(y)

plt.subplot(223)
#plt.semilogx(freq,abs(X_n))
plt.yscale('symlog')
plt.pcolormesh(txx_ds, X_ds, np.abs(Zxx_ds), shading='gouraud')


plt.subplot(224)
#plt.semilogx(freq,abs(Y))
plt.yscale('symlog')
plt.pcolormesh(tyy_ds, Y_ds, np.abs(Zyy_ds), shading='gouraud')

#%%

plt.show()


















