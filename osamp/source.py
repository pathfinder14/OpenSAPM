"""
This class describes the source of propagating waves
source it's a addition to initial system
this class contains defenition of many source
current contained in the variable source
"""

class Source(object):
    """This class is responsible for creating external sources of waves"""
    def __init__(self, type):
        super(Source, self).__init__()
        self._type = type
        self._source = _get_source_by_type(type)

    @property
    def _get_source_by_type(type):
        pass