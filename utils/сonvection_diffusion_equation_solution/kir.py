"""Use numpy arrays and lists"""
def kir(t_nods_quantity, x_nods_quantity, grid, transfer_velocity, time_step, x_step):
    sigma = transfer_velocity * time_step / x_step
    print ('sigma')
    print (sigma)
    for n in range(1, t_nods_quantity - 1):
        for m in range(1, x_nods_quantity - 1):
            grid[n][m] = grid[n - 1][m] - sigma * (grid[n - 1][m + 1] - grid[n - 1][m])
    return grid
