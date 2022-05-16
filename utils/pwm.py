# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 10:20:30 2021

@author: francesco.maio
"""

import numpy as np
import matplotlib.pyplot as plt

Fn = lambda n,W,T : (W/T)*np.sinc(n*np.pi*(W/T))

figure, (axs) = plt.subplots(3, 2)

# different duty

N = np.arange(-20,20,1)

T = [ 0.1, 0.00001 ] #1ms

for k,t in enumerate(T):
    for i,d in enumerate( [0.2, 0.5, 0.7] ):
        print(i,d)
        W = t*d
        freqs = N*2*np.pi/t
       
        for n in N:
            f=freqs[n]
            axs[i,k].vlines(f,0,Fn(n,W,t)) 
            
        plt.draw()
        plt.pause(0.2)