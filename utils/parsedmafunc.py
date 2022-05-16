# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 18:04:41 2021

@author: francesco.maio
"""

"""
Find the xaxidma calls inside the relative function
"""
outFunction = 0
inFunction = 1
state = outFunction
level = 0

with open(fname) as fr:
    lines = fr.read().split("\n")
    
for l in lines:
    if state == inFunction:
        if "\{" in l:

            level+=1
        
        if "\}" in l:
            if level>0:
                level-=1
            else:
                state = outFunction
                
    else:
        
        if "\{" in l:
            print(l)
            state = inFunction
        