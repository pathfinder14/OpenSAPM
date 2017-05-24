import math as m
import numpy as np
import matplotlib.pyplot as plt
import kir
import McCormack as mc
import beam_warming as bm
import fedorenko as f
import lax_wendroff as lw

t = [0, 1]  # time interval
x = [0, 1]  # x interval
tau = 0.001  # time step
h = 0.01    # x step
x_nods_quantity = int((x[1]-x[0]) / h)
n1 = int(t[1] / tau)

X = np.arange(x[0], x[1], h)

#different initial conditions
#sin
def sin():
    x0 = x[0]
    init_cond = np.zeros_like(X)
    for i in range(0, x_nods_quantity):
        if 0 <= x0 <= 0.5:
            init_cond[i] = (m.sin(2*m.pi*x0))**3
            x0 += h
        else:
            init_cond[i] = 0.0
            x0 += h
    return init_cond
# end sin

#sharp peak
def sharp_peak():
    x0 = x[0]
    init_cond = np.zeros_like(X)
    for i in range(0, x_nods_quantity):
        init_cond[i] = 10 - 10*abs(x0)
        x0 += h
    return init_cond
#sharp peak end

#stupenka
def stup():
    x0 = x[0]
    init_cond = np.zeros_like(X)
    for i in range(0, x_nods_quantity):
        if 0 <= x0 < 0.3:
            init_cond[i] = 0
            x0 += h
        elif(0.3 <= x0 <= 0.7):
            init_cond[i] = 1
            x0 += h
        else:
            init_cond[i] = 0
            x0 += h
    return init_cond
#stupenka end
#different initial conditions end

# different transfer velocity
def transfer_velocity_const(value):
    return np.array([value] * x_nods_quantity)

def transfer_velocity_x():
    return np.arange(x[0]+0.005, x[1]+0.005, h)

def transfer_velocity_func():
    transfer_velocity = np.zeros_like(X)
    for i in range(0, len(X)):
        transfer_velocity[i] = 1/(1+X[i]**2)
    return transfer_velocity
# different transfer velocity end

def testing(method, initial, velocity):

    u = np.zeros((n1, x_nods_quantity))  # set the grid
    if initial == 'sin':
        u[0] = sin()

    elif initial == 'peak':
        u[0] = sharp_peak()

    elif initial == 'rectangle':
        u[0] = stup()

    if velocity == 'const':
        transfer_velocity = transfer_velocity_const(0.05)

    elif velocity == 'x':
        transfer_velocity = transfer_velocity_x()

    elif velocity == 'func':
        transfer_velocity = transfer_velocity_func()


    if method == 'KIR':
        for j in range(1, n1-1):
            u[j][0] = 0
            u[j] = kir.kir(x_nods_quantity, u[j-1], transfer_velocity, tau, h)

    elif method == 'McCormack':
        for j in range(1, n1-1):
            u[j][0] = 0
            u[j] = mc.McCormack(x_nods_quantity, u[j-1], transfer_velocity, tau, h)

    elif method == 'Beam-Warming':
        for j in range(1, n1-1):
            u[j][0] = 0
            u[j] = bm.beam_warming(tau, h, u[j-1], transfer_velocity)

    elif method == 'Lax-Wendroff':
        for j in range(1, n1-1):
            u[j][0] = 0
            u[j] = lw.lax_wendroff(x_nods_quantity, u[j-1], transfer_velocity, tau, h)

    elif method == 'Fedorenko':
        transfer_velocity = transfer_velocity_const(1)
        for j in range(1, n1-1):
            u[j][0] = 0
            u[j] = f.fedorenko(grid = u[j-1], tau = tau, h = h)

    """elif method == 'Rusanov':
        for j in range(1, n1-1):
            u[j][0] = 0
            u[j] = f.fedorenko(x_nods_quantity, grid = u[j-1], transfer_velocity[j], tau = tau, h = h)
            """


    fig = plt.figure()
    fig = fig.add_subplot(111)
    plt.plot(X, u[0], label = 't = 0')
    plt.plot(X, u[100], label = 't = 0.1 s')
    plt.plot(X, u[300], label = 't = 0.3 s')
    plt.plot(X, u[500], label = 't = 0.5 s')
    plt.plot(X, u[700], label = 't = 0.7 s')
    plt.plot(X, u[900], label = 't = 0.9 s')
    plt.grid()
    plt.legend()
    fig.set_title(method + ' ' + initial + ' ' + velocity)
    fig.set_xlabel(u'x')
    fig.set_ylabel(u'u(x)')
    plt.savefig(method + '_' + initial +'_'+ velocity +'.png')
