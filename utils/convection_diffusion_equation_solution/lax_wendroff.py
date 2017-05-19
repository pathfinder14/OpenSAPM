import numpy as np
''' This method solve transfer equation with Lax_wendroff method '''
def Lax_wendroff(x_nods_quantity, grid, transfer_velocity, tau, h):
    sigma = transfer_velocity * tau / h
    for m in range(1, x_nods_quantity):
        grid[m] = grid[m] - np.dot(sigma/2, (grid[m+1] - grid[m-1])) + np.dot((sigma**2)/2, (grid[m+1] - 2 * grid[m] + grid[m-1]))
    return grid
