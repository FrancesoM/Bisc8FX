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

class queue(object):
    def __init__(self,lenght):
        self.internal_array=np.zeros(lenght)
        
    def push(self,val):
        out = self.internal_array[0]
        for i in range(1,len(self.internal_array)):
            self.internal_array[i-1] = self.internal_array[i]
        self.internal_array[-1] = val
        return out
    
    def __str__(self):
        return str(self.internal_array)
    
    def __getitem__(self,i):
        return self.internal_array[i]

def sat_16b_signed(x):
    return ( math.atan(x/ ( (1<<15)/10)  ) ) * ( (1<<15)/1.5)


def moving_average(x,n):
    out = np.zeros(np.shape(x))
    out[0:n] = x[0:n]
    
    sm = 0
    for k in range(n):
        sm += x[k]
    
    out[n] = sm/n
    
    for i in range(n,len(x)):
        sm -= x[i-n]
        sm += x[i]
        out[i] = sm/n
        
    return out
        

def float2fix(f,nbits):
    ret = int( f*(2**nbits) )
    return ret

def hls_filter(b,a,x,fixed=True,n_bits=16,do_debug=True):
    
    ret_deb_string = ""
    
    #print("Poles and zeros before quantization: ",signal.tf2zpk(b,a))
    
    #fixed point calculations
    if fixed:
        b = np.array(list(map(lambda coeff: float2fix(coeff,n_bits), b)), dtype=int)
        a = np.array(list(map(lambda coeff: float2fix(coeff,n_bits), a)), dtype=int)
    
    #print("Poles and zeros after quantization: ",signal.tf2zpk(b/(1<<n_bits),a/(1<<n_bits)))
    
    out_x = np.zeros(x.shape)
    
    Q = len(b)
    xqueue = np.zeros(Q)
    yqueue = np.zeros(Q)
    q_idx = 0
    
    yqueue_filled = False
    
    quant_err = 0
    
    for i in range(len(x)):
        #t0 = datetime.datetime.now()
        ############## filter operations ####################
        
        # new sample arrives
        xqueue[q_idx] = int(x[i])
        
        b0m = q_idx
        b1m = q_idx-1 if q_idx-1 >= 0 else q_idx-1+Q
        b2m = q_idx-2 if q_idx-2 >= 0 else q_idx-2+Q
        
        yq_idx = q_idx
        a0m = yq_idx-1 if yq_idx-1 >= 0 else yq_idx-1+Q
        a1m = yq_idx-2 if yq_idx-2 >= 0 else yq_idx-2+Q
        
        
        if( yqueue_filled == True):
            temp = int(b[0])*int(xqueue[b0m])+\
                   int(b[1])*int(xqueue[b1m])+\
                   int(b[2])*int(xqueue[b2m])-\
                   int(a[1])*int(yqueue[a0m])-\
                   int(a[2])*int(yqueue[a1m])+\
                   int(quant_err)
        else:
            temp = int(b[0])*int(xqueue[b0m])
                
        if fixed:
            out_v = int(temp)//(1<<n_bits)
            quant_err = temp - (out_v*(1<<n_bits) )
        else:
            out_v = temp

           
        yqueue[q_idx] = out_v
        
        out_x[i] = out_v
        
        
        ############## debug operations ####################
        
        if( do_debug and i<100):
            debug_string = """ 
                
                a = {}
                b {}
            
                q_idx = {}       
                b0m = {}
                b1m = {}
                b2m = {}
                
                a0m = {}
                a1m = {}
                xqueue = {}
                yqueue = {}\n\n""".format(a,b,q_idx,b0m,b1m,b2m,a0m,a1m,xqueue,yqueue)
                                   
            ret_deb_string += debug_string
                  
        ############## update operations ####################
        
        q_idx = (q_idx+1)%Q
        
        if i >= len(yqueue):
            yqueue_filled = True
        
        # t1 = datetime.datetime.now()
        # delta = t1  - t0
        # print("{}: {}".format(i,delta.total_seconds() * 1000000))
        
    return out_x,ret_deb_string

