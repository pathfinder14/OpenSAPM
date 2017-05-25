# coding=utf-8
import numpy as np
import importlib.util
import border_conditions
import postprocess
#TODO chsnge type of imort module
spec = importlib.util.spec_from_file_location("kir", "../utils/convection_diffusion_equation_solution/kir.py")
kir = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kir)

spec = importlib.util.spec_from_file_location("beam_warming", "../utils/convection_diffusion_equation_solution/beam_warming.py")
beam_warming = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beam_warming)

spec = importlib.util.spec_from_file_location("bicompact", "../utils/bicompact_method/bicompact.py")
bicompact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bicompact)

p = 0  # index of pressure in values array
v = 1  # index of velocity in values array

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
        self.matrix_of_eigns = Problem.model.lambda_matrix
        self.omega_matrix = Problem.model.omega_matrix
        self.inv_matrix = Problem.model.inverse_omega_matrix
        self._grid = Problem._grid._grid
        self.source = Problem.source
        self.type = Problem._type
        self.buffering_step = Problem._buffering_step
        self.x_velocity = Problem.model.env_prop.x_velocity
        self.tension = Problem.tension
        self.time_step = self.cfl*self.problem._grid._dx/self.x_velocity
        self.spatial_step = 1

        if self._dimension == 1:
            self.solve_1D()
        else:
            self.solve_2D()


    def solve_1D(self):
        grid = self._grid
        source_of_grid = self.source
        spatial_step = 1
        time_step = self.time_step
        matrix_of_eigns = self.problem.model.lambda_matrix
        omega_matrix = self.problem.model.omega_matrix
        inv_matrix = self.problem.model.inverse_omega_matrix
        grid_prev_t = np.zeros(grid.shape)
        grid_next_t = np.zeros(grid.shape)
        #let's imagine that grid has not information about time
        #for t in range(1, grid.shape[0]):
        ##get only pressure values : array[:, 0]
        time = np.arange(0, 50, time_step)
        result_grid = np.zeros((len(time), grid.shape[0], grid.shape[1]))

        for i in range(len(time)):
            grid_prev_t = grid_next_t
            grid_prev_t = self._generate_border_conditions(grid_prev_t)
            source_of_grid.update_source_in_grid(grid_prev_t) ##TODO
            #source_of_grid.update_source_in_grid(grid_next_t) ##TODO

            for k in range(len(grid_prev_t)):#recieve Riman's invariant
                grid_prev_t[k] = np.dot(omega_matrix, grid_prev_t[k])
            if(self.problem._method == 'kir'):
                for index in self.tension.values():
                    grid_next_t[:, index] = kir.kir(grid_prev_t.shape[0], grid_prev_t[:,index], matrix_of_eigns[index][index], time_step, spatial_step)
                #grid_next_t[:, p] = kir.kir(grid_prev_t.shape[0], grid_prev_t[:, p], matrix_of_eigns[p][p], time_step, spatial_step)
                #grid_next_t[:, v] = kir.kir(grid_prev_t.shape[0], grid_prev_t[:, v], matrix_of_eigns[v][v], time_step, spatial_step)

            elif(self.problem._method == 'beam_warming'):
                grid_next_t = beam_warming.beam_warming(matrix_of_eigns, time_step, spatial_step, grid_prev_t)
                #TODO add new method
            elif(self.problem._method == 'bicompact'):
                grid_next_t[:, p] = bicompact.bicompact_method(matrix_of_eigns[p][p], time_step, spatial_step, grid_prev_t[:, p], grid_next_t[:, p])
                grid_next_t[:, v] = bicompact.bicompact_method(matrix_of_eigns[v][v], time_step, spatial_step, grid_prev_t[:, v], grid_next_t[:, v])
                grid_next_t = grid_next_t[1:-1]
            else:
                raise Exception('Unknown method name: ' + self.problem._method)
            for k in range(len(grid_next_t)):#recieve Riman's invariant
                grid_next_t[k] = np.dot(inv_matrix, grid_next_t[k]) 
            result_grid[i] = grid_next_t
        #print(result_grid) #TODO return grid to postprocess
        return result_grid
        #postprocess.do_postprocess(result_grid, float(self.buffering_step), -300, 300, "acoustic", time_step)
        #TODO add saving to file every N time steps


    def solve_2D_acoustic(self):
        pass

    def solve_2D_seismic(self):
        pass

    def solve_2D(self):
        self.splitting_method()
        pass

    def solve_splitted_2D(self, type_of_task, real_grid):
        grid_next = np.zeros_like(real_grid[0])
        grid_prev = np.zeros_like(real_grid[0])
        j = 0

        for i in range(2*real_grid.shape[0]):
            #grid[3][3] = np.array([1, 20, 20])
            
            self.source.update_source_in_grid(real_grid[3])
            if (i % 2 == 0):
                grid_prev = real_grid[j, :]
                grid_prev = self._generate_border_conditions(grid_prev)
            else:
                grid_prev = real_grid[:, j]
                grid_prev = self._generate_right_border_conditions(grid_prev)

            #self.source.update_source_in_grid(grid_prev)
            for k in range(grid_prev.shape[0]):#recieve Riman's invariant
                 grid_prev[k] = np.dot(self.omega_matrix, grid_prev[k])
            if(self.problem._method == 'kir'):
                for index in self.tension.values():
                    grid_next[:, index] = kir.kir(grid_prev.shape[0], grid_prev[:,index], self.matrix_of_eigns[index][index], self.time_step, self.spatial_step)
            for k in range(grid_next.shape[0]):#recieve Riman's invariant
                 grid_next[k] = np.dot(self.inv_matrix, grid_next[k])
            if (i % 2 == 0):
                real_grid[j, :] = grid_next 
            else:
                real_grid[:, j] = grid_next
                j+=1
            
            #print("Grid {0} on iter{1}\n".format(grid, j))

        return real_grid

    def splitting_method(self):
        grid = self._grid
        source_of_grid = self.source
        spatial_step = 1
        self.time_step = 1
        #for t in range(1, grid.shape[0]):
        ##get only pressure values : array[:, 0]
        time = np.arange(0, 100, self.time_step)
        result_of_iteration_grid = np.zeros((len(time), grid.shape[0], grid.shape[1], grid.shape[2]))
        #do iter
        for i in range(len(time)):
            grid_n = self.solve_splitted_2D(self.type, grid)
            result_of_iteration_grid[i] = grid_n
        print(result_of_iteration_grid)
        #Create time array 


    def _generate_border_conditions(self, grid):
        # for i in range(len(grid[0])):
        #     grid[0][i] = [1,1]
        # return 
        if self._dimension == 1:
            return border_conditions.border_condition_1d(
                grid, self.problem._type,
                self.problem._left_boundary_conditions,
                self.problem._right_boundary_conditions,
                self.problem._method)
        elif self._dimension == 2:
            return border_conditions.border_condition(
                grid, self.problem._type,
                self.problem._left_boundary_conditions,
                self.problem._right_boundary_conditions,
                self.problem._method, self.tension)

    def _generate_right_border_conditions(self, grid):
        return border_conditions.border_condition(grid, self.problem._type, "applied_force","absorb",
                                        self.problem._method, self.tension, force_left=100)