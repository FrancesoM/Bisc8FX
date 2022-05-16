# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:15:30 2021

@author: francesco.maio
"""

no_opt = False
if no_opt:
    FILTER_LEN = 8
    queue = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N"]
    x = [0]*FILTER_LEN
    q_idx = 0
    
    history_idx = 0
    for i in range(len(queue)):
        x[history_idx] = queue[q_idx]
        print(x)
    
        for ii in range(0,FILTER_LEN):
            data_idx = ( history_idx - ii )
            if data_idx < 0:
               data_idx = FILTER_LEN + data_idx
            print( "{} * c[{}]".format(x[data_idx],ii) )
        print("---------")
        history_idx = (history_idx + 1)%FILTER_LEN
        q_idx += 1
else:
    FILTER_LEN = 8
    queue = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N"]
    x = [0]*FILTER_LEN
    q_idx = 0
    
    history_idx = 0
    for i in range(len(queue)):
        x[history_idx] = queue[q_idx]
        print(x)
    
        for ii in range(0,FILTER_LEN):
            data_idx = (history_idx + 1 + ii) % FILTER_LEN
            coeff_idx = FILTER_LEN - ii - 1 
            print( "{} * c[{}]".format(x[data_idx],coeff_idx) )
        print("---------")
        history_idx = (history_idx + 1)%FILTER_LEN
        q_idx += 1        