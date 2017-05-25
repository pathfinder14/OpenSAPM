import matplotlib.pyplot as plt
import math as math
'''
Тест для функции решения уравнения переноса (TVD)
Вычисляется u спустя время t_end
'''
a0 = -0.5
left = 1.0 # пределы по оси x
right = 2.0
dx = 0.01
cfl = 0.09
dt = cfl*dx/abs(a0)
t_end = dt
t_end = 0.6 # Время (t_end / dt задает количество итераций)
t_end = 0.6
n = int((right - left) / dx)

aTest = 'const' # Выбор теста (вариант параметра a)
uTest = 'gauss'

a = np.zeros((1,n))
# Задание параметра a
if aTest == 'const': # постоянный параметр
    for i in range(int(n/2)):
        a[0][i] = 0.5
    for i in range(int(n/2), n):
        a[0][i] = 0.5
elif aTest == 'devided': # разрыв
    for i in range(int(n/2)):
        a[0][i] = 0.5
    for i in range(int(n/2), n):
        a[0][i] = 1
elif aTest == 'hat': # "шляпка"
    mu = 1.5
    for i in range(n):
        a[0][i] =  0.5 + 0.5/(1 + 100*(left + i*dx - mu)*(left + i*dx - mu))

# Задание тестовой функции
u_0 = np.zeros((1,n))
u0 = np.zeros((1,n))
if uTest == 'step': # струпенька
    for i in range(int(n/3)):
        u_0[0][i] = 1
    for i in range(int(n/3), 2 * int(n/3)):
        u_0[0][i] = 2
    for i in range(2 * int(n/3), n):
        u_0[0][i] = 1
elif uTest == 'gauss': # функция Гаусса
    sigma = 0.1
    pi = 3.14
    mu = 1.5
    for i in range(n):
        u_0[0][i] = 1.0 + 0.1 * 1.0 / (sigma * math.sqrt(2*pi)) * math.exp(-((left + i*dx - mu)*(left + i*dx - mu)) / (2.0 * sigma * sigma))
elif uTest == 'peack': # пик
    sigma = 0.1
    pi = 3.14
    mu = 1.5
    for i in range(n):
        # u_0[0][i] =  1/(1 + 1000*(left + i*dx - mu)*(left + i*dx - mu))
        if (left + i*dx - mu) == 0.0:
            u_0[0][i] = 1.0
        else:
            u_0[0][i] = math.sin(100*(left + i*dx - mu)) / (100*(left + i*dx - mu))
    
    
# Создание копии начальной функции, которая будет меняться в процессе вычислений
for i in range(n):
    u0[0][i] = u_0[0][i]
    
u = np.zeros((1,n-2), dtype=np.float)
x = np.zeros((1,n-2), dtype=np.float)

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
# i = dx
i= left
for j in range(n-2):
    x[0][j] = i
    j = j + 1
    i = i + dx   
x1 = np.zeros((1,n), dtype=np.float)
j = 0
i= left
for j in range(n):
    x1[0][j] = i
    j = j + 1
    i = i + dx

    
# Построение графика
plt.subplot(211)
plt.plot(x[0], u[0], marker = '*', label = 'U_1') #'.')
plt.plot(x1[0], u_0[0], marker = '.', label = 'U_0') # '.')
# plt.legend()
plt.legend(bbox_to_anchor=(0.2, 1), loc=1, borderaxespad=0.25)
plt.ylabel('U')
plt.xlabel('x')
plt.subplot(212)
plt.plot(x1[0], a[0], marker = '.', label = 'a') # '.')
plt.ylabel('a')
plt.xlabel('x')
plt.legend(bbox_to_anchor=(0.16, 1), loc=1, borderaxespad=0.25)
#plt.savefig('plots/a_' + aTest + '_U0_' + uTest + '.png')
plt.show()