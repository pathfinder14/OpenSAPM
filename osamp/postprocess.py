import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import imageio
import os
import shutil
import glob
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d

def draw1DSlice(solution, t_slice, x_start, x_end, legend, solution_max_value):
    print ('in draw 1d slice')
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
    plt.ylim(-3/2 * solution_max_value, 3/2 * solution_max_value)
    plt.xlim(x[0],x[-1])
        
    #Устанавливаем легенду на графике, включаем отображение сетки.
    plt.title(legend + ' plot, '  + 't = ' + str(t_slice) + 's', fontsize = 50) 
    plt.xlabel('x', fontsize = 40)
    plt.ylabel(legend+'(x)', fontsize = 40)
    plt.grid(True)
    
    plt.plot(x, solution, "--",linewidth=5)
    plt.savefig('img' + os.sep + str(t_slice) + 's.png' ) # - если рисовать мувик, будет сохранять .png
    plt.clf()
    #plt.show() - если нужно отображать, не будет сохранять



#t_step = T_real_step / t_real_step
#t_filming_step - шаг, с которым мы хотим отрисовывать, секунды
#t_grid_step - шаг по сетке, секунды

def draw1DMovie(solution, t_filming_step, x_start, x_end, legend, t_grid_step):

    #Удаляем файлы из директории img\ перед рисование мультика.
    files = glob.glob('img' + os.sep + '*')
    for f in files:
        os.remove(f)

    #Вызываем рисовалку срезов по времени в цикле.
    for i in range(0, solution.shape[1], t_filming_step):
        draw1DSlice(solution[:,i, :], i * t_grid_step, x_start, x_end, legend, np.max(solution[:,i, :]))

    #Рисуем гифку из содержимого папки img\, сохраняем ее туда же.      
    images = []
    print("Making gif")
    filenames = [str(i * t_grid_step) + 's.png' for i in range(solution.shape[1])]
    for filename in filenames:
        images.append(imageio.imread('img' + os.sep + filename))
    imageio.mimsave('img' + os.sep + 'movie.gif', images, duration = 0.1)
    


def draw2DSlice(solution, t_slice, x_start, x_end, y_start, y_end, legend, solution_min_value, solution_max_value,
                time_marker_length):
    print('in draw 2d slice')
    # npArray = np.array(solution)
    # npArrayTransposed = npArray.transpose()
    # solution = npArrayTransposed
    
    M = len(solution)
    x_step = (x_end - x_start) / M
    x = np.arange(x_start,x_end,x_step)
    
    M = len(solution[0])
    y_step = (y_end - y_start) / M
    y =  np.arange(y_start,y_end,y_step)
    
    #Устанавливаем размеры рисунка.
    fig = plt.figure(figsize = (15,10))
    ax = fig.add_subplot(111)
   
    x_axis_step = (x_end - x_start)/8
    xlabel = np.arange(x_start, x_end, x_axis_step) # Сделаем подписи произвольных долгот     
    ax.set_xticklabels(xlabel)
    ax.set_xlabel('x', fontsize = 40)
    y_axis_step = (y_end - y_start)/8
    ylabel = np.arange(y_start, y_end, y_axis_step) # Сделаем подписи произвольных долгот     
    ax.set_yticklabels(ylabel)
    ax.set_ylabel('y', fontsize = 40)
    
    ax.set_title(legend + ' colorbar, '  + 't = ' + str(t_slice) + 's', fontsize = 50)
    ax.grid(True)
    
    # cpool = ['blue','cyan','green','yellow','pink']
    cpool = ['#f7f5f2','#e5dfd3','#ccbea1','#ad9b74','#8e7a4e', '#705b2f', '#4f3d17', '#352709', '#070500']
    cmap = mpl.colors.ListedColormap(cpool) # Задаём дискретную шкалу цветов из списка cpool
    cmap.set_over('red') # задаём цвет для значений, выходящих за рамки границы levels[-1] (сверху шкалы)
    cmap.set_under('grey') # задаём цвет для значений, выходящих за рамки границы levels[0] (снизу шкалы)
    
    # Задаём список границ изолиний. Причём значения попадают в интервал z1 < z <= z2
    levels = np.linspace(solution_min_value, solution_max_value, len(cpool)+1)
    
    norm = mpl.colors.Normalize(vmin=solution_min_value, vmax=solution_max_value) # Ставим границы для цветовых отрезков шкалы

    #Боковая шкала
    # Задаём границы для изолиний levels.
    # Также для метода contour и contourf треугольные индикаторы, которые отражают превышение заданных 
    # границ levels указываются в самом методе contour. 
    
    #Привязываем границы по значениям зон нашей боковой шкалы к цветам.
    cs = ax.contourf(solution, levels, cmap=cmap, norm=norm, extend='both')
    cbar = fig.colorbar(cs, ax=ax, spacing='proportional',   # сделаем цветовые сегменты шкалы пропоциональными границам levels
                    extendfrac='auto',   # изменим длину треугольных индикаторов
                    orientation='vertical') # можно изменить положение шкалы на горизонтальное (horizontal)
    
    #Создаем папку, если ее не существует
    if not os.path.exists('img'):
        os.makedirs('img')
    
    plt.savefig('img' + os.sep + str(t_slice) + 's.png') # - если рисовать мувик, будет сохранять .png
    plt.clf()
    #plt.show() - если нужно отображать, не будет сохранять



