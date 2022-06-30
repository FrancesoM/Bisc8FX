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

xname = "monitor0.bin"
yname = "monitor1.bin"

out_name = xname

do_ac_filter=0
do_filter=0
do_saturate=1
built_in_filter=0

do_write = 0

fs = 41810

LUT = io_helpers.open_decimal(".","atan_lut_steep_1.dat")

x = io_helpers.data_file(path_in, xname, 16, True).open()
#y = io_helpers.data_file(path_in, yname, 16, True).open()

xn = x[512:] 
xn = xn - xn.mean()
#yn = y[512:]

io_helpers.listen_wave(x,fs)

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

    y = dsp_helpers.apply_lut(y,LUT)
    
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
    
io_helpers.listen_wave(y,fs)

X, txx, Zxx = signal.stft(xn, fs, nperseg=4096)
Y, tyy, Zyy   = signal.stft(y, fs, nperseg=4096)

freq = np.fft.fftfreq(len(xn))*fs

# Harsh downsample by 4 for displaying purposes

DS_factor =4
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


















