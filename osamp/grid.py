import numpy as np


class Grid(object):   
    """Generate grid/mesh."""
    def __init__(self, grid_dim_sizes):
        self._dx = 1
        self._dy = 1
        self._dt = 1
        self._grid = np.zeros(grid_dim_sizes, dtype=np.float64)
        self.nt = grid_dim_sizes[0]
        self.nx = grid_dim_sizes[1]
        if len(grid_dim_sizes) > 2:
            self.ny = grid_dim_sizes[2]
            self.j_max = self.ny - 1
        self.i_max = self.nx - 1
        self.k_max = self.nt - 1


    @property
    def grid():
        return self._grid