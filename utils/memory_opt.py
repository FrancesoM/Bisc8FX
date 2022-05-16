# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:35:38 2021

@author: francesco.maio
"""

import numpy as np
import matplotlib.pyplot as plt

def roofline(t,m,r):
    y = t*m
    ret = np.array([int(x) if x < r else r for x in y]) if r != None else y
    return ret

def ptr_pos(y,O):
    return np.array([x%O for i,x in enumerate(y)])

def check_overwrite(idx_fast,idx_slow,O):
    
    max_address  = np.max(idx_slow)
    memory       = np.array([0]*max_address)
    
    L = len(idx_slow)
    conflicts    = np.zeros(L)
    for i in range(1,L):
        
        w_addr_pre = idx_fast[i-1]
        w_addr = idx_fast[i]
        
        r_addr_pre = idx_slow[i-1]
        r_addr = idx_slow[i]
        
        if (np.any(memory[w_addr_pre:w_addr]) ):
            print("Writing to un-read address!")
            conflicts[i] = 1
            return conflicts,-1
        
        #write here
        if idx_fast[i] < max_address:
            memory[w_addr_pre:w_addr] = 1
        #read here
        memory[r_addr_pre:r_addr] = 0
        
        
    return conflicts,0
    
        

T = 20000000 - 5000000
fs = 10000000
D = fs*8/2

M = None
cyclic = 0
find_best = 0


figure, ( ax1,ax2,ax3) = plt.subplots(3, 1)

tmax = M/T if M != None else 0.0002
t = np.linspace(0,tmax,1000)

TCP_transfer = roofline(t,T,M)
DMA_transfer = roofline(t,D,M)

ax1.plot(t,TCP_transfer,"b")
ax1.plot(t,DMA_transfer,"r")

if M != None and cyclic == True:
    if find_best == True:
        O = 1000
        trials = 0
        
        ptr_TCP = ptr_pos(TCP_transfer,O)
        ptr_DMA = ptr_pos(DMA_transfer,O)
        
        while( check_overwrite(ptr_DMA,ptr_TCP,O)[1] == -1 and trials < 100):
            O += 100
            ptr_TCP = ptr_pos(TCP_transfer,O)
            ptr_DMA = ptr_pos(DMA_transfer,O)
            trials+=1
        
        print("O : ",O)
        
        
        ax2.plot(t,ptr_TCP,"b")
        ax2.plot(t,ptr_DMA,"r")
        
        #overwrite(ptr_DMA,ptr_TCP,O)
        
        ax3.plot(t,check_overwrite(ptr_DMA,ptr_TCP,O)[0])
    else:
        O = 1000
        
        ptr_TCP = ptr_pos(TCP_transfer,O)
        ptr_DMA = ptr_pos(DMA_transfer,O)
        
       
        ax2.plot(t,ptr_TCP,"b")
        ax2.plot(t,ptr_DMA,"r")
        
        #overwrite(ptr_DMA,ptr_TCP,O)
        
        ax3.plot(t,check_overwrite(ptr_DMA,ptr_TCP,O)[0])        

plt.show()