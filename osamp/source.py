import numpy as np
"""
This class describes the source of propagating waves
source it's a addition to initial system

this class contains defenition of many source
current contained in the variable source

Different types:
    Spherical

"""

class Source:
    """This class is responsible for creating external sources of waves"""
    def __init__(self, type):
        self._type = type
        self.coordinates_x = 10
        self.coordinates_y = 10
        self._source = self._get_source_by_type(type)

    # TODO: make return valid value
    def _get_source_by_type(self, type):
        return 'Temp source value'

    def _create_spherical_source(self, grid, dimension):
        #TODO delete unnamed constants
        if dimension == 2  and len(grid[0][0][0]) == 3:
            grid[self.coordinates_x][self.coordinates_y][0] = np.array([10, 0, 0])
        elif dimension == 1:
            grid[self.coordinates_x][0] = np.array([100, 20])
        else:
            grid[self.coordinates_x][self.coordinates_y][0] = np.array([10, 0, 0, 0, 0])
        return grid

    def update_source_in_grid(self, grid, dimension):
        return self._create_spherical_source(grid, dimension)
        #grid[self.coordinates] = np.array([1,1])#TODO create real source



    class SourcesTypes:
        def __init__(self):
            pass

