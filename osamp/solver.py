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

spec = importlib.util.spec_from_file_location("tvd", "../utils/TVD_method/TVDMethod.py")
tvd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tvd)

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
        self.spatial_step = 1
        self.time_step = self.cfl*self.spatial_step/self.x_velocity
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
        #time_step = 1
        time = np.arange(0, 100, time_step)
        result_grid = np.zeros((len(time), grid.shape[0], grid.shape[1]))

        for i in range(len(time)):
            grid_prev_t = grid_next_t

            #grid_prev_t = self._generate_border_conditions(grid_prev_t)
            ##for seismic
            grid_prev_t =  border_conditions.border_condition_1d(grid_prev_t, self.problem._type, "applied_force","absorb", 
                                            self.problem._method, force_left=100)
            source_of_grid.update_source_in_grid(grid_prev_t)
            #source_of_grid.update_source_in_grid(grid_next_t) ##TODO

            for k in range(len(grid_prev_t)):#recieve Riman's invariant
                grid_prev_t[k] = np.dot(omega_matrix, grid_prev_t[k])
            #TODO add new method

            if(self.problem._method == 'kir'):
                for index in self.tension.values():
                    grid_next_t[:, index] = kir.kir(grid_prev_t.shape[0], grid_prev_t[:,index], matrix_of_eigns[index][index], time_step, spatial_step)

            elif(self.problem._method == 'beam_warming'):
                grid_next_t = beam_warming.beam_warming(matrix_of_eigns, time_step, spatial_step, grid_prev_t)

            elif(self.problem._method == 'bicompact'):
                for index in self.tension.values():
                    grid_next_t[:, index] = bicompact.bicompact_method(matrix_of_eigns[index][index], time_step, spatial_step, grid_prev_t[:, index])
            else:
                raise Exception('Unknown method name: ' + self.problem._method)
            for k in range(len(grid_next_t)):#recieve Riman's invariant
                grid_next_t[k] = np.dot(inv_matrix, grid_next_t[k]) 
            result_grid[i] = grid_next_t
            
        postprocess.do_postprocess(result_grid, float(self.buffering_step), 0, 2300, self.type, time_step)
        return result_grid
        #TODO add saving to file every N time steps


    def solve_2D_acoustic(self):
        pass

    def solve_2D_seismic(self):
        pass



    def solve_splitted_2D(self, type_of_task, real_grid):
        """
        Method for splitted 2d problem to two 1d equation on one time slice
        """
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
            elif(self.problem._method == 'bicompact'):
                for index in self.tension.values():
                    grid_next[:, index] = bicompact.bicompact_method(self.matrix_of_eigns[index][index], self.time_step, self.spatial_step, grid_prev[:, index])
            elif(self.problem._method == 'beam_warming'):
                grid_next = beam_warming.beam_warming(self.matrix_of_eigns, self.time_step, self.spatial_step, grid_prev)        
            elif(self.problem._method == 'tvd'):
                    grid_next= tvd.TVDMethod(self.matrix_of_eigns, self.time_step, self.spatial_step, grid_prev, 'MC')
            else:
                raise Exception('Unknown method name: ' + self.problem._method)
            for k in range(grid_next.shape[0]):#recieve Riman's invariant
                 grid_next[k] = np.dot(self.inv_matrix, grid_next[k])
            if (i % 2 == 0):
                real_grid[j, :] = grid_next 
            else:
                real_grid[:, j] = grid_next
                j+=1
            
            #print("Grid {0} on iter{1}\n".format(grid, j))

        return real_grid

    def solve_2D(self):
        grid = self._grid
        source_of_grid = self.source
        spatial_step = 1
        self.time_step = 20
        #for t in range(1, grid.shape[0]):
        ##get only pressure values : array[:, 0]
        time = np.arange(0, 400, self.time_step)
        result_of_iteration_grid = np.zeros((len(time), grid.shape[0], grid.shape[1], grid.shape[2]))
        #do iter
        for i in range(len(time)):
            grid_n = self.solve_splitted_2D(self.type, grid)
            result_of_iteration_grid[i] = grid_n
        print(result_of_iteration_grid)
        postprocess.do_2_postprocess(result_of_iteration_grid[:,:,:,2], float(self.buffering_step), 0, 50, 50, "kaka", np.min(np.min(np.min(result_of_iteration_grid[:,:,:,2]))), np.max(np.max(np.max(result_of_iteration_grid[:,:,:,2]))),self.time_step)
        #Create time array 


    def _generate_border_conditions(self, grid):
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
        return border_conditions.border_condition(grid, self.problem._type,  "applied_force","applied_force",
                                        self.problem._method, self.tension, force_left=0)

