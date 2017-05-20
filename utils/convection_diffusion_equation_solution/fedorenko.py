#!/usr/bin/python
import numpy as np

def fedorenko(tau, h, grid):
    relation = tau / h
    new_grid = np.zeros(len(grid) - 1)
    for m in range(1, len(grid) - 1):
        new_grid[m-1] = grid[m] - np.dot(relation, grid[m] - grid[m-1]) - np.dot(relation / 2 * (relation - relation ** 2), grid[m-1] - 2 * grid[m] + grid[m+1])
    return new_grid[0:-1]
