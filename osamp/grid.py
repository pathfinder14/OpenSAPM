import numpy as np

class Grid():
    """Generate grid/mesh."""
    # TODO make different grid for different problems
    def __init__(self, dimension, type, size_list, step_list):

        self._dimension = dimension
        self._dx = step_list[0]
        self._dy = step_list[1]
        self._dt = step_list[2]
        self._x_size = int(size_list[0])
        self._y_size = int(size_list[1])
        self._t_size = int(size_list[2])

        if(dimension == 2):

            if type == "acoustic":
                self._grid = np.zeros((self._x_size, self._y_size, self._t_size, 3), np.float64)
            else:
                self._grid = np.zeros((self._x_size, self._y_size, self._t_size, 5), np.float64)
        else:
            self._grid = np.zeros((self._x_size, self._t_size, 2), np.float64)


    @property
    def grid(self):
        return self._grid

    @property
    def dx(self):
        return self._dx

    @property
    def dy(self):
        return self._dy

    @property
    def dt(self):
        return self._dt

    @property
    def x_size(self):
        return self._x_size

    @property
    def y_size(self):
        return self._y_size

    @property
    def t_size(self):
        return self._t_size

    @property
    def dimension(self):
        return self._dimension