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
        self.coordinates = 2
        self._source = self._get_source_by_type(type)

    # TODO: make return valid value
    def _get_source_by_type(self, type):
        return 'Temp source value'

    def _create_spherical_source(self, grid):
        #TODO delete unnamed constants
        if grid.shape[1] == 2:
            grid[self.coordinates] = np.array([100, 2])
        elif grid.shape[1] == 3:
            grid[self.coordinates] = np.array([100, 2, 2])
        else:
            pass
        #grid[self.coordinates - 1] = np.array([100*np.cos(15),20*np.cos(15)])
        #grid[self.coordinates + 1] = np.array([100*np.cos(15),20*np.cos(15)])
        return grid

    def update_source_in_grid(self, grid):
        return self._create_spherical_source(grid)
        #grid[self.coordinates] = np.array([1,1])#TODO create real source



    class SourcesTypes:
        def __init__(self):
            pass

