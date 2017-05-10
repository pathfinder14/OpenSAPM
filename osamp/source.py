import numpy as np
"""
This class describes the source of propagating waves
source it's a addition to initial system
this class contains defenition of many source
current contained in the variable source
"""

class Source:
    """This class is responsible for creating external sources of waves"""
    def __init__(self, type):
        self._type = type
        self.coordinates = 1
        self._source = self._get_source_by_type(type)

    # TODO: make return valid value
    def _get_source_by_type(self, type):
        return 'Temp source value'

    def update_source_in_grid(self, grid):
        grid[self.coordinates] = np.array([1,1])#TODO create real source