def draw2DMovie(solution, t_filming_step, x_start, x_end, y_start, y_end, legend, solution_min_value, solution_max_value, t_grid_step):
    #Переменная, контролирующая длину имен файла(Нужна для округления)
    time_marker_length = len(str(t_filming_step))

    #!!!Здесь указываем, вдоль какого x и вдоль какого y мы хотим получить срезы
    x_slice_value = 3
    y_slice_value = -1
    #Ищем значения на сетке, которые наиболее близки к заданным значениям срезов:
    #1: Взяли один срез по времени
    # npArray = np.array(solution[0])

    #2: Ищем индекс по иксу
    M = solution.shape[0]
    x_step = (x_end - x_start) / M
    x =  np.arange(x_start,x_end,x_step)

    #3: Ищем индекс по игреку
    M = solution.shape[1]
    y_step = (y_start - y_end) / M
    y =  np.arange(y_start,y_end,y_step)
    #Создаем папку, если ее не существует
    if not os.path.exists('img'):
        os.makedirs('img')
    
    #Удаляем файлы из директории img\ перед рисование мультика.
    files = glob.glob('img' + os.sep + '*')
    for f in files:
        os.remove(f)

    #Если откомментили это, значит, вы готовы к тому, что малые значения сеточной функции отображаться не будут. 
    #Закомментите инициализацию этих же переменных в цикле.
    #Нормировка по цвету будет единой для всего фильма.
    # absolute_solution_minimum = solution_min_value
    # absolute_solution_maximum = solution_max_value

    #Вызываем рисовалку срезов по времени в цикле.
    # Если откомментили это, значит вы готовы к мигающему фону. Закомментите инициализацию этих же переменных прямо перед циклом
    # Нормировка по цвету будет выполняться отдельно для каждого кадра
    absolute_solution_minimum = np.min(solution[:, :, :])
    absolute_solution_maximum = np.max(solution[:, :, :])
    for i in range(0, solution.shape[2], t_filming_step):
        draw2DSlice(solution[:,:,i], i * t_grid_step,
                    x_start, x_end, y_start, y_end, legend,
                    absolute_solution_minimum, absolute_solution_maximum,
                    time_marker_length)

    #Рисуем гифку из содержимого папки img\, сохраняем ее туда же.      
    images = []
    filenames = [str(i * t_grid_step) + 's.png' for i in range(solution.shape[2])]
    print("Making gif")
    for filename in filenames:
        tmp = imageio.imread('img' + os.sep + filename)
        images.append(tmp)
    imageio.mimsave('img' + os.sep + legend + ' movie.gif', images, duration = 0.2)


