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
        label.set_fontsize(40)
    yax= ax.yaxis 
    ylabels = yax.get_ticklabels()
    for label in ylabels:
        label.set_fontsize(40)
    #Устанавливаем границы отображения по x,f(x). 
    plt.ylim(-3/2*solution_max_value, 3/2*solution_max_value)
    plt.xlim(x[0],x[-1])
        
    #Устанавливаем легенду на графике, включаем отображение сетки.
    plt.title(legend + ' plot, '  + 't = ' + str(t_slice) + 's', fontsize = 50) 
    plt.xlabel('x', fontsize = 40)
    plt.ylabel(legend+'(x)',fontsize = 40)
    plt.grid(True)
    
    plt.plot(x, solution, "--",linewidth=5)
    plt.savefig("img/"+str(t_slice)+"s.png") # - если рисовать мувик, будет сохранять .png
    #plt.show() - если нужно отображать, не будет сохранять



#t_step = T_real_step / t_real_step
#t_filming_step - шаг, с которым мы хотим отрисовывать, секунды
#t_grid_step - шаг по сетке, секунды

def draw1DMovie(solution, t_filming_step, x_start, x_end, legend, t_grid_step):

    #Удаляем файлы из директории img\ перед рисование мультика.
    files = glob.glob('img/*')
    for f in files:
        os.remove(f)
        
    #Перевели шаг из "реального времени" в шаг по массиву решения.
    t_step = int(t_filming_step / t_grid_step)
    
    #Вызываем рисовалку срезов по времени в цикле.
    for i in range(0, len(solution), t_step):
        draw1DSlice(solution[i], i * t_grid_step, x_start, x_end, legend, np.max(solution))

    #Рисуем гифку из содержимого папки img\, сохраняем ее туда же.      
    images = []
    filenames = sorted(fn for fn in os.listdir(path='img/') if fn.endswith('.png'))
    for filename in filenames:
        tmp = imageio.imread('img/' + filename)
        images.append(tmp)
    imageio.mimsave('img/movie.gif', images, duration = 0.1)
    

def do_postprocess(solution, t_filming_step, x_start, x_end, legend, t_grid_step):
    draw1DMovie(solution, t_filming_step, x_start, x_end, legend, t_grid_step)