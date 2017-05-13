# coding=utf-8
import numpy as np
import importlib.util
import matplotlib.pyplot as plt
import source
import border_conditions

#TODO chsnge type of imort module
spec = importlib.util.spec_from_file_location("kir", "../utils/convection_diffusion_equation_solution/kir.py")
kir = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kir)

spec = importlib.util.spec_from_file_location("kir", "../utils/convection_diffusion_equation_solution/beam_warming.py")
beam_warming = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beam_warming)


class Solver:
    """
    Solver class for simulations. 
    Time axis is labed as t, spaces ax, ay
    TODO get type of border conditions from user
    cfl - Kur's number c*tau/h
    TODO In this task grid - it's a time slice
    """
    def __init__(self, Problem):
        self.cfl = 0.1 # TODO change this parametrs to user's propertyies
        self._dimension = Problem.dimension
        self.problem = Problem
        matrix_of_eigns = Problem.model.lambda_matrix
        omega_matrix = Problem.model.omega_matrix
        inv_matrix = Problem.model.inverse_omega_matrix
        self._grid = Problem._grid._grid
        self.source = Problem.source
        self.x_velocity = Problem.model.env_prop.x_velocity
        self.solve_1D()
        # TODO generating source 

    def solve_1D(self):
        grid = self._grid
        source_of_grid = self.source
        time_step = self.cfl*self.problem._grid._dx/self.x_velocity
        spatial_step = 1
        matrix_of_eigns = self.problem.model.lambda_matrix
        omega_matrix = self.problem.model.omega_matrix
        inv_matrix = self.problem.model.inverse_omega_matrix

        for t in range(1, grid.shape[0]):
            source_of_grid.update_source_in_grid(grid[t-1])
            self._generate_border_conditions(grid[t-1], self.problem._type)
            for k in range(len(grid[t-1])):#recieve Riman's invariant
                grid[t-1][k] = np.dot(omega_matrix, grid[t-1][k])
            if(self.problem._method == 'kir'):
                grid[t] = kir.kir(grid.shape[1], grid[t-1], matrix_of_eigns, time_step, spatial_step)
            if(self.problem._method == 'beam_warming'):
                grid[t] = beam_warming.beam_warming(matrix_of_eigns, time_step, spatial_step, grid[t-1])
            else:
                raise Exception('Unknown method name: ' + self.problem._method)
            for k in range(len(grid[t-1])):#recieve Riman's invariant
                grid[t-1][k] = np.dot(inv_matrix, grid[t-1][k])
            #should i return to previous value on lvl t-1 ?
        print(grid) #TODO return grid to postprocess


    def solve_2D_acoustic(self):
        pass

    def solve_2D_seismic(self):
        pass


    def _generate_border_conditions(self, grid, type_of_task):
        # for i in range(len(grid[0])):
        #     grid[0][i] = [1,1]
        # return 
        if self._dimension == 1:
            return border_conditions.border_condition_1d(self._grid, type_of_task, 'reflection', 'reflection')
            # TODO: no idea what to pass as parameters cause method signature is not easily understandable
        elif self._dimension == 2:
            return border_conditions.border_condition_2d()
    