#!/usr/bin/python
import numpy as np

def beam_warming(tau, h, grid, transfer_velocity):
    new_grid = np.zeros_like(grid)
    for m in range(2, len(grid) - 1):
        sigma = transfer_velocity[m] * tau / h
        new_grid[m] = grid[m] - np.dot(sigma ,(grid[m] - grid[m-1])) +\
         np.dot(sigma/2, np.dot((1 - sigma) , (grid[m] - 2 * grid[m-1] + grid[m-2])))
    return new_grid
