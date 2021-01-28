# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 11:40:48 2021

@author: francesco.maio
"""

import numpy as np
import matplotlib.pyplot as plt

"""
figure, (ax1, ax2) = plt.subplots(2, 1)


# Check that the frequency content is the expected
X_n = np.fft.fft(x_n)
freq = np.fft.fftfreq(len(x_n))*fs

# Plot the results 
ax1.plot(x_n)
ax2.semilogx(freq,abs(X_n))
"""

initial = 0
if initial:
    #Rin = 1e6
    R2 = 1e6
    R3 = 1e6
    C1 = 10*1e-9
    C2 = 10*1e-9    
else:
    #Rin = 1e6
    R2 = 2*1e6
    R3 = 1e5
    C1 = 30*1e-9
    C2 = 30*1e-9


A = lambda s: 1/(R2*C1*s)
B = lambda s,Rin: (C1*Rin*s - 1)/(C1*R2*s)
C = lambda s: (R3*C2*s - 1)/(R3*C2*s)

in_over_out = lambda s,Rin: 1 + A(s) + B(s,Rin)*C(s)

G = lambda s,Rin: 1/in_over_out(s,Rin)

freqs = np.arange(1,10000,1,dtype=np.single)
freqs = freqs*1j

bode = lambda Rin: [ abs(G(f,Rin)) for f in freqs ]

lg = []
for r in [0.4*1e6, 0.5*1e6, 1e6, 1.5*1e6,  2*1e6]:
    plt.semilogx(abs(freqs),bode(r))
    lg.append(str(r))

plt.semilogx([80,80],[0,1],"-")

plt.legend(lg)



















