# -*- coding: utf-8 -*-

def riht_to_left_vec(u):
	"""
	u(i) получается из расщепления потоков в центре ячейки
	Input: u(i) = [u(i-2) u(i-1) u(i) u(i+1) u(i+2)];
	Output: h(i) = $u_{i-1/2}^{+}$
	"""

	"""
	Выбираются отрицательные потоки для вычисления левой границы ячейки
	$u_{i-1/2}^{+}$
	"""
	um = np.roll(u, 1, axis = 0) #down
	umm = np.roll(u, 1, axis = 0).roll(u, 1, axis = 0)
	up = np.roll(u, -1, axis = 0) #up
	upp = np.roll(u, -1, axis = 0).roll(u, -1, axis = 0)

	# Полиномы
	p0p = ( -umm + 5*um + 2*u  )/6
	p1p = ( 2*um + 5*u  - up   )/6
	p2p = (11*u  - 7*up + 2*upp)/6

	# Индикаторы гладкости
	B0p = 13/12*(umm-2*um+u  )**2 + 1/4*(umm-4*um+3*u)**2
	B1p = 13/12*(um -2*u +up )**2 + 1/4*(um-up)**2
	B2p = 13/12*(u  -2*up+upp)**2 + 1/4*(3*u -4*up+upp)**2

	# Константы
	d0p = 3/10
	d1p = 6/10
	d2p = 1/10
	epsilon = 1e-6

	# Веса
	alpha0p = d0p/(epsilon + B0p)**2
	alpha1p = d1p/(epsilon + B1p)**2
	alpha2p = d2p/(epsilon + B2p)**2
	alphasum = alpha0p + alpha1p + alpha2p

	#Веса для каждого ENO шаблона
	w0p = alpha0p/alphasum
	w1p = alpha1p/alphasum
	w2p = alpha2p/alphasum

	#Граница ячейки текущего потока
	hp = w0p * p0p + w1p * p1p + w2p * p2p
	h = hp
	return h


