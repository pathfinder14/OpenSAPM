import numpy as np

def McCormack(grid, x_step, transfer_velocity, time_step):
    if (transfer_velocity > 0):
        new_grid = grid
        for m in range(2, grid.shape[0]):
            sigma = transfer_velocity * time_step / x_step
            new_grid[m] = grid[m] - np.dot(sigma, (grid[m] - grid[m-1])) + \
                  np.dot(sigma**2, (grid[m] - grid[m-2]))
    else:
        new_grid = grid
        for m in range(0, grid.shape[0] - 3):
            sigma = transfer_velocity * time_step / x_step
            new_grid[m] = grid[m] - np.dot(sigma, (grid[m+1] - grid[m])) + \
                          np.dot(sigma ** 2, (grid[m+2] - grid[m]))
    #new_grid = np.delete(grid, [0, 1])
        # returning array without additional nod and border condition
    return new_grid[2:grid.shape[0] - 2]
