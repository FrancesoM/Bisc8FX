# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:29:36 2022

@author: francesco.maio
"""

import os
import struct
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
import time

class data_file(object):
    
    def __init__(self,path,name,bits,signed,out_type=float,el_per_row=1):
        self.ext = name.split(".")[-1]
        if( self.ext == "dat"):
            op = open_decimal
            op_params = [path,name,out_type]
        elif( self.ext == "mem" ):
            op = rmem
            op_params = [path,name,bits,el_per_row,out_type,signed]
        elif( self.ext == "bin"):
            op = rvitis_memdump
            op_params = [path,name,bits,signed]
        else:
            assert False,"Can't recognize extension"
            
        self.open_handle = op
        self.open_params = op_params
        
    def open(self):
        
        return self.open_handle(*self.open_params)

def open_decimal(path,name,dtype=int):
    data = []
    with open(os.path.join(path,name)) as fd:
        lines = fd.readlines()
        lines = list(filter( lambda l : len(l)>1 ,lines))
        for l in lines:
            data.append(dtype(l))
        return np.array(data)

def write_decimal(path,name,data,dtype=int):
    
    with open(os.path.join(path,name),"w") as fd:
        for d in data:
            fd.write(str(dtype(d)))
            fd.write("\n")

def rvitis_memdump(basepath,name,bits,signed):
        
    full_path = os.path.join(basepath,name)
    
    width_format = "h" if bits == 16 else "i"
    type_format  = width_format if signed else width_format.upper()
    endianness   = "<"
    
    formatter = endianness + type_format*1
    
    with open(full_path,"rb") as fd:
        content = fd.read()
    
    
    a = []
    k = 0
    for i in range(len(content)//2):
        bstring = content[k:k+2]
        a.append( struct.unpack(formatter,bstring)[0]  )
        k = k+2
            
    return np.array(a)
            
def rmem(basepath,name,bits,el_packed,dtype=int,signed=True):
      
    full_path = os.path.join(basepath,name)
    #print_file_info(full_path)
     
    assert bits in (16,32)
    
    # elements per line
    N = el_packed
    
    width_format = "h" if bits == 16 else "i"
    type_format  = width_format if signed else width_format.upper()
    endianness   = "<"
        
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
    
    
def listen_wave(x,fs):
    # Duration
    duration_s = len(x)/fs
    
    # Attenuation so the sound is reasonable
    atten = 0.3
    
    # Rescale between -1 and 1 
    waveform = x / np.abs( x.max() -  x.min() )
    waveform_quiet = waveform*atten
    
    # Play the waveform out the speakers
    sd.play(waveform_quiet, fs)
    time.sleep(duration_s)
    sd.stop()
    
    
if __name__ == "__main__":
    
    p = "raw_data/monitor0.bin"
    with open(p,"rb") as fb:
        content = fb.read()
    
    a = []
    k = 0
    for i in range(len(content)//8):
        bstring = content[k:k+2]
        a.append( struct.unpack("<h",bstring)[0]  )
        k = k+2
        
    
    
    
    
    
    