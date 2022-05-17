# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 17:17:18 2021

@author: francesco.maio
"""

import numpy as np
import math
import matplotlib.pyplot as plt

def sat_16b_signed(x,steep):
    return math.atan(x/( (1<<15) * (0.05 + 0.1*steep) ))   

N = 4
LUTs = []

for sig in range(N):
    LUT = np.zeros((1<<16),dtype=float)
    for i in range(LUT.shape[0]):
        LUT[i] = sat_16b_signed( i - (1<<15) , sig)
        
    #rescale such that it's between -32k and +32k
    LUT = (1<<16)*LUT/(np.max(LUT)-np.min(LUT))
        
    print(f"{sig} - max {np.max(LUT)} - min {np.min(LUT)}")
    LUTs.append(LUT)



for i in range(N):
    plt.plot(np.arange(0,LUTs[i].shape[0],dtype=int),LUTs[i])
    
    
    with open(f"atan_lut_steep_{i}.h","w") as fd:
        fd.write(f"#ifndef ATAN_LUT_{i}_H\n")
        fd.write(f"#define ATAN_LUT_{i}_H\n")
        fd.write("#include <ap_axi_sdata.h>\n")
        fd.write("ap_int<16>  atan_lut_steep_{}[{}] = {} {},\n".format(i,len(LUT),'{',int(LUT[0])))
        for x in LUT[1:-1]:
            fd.write("\t\t")
            fd.write(str(int(x))+",\n")
        fd.write("{} {};\n".format(int(LUT[-1]),'}'))
        fd.write("#endif")
