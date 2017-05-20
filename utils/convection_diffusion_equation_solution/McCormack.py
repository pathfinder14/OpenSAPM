import numpy as np

def McCormack(x_nods_quantity, grid, transfer_velocity, time_step, x_step):
    sigma = transfer_velocity * time_step / x_step
    if (transfer_velocity > 0):
        new_grid = grid
        for m in range(2, x_nods_quantity - 1):
            new_grid[m] = grid[m] - np.dot(sigma, (grid[m] - grid[m-1])) + \
                  np.dot(sigma**2, (grid[m] - grid[m-2]))

    else:
        new_grid = grid
        for m in range(2, x_nods_quantity - 1):
            new_grid[m] = grid[m] - np.dot(sigma, (grid[m+1] - grid[m])) + \
                          np.dot(sigma ** 2, (grid[m+2] - grid[m]))

    new_grid = np.delete(grid, [0, 1, -1, -2])

    return new_grid