def hls_filter_Q_model(b,a,x,fixed=True,n_bits=16,do_debug=True):
    
    ret_deb_string = ""
    
    #print("Poles and zeros before quantization: ",signal.tf2zpk(b,a))
    
    #fixed point calculations
    if fixed:
        b = np.array(list(map(lambda coeff: float2fix(coeff,n_bits), b)), dtype=int)
        a = np.array(list(map(lambda coeff: float2fix(coeff,n_bits), a)), dtype=int)
    
    #print("Poles and zeros after quantization: ",signal.tf2zpk(b/(1<<n_bits),a/(1<<n_bits)))
    
    out_x = np.zeros(x.shape)
    
    Q = len(b)
    xqueue = queue(Q)
    yqueue = queue(Q)
    
    quant_err = 0
    
    for i in range(len(x)):
        #t0 = datetime.datetime.now()
        ############## filter operations ####################
        
        # new sample arrives
        xqueue.push(int(x[i]))
        
        temp = int(b[0])*int(xqueue[2])+\
               int(b[1])*int(xqueue[1])+\
               int(b[2])*int(xqueue[0])-\
               int(a[1])*int(yqueue[2])-\
               int(a[2])*int(yqueue[1])+\
               int(quant_err)
                
        if fixed:
            out_v = int(temp)//(1<<n_bits)
            quant_err = temp - (out_v*(1<<n_bits) )
        else:
            out_v = temp

           
        yqueue.push(out_v)
        
        out_x[i] = out_v
    
    return out_x,ret_deb_string

path_in = "raw_data"
path_out = "wav_files"
name = "digital_setup_out.dat"
name2 = None
out_name = name

do_ac_filter=0
do_filter=1
do_saturate=0
built_in_filter=0

do_write = 1

fs = 41810

with open("LUT_sat_16b_signed") as fd:
    LUT = fd.read().split("\n")[1:]


data = []
with open(os.path.join(path_in,name)) as fd:
    lines = fd.read().split("\n")
    for l in lines[512:]:
        if len(l) > 0:
            data.append(float(l))

if name2 != None:
    #Concat the two recordings
    out_name += "_"+name2
    with open(os.path.join(path_in,name2)) as fd:
        lines = fd.read().split("\n")
        for l in lines:
            if len(l) > 0:
                data.append(float(l))

    
xn = np.asarray(data,dtype=np.float64) #- np.mean(data)
#xn = xn[50000:]
print(xn)
print(xn.shape)

#remove hf noise
b, a = signal.butter(2, 0.1)
bhp,ahp = signal.butter(2,0.00239,btype="high")

#remove power supply noise
bp, ap = signal.iirnotch(50, 30, fs)

#zi = signal.lfilter_zi(b, a)
#z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

#z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

y=xn

if do_saturate:
    #y = np.array([ ( np.sign(y_i) )*(1 - np.exp( - 100*(1/amplitude)*abs(y_i) ) ) for y_i in y  ])*amplitude
    #y = np.array([ sat_16b_signed(y_i) for y_i in y  ])
    y = np.array( [ LUT[int(y_i) + (1<<15)] for y_i in y] , dtype=np.float64) 
    
    out_name += "_saturated_"

if do_filter:
    if built_in_filter:
        y = signal.filtfilt(b, a, y)
        y = signal.filtfilt(bhp, ahp, y)
    else:
        
        
        y,debug2 = hls_filter_Q_model(bhp,ahp,y,fixed=True,do_debug=True)
        y,debug1 = hls_filter_Q_model(b,a,y,fixed=True)
    

    out_name+="_filtered_"


if do_ac_filter:
    y = signal.filtfilt(bp,ap,y)
    out_name+="_noAC_"
    
#y = y - np.mean(y)

#X_n = np.fft.fft(xn - np.mean(xn))
#Y = np.fft.fft(y - np.mean(y))

X, txx, Zxx = signal.stft(xn, fs, nperseg=4096)
Y, tyy, Zyy   = signal.stft(y, fs, nperseg=4096)

freq = np.fft.fftfreq(len(xn))*fs

# Harsh downsample by 4 for displaying purposes

assert Zxx.shape == Zyy.shape

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


















