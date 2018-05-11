#!/usr/bin/python
import numpy as np

def beam_warming(tau, h, grid, transfer_velocity):
    new_grid = [grid[i] for i in range(len(grid))]
    sigma = np.dot(transfer_velocity, tau / h)
    for m in range(2, grid.shape[0] - 1):
        new_grid[m] = grid[m] - np.dot(sigma ,(grid[m] - grid[m-1])) +\
         np.dot(sigma/2, np.dot((1 - sigma) , (grid[m] - 2 * grid[m-1] + grid[m-2])))
    return new_grid[1:grid.shape[0] - 1]
