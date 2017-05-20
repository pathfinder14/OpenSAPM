import matplotlib.pyplot as plt
'''
Тест для функции решения уравнения переноса (TVD)
Вычисляется u спустя время t_end
'''
a = -0.5
left = 1.0 # пределы по оси x
right = 2.0
dx = 0.01
cfl = 0.09
dt = cfl*dx/abs(a)
t_end = 0.6 # Время (t_end / dt задает количество итераций)
n = int((right - left) / dx)


# Задание тестовой функции
u_0 = np.zeros((1,n))
for i in range(int(n/2)):
    u_0[0][i] = 1
for i in range(int(n/2), n):
    u_0[0][i] = 2

u = np.zeros((1,n-2), dtype=np.float)
x = np.zeros((1,n-2), dtype=np.float)
u0 = u_0 # u_0 не меняется в процессе вычислений, u0 меняется

# Вычисление u
for k in range(int(t_end / dt)):
    u = TVDMethod(a, dt, dx, u0, 'VanLeer')
    for i in range(n-2):
        u0[0][i+1] = u[0][i]
    # Граничные условия
    u0[0][0] = u0[0][1]
    u0[0][n-1] = u0[0][n-2]

# Инициализация вектора x для построения графика
j = 0
i = dx
for j in range(n-2):
    x[0][j] = i
    j = j + 1
    i = i + dx
    
# Построение графика
plt.plot(x[0], u[0], '.')
plt.ylabel('U')
plt.xlabel('x')
plt.show()