# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 16:34:53 2021

@author: francesco.maio
"""

import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from scipy import signal
import os
import math

from pydub import AudioSegment


import datetime

path_in = "debug_data"
path_out = "wav_files"
name = "Recording.m4a"

out_name = name

full_path = os.path.join(os.getcwd(),name)
print(full_path)

audio = AudioSegment.from_file(full_path)

xn = np.array( audio.get_array_of_samples() ) 

X, txx, Zxx = signal.stft(xn, audio.frame_rate*2, nperseg=4096)

X = X[3500:]
Zxx = Zxx[3500:,:]

plt.yscale('symlog')
plt.pcolormesh(txx, X, np.abs(Zxx), shading='gouraud')