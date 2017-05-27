import numpy as np
import matplotlib.pyplot as plt
from WENOmethod import *


nx = 81
h = 2./(nx-1)
x = np.linspace(0,2,nx)
nt = 25    
tau = .02  
a = 1.      #assume wavespeed of a = 1
u = np.zeros(nx)
for i in range(int(nx/2)):
    u[i] = 1
for i in range(int(nx/2), nx):
    u[i] = 2






plt.plot(WENOmethod(a, tau, h, u), '.')
plt.show()