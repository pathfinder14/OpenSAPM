from numpy import *
import eno_weno_routines
nx = 81
dx = 2./(nx-1)
x = linspace(0,2,nx)
nt = 25    
dt = .02  
c = 1.      #assume wavespeed of c = 1
u = zeros(nx)      #numpy function ones()
u[.5/dx : 1/dx+1]=2  #setting u = 2 between 0.5 and 1 as per our I.C.s
k = 3 # number of weights Order= 2*k-1
gc = k-1 #number of ghost cells 
#adding ghost cells 
gcr=x[-1]+linspace(1,gc,gc)*dx
gcl=x[0]+linspace(-gc,-1,gc)*dx
xc = append(x,gcr)
xc = append(gcl,xc)
uc = append(u,u[-gc:])
uc = append(u[0:gc],uc)

gs = zeros((nx+2*gc,nt))
flux = zeros(nx+2*gc)

for n in range(1,nt):  
    un = uc.copy() 
    for i in range(gc,nx-1+gc): #i=2
        xloc = xc[i-(k-1):i+k] #i+k-1-(i-(k-1)-1) = 2k -1 
        uloc = uc[i-(k-1):i+k]
        f_left,f_right = WENO(xloc,uloc,k)
        #upwind flux
        flux[i]=0.5*(c+fabs(c))*f_left + 0.5*(c-fabs(c))*f_right

    for i in range(gc,nx-gc):
        if c>0:
            uc[i] = un[i]-dt/dx*(flux[i]-flux[i-1])
        else:
            uc[i] = un[i]-dt/dx*(flux[i+1]-flux[i])