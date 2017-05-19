#!/usr/bin/python
import numpy as np

def beam_warming(transfer_velocity, tau, h, grid):
    #grid = grid.tolist()
    ext_grid = grid
    sigma = transfer_velocity * tau / h
    for m in range(2, len(ext_grid) - 1):
        grid[m] = grid[m] - np.dot(sigma ,(grid[m] - grid[m-1])) + np.dot(sigma/2, np.dot((1 - sigma) , (grid[m] - 2 * grid[m-1] + grid[m-2])))
        #ext_grid[cols] = ext_grid[cols] - sigma * (ext_grid[cols] - ext_grid[cols-1]) + sigma/2 * (1 - sigma) * (ext_grid[cols] - 2 * ext_grid[cols-1] + ext_grid[cols-2])
    ext_grid = np.array(ext_grid)
    return grid[1:-1]
