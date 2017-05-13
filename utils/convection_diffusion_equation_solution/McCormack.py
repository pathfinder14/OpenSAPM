import numpy as np

def McCormack(t_nods_quantity, x_nods_quantity, grid, transfer_velocity, time_step, x_step):
    ext_grid = np.insert(grid, 0, -grid[0])

    sigma = transfer_velocity * time_step / x_step

    for m in range(2, x_nods_quantity - 1):
        ext_grid[m] = ext_grid[m] - np.dot(sigma, (ext_grid[m] - ext_grid[m-1])) + \
                  np.dot(sigma**2, (ext_grid[m] - ext_grid[m-2]))

    ext_grid = np.delete(ext_grid, 0)
    return ext_grid