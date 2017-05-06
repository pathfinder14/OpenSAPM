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
        self._source = self._get_source_by_type(type)

    # TODO: make return valid value
    def _get_source_by_type(self, type):
        return 'Temp source value'