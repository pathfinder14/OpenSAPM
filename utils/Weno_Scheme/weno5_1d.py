import numpy as np
import matplotlib.pyplot as plt
from eno_weno_routines import *


nx = 81
dx = 2./(nx-1)
x = np.linspace(0,2,nx)
nt = 25    
dt = .02  
c = 1.      #assume wavespeed of c = 1
u = np.zeros((1,nx))
for i in range(int(nx/2)):
    u[0][i] = 1
for i in range(int(nx/2), nx):
    u[0][i] = 2
#u = np.zeros(nx)      #numpy function ones()
#u[.5/dx : 1/dx+1]=2  #setting u = 2 between 0.5 and 1 as per our I.C.s
k = 3 # number of weights Order= 2*k-1
gc = k-1 #number of ghost cells 
#adding ghost cells 
gcr=x[-1] + np.linspace(1,gc,gc)*dx
gcl=x[0] + np.linspace(-gc,-1,gc)*dx
xc = np.append(x,gcr)
xc = np.append(gcl,xc)
uc = np.append(u,u[-gc:])
uc = np.append(u[0:gc],uc)

gs = np.zeros([nx+2*gc,nt])
flux = np.zeros(nx+2*gc)

for n in range(1,nt):  
    un = uc.copy() 
    for i in range(gc,nx-1+gc): #i=2
        xloc = xc[i-(k-1):i+k] #i+k-1-(i-(k-1)-1) = 2k -1 
        uloc = uc[i-(k-1):i+k]
        f_left,f_right = WENO(xloc,uloc,k)
        #upwind flux
        flux[i]=0.5*(c+np.fabs(c))*f_left + 0.5*(c-np.fabs(c))*f_right

    for i in range(gc,nx-gc):
        if c>0:
            uc[i] = un[i]-dt/dx*(flux[i]-flux[i-1])
        else:
            uc[i] = un[i]-dt/dx*(flux[i+1]-flux[i])


plt.plot(uc, '.')
plt.show()