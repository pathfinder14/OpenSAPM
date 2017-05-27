import numpy as np
'''
du/dt + a du/dx = 0
WENO метод для уравнения переноса
a - параметр перед производной по x
dt - шаг по времени
dx - шаг по координате
u - начальное условие t = 0 (numpy array)
Возвращаемое значение: Следующий слой (numpy array)
'''
def WENOmethod(a, tau, h, u):
    # Количество весов: Порядок = 2k - 1
    k = 3       
    # Количество узлов    
    nx = len(u)
    # Количество пустых клеток
    gc = k - 1  
    # Добавление пустых клеток
    x = np.linspace(0, 2, nx)
    gcr = x[-1] + np.linspace(1, gc, gc) * h
    gcl = x[0] + np.linspace(-gc, -1, gc) * h
    xc = np.append(x, gcr)
    xc = np.append(gcl, xc)
    uc = np.append(u, u[-gc:])
    uc = np.append(u[0:gc], uc)

    gs = np.zeros([nx + 2 * gc, 1])
    flux = np.zeros(nx + 2 * gc)
  
    un = uc.copy() 
    for i in range(gc, nx - 1 + gc):  # i = 2
        xloc = xc[i - (k - 1):i + k]  # i + k - 1 - (i - (k - 1) - 1) = 2k -1 
        uloc = uc[i - (k - 1):i + k]
        f_left, f_right = WENO(xloc, uloc, k)
        # Положительный поток
        flux[i] = 0.5 * (a + np.fabs(a)) * f_left + 0.5 * (a - np.fabs(a)) * f_right

    for i in range(gc, nx - gc):
        if (a > 0):
            uc[i] = un[i] - tau / h * (flux[i] - flux[i - 1])
        else:
            uc[i] = un[i] - tau / h * (flux[i + 1] - flux[i])

    return  uc[1:-1]

'''
Функция вычисляет левые и правые границы клетки, используя ENO
xloc - 2k - 1 узел 
uloc - 2k - 1 значение в узле
k - количество весов
Возвращаемое значение: Кортеж из левого и правого значений
'''
def WENO(xloc, uloc, k):
    
    # Особый случай - не нужно выбирать шаблон
    if (k == 1):
        ul = uloc[0]
        ur = uloc[1]

    # Применение процедур WENO
    alphal = np.zeros(k, dtype = np.float)
    alphar = np.zeros(k, dtype = np.float)
    omegal = np.zeros(k, dtype = np.float)
    omegar = np.zeros(k, dtype = np.float)
    beta = np.zeros(k, dtype = np.float)
    d = np.zeros(k, dtype = np.float)
    vareps = 1e-6

    # Вычисление k значений xl и xr построенных на разных шаблонах
    ulr = np.zeros(k, dtype = np.float)
    urr = np.zeros(k, dtype = np.float)

    for r in range(0, k):
        cr = ENOweights(k, r)
        cl = ENOweights(k, r - 1)

        for i in range(0, k):
            urr[r] = urr[r] + cr[i] * uloc[k - r + i - 1] 
            ulr[r] = ulr[r] + cl[i] * uloc[k - r + i - 1] 

    # Вычисление WENO коэффициентов для разных порядков 2k - 1 (3 и 5 порядки)
    if (k == 2):
        # Оптимальные веса
        d[0] = 2 / 3.
        d[1] = 1 / 3.
        # Вычисление индикатора гладкости для каждого шаблона
        beta[0] = (uloc[2] - uloc[1]) ** 2
        beta[1] = (uloc[1] - uloc[0]) ** 2

    if(k == 3):
        # Оптимальные веса
        d[0] = 3 / 10. 
        d[1] = 3 / 5.
        d[2] = 1 / 10.
        # Вычисление индикатора гладкости для каждого шаблона
        beta[0] = 13/12.*(uloc[2]-2*uloc[3]+uloc[4])**2 + 1/4.*(3*uloc[2]-4*uloc[3]+uloc[4])**2
        beta[1] = 13/12.*(uloc[1]-2*uloc[2]+uloc[3])**2 + 1/4.*(uloc[1]-uloc[3])**2
        beta[2] = 13/12.*(uloc[0]-2*uloc[1]+uloc[2])**2 + 1/4.*(3*uloc[2]-4*uloc[1]+uloc[0])**2

    # Вычисление альфа параметров 
    for r in range(0,k):
        alphar[r] = d[r] / (vareps + beta[r]) ** 2
        alphal[r] = d[k - r - 1] / (vareps + beta[r]) ** 2

    # Вычисление весовых параметров WENO
    for r in range(0,k):
        omegal[r] = alphal[r] / alphal.sum()
        omegar[r] = alphar[r] / alphar.sum()

    # Вычисление значений на краях ячейки
    ul = 0 
    ur = 0 
    for r in range(0,k):
        ul = ul + omegal[r] * ulr[r]
        ur = ur + omegar[r] * urr[r]

    return (ul,ur)

'''
Функция вычисляет оптимальные веса C__k ^ r для WENO
v_[i+1/2] = \sum_[j=0]^[k-1] c_[rj] v_[i-r+j]
k - порядок
r - смещение
Возвращаемое значение: Массив весов c_rk (numpy array)
'''
def ENOweights(k,r):
    c = np.zeros(k)

    for j in range(0,k):
            de3 = 0.
            for m in range(j + 1, k + 1):
                # Вычисление знаменателя (denominator) 
                de2 = 0.
                for l in range(0, k + 1):
                    if l is not m:
                        de1 = 1.
                        for q in range(0, k + 1):
                            if (q is not m) and (q is not l):
                                de1 = de1 * (r - q + 1)


                        de2 = de2 + de1


                # Вычисление числителя 
                de1 = 1.
                for l in range(0, k + 1):
                    if (l is not m):
                        de1 = de1 * (m - l)

                de3 = de3 + de2 / de1

            c[j] = de3
    return c