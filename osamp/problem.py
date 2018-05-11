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


    def __init__(self, params = None):
        if params is None:
            params = {}
        self.params = params
        self._dimension = int(params['dimension'])
        self._type = params['type']
        if params['image_path'] is not None:
            self._image_path = params['image_path']
        self._density = float(params['density'])
        self._mu_lame = float(params['mu_lame'])
        self._elasticity_quotient = float(params['elasticity_quotient'])
        self._v_p = float(params['v_p'])
        self._v_s = float(params['v_s'])
        self._n = [0 for i in range(2)]
        self._n[0] = float(params['n_x'])
        self._n[1] = float(params['n_y'])
        self._method = params['method']
        self._source = params['source']
        self._buffering_step = int(params['buffering_step'])
        self._end_time = float(params['end_time'])
        self._time_step = float(params['time_step'])
        self._x_step = float(params['x_step'])
        self._y_step = float(params['y_step'])
        self._x_start = 0
        self._x_end = float(params['x_end'])
        self._y_start = 0
        self._y_end = float(params['y_end'])
        self._left_boundary_conditions = params['left_boundary_conditions']
        self._right_boundary_conditions = params['right_boundary_conditions']
        self._force_left = params['force_left']
        self._force_right = params['force_right']
        self._graph = int(params['graph'])
        self.source = self._produce_source_of_waves()
        if (self.type == 'acoustic') & (self.dimension == 2):
            self.tension = {
            'p':0,
            'v':1,
            'u':2
             }
        elif (self.type == 'acoustic') & (self.dimension == 1):
            self.tension = {
            'p':0,
            'v':1
             }
        elif (self.type == 'seismic') & (self.dimension == 1):
            self.tension = {
            'mu':0,
            'v':1
             }
        else:# (self.type == 'seismic') & (self.dimension == 2):
            self.tension = {
            'sigma11':0,
            'sigma22':1,
            'sigma21':2,
            'u':3,
            'v':4
             }
        self._grid = self._define_grid()
        self._model = self._assemble_model()

        #print('Problem: ' + str(self))

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
    def graph(self):
        return  self._graph

    @property
    def model(self):
        return self._model


    @property
    def n(selfs):
        return selfs._n

    @property
    def prop_env(self):
        return self._prop_env

    @property
    def type(self):
        return self._type

    def _define_grid(self):
        """
        Generate a grid/mesh to the problem
        """
        # TODO create Grid2d class and replace the following with it
        step_list = []
        step_list.append(self._x_step)
        step_list.append(self._y_step)
        step_list.append(self._time_step)
        size_list = []
        size_list.append((self._x_end - self._x_start) / self._x_step)
        size_list.append((self._y_end - self._y_start) / self._y_step)
        size_list.append((self._end_time) / self._time_step)
        return grid.Grid(self._dimension, self.type, size_list, step_list)

    def _assemble_model(self):
        """
        Create a model
        :return model
        """
        result_model = model.Model({
            "dimension" : self._dimension,
            "type" : self._type,
            "image_path" : self._image_path,
            "elasticity_quotient": self._elasticity_quotient,
            "mu_lame": self._mu_lame,
            "density": self._density,
            "v_p": self._v_p,
            "v_s": self._v_s,
            "n_x": self._n[0],
            "n_y": self._n[1]

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
        result_srt += '\ndensity: ' + str(self._density)
        result_srt += '\nelasticity_quotient: ' + str(self._elasticity_quotient)
        result_srt += '\nsource: ' + str(self._source)
        result_srt += '\nmethod: ' + self._method
        result_srt += '\nmodel: {' + str(self._model) + '\n}'
        # result_srt += 'method: ' + self._method
        # result_srt += 'source: ' + self._source
        # result_srt += 'grid: ' + self._grid
        return result_srt + '\n}'




