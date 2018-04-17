# coding=utf-8
import numpy as np
import importlib.util
import border_conditions
import postprocess

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
            #     result_grid[i + 1] = grid_next_t

        postprocess.do_postprocess(grid_next_t, self.buffering_step,
                                    self.x_start, self.x_end, self.type,
                                    self.time_step)

        return grid_next_t
        # TODO add saving to file every N time steps

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
        for i in range(2 * real_grid.shape[0]):
            # grid[3][3] = np.array([1, 20, 20])

            self.source.update_source_in_grid(real_grid[10])
            if (i % 2 == 0):
                grid_prev = real_grid[j, :]
                grid_prev = self._generate_border_conditions(grid_prev)
            else:
                grid_prev = real_grid[:, j]
                grid_prev = self._generate_right_border_conditions(grid_prev)

            # self.source.update_source_in_grid(grid_prev)
            for k in range(grid_prev.shape[0]):  # recieve Riman's invariant
                grid_prev[k] = np.dot(self.omega_matrix, grid_prev[k])
            if (self.problem._method == 'kir'):
                for index in self.tension.values():
                    grid_next[:, index] = kir.kir(grid_prev.shape[0], grid_prev[:, index],
                                                  self.matrix_of_eigns[index][index], self.time_step, self.spatial_step)
            # elif (self.problem._method == 'bicompact'):
            #     for index in self.tension.values():
            #         grid_next[:, index] = bicompact.bicompact_method(self.matrix_of_eigns[index][index], self.time_step,
            #                                                          self.spatial_step, grid_prev[:, index])
            # elif (self.problem._method == 'beam_warming'):
            #     grid_next = beam_warming.beam_warming(self.matrix_of_eigns, self.time_step, self.spatial_step,
            #                                           grid_prev)
            # elif (self.problem._method == 'tvd'):
            #     grid_next = tvd.TVDMethod(self.matrix_of_eigns, self.time_step, self.spatial_step, grid_prev, 'MC')
            # else:
            #     raise Exception('Unknown method name: ' + self.problem._method)
            # for k in range(grid_next.shape[0]):  # recieve Riman's invariant
            #     grid_next[k] = np.dot(self.inv_matrix, grid_next[k])
            # if (i % 2 == 0):
            #     real_grid[j, :] = grid_next
            # else:
            #     real_grid[:, j] = grid_next
            #     j += 1
            #
            # # print("Grid {0} on iter{1}\n".format(grid, j))
            #
        return real_grid

    def solve_2D(self):
        grid = self._grid
        source_of_grid = self.source
        # self.time_step = 0.01
        # self.spatial_step = 0.1

        # for t in range(1, grid.shape[0]):
        ##get only pressure values : array[:, 0]
        time = np.arange(0, self.end_time, self.time_step)
        result_grid = np.zeros((len(time), grid.shape[0], grid.shape[1], grid.shape[2]))
        # do iter
        for i in range(len(time)):
            grid_n = self.solve_splitted_2D(self.type, grid)
            if (i < result_grid.shape[0] - 1):
                result_grid[i] = grid_n

        print('Result grid shape: ' + str(result_grid.shape))

        postprocess.do_2_postprocess(result_grid[:, :, :, 2], self.buffering_step,
                                     self.x_start, self.x_end, self.y_start, self.problem.type,
                                     np.min(np.min(np.min(result_grid[:, :, :, 2]))),
                                     np.max(np.max(np.max(result_grid[:, :, :, 2]))),
                                     self.time_step)
        # Create time array

    def _generate_border_conditions(self, grid, time):
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
                self.problem._method, time)

    def _generate_right_border_conditions(self, grid, time):
        return border_conditions.border_condition_2d(grid, self.problem._type, self.problem._left_boundary_conditions,
                                                     self.problem._right_boundary_conditions,
                                                     self.problem._method, time)
