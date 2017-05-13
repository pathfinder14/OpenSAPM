#!/usr/bin/python
import numpy as np

"""The function returns the next grid (numpy array)"""
def beam_warming(transfer_velocity, tau, h, grid):

    sigma = transfer_velocity * tau / h
    for m in range(1, len(grid)):
        grid[m] = grid[m] - np.dot(sigma ,(grid[m] - grid[m-1])) + np.dot(sigma/2, np.dot((1 - sigma) , (grid[m] - 2 * grid[m-1] + grid[m-2])))

    return grid
