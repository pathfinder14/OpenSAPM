import numpy as np
import bicompact as bt

x1 = np.zeros(10)
h=1
tau=1
x1[0] = 1;
x0 = np.arange(1,11,1)
a = np.ones(10)
for i in range (5):
	a[i]=2;
print(a)

for i in range (x0.size-2):
	tmpx1 = np.copy(x1[i:i+3])
	tmp = bt.bicompact_method(a[i+1],tau,h,x0[i:i+3],tmpx1)
	print(x1)
	print(x0)
	x1[i+1] = tmp[0]

print(x1[1:x0.size-1])
print(x0[1:x0.size-1])