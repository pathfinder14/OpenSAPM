#!/usr/bin/python
"""Use standard python arrays"""
def get_border_cond_for_beam_warming(row):
    return [-row[0]] + row

def beam_warming(transfer_velocity, tau, h, grid):
    ext_grid = []
    for i in range(0, len(grid[0])):
        ext_grid.append(get_border_cond_for_beam_warming(grid[i]))

    sigma = transfer_velocity * tau / h
    for rows in range(0, len(ext_grid) - 1):
        for cols in range(2, len(ext_grid[0]) - 1):
            ext_grid[rows+1][cols] = ext_grid[rows][cols] - sigma * (ext_grid[rows][cols] - ext_grid[rows][cols-1]) + sigma/2 * (1 - sigma) * (ext_grid[rows][cols] - 2 * ext_grid[rows][cols-1] + ext_grid[rows][cols-2])
        del ext_grid[rows][0]
    return ext_grid
