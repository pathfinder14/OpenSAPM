# coding=utf-8
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("kir", "../utils/сonvection_diffusion_equation_solution/kir.py")
kir = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kir)

class Solver:
    """
    Solver class for simulations. 
    Time axis is labed as t, spaces ax, ay
    
    """
    def __init__(self, Problem):
        self.cfl = 0.1 #TODO change this parametrs to user's propertyies
        self._dimension = Problem.dimension
        matrix_of_eigns = Problem.model.lambda_matrix
        omega_matrix = Problem.model.omega_matrix
        inv_matrix = Problem.model.inverse_omega_matrix
        grid = Problem._grid._grid
        #solve dv/dt=a dv/dx
        #TODO: find information v = omega*u
        num_of_equation = len(matrix_of_eigns)
        v = np.zeros(num_of_equation)
        u = np.zeros(num_of_equation)
        # TODO
        for i in range(num_of_equation):
            #v = np.dot(omega_matrix, u)
            new_grid = kir.kir(grid.shape[0], grid.shape[1], grid, matrix_of_eigns[i][i], self.cfl, 1)
            for j in range(len(new_grid)):
                u[j] = np.dot(inv_matrix, new_grid[j])




def _generate_border_conditions(self):
    if self._dimension == 1:
        return border_conditions.border_condition_1d(self._grid, TODO, TODO)
        # TODO: no idea what to pass as parameters cause method signature is not easily understandable
    elif self._dimension == 2:
        return border_conditions.border_condition_2d()