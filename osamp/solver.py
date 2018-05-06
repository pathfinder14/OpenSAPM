# coding=utf-8
import numpy as np
import importlib.util
import border_conditions
import postprocess
import matplotlib.pyplot as plt
import border_conditions as b
from mpl_toolkits import mplot3d


# TODO chsnge type of imort module
spec = importlib.util.spec_from_file_location("kir", "../utils/convection_diffusion_equation_solution/kir.py")
kir = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kir)

spec = importlib.util.spec_from_file_location("beam_warming",
                                              "../utils/convection_diffusion_equation_solution/beam_warming.py")
beam_warming = importlib.util.module_from_spec(spec)
spec.loader.exec_module(beam_warming)

spec = importlib.util.spec_from_file_location("weno", "../utils/WENO_method/WENOmethod.py")
weno = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weno)

spec = importlib.util.spec_from_file_location("bicompact", "../utils/bicompact_method/bicompact.py")
bicompact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bicompact)

spec = importlib.util.spec_from_file_location("tvd", "../utils/TVD_method/TVDMethod.py")
tvd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tvd)


spec = importlib.util.spec_from_file_location("McCormack", "../utils/convection_diffusion_equation_solution/McCormack.py")
McCormack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(McCormack)


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

    def __init__(self, problem):
        self.cfl = 0.1  # TODO change this parametrs to user's propertyies
        self._dimension = problem.dimension
        self.problem = problem
        if(self._dimension != 2):
            self.matrix_of_eigns = problem.model.lambda_matrix
            self.omega_matrix = problem.model.omega_matrix
            self.inv_matrix = problem.model.inverse_omega_matrix
        self._grid = problem._grid.grid
        self.source = problem.source
        self.type = problem._type
        self.buffering_step = problem._buffering_step
        self.v_p = problem.model.env_prop.v_p
        self.tension = problem.tension
        self.time_step = problem._time_step
        self.end_time = problem._end_time
        self.x_start = problem._x_start
        self.x_end = problem._x_end
        self.y_start = problem._y_start
        self.y_end = problem._y_end
        self.spatial_step = problem._x_step
        # self.time_step = self.cfl*self.spatial_step/self.v_p
        if self._dimension == 1:
            self.solve_1D()
        else:
            self.solve_2D()

    def solve_1D(self):
        grid = self._grid
        source_of_grid = self.source
        # time_step = self.time_step
        matrix_of_eigns = self.problem.model.lambda_matrix
        omega_matrix = self.problem.model.omega_matrix
        inv_matrix = self.problem.model.inverse_omega_matrix
        grid_prev_t = np.zeros(grid.shape)
        grid_next_t = np.zeros(grid.shape)
        # let's imagine that grid has not information about time
        # for t in range(1, grid.shape[0]):
        ##get only pressure values : array[:, 0]
        time = np.arange(0, self.end_time, self.time_step)
        source_of_grid.update_source_in_grid(grid_prev_t, self._dimension)
        result_grid = np.zeros((len(time), grid.shape[0], grid.shape[1]))

        for i in range(self.problem.grid._t_size - 1):
            grid_prev_t = self._generate_border_conditions(grid_prev_t,  i)
            ##for seismic
            # grid_prev_t =  border_conditions.border_condition_1d(grid_prev_t, self.problem._type, "applied_force","absorb",
            #                                 self.problem._method, force_left=100)

            # source_of_grid.update_source_in_grid(grid_next_t) ##TODO
            for k in range(1, grid_next_t.shape[0]):
                for j in self.tension.values():
                    grid_next_t[k - 1][i][j] = grid_prev_t[k][i][j]
            for k in range(len(grid_prev_t)):  # recieve Riman's invariant
                grid_prev_t[k][i] = np.dot(omega_matrix, grid_prev_t[k][i])
            # TODO add new method
            if (self.problem._method == 'kir'):
                for index in self.tension.values():
                    grid_next_t[:, i + 1, index] = kir.kir(grid_prev_t[:, i, index], self.spatial_step,
                                                     matrix_of_eigns[index][index], self.time_step)
            elif (self.problem._method == 'beam_warming'):
                for index in self.tension.values():
                    grid_next_t[:, i + 1, index] = beam_warming.beam_warming(self.time_step, self.spatial_step, grid_prev_t[:, i, index], matrix_of_eigns[index][index])

            elif (self.problem._method == 'bicompact'):
                for index in self.tension.values():
                    grid_next_t[:, i + 1, index] = bicompact.bicompact_method(matrix_of_eigns[index][index], self.time_step,
                                                                       self.spatial_step, grid_prev_t[:, i, index])

            elif (self.problem._method == 'McCormack'):
                for index in self.tension.values():
                    grid_next_t[:, i + 1, index] = McCormack.McCormack(grid_prev_t[:, i, index], self.spatial_step,
                                                     matrix_of_eigns[index][index], self.time_step)
            elif (self.problem._method == 'weno'):
                for index in self.tension.values():
                    grid_next_t[:, i + 1, index] = weno.WENOmethod(matrix_of_eigns[index][index], self.time_step,
                                                            self.spatial_step, grid_prev_t[:, i, index])

            for k in range(grid_next_t.shape[0]):  # recieve Riman's invariant
                grid_next_t[k][i + 1] = np.dot(inv_matrix, grid_next_t[k][i + 1])
            grid_prev_t = grid_next_t

            #
            # if (i < result_grid.shape[0] - 1):
            #
            #result_grid[i + 1] = grid_next_t
        postprocess.do_postprocess(grid_next_t, self.buffering_step,
                                    self.x_start, self.x_end, self.type,
                                    self.time_step)

        return grid_next_t
        # TODO add saving to file every N time steps

    def solve_2D_acoustic(self):
        pass

    def solve_2D_seismic(self):
        pass


    def solver(self, i, k, grid):
        grid_next_t = np.zeros(grid.shape)
        for j in range(grid.shape[k]):
            if k == 1:
                grid_prev = grid[:, j, :, :]
                matrix = self.problem.model.omega_a_matrix
                matrix_inverse = self.problem.model.inverse_omega_a_matrix
                self.spatial_step = self.problem._x_step
                directions = b.Directions.X
                lambda_matrix = self.problem.model._lamda_a_matrix
            else:
                grid_prev = grid[j, :, :, :]
                matrix = self.problem.model.omega_b_matrix
                matrix_inverse = self.problem.model.inverse_omega_b_matrix
                self.spatial_step = self.problem._y_step
                directions = b.Directions.Y
                lambda_matrix = self.problem.model._lamda_b_matrix
            grid_next = np.zeros(grid_prev.shape)
            grid_prev = self._generate_border_conditions(grid_prev, i, directions)
            for z in range(grid_prev.shape[0]):  # recieve Riman's invariant
                grid_prev[z][i] = np.dot(matrix, grid_prev[z][i])
            if (self.problem._method == 'kir'):
                for index in self.tension.values():
                    grid_next[:, i + 1, index] = kir.kir(grid_prev[:, i, index], self.spatial_step,
                                                         lambda_matrix[index][index], self.time_step)
            elif (self.problem._method == 'bicompact'):
                for index in self.tension.values():
                    grid_next[:, i + 1, index] = bicompact.bicompact_method(lambda_matrix[index][index],
                                                                                  self.time_step,
                                                                                  self.spatial_step,
                                                                                  grid_prev[:, i, index])
            for z in range(grid_next.shape[0]):  # recieve Riman's invariant
                grid_next[z][i + 1] = np.dot(matrix_inverse, grid_next[z][i + 1])
            if(k == 1):
                grid_next_t[:, j, i, :] = grid_next[:, i + 1, :]
            else:
                grid_next_t[j, :, i, :] = grid_next[:, i + 1, :]
        return grid_next_t

    def solve_splitted_2D(self):
        """
        Method for splitted 2d problem to two 1d equation on one time slice
        """
        grid = self._grid
        for i in range((grid.shape[2] - 1)):
            grid_next_t_a = self.solver(i, 1, grid)
            grid_next_t_b = self.solver(i, 0, grid)
            grid[:,:, i + 1,:] = self.problem.n[0] * grid_next_t_a[:,:, i,:] + self.problem.n[1] * grid_next_t_b[:,:, i, :]
        return grid

    def solve_2D(self):
        grid = self._grid
        # source_of_grid = self.source
        # # self.time_step = 0.01
        # # self.spatial_step = 0.1
        #
        # # for t in range(1, grid.shape[0]):
        # ##get only pressure values : array[:, 0]
        print(2)
        self.source.update_source_in_grid(grid, self._dimension)
        # for i in range(grid.shape[1] - 1):
        #     grid[:,i + 1, :] = self.solve_splitted_2D(self.type, grid[:, i, :])

        grid = self.solve_splitted_2D()
        print('Result grid shape: ' + str(grid.shape))
        # list_x = [i * self.problem._y_step for i in range(grid.shape[1])]
        # plt.plot(list_x, grid[5, :, 5, 2])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        print(grid.shape)
        list_x = [i * self.problem._x_step for i in range(grid.shape[0])]
        list_y = [i * self.problem._y_step for i in range(grid.shape[1])]
        xgrid, ygrid = np.meshgrid(list_x, list_y)

        ax.plot_wireframe(xgrid, ygrid, grid[:, :,80,1])
        # j = 0
        # postprocess.do_2_postprocess(grid[:, :, :, j], self.buffering_step,
        #                              self.x_start, self.x_end, self.y_start, self.y_end, self.problem.type,
        #                              np.min(np.min(np.min(grid[:, :, :, j]))),
        #                              np.max(np.max(np.max(grid[:, :, :, j]))),
        #                              self.time_step)
        plt.show()

    def _generate_border_conditions(self, grid, time = 0, direction=b.Directions.X):
        if self._dimension == 1:
            return border_conditions.border_condition_1d(
                grid, self.problem._type,
                self.problem._left_boundary_conditions,
                self.problem._right_boundary_conditions,
                self.problem._method, time, self.problem._force_left, self.problem._force_right)
        elif self._dimension == 2:
            return border_conditions.border_condition_2d(
                grid, self.problem._type,
                self.problem._left_boundary_conditions,
                self.problem._right_boundary_conditions,
                self.problem._method, time, direction)

    def _generate_right_border_conditions(self, grid, time):
        return border_conditions.border_condition_2d(grid, self.problem._type, self.problem._left_boundary_conditions,
                                                     self.problem._right_boundary_conditions,
                                                     self.problem._method, time = 0)
