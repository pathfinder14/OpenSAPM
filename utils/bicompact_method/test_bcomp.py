import numpy as np
from bicompact import bicompact_method

#a = const, signal is a "step"

a1=1
tau1=1
h1=1
x1_1 = np.arange(0,10,h1)
for i in range(x1_1.size):
	x1_1[i] = 0
x0_1 = np.array([1, 1, 1, 3, 3, 3, 3, 1, 1, 1])

x1_1 = bicompact_method(a1,tau1,h1,x0_1)
print(x0_1)
print(x1_1)


#a = const, signal is a "peak"

a2=1
tau2=1
h2=1
x1_2 = np.arange(0,10,h2)
for i in range(x1_2.size):
	x1_2[i] = 0
x0_2 = np.array([0, 1, 1, 3, 10, 10, 3, 1, 1, 0])

x1_2 = bicompact_method(a2,tau2,h2,x0_2)
print(x0_2)
print(x1_2)


#a = const, signal is a gaussian

a3=1
tau3=1
h3=1
x1_3 = np.arange(0,8,h3)
for i in range(x1_3.size):
	x1_3[i] = 0
x0_3 = np.array([5, 8, 9, 10, 10, 9, 8, 5])

x1_3 = bicompact_method(a3,tau3,h3,x0_3)
print(x0_3)
print(x1_3)


"""
#a - "tear", signal is a peak

a4_1=0
a4_2=2
tau4=1
h4=1
x1_4_1 = np.arange(0,5,h4)
x1_4_2 = np.arange(0,5,h4)
for i in range(x1_4_1.size):
	x1_4_1[i] = 0
	x1_4_2[i] = 0
x0_4_1 = np.array([0, 1, 1, 3, 10])
x0_4_2 = np.array([10, 3, 1, 1, 0])

x1_4_1 = bicompact_method(a4_1,tau4,h4,x0_4_1,x1_4_1)
x1_4_2 = bicompact_method(a4_2,tau4,h4,x0_4_2,x1_4_2)
#x1_4 = x1_4_1 + x1_4_2
#x0_4 = x0_4_1 + x0_4_2
np.vstack((x0_4_1,x0_4_2))
print(np.hstack((x0_4_1,x0_4_2)))
print(np.hstack((x1_4_1,x1_4_2)))
"""

#a - "tear", signal is a peak

x1 = np.zeros(10)
h=1
tau=1
x1[0] = 1;
x0 = np.array([0, 1, 1, 3, 10, 10, 3, 1, 1, 0])
a = np.array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
print(a)

for i in range (x0.size-2):
	tmpx1 = np.copy(x1[i:i+3])
	tmp = bicompact_method(a[i+1],tau,h,x0[i:i+3],tmpx1)
	#print(x1)
	#print(x0)
	x1[i+1] = tmp[0]

print(x0[1:x0.size-1])
print(x1[1:x0.size-1])

#a - "hat", signal is a peak

x1 = np.zeros(10)
h=1
tau=1
x1[0] = 1;
x0 = np.array([0, 1, 1, 3, 10, 10, 3, 1, 1, 0])
a = np.array([6, 6, 7, 8, 10, 10, 8, 7, 6, 6])
print(a)

for i in range (x0.size-2):
	tmpx1 = np.copy(x1[i:i+3])
	tmp = bicompact_method(a[i+1],tau,h,x0[i:i+3],tmpx1)
	#print(x1)
	#print(x0)
	x1[i+1] = tmp[0]

print(x0[1:x0.size-1])
print(x1[1:x0.size-1])

import matplotlib.pyplot as plt
import numpy as np
import sys
import imageio
import os
import shutil
import glob

def draw1DSlice(solution, t_slice, x_start, x_end, legend, solution_max_value):
    M = len(solution)
    x_step = (x_end - x_start) / M
    x =  np.arange(x_start,x_end,x_step) 
    #Устанавливаем размеры рисунка.
    ax = plt.figure(figsize = (30,30)).add_subplot(111)
    #Устанавливаем подписи значений по осям.
    xax = ax.xaxis 
    xlabels = xax.get_ticklabels()
    for label in xlabels:
        label.set_fontsize(12)
    yax= ax.yaxis 
    ylabels = yax.get_ticklabels()
    for label in ylabels:
        label.set_fontsize(12)
    #Устанавливаем границы отображения по x,f(x). 
    plt.ylim(-3/2 * solution_max_value, 3/2 * solution_max_value)
    plt.xlim(x[0],x[-1])
        
    #Устанавливаем легенду на графике, включаем отображение сетки.
    plt.title(legend + ' plot, '  + 't = ' + str(t_slice) + 's', fontsize = 14) 
    plt.xlabel('x', fontsize = 12)
    plt.ylabel(legend+'(x)', fontsize = 12)
    plt.grid(True)
    
    plt.plot(x, solution, "--",linewidth=5)
    #plt.savefig('img' + os.sep + str(t_slice)+ 's.png' ) # - если рисовать мувик, будет сохранять .png
    plt.show() # - если нужно отображать, не будет сохранять



#t_step = T_real_step / t_real_step
#t_filming_step - шаг, с которым мы хотим отрисовывать, секунды
#t_grid_step - шаг по сетке, секунды

def draw1DMovie(solution, t_filming_step, x_start, x_end, legend, t_grid_step):

    #Удаляем файлы из директории img\ перед рисование мультика.
    files = glob.glob('img' + os.sep + '*')
    for f in files:
        os.remove(f)
        
    #Перевели шаг из "реального времени" в шаг по массиву решения.
    t_step = int(t_filming_step / t_grid_step)
    
    #Вызываем рисовалку срезов по времени в цикле.
    for i in range(0, len(solution), t_step):
        draw1DSlice(solution[i], i * t_grid_step, x_start, x_end, legend, np.max(solution))

    #Рисуем гифку из содержимого папки img\, сохраняем ее туда же.      
    images = []
    filenames = sorted(fn for fn in os.listdir(path='img' + os.sep) if fn.endswith('.png'))
    for filename in filenames:
        tmp = imageio.imread('img' + os.sep + filename)
        images.append(tmp)
    imageio.mimsave('img' + os.sep + 'movie.gif', images, duration = 0.1)


def do_postprocess(solution, t_filming_step, x_start, x_end, legend, t_grid_step):
    draw1DMovie(solution, t_filming_step, x_start, x_end, legend, t_grid_step)

draw1DSlice (x1_1, 1, 0, 10, 'a = const, signal is a "step"', max(x1_1))
draw1DSlice (x1_2, 1, 0, 10, 'a = const, signal is a "step"', max(x1_2))
draw1DSlice (x1_3, 1, 0, 10, 'a = const, signal is a "step"', max(x1_3))
#draw1DSlice (x1_1, 1, 0, 10, 'a = const, signal is a "step"', max(x1_1))
