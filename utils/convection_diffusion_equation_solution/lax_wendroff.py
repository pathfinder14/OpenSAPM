import numpy as np
''' This method solve transfer equation with Lax_wendroff method '''
def lax_wendroff(x_nods_quantity, grid, transfer_velocity, tau, h):
    new_grid = np.zeros_like(grid)
    for m in range(1, x_nods_quantity -1):
        sigma = transfer_velocity[m] * tau / h
        new_grid[m] = grid[m] - np.dot(sigma/2, (grid[m+1] - grid[m-1])) + np.dot((sigma**2)/2, (grid[m+1] - 2 * grid[m] + grid[m-1]))
    return new_grid
