# coding=utf-8
import grid
import model
import border_conditions
import source

class Problem(object):
    """
    Problem class is the completly form task with created parametrs.
    Necessary attributes for 1D or 2D problem:
    ---------------
    ndim - dimension 1 or 2

    _x, _t
    
    grid - TODO

    sorces - the prameter, that presents the source of propagating waves
    
    model - seismic or acoustic

    method_of_solving - Method of solving  one-dimensional convection–diffusion equations
    
    method_of_decomposition

    ...    property of environment (will be contained in a model)
    
    border conditions
    """

    GRID_SIZE = 10

    def __init__(self, params = None):
        if params is None:
            params =  {}
        self.params = params
        self._dimension = int(params['dimension'])
        self._type = params['type']
        self._rho = float(params['rho'])
        self._elasticity_quotient = float(params['elasticity_quotient'])
        self._model = self._assemble_model()
        self._method = params['method']
        self._source = params['source']
        self._source = self._produce_source_of_waves()
        self._grid = self._define_grid()
        # print('Problem: ' + str(self))

    @property
    def border_conditions(self):
        return self._border_conditions

    @property
    def dimension(self):
        return self._dimension

    @property
    def grid(self):
        return self._grid

    @property
    def model(self):
        return self._model

    @property
    def prop_env(self):
        return self._prop_env

    def _define_grid(self):
        """
        Generate a grid/mesh to the problem
        """
        grid_dim = ()
        if self._dimension == 1:
            return grid.Grid((Problem.GRID_SIZE, Problem.GRID_SIZE, self.dimension +1))
        else:
            # TODO create Grid2d class
            grid_dim = (Problem.GRID_SIZE, Problem.GRID_SIZE, Problem.GRID_SIZE)
            return grid.Grid2d()

    def _assemble_model(self):
        """
        Create a model
        :return model
        """
        result_model = model.Model({
            "dimension" : self._dimension,
            "type" : self._type,
            "elasticity_quotient": self._elasticity_quotient,
            "rho": self._rho
        })
        return result_model


    # TODO: produce different source types
    def _produce_source_of_waves(self):
        """
        Create a source of propagating waves
        :return Source
        """
        return source.Source(self._source)

    def __str__(self):
        result_srt = '{'
        result_srt += '\ndimension: ' + str(self._dimension)
        result_srt += '\ntype: ' + self._type
        result_srt += '\nrho: ' + str(self._rho)
        result_srt += '\nelasticity_quotient: ' + str(self._elasticity_quotient)
        result_srt += '\nmodel: {' + str(self._model) + '\n}'
        result_srt += '\nsource: ' + str(self._source)
        # result_srt += 'method: ' + self._method
        # result_srt += 'source: ' + self._source
        # result_srt += 'grid: ' + self._grid
        return result_srt + '\n}'




