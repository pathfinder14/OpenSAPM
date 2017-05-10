# coding=utf-8
import numpy as np
import importlib.util
import source
spec = importlib.util.spec_from_file_location("kir", "../utils/сonvection_diffusion_equation_solution/kir.py")
kir = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kir)

class Solver:
    """
    Solver class for simulations. 
    Time axis is labed as t, spaces ax, ay
    
    cfl - Kur's number c*tau/h
    """
    def __init__(self, Problem):
        self.cfl = 0.1 #TODO change this parametrs to user's propertyies
        self._dimension = Problem.dimension
        self.problem = Problem
        matrix_of_eigns = Problem.model.lambda_matrix
        omega_matrix = Problem.model.omega_matrix
        inv_matrix = Problem.model.inverse_omega_matrix
        self._grid = Problem._grid._grid
        #solve dv/dt=a dv/dx
        #TODO: find information v = omega*u
        num_of_equation = len(matrix_of_eigns)
        v = np.zeros(num_of_equation)
        u = []
        self.c = Problem.model.lame
        # TODO generating source 
        self.solve_1D_acoustic()




    def solve_1D_acoustic(self):
        grid = self._grid
        source_of_grid = source.Source("point")
        time_step = self.cfl*self.problem._grid._dx/self.c
        matrix_of_eigns = self.problem.model.lambda_matrix
        omega_matrix = self.problem.model.omega_matrix
        inv_matrix = self.problem.model.inverse_omega_matrix
        generate_border_conditions(grid)
        for t in range(1, grid.shape[0]):
            source_of_grid.update_source_in_grid(grid[t-1])
            for k in range(len(grid[t-1])):#recieve Riman's invariant
                grid[t-1][k] = np.dot(omega_matrix, grid[t-1][k])
            grid[t] = (kir.kir(grid.shape[0], grid.shape[1], grid[t-1], matrix_of_eigns, time_step, 1))
            for k in range(len(grid[t-1])):#recieve Riman's invariant
                grid[t-1][k] = np.dot(inv_matrix, grid[t-1][k])
            #should i return to previous value on lvl t-1 ?
        print(grid)

def generate_border_conditions(grid):
    for i in range(len(grid[0])):
        grid[0][i] = [1,1]
    return 
    if self._dimension == 1:
        return border_conditions.border_condition_1d(self._grid, TODO, TODO)
        # TODO: no idea what to pass as parameters cause method signature is not easily understandable
    elif self._dimension == 2:
        return border_conditions.border_condition_2d()