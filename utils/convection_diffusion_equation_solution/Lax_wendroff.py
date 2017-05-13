# -*- coding: utf-8 -*-
def Lax_wend(t_nods_quantity, x_nods_quantity, grid, transfer_velocity, time_step, x_step):
    #  t_nods_quantity: number of time nods  (int)
    #  x_nods_quantity: number of x-axe nods  (int)
    #  grid: x,t grid with initial conditions (numpy array)
    #  transfer_velocity: float constant
    #  time_step: float
    #  x_step: float
    #  grid with solutions (numpy array)
    #
    #
    #  Схема Лакса-Вендроффа

    sigma = transfer_velocity * time_step / x_step
    for n in range(1, t_nods_quantity - 1):
        for m in range(1, x_nods_quantity - 1):
            grid[n][m] = grid[n - 1][m] - sigma * (1/2 * (grid[n - 1][m + 1] - grid[n - 1][m-1]) - sigma * 1/2 * (grid[n-1][m+1] - 2 * grid[n-1][m] + grid[n-1][m-1]))
    return grid