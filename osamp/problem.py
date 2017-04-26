class Problem(object):
    """
    Problem class is the completly form task with created parametrs.
    Necessary attributes for 1D or 2D problem:
    ---------------
    ndim - dimension 1 or 2

    _x, _t
    
    matrix - the matrix corresponding to system (will be contained in a model)
    
    grid - TODO

    sorces - the prameter, that presents the source of propagating waves
    
    model - seismic or acoustic

    method_of_solving - Method of solving  one-dimensional convection–diffusion equations
    
    method_of_decomposition

    ...    property of environment (will be contained in a model)
    
    border conditions



    """
    def __init__(self, params = None):

        if params is None:
            params =  {}
        self.params = params
        self._dimension = params['dimension']
        self._type = params['type']
        self._model = _assemble_model()
        self._matrix = _get_matrix()
        self._method = _get_method_of_solving(params['method'])
        self._prop_env = _get_property_of_environment()
        self._source = _produce_source_of_waves()
        self._border_conditions = generate_border_conditions(type_of_conditions)
        self._grid = _define_grid()
        self._x = self.grid.get_x()
        self._t = self.grid.get_t()
        if self.dimension == 2
            self._y = self.grid.get_y()

    @property
    def border_conditions(self):
        return self._border_conditions

    @property
    def dimension():
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

    @property
    def matrix
        return self._matrix


    def _define_grid():
    ''' Generate a grid/mesh to the problem'''    
        return Grid()    

    def _get_matrix():
    ''' Get matrix for corresponding problem type '''
        return self._model.matrix

    def _assemble_model():
        """
        Create a model
        :return model
        """
        model = Model([self._dimension, self.type])
        return model

    def _get_method_of_solving(name_of_method):
        """
        return one of the method to solve convection–diffusion equation 
        """
        return Method(name_of_method)

    def _get_property_of_environment(): #TODO arguments for environment
        """
        initialize a property of env
        :return new property  
        """
        return Environment_properties()

    def _produce_source_of_waves(type = None):
        """
        Create a source of propagating waves
        :return Source
        """
        return Source(type)
