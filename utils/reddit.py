# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 17:17:18 2021

@author: francesco.maio
"""

import numpy as np
import math
import matplotlib.pyplot as plt

def sat_16b_signed(x):
    return ( math.atan(x/ ( (1<<15)/2)  ) ) * ( (1<<15)/1.2)

t = np.linspace(-(1<<15),(1<<15),50)
y = np.array([ sat_16b_signed(y_i) for y_i in t  ])

LUT = np.zeros((1<<16),dtype=int)

for i in range(LUT.shape[0]):
    LUT[i] = sat_16b_signed( i - (1<<15) )

print("LUT has shape: ",LUT.shape)

with open("atan_lut_almost_linear.h","w") as fd:
    fd.write("#ifndef ATAN_LUT_H\n")
    fd.write("#define ATAN_LUT_H\n")
    fd.write("short atan_lut_almost_linear[{}] = {} {},\n".format(len(LUT),'{',int(LUT[0])))
    for x in LUT[1:-1]:
        fd.write("\t\t")
        fd.write(str(int(x))+",\n")
    fd.write("{} {};\n".format(int(LUT[-1]),'}'))
    fd.write("#endif")

#plt.plot(t,y)

plt.plot(np.arange(0,LUT.shape[0],dtype=int),LUT)

