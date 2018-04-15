#!/usr/bin/python
import numpy as np

def beam_warming(tau, h, grid, transfer_velocity, i):
    new_grid = np.zeros_like(grid)
    sigma = np.dot(transfer_velocity, tau / h)
    for m in range(2, grid.shape[0] - 1):
        new_grid[m][i+1] = grid[m][i] - np.dot(sigma ,(grid[m][i] - grid[m-1][i])) +\
         np.dot(sigma/2, np.dot((1 - sigma) , (grid[m][i] - 2 * grid[m-1][i] + grid[m-2][i])))
    return new_grid
