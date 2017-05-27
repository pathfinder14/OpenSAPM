import matplotlib.pyplot as plt
import math as math
from bicompact import bicompact_method
import numpy as np
'''
Тест для функции решения уравнения переноса (TVD)
'''


aTestList = ['const','tear', 'hat']
uTestList = ['step', 'gauss', 'peak']

for aIndex in range(len(aTestList)):
        for uIndex in range(len(uTestList)):
            aTest = aTestList[aIndex] # параметр a
            uTest = uTestList[uIndex] # начальное условие            
            
            a0 = -0.5
            left = 1.0 # пределы по оси x
            right = 5.0
            dx = 0.01
            cfl = 0.09
            dt = cfl*dx/abs(a0)
            t_end = 0.6 # Время (t_end / dt задает количество итераций)
            n = int((right - left) / dx)
            a = np.zeros(n)
            # Задание параметра a
            if aTest == 'const': # постоянный параметр
                for i in range(int(n/2)):
                    a[i] = 0.5
                for i in range(int(n/2), n):
                    a[i] = 0.5
            elif aTest == 'tear': # разрыв
                for i in range(int(n/2)):
                    a[i] = 0.5
                for i in range(int(n/2), n):
                    a[i] = 1
            elif aTest == 'hat': # "шляпка"
                mu = (right + left) / 2.0
                for i in range(n):
                    a[i] =  0.5 + 0.5/(1 + 100*(left + i*dx - mu)*(left + i*dx - mu))

            # Задание тестовой функции
            u_0 = np.zeros(n)
            u0 = np.zeros(n)
            if uTest == 'step': # ступенька
                for i in range(int(n/50)):
                    u_0[i] = 1
                for i in range(int(n/50), int(n/3)):
                    u_0[i] = 2
                for i in range(int(n/3), n):
                    u_0[i] = 1
            elif uTest == 'gauss': # функция Гаусса
                sigma = 0.02
                pi = 3.14
                # mu = 1.5
                mu = left + (right - left) / 2.5
                for i in range(n):
                    u_0[i] = 1.0 + 0.05 * 1.0 / (sigma * math.sqrt(2*pi)) * math.exp(-((left + i*dx - mu)*(left + i*dx - mu)) / (2.0 * sigma * sigma))
            elif uTest == 'peak': # пик
                sigma = 0.1
                pi = 3.14
                # mu = 1.5
                mu = left + (right - left) / 2.5
                delta = (mu - left) / 2.0
                length = right - left
                for i in range(int(delta/length * n), int(3 * delta/length * n)): # пик на финитном носителе
                    if (left + i*dx - mu) == 0.0:
                        u_0[i] = 1.0
                    else:
                        u_0[i] = math.sin(100*(left + i*dx - mu)) / (100*(left + i*dx - mu))
                
            for i in range(n):
                u0[i] = u_0[i]
                
            u = np.zeros(n, dtype=np.float)
            x = np.zeros(n, dtype=np.float)

            # Вычисление u
            ut1 = np.zeros(n, dtype=np.float)
            ut2 = np.zeros(n, dtype=np.float)
            ut3 = np.zeros(n, dtype=np.float)
            
            #отработка метода на векторе параметров
            for k in range(int(t_end / dt)):
                
                for j in range (u0.size-5):
                    tmpx1 = np.copy(u[j:j+3])
                    tmp = bicompact_method(a[j+1],dt,dx,u0[j:j+3],tmpx1)
                    u[j+1] = tmp[0] 
                            
                for i in range(n-2):
                    u0[i+1] = u[i]
                # Граничные условия
                u0[0] = u0[1]
                u0[n-1] = u0[n-2]
                if k == int(t_end / dt * 0.25):
                    for i in range(n):
                        ut1[i] = u0[i]
                elif k == int(t_end / dt * 0.5):
                    for i in range(n):
                        ut2[i] = u0[i]
                elif k == int(t_end / dt * 0.75):
                    for i in range(n):
                        ut3[i] = u0[i]
                
            # Инициализация вектора x для построения графика
            j = 0
            i= left
            for j in range(n-2):
                x[j] = i
                j = j + 1
                i = i + dx   
            x1 = np.zeros(n, dtype=np.float) # длины n для построения графиков входных данных
            x2 = np.ones(n, dtype=np.float) # для построения аналитического решения
            j = 0
            i= left
            for j in range(n):
                x1[j] = i
                j = j + 1
                i = i + dx            
            j = 0
            i = left + a[0] * t_end
            while (j < n) and (i < right):
                x2[j] = i
                j = j + 1
                i = i + dx
            
                
            # Построение графика
            plt.subplot(311)
            plt.plot(x, u, label = 'x_1 (t = ' + str(t_end) + ')')
           
            if (aTest == 'const'):
                plt.plot(x2, u_0, label = 'x (t = ' + str(t_end) + ')')
                plt.axis([1.0,5.4,1.0,2.2])
                if uTest == 'peak':
                    plt.axis([1.0,5.4,-0.4,1.2])
                
            else:
                plt.plot(x1, u_0, label = 'x_0 (t = 0)')
            if uTest != 'peak':
                plt.axis([1.0,5.4,1,2.2])
            plt.legend(bbox_to_anchor=(0.35, 1), loc=1, borderaxespad=0.25)
            plt.ylabel('x')
            plt.xlabel('h')
            
            plt.subplot(312)
            plt.plot(x1, u_0) 
            plt.plot(x1, ut1, label = 'x (t = ' + str(t_end * 0.25) + ')')
            plt.plot(x1, ut2, label = 'x(t = ' + str(t_end * 0.5) + ')')  
            plt.plot(x1, ut3, label = 'x (t = ' + str(t_end * 0.75) + ')')  
            plt.plot(x, u,label = 'x (t = ' + str(t_end) + ')')
            if uTest != 'peak':
                plt.axis([1.0,5.4,1,2.2])
            plt.legend(bbox_to_anchor=(0.33, 1), loc=1, borderaxespad=0.25)
            
            plt.subplot(313)
            plt.plot(x1, a, marker = '.', label = 'a')
            plt.ylabel('a')
            plt.xlabel('h')
            plt.legend(bbox_to_anchor=(0.16, 1), loc=1, borderaxespad=0.25)
            plt.savefig('plots/' + 'a_' + aTest + '_x0_' + uTest + '.png')
            #plt.show()
            plt.close()
            
