#!/usr/bin/python
import numpy as np

def get_border_cond_for_beam_warming(row):
    return [-row[0]] + row

"""The function returns the next grid (numpy array) with zero left border condition"""
def beam_warming(transfer_velocity, tau, h, grid):
    ext_grid = np.array(get_border_cond_for_beam_warming(grid.tolist()))
    sigma = transfer_velocity * tau / h
    result_grid = np.zeros(ext_grid.size)
    for m in range(2, len(ext_grid)):
        result_grid[m] = ext_grid[m] - sigma * (ext_grid[m] - ext_grid[m-1]) + sigma/2 * (1 - sigma) * (ext_grid[m] - 2 * ext_grid[m-1] + ext_grid[m-2])
    result_grid = np.delete(result_grid, 0)
    return result_grid
