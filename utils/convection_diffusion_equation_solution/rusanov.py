import numpy as np
''' This method solve transfer equation with Rusanov method '''
def rusanov(transfer_velocity, tau, h, grid):
    sigma = transfer_velocity * tau / h
    omega = (3 + 4*(sigma**2) - (sigma**4))/2
    miu = tau / h
    new_grid = np.zeros_like(grid)
    grid = np.insert(grid, 0, -grid[0])
    grid = np.insert(grid, -1, -grid[-1])
    for m in range(2, len(new_grid) - 1):
        new_grid[m] = np.dot((1 - omega/4 - (miu**2)/4) , grid[m]) + np.dot((omega/6 - 2*miu/3) , grid[m+1]) + np.dot((-omega/24 + miu/12 + (miu**2)/8 - (miu**3)/12) , grid[m+2]) + np.dot((omega/6 + 2*miu/3) , grid[m-1]) + np.dot((-omega/24 - miu/12 + (miu**2)/8 + (miu**3)/12) , grid[m-2])
    return new_grid
