#!/usr/bin/python
import numpy as np

def rusanov(tau, h, grid, transfer_velocity):
    new_grid = np.zeros_like(grid)
    for m in range(2, len(grid) - 2):
        sigma = transfer_velocity[m] * tau / h
        omega = (3 + 4 * (sigma ** 2) - (sigma ** 4)) / 2
        miu = tau / h
        new_grid[m] = np.dot((1 - omega/4 -(miu**2)/4),grid[m]) + np.dot((omega/6 - 2*miu/3 + (miu**3)/6),grid[m+1]) + np.dot((-omega/24 + miu/12 + (miu**2)/8 - (miu**3)/12),grid[m+2]) +\
            np.dot((omega/6 + 2*miu/3 - (miu**3)/6),grid[m-1]) + np.dot((-omega/24 - miu/12 + (miu**2)/8 + (miu**3)/12),grid[m-2])
    return new_grid
