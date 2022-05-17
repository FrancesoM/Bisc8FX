# -*- coding: utf-8 -*-
"""
Created on Fri May 13 13:59:42 2022

@author: francesco.maio
"""

import os
import matplotlib.pyplot as plt
import numpy as np

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

def load_dat(path,name):
    data = []
    with open(os.path.join(path,name)) as fr:
        lines = fr.readlines()

    for line in lines[:-1]:
        data.append( int(line,10))
        
    return data

def print_data_characteristics(data):
    
    peak2peak = abs(max(data)-min(data))
    mean = sum(data)/len(data)
    
    print(" peak_to_peak amplitude: {} mean: {} ".format(peak2peak,mean))
    

opath = "C:\\Users\\francesco.maio\\Desktop\\Bisc8FX\\ip_repo\\hls_ip\\digital_setup\\digital_setup_prj\\csim\\build"
oname = "digital_setup_out.dat"

opathrtl = "C:\\Users\\francesco.maio\\Desktop\\Bisc8FX\\ip_repo\\hls_ip\\digital_setup\\digital_setup_prj\\sim\\wrapc"

ipath = "C:\\Users\\francesco.maio\\Desktop\\Bisc8FX\\ip_repo\\hls_ip\\digital_setup\\srcs"
iname = "axis_tdata_full.dat"

oo = load_dat(opath,oname)[512:10000]
oortl = load_dat(opathrtl,oname)[512:10000]

ii = load_dat(ipath,iname)[512:10000]

print("Data characteristics: \n")

print("input: " ); print_data_characteristics(ii)
print("output: " ); print_data_characteristics(oo)




plt.plot(oo)
plt.plot(np.array(oortl)+1000)

