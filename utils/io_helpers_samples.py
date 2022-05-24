# -*- coding: utf-8 -*-
"""
Created on Mon May 23 23:19:49 2022

@author: francesco.maio
"""

# This is an example script on how to use the io_helpers to create files to feed the vivado simulator, or to read the captured
# waveforms and transform them into files for further python analysis. 

# It's good practice to declare paths at the beginning of the script
input_path  = "..."  # this is where data will be taken
output_path = "..."  # this is where data will be saved. 

# Read memory dump from vitis. In this case data is written in binary format, and since we are reading from the Bisc8 bitstream
# we have always 2 arrays. Where those arrays come from depends on where the data_gather IP is placed in the hardware design. 

