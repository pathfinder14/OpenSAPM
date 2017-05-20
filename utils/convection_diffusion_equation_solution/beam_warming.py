#!/usr/bin/python
import numpy as np

def beam_warming(transfer_velocity, tau, h, grid):
    sigma = transfer_velocity * tau / h
    new_grid = np.zeros(len(grid) - 2)
    for m in range(2, len(grid) - 1):
        new_grid[m-2] = grid[m] - np.dot(sigma ,(grid[m] - grid[m-1])) + np.dot(sigma/2, np.dot((1 - sigma) , (grid[m] - 2 * grid[m-1] + grid[m-2])))
    return new_grid[0:-1]
