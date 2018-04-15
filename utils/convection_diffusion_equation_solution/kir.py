import numpy as np
"""Use numpy arrays and lists"""

# def kir(x_nods_quantity, grid, transfer_velocity, time_step, x_step):
#     new_grid = grid
#     sigma = transfer_velocity * time_step / x_step
#     for m in range(1, x_nods_quantity - 1):
#         if (transfer_velocity >= 0):
#             new_grid[m] = grid[m] - np.dot(sigma, (grid[m] - grid[m-1]))
#             continue
#         else:
#             new_grid[m] = grid[m] - np.dot(sigma, (grid[m+1] - grid[m]))
#     return new_grid[1:-1]


def kir(grid, x_step, transfer_velocity, time_step):
    new_grid = [grid[i] for i in range(len(grid))]
    sigma = transfer_velocity * time_step / x_step
    print("sigma   " + str(sigma))
    print("volocity   " + str(transfer_velocity))
    for m in range(1, grid.shape[0] - 1):
        if(transfer_velocity >= 0):
            new_grid[m] = grid[m] - sigma * (grid[m] - grid[m-1])
            continue
        else:
            new_grid[m] = grid[m] - sigma * (grid[m + 1] - grid[m])
    # m = grid.shape[0] - 2
    # new_grid[m] = grid[m] - np.dot(-sigma, (grid[m + 1] - grid[m]))
    return new_grid[1:grid.shape[0] - 1]