import numpy as np

class Grid(object):   
    """Generate grid/mesh."""
    def __init__(self,grid_dim ):
        self._dx = 1
        self._dy = 1
        self._dt = 1
        self._grid = np.zeros(grid_dim, dtype=floattype)
        self.nt = grid_dim[0]
        self.nx = grid_dim[1]
        self.ny = grid_dim[2]
        self.i_max = self.nx - 1
        self.j_max = self.ny - 1
        self.k_max = self.nt - 1


    @property
    def grid():
        return self._grid


