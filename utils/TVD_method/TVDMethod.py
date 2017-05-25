import numpy as np
'''
du/dt + a du/dx = 0
TVD метод для уравнения переноса
a - параметр перед производной по x
dt - шаг по времени
dx - шаг по координате
u - начальное условие t=0
limitter - выбор лимиттера, может принимать следующие значения,
    соответсвующие лимиттерам с тем же названием:
    'Superbee'
    'MC'
    'Minmod'
    'Koren'
    'Osher'
    'Ospre'
    'Smart'
    'Sweby'
    'VanAlbada1'
    'UMIST'
    'VanAlbada2'
    'VanLeer'
'''
def TVDMethod(a,dt,dx, u, limitter): #,u0,u):
    
    n = len(u[0])

    # Инициализация векторов
    r = np.zeros((1,n), dtype=np.float)
    F_rl = np.zeros((1,n), dtype=np.float)
    F_rh = np.zeros((1,n), dtype=np.float)
    F_ll = np.zeros((1,n), dtype=np.float)
    F_lh = np.zeros((1,n), dtype=np.float)
    F_right = np.zeros((1,n), dtype=np.float)
    F_left  = np.zeros((1,n), dtype=np.float)
    u_next = np.zeros((1,n), dtype=np.float)

    # Вычисление параметра r
    for j in range(1, n - 1):           
        if u[0][j] == u[0][j+1]:
            r[0][j] = 1
        elif a[0][0] > 0:
            r[0][j] = (float(u[0][j]) - float(u[0][j-1])) / (float(u[0][j+1]) - float(u[0][j]))
        elif a[0][0] < 0:    
            r[0][j] = (float(u[0][j+2]) - float(u[0][j+1])) / (float(u[0][j+1]) - float(u[0][j]))
        r[0][0] = 1.0; r[0][n - 1] = 1.0

    # Инициализация лимиттера (phi)
    phi = np.zeros((1, n))

    if limitter == 'Superbee':
        for j in range(n):
            phi[0][j] = max(0, min(2*r[0][j], 1), min(r[0][j], 2)) # Superbee
    elif limitter == 'MC':
        for j in range(n):
            phi[0][j] = max(0, min(2*r[0][j], 0.5*(1 + r[0][j]), 2)) # MC или monotonized central
    elif limitter == 'Minmod':
        for j in range(n):
            phi[0][j] = max(0,min(1, r[0][j])) # Minmod
    elif limitter == 'Koren':
        for j in range(n):
            phi[0][j] = max(0, min(2 * r[0][j], (1 + 2*r[0][j]) / 3.0, 2)) # Koren
    elif limitter == 'Osher':
        for j in range(n):
            phi[0][j] = max(0, min(r[0][j], 1)) # Osher, 1 <= beta <= 2 (вместо 1))
    elif limitter == 'Ospre':
        for j in range(n):
            phi[0][j] = (1.5 * (r[0][j] * r[0][j] + r[0][j])) / (r[0][j] * r[0][j] + r[0][j] + 1.0) # Ospre
    elif limitter == 'Smart':
        for j in range(n):
            phi[0][j] = max(0, min(2*r[0][j], (0.25 + 0.75 * r[0][j]), 4)) # Smart
    elif limitter == 'Sweby':
        for j in range(n):
            beta = 1.0
            phi[0][j] = max(0, min(beta * r[0][j], 1), min(r[0][j], beta)) # Sweby, 1 <= beta <= 2
    elif limitter == 'VanAlbada1':
        for j in range(n):
            phi[0][j] = (r[0][j] * r[0][j] + r[0][j]) / (r[0][j] * r[0][j] + 1) # Van Albada 1
    elif limitter == 'UMIST':
        for j in range(n):
             phi[0][j] = max(0, min(2*r[0][j], (0.25 + 0.75*r[0][j]), (0.75 + 0.25*r[0][j]), 2)) # UMIST
    elif limitter == 'VanAlbada2':
        for j in range(n):
             phi[0][j] = (2 * float(r[0][j]))/(1 + (float(r[0][j])) * (float(r[0][j]))) # Van Albada 2
    elif limitter == 'VanLeer':
        for j in range(n):
             phi[0][j] = (float(r[0][j]) + abs(float(r[0][j])))/(1 + abs(float(r[0][j]))) # Van Leer
    else:
        print "ERROR: invalid limitter!"
        return 0

    for j in range (1, n-1):
        a_m = min(0,a[0][j])
        a_p = max(0,a[0][j])
        
        # Вычисление антидиффузионных потоков   
        F_rl[0][j] = float(a_p)*float(u[0][j]) + float(a_m)*float(u[0][j+1])
        F_rh[0][j] = 0.5*float(a[0][j])*(float(u[0][j])+float(u[0][j+1])) - 0.5*(float(a[0][j]) * float(a[0][j]))*(dt/dx)*(float(u[0][j+1])-float(u[0][j]))           
        F_ll[0][j] = float(a_p)*float(u[0][j-1]) + float(a_m)*float(u[0][j])
        F_lh[0][j] = 0.5*float(a[0][j])*(float(u[0][j-1])+float(u[0][j])) - 0.5*(float(a[0][j]) * float(a[0][j]))*(dt/dx)*(float(u[0][j])-float(u[0][j-1]))
            
        # Вычисление слудующего шага по времени   
        F_right[0][j] = float(F_rl[0][j]) + float(phi[0][j])*( float(F_rh[0][j]) - float(F_rl[0][j]) )
        F_left[0][j]  = F_ll[0][j] + float(phi[0][j-1])*( float(F_lh[0][j]) - float(F_ll[0][j]) )            
        u_next[0][j] = float(u[0][j]) - dt/dx*(float(F_right[0][j]) - float(F_left[0][j]))
    
    # Отбрасыване фиктивных узлов
    u1 = np.zeros((1,n-2), dtype=np.float)
    for i in range(n-2):
        u1[0][i] = u_next[0][i+1]
    return u1