def draw3DSlice(solution, t_slice, x_start, x_end, y_start, y_end, legend, solution_min_value, solution_max_value,
                time_marker_length):
    print('in draw 3d slice')

    M = len(solution)
    x_step = (x_end - x_start) / M
    x = np.arange(x_start, x_end, x_step)

    M = len(solution[0])
    y_step = (y_end - y_start) / M
    y = np.arange(y_start, y_end, y_step)

    # Устанавливаем размеры рисунка.
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')

    x_axis_step = (x_end - x_start) / 8
    xlabel = np.arange(x_start, x_end, x_axis_step)  # Сделаем подписи произвольных долгот
    ax.set_xticklabels(xlabel)
    ax.set_xlabel('x', fontsize=40)
    y_axis_step = (y_end - y_start) / 8
    ylabel = np.arange(y_start, y_end, y_axis_step)  # Сделаем подписи произвольных долгот
    ax.set_yticklabels(ylabel)
    ax.set_ylabel('y', fontsize=40)

    ax.set_title(legend + ' colorbar, ' + 't = ' + str(t_slice) + 's', fontsize=50)
    ax.grid(True)

    xgrid, ygrid = np.meshgrid(x, y)
    ax.plot_wireframe(xgrid, ygrid, solution[:, :])

    # Создаем папку, если ее не существует
    if not os.path.exists('img'):
        os.makedirs('img')

    plt.savefig('img' + os.sep  + str(t_slice) + 's.png')  # - если рисовать мувик, будет сохранять .png
    plt.clf()
    # plt.show() - если нужно отображать,


def draw3DMovie(solution, t_filming_step, x_start, x_end, y_start, y_end, legend, solution_min_value,
                solution_max_value, t_grid_step):
    # Переменная, контролирующая длину имен файла(Нужна для округления)
    time_marker_length = len(str(t_filming_step))

    M = solution.shape[0]
    x_step = (x_end - x_start) / M
    x = np.arange(x_start, x_end, x_step)

    # 3: Ищем индекс по игреку
    M = solution.shape[1]
    y_step = (y_start - y_end) / M
    y = np.arange(y_start, y_end, y_step)
    # Создаем папку, если ее не существует
    if not os.path.exists('img'):
        os.makedirs('img')

    # Удаляем файлы из директории img\ перед рисование мультика.
    files = glob.glob('img' + os.sep + '*')
    for f in files:
        os.remove(f)

    absolute_solution_minimum = np.min(solution[:, :, :])
    absolute_solution_maximum = np.max(solution[:, :, :])
    for i in range(0, solution.shape[2], t_filming_step):
        draw3DSlice(solution[:, :, i], i * t_grid_step,
                    x_start, x_end, y_start, y_end, legend,
                    absolute_solution_minimum, absolute_solution_maximum,
                    time_marker_length)

    # Рисуем гифку из содержимого папки img\, сохраняем ее туда же.
    images = []
    print("Making gif")
    filenames = [str(i * t_grid_step) + 's.png' for i in range(solution.shape[2])]
    for filename in filenames:
        tmp = imageio.imread('img' + os.sep + filename)
        images.append(tmp)
    imageio.mimsave('img' + os.sep + legend + ' movie.gif', images, duration=0.2)



def do_2_postprocess(solution, t_filming_step, x_start, x_end, y_start, y_end, legend, solution_min_value, solution_max_value, t_grid_step):
    draw2DMovie(solution, t_filming_step, x_start, x_end, y_start, y_end, legend, solution_min_value, solution_max_value, t_grid_step)

def do_postprocess(solution, t_filming_step, x_start, x_end, legend, t_grid_step):
    draw1DMovie(solution, t_filming_step, x_start, x_end, legend, t_grid_step)


def do_3_postprocess(solution, t_filming_step, x_start, x_end, y_start, y_end, legend, solution_min_value, solution_max_value, t_grid_step):
    draw3DMovie(solution, t_filming_step, x_start, x_end, y_start, y_end, legend, solution_min_value, solution_max_value, t_grid_step)