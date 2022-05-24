# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:29:36 2022

@author: francesco.maio
"""

import os
import struct
import numpy as np
import scipy.io.wavfile as wav

def open_decimal(path,name,dtype=int):
    data = []
    with open(os.path.join(path,name)) as fd:
        lines = fd.readlines()
        lines = list(filter( lambda l : len(l)>1 ,lines))
        for l in lines:
            data.append(dtype(l))
        return data
    
def rvitis_memdump(basepath,name,f1="H",f2="h"):
    
    full_path = os.path.join(basepath,name)
    
    with open(full_path,"rb") as fd:
        content = fd.read()
    
    S = len( content)//4 #/2 2 array, /2 2 bytes per number
    ret1 = np.zeros(S)
    ret2 = np.zeros(S)
    
    for i in range(S):
        ret1[i] = struct.unpack("<"+f1,content[4*i   : 4*i+2])[0]
        ret2[i] = struct.unpack("<"+f2,content[4*i+2 : 4*i+4])[0]
            
    return ret1,ret2
            
def rmem(basepath,name,bits,el_packed,dtype=int,signed=True):
      
    full_path = os.path.join(basepath,name)
    #print_file_info(full_path)
     
    assert bits in (16,32)
    
    # elements per line
    N = el_packed
    
    width_format = "h" if bits == 16 else "i"
    type_format  = width_format if signed else width_format.upper()
    endianness   = ">"
        
    formatter = endianness + type_format*N
    
    with open(full_path) as fd:
        lines = fd.readlines()
        #get all the hex strings
        lines = list( filter ( lambda l: len(l)>1 , lines))

        ou = []
        ou_temp = [ list(struct.unpack(formatter,bytes.fromhex(hstr)))[::-1] for hstr in lines ]
        
        for l in ou_temp:
            ou += l
            

    return np.array(ou,dtype=dtype)

def wmem(arr,opath,oname,ipath=None,iname=None,pack_elements=1,from_file=False,formatter="h"):
    
    
    # if arr = None fetch data from file
    if from_file == True:
        v = open_decimal(ipath,iname)
    else:
        v = arr
    
    
    i = 0
    vec_slice = v[0:pack_elements]
    with open(os.path.join(opath,oname),"w") as fd:
        #format is: left most in the string is the latest sample, right most is the earliest
        #that's because in system verilog, if it is read as 0x1234abcd the "d" is the LSB hence at pos [3:0]
        while len(vec_slice) == pack_elements:
            vec_slice = vec_slice[::-1]
            fd.write("{}\n".format(struct.pack("{}{}".format(">",formatter*pack_elements),*vec_slice).hex()))
            i += pack_elements
            vec_slice = v[i:i+pack_elements]
            
def wcoe_file(arr,opath,oname,ipath=None,iname=None,pack_elements=1,from_file=False):
    
    temp_ext = ".temp"
    wmem(arr.astype(np.int16),opath,oname+temp_ext,pack_elements=1,formatter="h")
    
    with open(os.path.join(opath,oname+temp_ext)) as fr:
        lines = fr.readlines()
        
    with open(os.path.join(opath,oname+".coe"),"w") as fw:
        fw.write("memory_initialization_radix = 16;\n")
        fw.write("memory_initialization_vector =\n")
        for line in lines:
            fw.write(line)
    
    os.remove(os.path.join(opath,oname+temp_ext)) 
    
    
    
def save_WAV(arr,fs,path_out,out_name):
    
    x = arr.astype(np.int16)

    write_done = 0
    while(write_done == 0):
        try:
            print("writing to ",os.path.join(path_out,out_name+".wav"))
            wav.write(os.path.join(path_out,out_name+".wav"), fs, x)
            write_done = 1
        except PermissionError: 
            input("Close media player")
    
    
    
    
    
    
    
    