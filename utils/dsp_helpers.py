# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:29:57 2022

@author: francesco.maio
"""

import numpy as np
import math

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

def apply_lut(y,LUT):
    return np.array( [ LUT[int(y_i) + (1<<15)] for y_i in y] , dtype=np.float64) 