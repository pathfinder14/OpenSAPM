# -*- coding: utf-8 -*-

def left_to_right_vec(v):
	"""
	u(i) получается из расщепления потоков в центре ячейки
	Input: u(i) = [u(i-2) u(i-1) u(i) u(i+1) u(i+2)];
	Output: h(i) = $u_{i+1/2}^{-}$
	"""

	"""
	Выбираются отрицательные потоки для вычисления левой границы ячейки
	$u_{i-1/2}^{+}$
	"""
	vm = np.roll(u, 1, axis = 0) #down
	vmm = np.roll(u, 1, axis = 0).roll(u, 1, axis = 0)
	vp = np.roll(u, -1, axis = 0) #up
	vpp = np.roll(u, -1, axis = 0).roll(u, -1, axis = 0)

	# Полиномы
	p0n = (2*vmm - 7*vm + 11*v)/6
	p1n = ( -vm  + 5*v  + 2*vp)/6
	p2n = (2*v   + 5*vp - vpp )/6

	# Индикаторы гладкости
	B0n = 13/12*(vmm-2*vm+v  )**2 + 1/4*(vmm-4*vm+3*v)**2 
	B1n = 13/12*(vm -2*v +vp )**2 + 1/4*(vm-vp)**2
	B2n = 13/12*(v  -2*vp+vpp)**2 + 1/4*(3*v-4*vp+vpp)**2;

	# Константы
	d0n = 1/10
	d1n = 6/10
	d2n = 3/10
	epsilon = 1e-6

	# Веса
	alpha0n = d0n/(epsilon + B0n)**2
	alpha1n = d1n/(epsilon + B1n)**2
	alpha2n = d2n/(epsilon + B2n)**2
	alphasum = alpha0n + alpha1n + alpha2n

	#Веса для каждого ENO шаблона
	w0n = alpha0n/alphasum
	w1n = alpha1n/alphasum
	w2n = alpha2n/alphasum

	#Граница ячейки текущего потока
	hn = w0n * p0n + w1n * p1n + w2n * p2n
	h = hn
	return h