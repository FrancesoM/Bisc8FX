# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:56:59 2022

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
path_out = "wav_files"
name = "digital_setup_out.dat"
out_name = name

do_ac_filter=0
do_filter=0
do_saturate=0
built_in_filter=0

do_write = 1

fs = 41810

LUT = io_helpers.open_decimal(".","LUT_sat_16b_signed")

data = io_helpers.open_decimal(path_in,name,dtype=float)

    
xn = np.asarray(data,dtype=np.float64) #- np.mean(data)
#xn = xn[50000:]
print(xn)
print(xn.shape)

#remove hf noise
b, a = signal.butter(2, 0.1)
bhp,ahp = signal.butter(2,0.00239,btype="high")

#remove power supply noise
bp, ap = signal.iirnotch(50, 30, fs)


y=xn

if do_saturate:

    y = dsp_helpers.applyLUT(y,LUT)
    
    out_name += "_saturated_"

if do_filter:
    if built_in_filter:
        y = signal.filtfilt(b, a, y)
        y = signal.filtfilt(bhp, ahp, y)
    else:
        y,debug2 = dsp_helpers.hls_filter_Q_model(bhp,ahp,y,fixed=True,do_debug=True)
        y,debug1 = dsp_helpers.hls_filter_Q_model(b,a,y,fixed=True)

    out_name+="_filtered_"


if do_ac_filter:
    y = signal.filtfilt(bp,ap,y)
    out_name+="_noAC_"
    

X, txx, Zxx = signal.stft(xn, fs, nperseg=4096)
Y, tyy, Zyy   = signal.stft(y, fs, nperseg=4096)

freq = np.fft.fftfreq(len(xn))*fs

# Harsh downsample by 4 for displaying purposes

assert Zxx.shape == Zyy.shape
print( "Assertion passed ")

DS_factor = 4

freq_size = X.shape[0]
time_size = txx.shape[0]

freq_size_ds = freq_size//DS_factor + 1
time_size_ds = time_size//DS_factor + 1 

Zxx_ds=np.zeros((freq_size_ds,time_size_ds),dtype=complex)
Zyy_ds=np.zeros((freq_size_ds,time_size_ds),dtype=complex)

for f in range(freq_size-1):
    for t in range(time_size-1):
        if f%DS_factor==0 and t%DS_factor==0:
            Zxx_ds[f//DS_factor,t//DS_factor] = Zxx[f,t]
            Zyy_ds[f//DS_factor,t//DS_factor] = Zyy[f,t]

X_ds   = np.array( [ x for i,x in enumerate(X) if i%DS_factor==0 ]  )
txx_ds = np.array( [ x for i,x in enumerate(txx) if i%DS_factor==0 ]  )
        
Y_ds   = np.array( [ x for i,x in enumerate(Y) if i%DS_factor==0 ]  )
tyy_ds = np.array( [ x for i,x in enumerate(tyy) if i%DS_factor==0 ]  )

#%%
plt.subplot(221)
#plt.plot(xn[:500],'r',y[:500],'b')
plt.plot(xn)

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

print("average sample data: {}, {}".format(np.average(xn),np.average(y)))

scaled = np.int16(y/np.max(np.abs(y)) * 32767)
write_done = 0
while(write_done == 0 and do_write):
    try:
        print("writing to ",os.path.join(path_out,out_name+".wav"))
        write(os.path.join(path_out,out_name+".wav"), fs, scaled)
        write_done = 1
    except PermissionError: 
        input("Close media player")


















