import numpy as np
import matplotlib.pyplot as plt
from WENOmethod import *
import math

uTestList = ['step', 'gauss', 'peack']

for uTest in uTestList:
    nt = 25     
    a = -0.5      #assume wavespeed of a = 1
    left = 1.0 # пределы по оси x
    right = 2.4
    h = 0.005
    nx = int((right - left) / h)
    x = np.linspace(0,2,nx + 2)
    u = np.zeros(nx)
    ## h = 2./(nx-1)
    cfl = 0.09
    tau = cfl*h/abs(a)
    t_end = 0.6 # Время (t_end / dt задает количество итераций)
    if uTest == 'step':
        for i in range(int(nx/50)):
            u[i] = 1
        for i in range(int(nx/50), int(nx/3)):
            u[i] = 2
        for i in range(int(nx/3), nx):
            u[i] = 1
    elif uTest == 'gauss': # функция Гаусса
        sigma = 0.02
        pi = 3.14
        # mu = 1.5
        mu = left + (right - left) / 2.5
        for i in range(nx):
            u[i] = 1.0 + 0.05 * 1.0 / (sigma * math.sqrt(2*pi)) * math.exp(-((left + i*h - mu)*(left + i*h - mu)) / (2.0 * sigma * sigma))
    elif uTest == 'peack': # пик        
        sigma = 0.1
        pi = 3.14

        mu = left + (right - left) / 2.5
        delta = (mu - left) / 2.0
        length = right - left
        for i in range(int(delta/length * nx), int(3 * delta/length * nx)):#range(n/4, 3*n/4): # пик на финитном носителе
            # u_0[0][i] =  1/(1 + 1000*(left + i*dx - mu)*(left + i*dx - mu))
            if (left + i*h - mu) == 0.0:
                u[i] = 1.0
            else:
                u[i] = math.sin(100*(left + i*h - mu)) / (100*(left + i*h - mu))
    
    u0 = np.zeros(nx, dtype=np.float)
    for i in range(nx):
        u0[i] = u[i]

    u = WENOmethod(a, tau, h, u)
    ut1 = np.zeros(nx, dtype=np.float)
    ut2 = np.zeros(nx, dtype=np.float)
    ut3 = np.zeros(nx, dtype=np.float)
    '''
    for k in range(int(t_end / tau)):
        u = WENOmethod(a, tau, h, u0) # u0, a - матрицы 1xn
        
        if k == int(t_end / tau * 0.25):
            for i in range(nx):
                ut1[i] = u0[i]
        elif k == int(t_end / tau * 0.5):
            for i in range(nx):
                ut2[i] = u0[i]
        elif k == int(t_end / tau * 0.75):
            for i in range(nx):
                ut3[i] = u0[i]
        for i in range(nx - 2):
            u0[i] = u[0]
    '''
    x1 = np.zeros(nx + 2, dtype=np.float)
    i= left
    for j in range(nx + 2):
        x1[j] = i
        i = i + h  

    
    plt.subplot(311)
    plt.plot(x, u, marker = '*', label = 'U_1 (t = ' + str(t_end) + ')') #'.')
    if uTest == 'step':
        plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.25)
    else:
        plt.legend(bbox_to_anchor=(0.35, 1), loc=1, borderaxespad=0.25)
    plt.ylabel('U')
    plt.xlabel('x')

    '''print(len(x), len(x1), len(u))
    plt.subplot(312)
    plt.plot(x1[:-2], u0, marker = '.') # '.') 
    plt.plot(x1[:-2], ut1, marker = '.', label = 'U (t = ' + str(t_end * 0.25) + ')') # '.') 
    plt.plot(x1[:-2], ut2, marker = '.', label = 'U(t = ' + str(t_end * 0.5) + ')') # '.') 
    plt.plot(x1[:-2], ut3, marker = '.', label = 'U (t = ' + str(t_end * 0.75) + ')') # '.') 
    plt.plot(x, u, marker = '.', label = 'U (t = ' + str(t_end) + ')') #'.')
    if uTest == 'step':
        plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.25)
    else:
        plt.legend(bbox_to_anchor=(0.33, 1), loc=1, borderaxespad=0.25)
    '''        
    plt.savefig('plots/_' + '_U0_' + uTest + '.png')
    
